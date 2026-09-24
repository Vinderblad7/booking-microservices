import DestinationCard from "./DestinationCard";
import './PopularDestinations.css';

function PopularDestinations() {
    return (
        <sections className='popular-destinations'>

            <div className="popular-destinations-list">

                <h2 className="popular-now-text">Популярно сейчас</h2>

                <div className="destinations-list">
                    <DestinationCard 
                        name="Анталия"
                        price="32 000"
                    />
                
                    <DestinationCard 
                        name="Дубай"
                        price="66 000"
                    />

                    <DestinationCard 
                        name="Париж"
                        price="28 000"
                    />
                </div>
            </div>

            <div className="service-stats">

                <div className="stat">
                    <span className="stat-value">2 450+</span>
                    <span className="stat-label">Активных клиентов</span>
                </div>

                <div className="stat">
                    <span className="rating">4.9 / 5</span>
                    <span className="stat-label">Оценка на основе 923 отзывов</span>
                </div>

            </div>

        </sections>
    );
};

export default PopularDestinations