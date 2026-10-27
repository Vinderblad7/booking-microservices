import AuthForm from "../../components/AuthForm/AuthForm";
import '../Login/Login.css'

function Login() {
    return (
        <main className="login-page">
            <section className="login-visual">

                <div className="login-visual-location">
                    <span>Fanal Forest, Madeira, Portugal</span>
                </div>

                <div className="login-visual-content">

                    <h1>
                        Возвращайтесь к своим путешествиям
                    </h1>

                    <p>
                        Ваши любимые места и новые впечатления
                        всегда ждут вас.
                    </p>
                </div>
            </section>

            <section className="login-content">
                <AuthForm mode="login" />
            </section>
        </main>
    );
}

export default Login;