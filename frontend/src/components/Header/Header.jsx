import logoBadge from '../../assets/icons/logo-badge.svg';

function Header() {
    return (
        <header className="header">
            
            <div className="container">

                <div className="logo">
                    <img src={logoBadge} alt="Logo" />
                    <span className="logo-text">Vinderblad & Kudoxq</span>
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
                    <button className="login-button">Войти</button>
                    <button className="signup-button">Регистрация</button>
                </div>

            </div>

        </header>     
    )
}

export default Header