import AuthForm from "../../components/AuthForm/AuthForm";
import "./Register.css";

function Register() {
    return (
        <main className="register-page">
            <section className="register-visual">

                <div className="register-visual-location">
                        <span>Амальфитанское побережье, Италия</span>
                </div>

                <div className="register-visual-content">
                    
                    <h1>
                        Ваше следующее<br></br>путешествие
                        начинается<br></br>здесь
                    </h1>

                    <p>
                        Сохраняйте любимые места и планируйте
                        путешествия удобнее.
                    </p>

                </div>

            </section>

            <section className="register-form">
                <AuthForm mode="register"/>
            </section>

        </main>
    );
}

export default Register;
