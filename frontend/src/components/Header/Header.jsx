import logoBadge from '../../assets/icons/logo-badge.svg';
import './Header.css';

function Header() {
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
                    <a href="/login"><button className="login-button">Войти</button></a>
                    <a href="/register"><button className="signup-button">Регистрация</button></a>
                </div>

            </div>

        </header>     
    )
}

export default Header