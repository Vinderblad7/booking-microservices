import './DestinationCard.css'

function DestinationCard({ image, name, price }) {
    return (
        <article className='destination-card'>

            <img 
                className='destination-card-image'
                src={image}
                alt={name}
            />

            <div className="destination-card-info">
                <h3>{name}</h3>
                <span>от {price} ₽</span>
            </div>

        </article>
    );
};

export default DestinationCard;