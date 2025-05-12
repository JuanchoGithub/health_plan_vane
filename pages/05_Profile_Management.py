import streamlit as st
import sqlite3
from datetime import date
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

def get_user_data(username):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT start_date_plan, current_weight_kg FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def update_user_weight(username, new_weight):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET current_weight_kg = ? WHERE username = ?", (new_weight, username))
    conn.commit()
    conn.close()

def profile_management():
    st.title("Gestión de Perfil")

    if "username" not in st.session_state:
        st.error("Por favor, inicie sesión para acceder a esta página.")
        return

    username = st.session_state["username"]
    user_data = get_user_data(username)

    if user_data:
        start_date_plan, current_weight_kg = user_data

        st.subheader("Información del Usuario")
        st.write(f"**Fecha de Inicio del Plan:** {start_date_plan}")
        st.write(f"**Peso Actual:** {current_weight_kg} kg")

        st.subheader("Actualizar Peso")
        with st.form("update_weight_form"):
            new_weight = st.number_input("Nuevo Peso (kg)", min_value=0.0, step=0.1, value=current_weight_kg, key="new_weight_input")
            # Use st.form_submit_button inside a form
            submitted = st.form_submit_button("Actualizar Peso")
            if submitted:
                update_user_weight(username, new_weight)
                st.success("¡Peso actualizado exitosamente!")

        # Re-fetching data after update for immediate reflection:
        if submitted:
             user_data = get_user_data(username) # Re-fetch data to get the updated weight
             if user_data:
                 _, current_weight_kg = user_data # Update current_weight_kg for calculations below

        st.subheader("Metas Diarias")
        # Use the potentially updated current_weight_kg for calculations
        protein_target_min = round(current_weight_kg * 1.6, 1)
        protein_target_max = round(current_weight_kg * 2.2, 1)
        calorie_target = 2000  # Default calorie target

        st.write(f"**Proteínas Objetivo:** {protein_target_min}-{protein_target_max} g")
        st.write(f"**Calorías Objetivo:** {calorie_target} kcal")

        st.info("Las metas de proteínas se calculan automáticamente en función de su peso actual.")
    else:
        st.error("Datos del usuario no encontrados.")

profile_management()