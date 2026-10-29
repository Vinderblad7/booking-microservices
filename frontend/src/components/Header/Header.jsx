import logoBadge from '../../assets/icons/logo-badge.svg';
import './Header.css';
import { useAuth } from '../../context/AuthContext';
import { useState } from 'react';

function Header() {
    const { user, isAuthLoading, logout } = useAuth();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    return (
        <header className="header">

            <div className="header-container">

                <div className="logo">
                    <a href="/">
                        <img src={logoBadge} alt="badge" className="logo-badge" />
                    </a>

                    <div className="logo-text">
                        <span className="brand-top">Vinderblad &</span>
                        <span className="brand-bottom">Kudoxq</span>
                    </div>
                    
                </div>
                
                <nav className="navigation">
                    <a href="/directions">Направления</a>
                    <a href="/hotels">Отели</a>
                    <a href="/flights">Авиабилеты</a>
                    <a href="/tours">Готовые туры</a>
                    <a href="/contacts">Контакты</a>
                </nav>

                <div className="actions">
                    <button className="lang-currency-switcher">RU \ RUB</button>

                    {!isAuthLoading && (
                        user ? (
                            <div className='profile-menu'>
                                <button 
                                    className='user-avatar'
                                    type='button'
                                    aria-label={`Профиль пользователя ${user.email}`}
                                    onClick={() => setIsMenuOpen((isOpen) => !isOpen)}
                                >
                                    {user.email.charAt(0).toUpperCase()}
                                </button>

                                {isMenuOpen && (
                                    <div className='profile-dropdown' role='menu'>
                                        <p className='profile-email'>{user.email}</p>

                                        <button
                                            type='button'
                                            role='menuitem'
                                            onClick={() => {
                                                logout();
                                                setIsMenuOpen(false);
                                            }}
                                        >
                                            Выйти
                                        </button>
                                    </div>
                                )}
                            </div>
                        
                        ) : (
                            <>
                                <a href="/login">
                                    <button className="login-button">Войти</button>
                                </a>

                                <a href="/register">
                                    <button className="signup-button">Регистрация</button>
                                </a>
                            </>
                        )  
                    )}
                    
                </div>

            </div>

        </header>     
    )
}

export default Header