import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(password="a_secure_password_for_encryption")
if not cookies.ready():
    st.stop()

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
    st.error("Por favor, inicie sesión para acceder a esta página.")
    st.stop()

def plan_maestro():
    st.title("Plan Maestro")

    st.write("### Resumen del Plan de Salud de 3 Meses")
    st.write("Esta página proporciona un desglose detallado del plan de salud, incluyendo metas semanales y hitos.")

    st.write("### Metas Semanales")
    st.write("- **Semana 1-4**: Enfocarse en construir consistencia con ejercicios y hábitos dietéticos.")
    st.write("- **Semana 5-8**: Aumentar gradualmente la intensidad y realizar un seguimiento del progreso.")
    st.write("- **Semana 9-12**: Optimizar el rendimiento y prepararse para la sostenibilidad a largo plazo.")

    st.write("### Componentes Clave")
    st.write("- **Plan de Ejercicios**: Una combinación de entrenamiento de fuerza, ejercicios de flexibilidad y cardio de bajo impacto.")
    st.write("- **Plan Dietético**: Comidas balanceadas con un enfoque en la ingesta de proteínas y el control de calorías.")

    st.write("### Recursos")
    st.write("- Descargue el plan completo en formato PDF.")
    st.download_button(
        label="Descargar Plan PDF",
        data="Este es un marcador de posición para el contenido del PDF.",
        file_name="Plan_Maestro.pdf",
        mime="application/pdf",
        key="download_plan_pdf",
        aria_label="Download Plan PDF"
    )

plan_maestro()