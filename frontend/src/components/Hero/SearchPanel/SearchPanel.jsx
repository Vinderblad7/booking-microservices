import {useState} from 'react';
import './SearchPanel.css';
import fieldIcon1 from '../../../assets/icons/field-icon-bg.svg';
import fieldIcon2 from '../../../assets/icons/field-icon-bg2.svg';
import fieldIcon3 from '../../../assets/icons/field-icon-bg3.svg';

function SearchPanel() {

    const [destination, setDestination] = useState('Paris');
    const [date, setDate] = useState('');
    const [guests, setGuests] = useState('1 гость');

    function handleSearch() {
        if (!destination || !date) {
            console.log('Выберите место и дату')
            return;
        }

        console.log({
            destination,
            date,
            guests
        });
    };

    return (
        <div className="search-panel">

            <div className="search-field">
                <img src={fieldIcon1} alt="location" className="search-field-icon" />

                <div className="search-field-content">
                    <span className='search-field-label'>Куда едем</span>
                    <select className='search-field-select'
                        value={destination}
                        onChange={(event) => setDestination(event.target.value)}
                    >
                        <option value="Paris">Париж</option>
                        <option value="Praha">Прага</option>
                        <option value="Barcelona">Барселона</option>
                        <option value="Rome">Рим</option>
                        <option value="Berlin">Берлин</option>
                    </select>
                </div>
                
            </div>

            <div className="search-field">
                <img src={fieldIcon2} alt="dates" className="search-field-icon" />

                <div className="search-field-content">
                    <span className="search-field-label">Даты</span>
                    
                    <input 
                        className="search-field-select-date" 
                        type='date'
                        value={date}
                        onChange={(event) => setDate(event.target.value)}
                     />
                </div>
                
            </div>

            <div className="search-field">
                <img src={fieldIcon3} alt="" className="search-field-icon" />

                <div className="search-field-content">
                    <span className="search-field-label">Кто едет</span>
                    
                    <select 
                        className="search-field-select"
                        value={guests}
                        onChange={(event) => setGuests(event.target.value)}
                    >
                        <option>1 гость</option>
                        <option>2 гостя</option>
                        <option>3 гостя</option>
                        <option>4 гостя</option>
                        <option>5 гостей</option>
                        <option>6 гостей</option>
                    </select>
                </div>
                
            </div>

            <button 
                className="search-field-button"
                onClick={handleSearch}
            >
                Найти туры
            </button>

        </div>
    );
}

export default SearchPanel