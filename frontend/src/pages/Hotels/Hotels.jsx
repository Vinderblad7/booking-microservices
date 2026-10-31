import { useState, useEffect } from 'react'
import { getHotels } from '../../services/api'
import './Hotels.css'
import imageIcon from '../../assets/icons/image-icon.svg';
import emptyListIcon from '../../assets/icons/Empty-list-symbol.svg';

function Hotels() {
    const [hotels, setHotels] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        async function loadHotels() {
            try {
                const hotelList = await getHotels();
                setHotels(hotelList);
            } catch {
                setError('Не удалось загрузить отели.')
            } finally {
                setIsLoading(false);
            }
        }

        loadHotels();
    }, []);

    return (
        <main className='hotels-page'>
            <div className='hotels-container'>
                <div className='hotels-intro'>
                    <h1>Отели</h1>
                    <p>Выберите место для следующего путешествия</p>
                </div>

                {isLoading && <p>Загружаем отели...</p>}

                {error && <p role='alert'>{error}</p>}

                {!isLoading && !error && hotels.length === 0 && (
                    <section className='hotel-empty-state'>
                        <img src={emptyListIcon} alt='' aria-hidden='true'></img>

                        <h2>Отелей пока нет</h2>

                        <p>Когда отели появятся, вы увидите их здесь.</p>
                    </section>
                )}

                {!isLoading && !error && hotels.length > 0 && (
                    <section className='hotels-grid' aria-label='Список отелей'>
                        {hotels.map((hotel) =>(
                            <article className='hotel-card' key={hotel.id}>
                                <div className='hotel-card-image'>
                                    {hotel.images?.length > 0 ? (
                                        <img 
                                            src={hotel.images[0].url}
                                            alt={hotel.name}
                                        />
                                    ) : (
                                        <div className='hotel-image-placeholder'>
                                            <img src={imageIcon} alt='' aria-hidden='true'></img>
                                            <span>Фото пока нет</span>
                                        </div>
                                    )}
                                </div>

                                <div className='hotel-card-content'>
                                    <h2>{hotel.name}</h2>

                                    <p>
                                        {hotel.description ||
                                            'Описание пока не добавлено.'}
                                    </p>

                                    <button type='button'>
                                        Подробнее
                                    </button>
                                </div>
                            </article>
                        ))}
                    </section>
                )}
            </div>
        </main>
    );
}

export default Hotels;
