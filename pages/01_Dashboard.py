import streamlit as st
import sqlite3
from datetime import date
from database import get_user_id
from streamlit_cookies_manager import EncryptedCookieManager
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def log_exercise(user_id, exercise_id, sets, reps, duration, pain_notes):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exercise_logs (user_id, date, exercise_id, sets_completed, reps_completed, duration_completed_seconds, pain_notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, date.today(), exercise_id, sets, reps, duration, pain_notes),
    )
    conn.commit()
    conn.close()

def log_meal(user_id, meal_type, description, calories, protein):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO food_logs (user_id, date, meal_type, description, calories_kcal, protein_g) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, date.today(), meal_type, description, calories, protein),
    )
    conn.commit()
    conn.close()

def get_weekly_exercises_with_media(current_week):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, exercise_name, description, media_path FROM exercise_plan WHERE ? BETWEEN week_start AND week_end",
        (current_week,)
    )
    exercises = cursor.fetchall()
    conn.close()
    return exercises

def calculate_daily_targets(weight_kg):
    # Calculate daily protein target (1.6-2.2 g/kg of body weight)
    protein_target_min = round(weight_kg * 1.6, 1)
    protein_target_max = round(weight_kg * 2.2, 1)

    # Set a fixed calorie target (e.g., 2000 kcal for simplicity, can be adjusted later)
    calorie_target = 2000

    return calorie_target, protein_target_min, protein_target_max

def get_weekly_monthly_summary(user_id):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()

    # Weekly summary (last 7 days)
    cursor.execute(
        """
        SELECT SUM(calories_kcal), SUM(protein_g), COUNT(DISTINCT date)
        FROM food_logs
        WHERE user_id = ? AND date >= date('now', '-7 days')
        """,
        (user_id,)
    )
    weekly_calories, weekly_protein, weekly_days_logged = cursor.fetchone()

    # Monthly summary (last 30 days)
    cursor.execute(
        """
        SELECT SUM(calories_kcal), SUM(protein_g), COUNT(DISTINCT date)
        FROM food_logs
        WHERE user_id = ? AND date >= date('now', '-30 days')
        """,
        (user_id,)
    )
    monthly_calories, monthly_protein, monthly_days_logged = cursor.fetchone()

    conn.close()

    return {
        "weekly": {
            "calories": weekly_calories or 0,
            "protein": weekly_protein or 0,
            "days_logged": weekly_days_logged or 0,
        },
        "monthly": {
            "calories": monthly_calories or 0,
            "protein": monthly_protein or 0,
            "days_logged": monthly_days_logged or 0,
        },
    }

