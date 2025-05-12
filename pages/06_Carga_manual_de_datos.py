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

def get_user_id(username):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def backfill_exercise(user_id, exercise_id, sets, reps, duration, pain_notes, backfill_date):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exercise_logs (user_id, date, exercise_id, sets_completed, reps_completed, duration_completed_seconds, pain_notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, backfill_date, exercise_id, sets, reps, duration, pain_notes),
    )
    conn.commit()
    conn.close()

def backfill_meal(user_id, meal_type, description, calories, protein, backfill_date):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO food_logs (user_id, date, meal_type, description, calories_kcal, protein_g) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, backfill_date, meal_type, description, calories, protein),
    )
    conn.commit()
    conn.close()

def backfill_data():
    st.title("Backfill Data")

    if "username" not in st.session_state:
        st.error("Por favor, inicie sesión para acceder a esta página.")
        return

    username = st.session_state["username"]
    user_id = get_user_id(username)

    if user_id:
        # Fetch all exercises from the database for the dropdown
        conn = sqlite3.connect("health_plan.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, exercise_name FROM exercise_plan")
        exercises = cursor.fetchall()
        conn.close()

        exercise_options = {exercise[1]: exercise[0] for exercise in exercises}

        # Backfill Exercises Form
        st.write("### Backfill Ejercicios")
        with st.form("backfill_exercise_form"):
            selected_exercise = st.selectbox("Seleccione un Ejercicio", options=list(exercise_options.keys()), key="exercise_select")

            sets = st.number_input("Series", min_value=1, step=1, key="sets_input")
            reps = st.number_input("Repeticiones", min_value=1, step=1, key="reps_input")
            duration = st.number_input("Duración (segundos)", min_value=1, step=1, key="duration_input")

            st.write("Notas sobre Dolor")
            pain_notes = st.radio(
                "",
                options=["😊", "😐", "😖"],
                horizontal=True,
                label_visibility="collapsed",
                key="pain_notes_radio"
            )

            backfill_date = st.date_input("Fecha del Ejercicio", key="exercise_date_input")

            if st.form_submit_button("Registrar Ejercicio Atrasado"):
                exercise_id = exercise_options[selected_exercise]
                backfill_exercise(user_id, exercise_id, sets, reps, duration, pain_notes, backfill_date)
                st.success("¡Ejercicio atrasado registrado exitosamente!")

        # Backfill Meals Form
        st.write("### Backfill Comidas")
        with st.form("backfill_meal_form"):
            meal_type = st.selectbox("Tipo de Comida", ["Desayuno", "Almuerzo", "Cena", "Merienda"], key="meal_type_select")
            description = st.text_input("Descripción", key="meal_description_input")
            calories = st.number_input("Calorías (kcal)", min_value=1, step=1, key="calories_input")
            protein = st.number_input("Proteínas (g)", min_value=0.1, step=0.1, key="protein_input")
            backfill_date = st.date_input("Fecha de la Comida", key="meal_date_input")

            if st.form_submit_button("Registrar Comida Atrasada"):
                if not description:
                    st.error("Por favor, ingrese una descripción para la comida.")
                else:
                    backfill_meal(user_id, meal_type, description, calories, protein, backfill_date)
                    st.success("¡Comida atrasada registrada exitosamente!")
    else:
        st.error("Datos del usuario no encontrados.")

backfill_data()