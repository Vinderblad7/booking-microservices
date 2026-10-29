import {
    createContext,
    useContext,
    useEffect,
    useState,
} from 'react';
import { getCurrentUser, loginUser } from '../services/auth';
import {
    getAccessToken,
    removeAccessToken,
    saveAccessToken,
} from '../services/authStorage'

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [isAuthLoading, setIsAuthLoading] = useState(true);

    useEffect(() => {
        let isCanceled = false;

        async function restoreUser() {
            const token = getAccessToken();
            
            if (!token) {
                setIsAuthLoading(false);
                return;
            }

            try {
                const currentUser = await getCurrentUser();

                if(!isCanceled) {
                    setUser(currentUser);
                }
 
            } catch (error) {
                if (error.status === 401) {
                    removeAccessToken();
                }

                if (!isCanceled) {
                    setUser(null);
                }
            } finally {
                if (!isCanceled) {
                    setIsAuthLoading(false);
                }
            }
        }

        restoreUser();

        return () => {
            isCanceled = true;
        }
    }, []);

    async function login(credentials) {
        setIsAuthLoading(true);
    

        try {
            const tokenData = await loginUser(credentials);
            saveAccessToken(tokenData.access_token);

            const currentUser = await getCurrentUser();
            setUser(currentUser);

            return currentUser;
        } catch (error) {
            removeAccessToken();
            setUser(null);
            throw error;
        } finally {
            setIsAuthLoading(false);
        }
    }

    function logout() {
        removeAccessToken();
        setUser(null);
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthLoading,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);

    if (context === null) {
        throw new Error('useAuth должен использоваться внутри AuthProvider')
    }

    return context;
}
