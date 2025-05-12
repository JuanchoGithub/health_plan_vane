import streamlit as st
from auth import authenticate_user, register_user
from database import initialize_database
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title="Plan de Salud de 3 Meses", layout="wide")

# Initialize cookie manager
cookies = EncryptedCookieManager(
    password="a_secure_password_for_encryption"  # Replace with a secure password
)
if not cookies.ready():
    st.stop()

def main():
    st.title("Bienvenido/a a la App del Plan de Salud de 3 Meses")

    # Initialize the database
    initialize_database()

    # Check for existing session via cookies
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None

    if not st.session_state["authenticated"]:
        cookie_username = cookies.get("username")
        if cookie_username:
            st.session_state["authenticated"] = True
            st.session_state["username"] = cookie_username

    if not st.session_state["authenticated"]:
        st.sidebar.title("Iniciar Sesión / Registrarse")
        auth_choice = st.sidebar.radio(
            "Seleccione una opción de autenticación", 
            ["Iniciar Sesión", "Registrarse"],
            key="auth_choice",
            format_func=lambda x: x,
        )

        if auth_choice == "Iniciar Sesión":
            username = st.sidebar.text_input("Nombre de Usuario", key="login_username")
            password = st.sidebar.text_input("Contraseña", type="password", key="login_password")
            if st.sidebar.button("Iniciar Sesión", key="login_button"):
                if authenticate_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    cookies["username"] = username
                    cookies.save()
                    st.success("¡Inicio de sesión exitoso!")
                else:
                    st.error("Nombre de usuario o contraseña inválidos.")

        elif auth_choice == "Registrarse":
            username = st.sidebar.text_input("Nombre de Usuario", key="register_username")
            password = st.sidebar.text_input("Contraseña", type="password", key="register_password")
            start_date_plan = st.sidebar.date_input("Fecha de Inicio del Plan", key="register_start_date")
            current_weight_kg = st.sidebar.number_input("Peso Actual (kg)", min_value=0.0, step=0.1, key="register_weight")
            if st.sidebar.button("Registrarse", key="register_button"):
                register_user(username, password, start_date_plan, current_weight_kg)
                st.success("¡Registro exitoso! Por favor, inicie sesión.")
                st.sidebar.markdown('<div data-testid="register_button"></div>', unsafe_allow_html=True)

    if st.session_state["authenticated"]:
        st.sidebar.title("Navegación")
        st.sidebar.write("Seleccione una página desde la barra lateral.")
        st.write(f"¡Bienvenido/a, {st.session_state['username']}!")
        st.info("👈 Utiliza el menú de la izquierda para navegar por las secciones de la aplicación.", icon="ℹ️")

        # Show toast only once per session
        if 'sidebar_toast_shown' not in st.session_state:
            st.toast('👈 ¡Usa el menú para navegar!', icon='⬅️')
            st.session_state['sidebar_toast_shown'] = True

        if st.sidebar.button("Cerrar Sesión"):
            cookies["username"] = ""
            cookies.save()
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state.clear()
            st.experimental_set_query_params()

if __name__ == "__main__":
    main()