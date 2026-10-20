import './AuthForm.css';

function AuthForm() {
    return (
        <div className="auth-form">
            <div className="auth-form-header">

                <h2 className="auth-form-title">Создать аккаунт</h2>
                <p className="auth-form-text">Зарегистрируйтесь, чтобы планировать путешествия.</p>

            </div>

            <form className="auth-form-fields">
                <div className="auth-form-field">
                    <label htmlFor="email">Электронная почта</label>
                    <input
                        className="auth-form__input"
                        type="email"
                        id="email"
                        name="email"
                        placeholder="Введите ваш email"
                        autoComplete="email"
                        required
                    />
                </div>

                <div className="auth-form-field">
                    <label htmlFor="password">Пароль</label>
                    <input
                        className="auth-form__input"
                        type="password"
                        id="password"
                        name="password"
                        placeholder="Создайте пароль"
                        autoComplete="new-password"
                        required
                    />

                    <span className="auth-field-hint">
                        От 6 до 128 символов
                    </span>
                </div>

                <button className="auth-submit-button" type="submit">
                    Создать аккаунт
                </button>

            </form>

            <div className="auth-devider">
                <span>или</span>
            </div>

            <button className=" auth-submit-button__google" type="button">
                <svg className="btn-icon__google" role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Google</title><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                Продолжить с Google
            </button>

            <div className='auth-footer'>
                <span>Уже есть аккаунт?</span>
                <a href='/Login'>Войти</a>
            </div>
        </div>
    );
}

export default AuthForm;