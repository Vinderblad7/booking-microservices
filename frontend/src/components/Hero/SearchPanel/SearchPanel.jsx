import './SearchPanel.css'
import fieldIcon1 from '../../../assets/icons/field-icon-bg.svg'
import fieldIcon2 from '../../../assets/icons/field-icon-bg2.svg'
import fieldIcon3 from '../../../assets/icons/field-icon-bg3.svg'

function SearchPanel() {
    return (
        <div className="search-panel">

            <div className="search-field">
                <img src={fieldIcon1} alt="location" className="search-field-icon" />

                <div className="search-field-content">
                    <span className="search-field-label">Куда летим</span>
                    <span className="search-field-value">Бали, Индонезия</span>
                </div>
                
            </div>

            <div className="search-field">
                <img src={fieldIcon2} alt="dates" className="search-field-icon" />

                <div className="search-field-content">
                    <span className="search-field-label">Даты</span>
                    <span className="search-field-value">24 Мая - 8 Июня</span>
                </div>
                
            </div>

            <div className="search-field">
                <img src={fieldIcon3} alt="" className="search-field-icon" />

                <div className="search-field-content">
                    <span className="search-field-label">Кто едет</span>
                    <span className="search-field-value">2 Взрослых, Бизнес</span>
                </div>
                
            </div>

            <button className="search-field-button">Найти туры</button>

        </div>
    );
}

export default SearchPanel