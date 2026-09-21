import './Hero.css'
import SearchPanel from './SearchPanel/SearchPanel';

function Hero() {
    return (
        <section className="hero">
            <div className="hero-container">

                <h1 className="hero-title">Путешествуйте умнее,<br></br> живите ярче</h1>

                <p className="hero-subtitle">Поиск лучших цен на авиабилеты, технологичные отели и авторские экспедиции.<br></br> Мир без границ начинается со звонка колокола.</p>

                <SearchPanel />

            </div>
        </section>
    );
}

export default Hero