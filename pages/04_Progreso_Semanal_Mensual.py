import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from database import get_user_id
from streamlit_cookies_manager import EncryptedCookieManager
import plotly.express as px

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

def fetch_progress_data(user_id):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()

    # Fetch exercise logs
    cursor.execute("""
        SELECT el.date, ep.exercise_name, el.sets_completed, el.reps_completed
        FROM exercise_logs el
        JOIN exercise_plan ep ON el.exercise_id = ep.id
        WHERE el.user_id = ?
    """, (user_id,))
    exercise_logs = cursor.fetchall()

    # Fetch food logs
    cursor.execute("SELECT date, meal_type, calories_kcal, protein_g FROM food_logs WHERE user_id = ?", (user_id,))
    food_logs = cursor.fetchall()

    conn.close()
    return exercise_logs, food_logs

def progreso():
    st.title("Progreso Semanal y Mensual")

    if "username" not in st.session_state:
        st.error("Por favor, inicie sesión para ver su progreso.")
        return

    username = st.session_state["username"]
    user_id = get_user_id(username)

    if user_id:
        exercise_logs, food_logs = fetch_progress_data(user_id)

        # Progreso Semanal
        st.subheader("Progreso Semanal")
        if exercise_logs:
            weekly_data = pd.DataFrame(exercise_logs, columns=["Fecha", "Ejercicio", "Series Completadas", "Repeticiones Completadas"])
            weekly_data["Fecha"] = pd.to_datetime(weekly_data["Fecha"])

            # Add a column to indicate completion status
            weekly_data["Estado"] = weekly_data["Series Completadas"].apply(lambda x: "Completado" if x > 0 else "Pendiente")

            # Group by week and summarize
            weekly_summary = weekly_data.groupby(weekly_data["Fecha"].dt.isocalendar().week).agg({
                "Series Completadas": "sum",
                "Repeticiones Completadas": "sum",
                "Estado": lambda x: (x == "Completado").sum()  # Count completed exercises
            })

            st.write("### Resumen Semanal de Ejercicios")
            st.dataframe(weekly_summary)

            # Weekly Progress Visualization
            weekly_summary = weekly_data.groupby(weekly_data["Fecha"].dt.isocalendar().week).sum(numeric_only=True).reset_index()
            weekly_summary.rename(columns={"week": "Semana"}, inplace=True)

            st.write("### Visualización Semanal de Ejercicios")
            fig = px.bar(weekly_summary, x="Semana", y="Series Completadas", title="Series Completadas por Semana", labels={"Series Completadas": "Series"},
                         hover_data={"Series Completadas": True})
            st.plotly_chart(fig)

            # Add filters for date ranges
            st.write("### Filtrar por Rango de Fechas")
            start_date = st.date_input("Fecha de Inicio", value=pd.to_datetime("2025-01-01"), key="start_date_input", aria_label="Start Date")
            end_date = st.date_input("Fecha de Fin", value=pd.to_datetime("2025-05-10"), key="end_date_input", aria_label="End Date")

            filtered_weekly_data = weekly_data[(weekly_data["Fecha"] >= pd.to_datetime(start_date)) & (weekly_data["Fecha"] <= pd.to_datetime(end_date))]
            filtered_weekly_summary = filtered_weekly_data.groupby(filtered_weekly_data["Fecha"].dt.isocalendar().week).sum(numeric_only=True).reset_index()
            filtered_weekly_summary.rename(columns={"week": "Semana"}, inplace=True)

            fig = px.bar(filtered_weekly_summary, x="Semana", y="Series Completadas", title="Series Completadas por Semana (Filtrado)", labels={"Series Completadas": "Series"})
            st.plotly_chart(fig)

            # Add annotations for milestones
            max_series = weekly_summary["Series Completadas"].max()
            max_week = weekly_summary[weekly_summary["Series Completadas"] == max_series]["Semana"].values[0]
            fig.add_annotation(x=max_week, y=max_series, text="Máximo", showarrow=True, arrowhead=2)
            st.plotly_chart(fig)

            # Add a summary table below charts
            st.write("### Resumen Semanal")
            st.dataframe(weekly_summary)

            # Add a comparison feature
            st.write("### Comparar Progreso")
            comparison_week = st.selectbox("Seleccione una Semana para Comparar", weekly_summary["Semana"], key="comparison_week_select", aria_label="Comparison Week")
            comparison_data = weekly_summary[weekly_summary["Semana"] == comparison_week]
            st.write(f"Comparación para la Semana {comparison_week}")
            st.dataframe(comparison_data)

        else:
            st.write("No hay datos de ejercicios disponibles para esta semana.")

        # Progreso Mensual
        st.subheader("Progreso Mensual")
        st.write("Esta sección mostrará resúmenes mensuales con visualizaciones.")

        # Ejemplo de Visualización
        st.write("### Gráfico de Progreso Ejemplo")
        dates = [log[0] for log in food_logs]
        calories = [log[2] for log in food_logs]

        if dates and calories:
            df = pd.DataFrame({"Fecha": dates, "Calorías": calories})
            df["Fecha"] = pd.to_datetime(df["Fecha"])
            df = df.groupby("Fecha").sum()

            fig, ax = plt.subplots()
            df.plot(ax=ax, kind="bar")
            st.pyplot(fig)

            # Monthly Progress Visualization
            monthly_data = pd.DataFrame(food_logs, columns=["Fecha", "Tipo de Comida", "Calorías", "Proteínas"])
            monthly_data["Fecha"] = pd.to_datetime(monthly_data["Fecha"])

            # Group by month and summarize
            monthly_summary = monthly_data.groupby(monthly_data["Fecha"].dt.to_period("M")).sum(numeric_only=True).reset_index()
            monthly_summary["Fecha"] = monthly_summary["Fecha"].dt.to_timestamp()

            st.write("### Visualización Mensual de Calorías y Proteínas")
            fig = px.line(monthly_summary, x="Fecha", y=["Calorías", "Proteínas"], title="Tendencias Mensuales de Calorías y Proteínas", labels={"value": "Cantidad", "variable": "Métrica"})
            fig.update_layout(legend_title_text="Métricas", legend=dict(itemsizing="constant"))
            st.plotly_chart(fig)

            # Add a summary table below charts
            st.write("### Resumen Mensual")
            st.dataframe(monthly_summary)

            # Improve chart titles and labels
            fig.update_layout(title="Series Completadas por Semana (Mejorado)", xaxis_title="Semana", yaxis_title="Series Completadas")
            st.plotly_chart(fig)
        else:
            st.write("No hay datos disponibles para visualización.")
    else:
        st.error("Datos del usuario no encontrados.")

progreso()