def get_completed_exercises(user_id, current_date):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT exercise_id, SUM(sets_completed), SUM(reps_completed), SUM(duration_completed_seconds)
        FROM exercise_logs
        WHERE user_id = ? AND date = ?
        GROUP BY exercise_id
        """,
        (user_id, current_date),
    )
    completed_exercises = cursor.fetchall()
    conn.close()
    return {exercise[0]: exercise for exercise in completed_exercises}

def get_exercise_defaults(exercise_id):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT description FROM exercise_plan WHERE id = ?",
        (exercise_id,)
    )
    description = cursor.fetchone()[0]
    conn.close()

    # Extract default values from the description
    # This is a simplified example; parsing may need to be adjusted based on actual descriptions
    sets = 2  # Default fallback
    reps = 10  # Default fallback
    duration = 30  # Default fallback

    if "series" in description.lower():
        try:
            sets = int(description.split("series")[0].split()[-1])
        except ValueError:
            pass  # Keep default if parsing fails

    if "repeticiones" in description.lower():
        try:
            reps = int(description.split("repeticiones")[0].split()[-1])
        except ValueError:
            pass  # Keep default if parsing fails

    if "segundos" in description.lower():
        duration_text = description.split("segundos")[0].split()[-1]
        if "-" in duration_text:
            try:
                duration = int(duration_text.split("-")[0])  # Take the lower bound of the range
            except ValueError:
                pass  # Keep default if parsing fails
        else:
            try:
                duration = int(duration_text)
            except ValueError:
                pass  # Keep default if parsing fails

    return sets, reps, duration

def get_exercise_defaults_from_plan(exercise_name):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT default_sets, default_reps, default_duration FROM exercise_plan WHERE exercise_name = ?",
        (exercise_name,)
    )
    defaults = cursor.fetchone()
    conn.close()
    return defaults if defaults else (1, 1, 0)  # Fallback to default values

def dashboard():
    st.title("Panel Diario")

    # Initialize exercise_df at the start of the dashboard function
    exercise_df = pd.DataFrame(columns=["Ejercicio", "Estado", "Series", "Repeticiones", "Duración (s)", "Notas"])

    if "username" not in st.session_state:
        st.error("Por favor, inicie sesión para ver su panel.")
        return

    username = st.session_state["username"]
    user_data = get_user_data(username)

    if user_data:
        start_date_plan, current_weight_kg = user_data
        days_in_plan = (date.today() - date.fromisoformat(start_date_plan)).days
        current_week = (days_in_plan // 7) + 1
        st.subheader(f"Semana {current_week} de su Plan")

        # Calculate daily targets
        calorie_target, protein_target_min, protein_target_max = calculate_daily_targets(current_weight_kg)

        # Fetch logged data for today
        conn = sqlite3.connect("health_plan.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(calories_kcal), SUM(protein_g) FROM food_logs WHERE user_id = ? AND date = ?", (get_user_id(username), date.today()))
        logged_calories, logged_protein = cursor.fetchone()
        conn.close()

        logged_calories = logged_calories or 0
        logged_protein = logged_protein or 0

        # Fetch exercises and completed exercises
        exercises = get_weekly_exercises_with_media(current_week)
        user_id = get_user_id(username)
        completed_exercises = get_completed_exercises(user_id, date.today())

        # Use a dictionary to ensure unique exercises by exercise_id
        unique_exercises = {exercise[0]: exercise for exercise in exercises}

        # Add notifications for incomplete tasks
        if len(completed_exercises) < len(unique_exercises):
            st.warning(f"Tienes {len(unique_exercises) - len(completed_exercises)} ejercicios pendientes hoy.")

        if logged_calories < calorie_target:
            st.warning(f"Te faltan {calorie_target - logged_calories} kcal para alcanzar tu meta diaria de calorías.")

        if logged_protein < protein_target_min:
            st.warning(f"Te faltan {protein_target_min - logged_protein} g de proteínas para alcanzar tu meta mínima diaria.")

        # Optimize layout using collapsible sections
        with st.expander("Resumen Diario", expanded=True):
            st.write("### Resumen Diario")
            st.metric("Calorías Consumidas", f"{logged_calories}/{calorie_target} kcal", delta=logged_calories - calorie_target, key="calories_metric")
            st.metric("Proteínas Consumidas", f"{logged_protein}/{protein_target_min}-{protein_target_max} g", delta=logged_protein - protein_target_min, key="protein_metric")
            st.metric("Ejercicios Completados", f"{len(completed_exercises)}/{len(unique_exercises)}", key="exercises_metric")

        with st.expander("Progreso de Hoy", expanded=True):
            st.write("### Progreso de Hoy")
            st.metric("Calorías Consumidas", f"{logged_calories}/{calorie_target} kcal", delta=logged_calories - calorie_target)
            st.metric("Proteínas Consumidas", f"{logged_protein} g", delta=logged_protein - protein_target_min)

            calorie_progress = min(int((logged_calories / calorie_target) * 100), 100)
            protein_progress = min(int((logged_protein / protein_target_min) * 100), 100)

            st.progress(calorie_progress, text=f"Calorías: {logged_calories}/{calorie_target} kcal")
            st.caption(f"Progreso de Calorías: {calorie_progress}%")

            st.progress(protein_progress, text=f"Proteínas: {logged_protein}/{protein_target_min}-{protein_target_max} g")
            st.caption(f"Progreso de Proteínas: {protein_progress}%")

        with st.expander("Resumen de Ejercicios", expanded=True):
            st.write("### Resumen de Ejercicios")
            # Ensure completed exercises are correctly reflected in the Resumen de Ejercicios table
            exercise_data = []
            if unique_exercises:
                for exercise_id, exercise_name, description, media_path in unique_exercises.values():
                    is_completed = exercise_id in completed_exercises
                    status = "Completado" if is_completed else "Pendiente"
                    sets, reps, duration = (completed_exercises[exercise_id][1:4] if is_completed else ("-", "-", "-"))
                    notes = "Ejercicio completado correctamente" if is_completed else ""
                    exercise_data.append({
                        "Ejercicio": exercise_name,
                        "Estado": status,
                        "Series": sets,
                        "Repeticiones": reps,
                        "Duración (s)": duration,
                        "Notas": notes
                    })

            # Update exercise_df if exercise_data is populated
            exercise_df = pd.DataFrame(exercise_data) if exercise_data else pd.DataFrame(columns=["Ejercicio", "Estado", "Series", "Repeticiones", "Duración (s)", "Notas"])
            st.dataframe(exercise_df)

        # Organize sections using tabs
        tabs = st.tabs(["Progreso Diario", "Resumen Semanal", "Resumen Mensual"])

        with tabs[0]:
            # Daily progress content
            st.write("### Metas de Hoy")
            st.metric("Calorías Objetivo", f"{calorie_target} kcal")
            st.metric("Proteínas Objetivo", f"{protein_target_min}-{protein_target_max} g")

            st.write("### Esto es lo que te falta hacer hoy")
            for exercise_id, exercise_name, description, media_path in unique_exercises.values():
                is_completed = exercise_id in completed_exercises
                with st.expander(f"{exercise_name} {'✅' if is_completed else '❌'}"):
                    st.markdown(f"<p style='font-size:18px'><b>Instrucciones:</b> {description}</p>", unsafe_allow_html=True)
                    if media_path:
                        media_video_path = media_path.replace('.jpg', '.mp4')
                        if os.path.exists(media_video_path):
                            st.video(media_video_path, format="video/mp4")
                        elif os.path.exists(media_path):
                            st.image(media_path, use_container_width=True)

                    if is_completed:
                        completed_data = completed_exercises[exercise_id]
                        st.success(f"Ejercicio completado: {completed_data[1]} series, {completed_data[2]} repeticiones, {completed_data[3]} segundos.")
                    else:
                        st.warning("Este ejercicio aún no se ha completado.")

                        # Add a button to log default exercise completion with actual defaults
                        if st.button(f"Registrar como completado - {exercise_name}", key=f"log_{exercise_id}", aria_label=f"Complete {exercise_name}"):
                            default_sets, default_reps, default_duration = get_exercise_defaults(exercise_id)
                            log_exercise(user_id, exercise_id, default_sets, default_reps, default_duration, "")
                            st.success(f"¡Ejercicio '{exercise_name}' registrado exitosamente con valores predeterminados!")

            # Custom Exercise Logging
            st.write("### Registrar Ejercicio Personalizado")
            st.write("Ingrese los detalles de un ejercicio que no esté en el plan o seleccione uno existente.")

            # Fetch all exercise names for selection
            conn = sqlite3.connect("health_plan.db")
            cursor = conn.cursor()
            cursor.execute("SELECT exercise_name FROM exercise_plan")
            exercise_names = [row[0] for row in cursor.fetchall()]
            conn.close()

            selected_exercise = st.selectbox("Seleccione un ejercicio (opcional)", [""] + exercise_names)

            if selected_exercise:
                default_sets, default_reps, default_duration = get_exercise_defaults_from_plan(selected_exercise)

                with st.form("custom_exercise_form"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        custom_sets = st.selectbox("Series", options=list(range(1, default_sets + 1)), index=default_sets - 1)
                    with col2:
                        custom_reps = st.selectbox("Repeticiones", options=list(range(1, default_reps + 1)), index=default_reps - 1)
                    with col3:
                        custom_duration = st.number_input("Duración (segundos)", min_value=0, step=1, value=default_duration)

                    st.write("Notas sobre Dolor")
                    custom_pain_notes = st.radio(
                        "",
                        options=["😊", "😐", "😖"],
                        horizontal=True,
                        label_visibility="collapsed",
                        key="emoji-radio"
                    )

                    if st.form_submit_button("Registrar Ejercicio Personalizado"):
                        log_exercise(user_id, None, custom_sets, custom_reps, custom_duration, custom_pain_notes)
                        st.success(f"¡Ejercicio '{selected_exercise}' registrado exitosamente!")
            else:
                st.warning("Debe seleccionar un ejercicio para registrar un ejercicio personalizado.")

            st.write("### Registrar Comida")
            st.write("Ingrese los detalles de las comidas que consumió hoy.")
            with st.form("log_meal_form", key="log_meal_form", aria_label="Log Meal Form"):
                meal_type = st.selectbox("Tipo de Comida", ["Desayuno", "Almuerzo", "Cena", "Merienda"], key="meal_type_select", aria_label="Meal Type")
                description = st.text_input("Descripción", key="meal_description", aria_label="Meal Description")
                calories = st.number_input("Calorías (kcal)", min_value=0, step=1, key="meal_calories", aria_label="Meal Calories")
                protein = st.number_input("Proteínas (g)", min_value=0.0, step=0.1, key="meal_protein", aria_label="Meal Protein")
                if st.form_submit_button("Registrar Comida", key="submit_meal", aria_label="Submit Meal"):
                    log_meal(username, meal_type, description, calories, protein)
                    st.success("¡Comida registrada exitosamente!")

        with tabs[1]:
            # Weekly summary content
            st.write("### Resumen Semanal")
            summary = get_weekly_monthly_summary(get_user_id(username))
            st.metric("Calorías Consumidas", f"{summary['weekly']['calories']} kcal")
            st.metric("Proteínas Consumidas", f"{summary['weekly']['protein']} g")
            st.metric("Días Registrados", f"{summary['weekly']['days_logged']} días")

            # Weekly trends
            weekly_data = []
            conn = sqlite3.connect("health_plan.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT date, SUM(calories_kcal), SUM(protein_g) FROM food_logs WHERE user_id = ? AND date >= date('now', '-7 days') GROUP BY date",
                (get_user_id(username),)
            )
            weekly_data = cursor.fetchall()
            conn.close()

            if weekly_data:
                dates, calories, proteins = zip(*weekly_data)
                fig, ax = plt.subplots()
                ax.plot(dates, calories, label="Calorías", marker="o")
                ax.plot(dates, proteins, label="Proteínas", marker="o")
                ax.set_title("Tendencias Semanales")
                ax.set_xlabel("Fecha")
                ax.set_ylabel("Cantidad")
                ax.legend()
                st.pyplot(fig)

        with tabs[2]:
            # Monthly summary content
            st.write("### Resumen Mensual")
            summary = get_weekly_monthly_summary(get_user_id(username))
            st.metric("Calorías Consumidas", f"{summary['monthly']['calories']} kcal")
            st.metric("Proteínas Consumidas", f"{summary['monthly']['protein']} g")
            st.metric("Días Registrados", f"{summary['monthly']['days_logged']} días")

            # Monthly trends
            monthly_data = []
            conn = sqlite3.connect("health_plan.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT date, SUM(calories_kcal), SUM(protein_g) FROM food_logs WHERE user_id = ? AND date >= date('now', '-30 days') GROUP BY date",
                (get_user_id(username),)
            )
            monthly_data = cursor.fetchall()
            conn.close()

            if monthly_data:
                dates, calories, proteins = zip(*monthly_data)
                fig, ax = plt.subplots()
                ax.plot(dates, calories, label="Calorías", marker="o")
                ax.plot(dates, proteins, label="Proteínas", marker="o")
                ax.set_title("Tendencias Mensuales")
                ax.set_xlabel("Fecha")
                ax.set_ylabel("Cantidad")
                ax.legend()
                st.pyplot(fig)

        st.write("### Resumen de Progreso")
        st.write("Esta sección mostrará sus métricas de progreso.")
    else:
        st.error("Datos del usuario no encontrados.")

dashboard()