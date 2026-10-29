import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AuthForm.css';
import '../../services/auth'
import eyeOpen from '../../assets/icons/eye-open.svg';
import eyeClosed from '../../assets/icons/eye-closed.svg';
import check from '../../assets/icons/check.svg';
import { registerUser } from '../../services/auth';
import { useAuth } from '../../context/AuthContext';

function AuthForm({ mode = 'register' }) {
    const isRegister = mode === 'register';
    const navigate = useNavigate();
    const { login } = useAuth();
    const [isPasswordVisible, setIsPasswordVisible] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [serverError, setServerError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    function validateForm() {
        const newErrors = {};

        const normalizedEmail = email.trim();

        if (!normalizedEmail) {
            newErrors.email = 'Введите email';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail)) {
            newErrors.email = 'Введите корректный email';
        }

        if (!password) {
            newErrors.password = 'Введите пароль';
        } else if (password.length < 6) {
            newErrors.password = 'Пароль должен содержать минимум 6 символов';
        } else if (password.length > 128) {
            newErrors.password = 'Пароль не должен превышать 128 символов';
        }

        setErrors(newErrors);

        return Object.keys(newErrors).length === 0;
    }

    async function handleSubmit(event) {
        event.preventDefault();

        setServerError('');
        setSuccessMessage('');

        if (!validateForm()) {
            return;
        }

        try {
            setIsSubmitting(true);

            if(isRegister) {
                await registerUser({ email, password });

                setSuccessMessage(
                    'Аккаунт успешно создан! Теперь вы можете войти.'
                );
                setEmail('');
                setPassword('');
                setErrors({});

            } else {

                await login({ email, password });
                navigate('/');
                
            }
        } catch (error) {
            if (isRegister && error.status === 409) {
                setServerError('Пользователь с таким email уже существует.');
            } else if (!isRegister && error.status === 401) {
                setServerError('Неверный email или пароль.');
            } else if (error.status === 422) {
                setServerError('Проверьте правильность введённых данных.');
            } else {
                setServerError(
                    error.message || 'Произошла ошибка. Попробуйте позже.'
                );
            }
        } finally {
            setIsSubmitting(false);
        }
    }
    return (
        <div className="auth-form">
            <div className="auth-form-header">

                <h2 className="auth-form-title">
                    {isRegister && successMessage && (
                        <img src={check} className="auth-success-icon" alt='' fill='none' aria-hidden="true">
                        </img>
                    )}

                    {isRegister && successMessage
                    ? 'Аккаунт успешно создан!' 
                    : isRegister
                        ? 'Создать аккаунт'
                        : 'С возвращением!'
                    }
                </h2>
                <p className="auth-form-text">
                    {isRegister && successMessage
                    ? 'Теперь вы можете войти в свой аккаунт и начать планировать путешествия.'
                    : isRegister
                        ? 'Зарегистрируйтесь, чтобы планировать путешествия.'
                        : 'Войдите, чтобы продолжить планировать путешествия.'
                    }
                </p>

            </div>

            {isRegister && successMessage ? (
                <div className='auth-success' role='status'>

                    <Link to='/login' className='auth-success-button'>
                    Перейти ко входу</Link>

                </div> 
            ) : (
                <>
                    <form 
                        className="auth-form-fields"
                        noValidate
                        onSubmit={handleSubmit}
                    >

                        <div className="auth-form-field">
                            <label htmlFor="email">Электронная почта</label>
                            <input
                                className="auth-email-wrapper"
                                type="email"
                                id="email"
                                name="email"
                                placeholder="Введите ваш email"
                                autoComplete="email"
                                value={email}
                                onChange={(event) => setEmail(event.target.value)}
                                required
                            />

                            {errors.email && (
                                <span className='auth-field-error'>
                                    {errors.email}
                                </span>
                            )} 
                        </div>

                        <div className="auth-form-field">
                            <label htmlFor="password">Пароль</label>

                            <div className='auth-password-wrapper'>

                                <input
                                    type={isPasswordVisible ? 'text' : 'password'}
                                    id="password"
                                    name="password"
                                    placeholder={isRegister ? 'Создайте пароль' : 'Введите пароль'}
                                    autoComplete={isRegister ? 'new-password' : 'current-password'}
                                    value={password}
                                    onChange={(event) => setPassword(event.target.value)}
                                    required
                                />

                                <button
                                    className="auth-password-toggle"
                                    type="button"
                                    onClick={() => 
                                        setIsPasswordVisible((visible) => !visible)
                                    }
                                    aria-label={
                                        isPasswordVisible ? 'Скрыть пароль' : 'Показать пароль'
                                    }

                                    aria-pressed={isPasswordVisible}
                                >
                                    <img
                                        src={isPasswordVisible ? eyeOpen : eyeClosed}
                                        alt=''
                                        aria-hidden="true"
                                    ></img>

                                </button>

                            </div>

                            {errors.password && (
                                <span className='auth-field-error'>
                                    {errors.password}
                                </span>
                            )}

                            {isRegister && (
                                <span className="auth-field-hint">
                                    От 6 до 128 символов
                                </span>
                            )}

                        </div>

                        {serverError && (
                            <p className='auth-field-error' role='alert'>
                                {serverError}
                            </p>
                        )}

                        {successMessage && (
                            <p role='status'>
                                {successMessage}
                            </p>
                        )}
                        <button 
                            className="auth-submit-button" 
                            type="submit"
                            disabled={isSubmitting}
                        >
                            {isSubmitting 
                                ? (isRegister ? 'Создаем аккаунт...' : 'Входим...')
                                : (isRegister ? 'Создать аккаунт' : 'Войти')
                            }
                        </button>

                    </form>

                    <div className="auth-devider">
                        <span>или</span>
                    </div>

                    <button className=" auth-submit-button__google" type="button">
                        <svg className="btn-icon__google" role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Google</title><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                        Продолжить с Google
                    </button>

                    {isRegister 
                        ? (
                            <div className='auth-footer'>
                                <span>Уже есть аккаунт?</span>
                                <a href='/login'>Войти</a>
                            </div>
                        )
                        : (
                            <div className='auth-footer'>
                                <span>Нету аккаунта?</span>
                                <a href='/register'>Регистрация</a>
                            </div>
                    )}
                </>
            
            )}

        </div>

    );
}

export default AuthForm;