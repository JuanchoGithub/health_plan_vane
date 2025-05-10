import streamlit as st
import sqlite3
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def register_user(username, password, start_date_plan, current_weight_kg):
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, start_date_plan, current_weight_kg) VALUES (?, ?, ?, ?)",
            (username, hash_password(password), start_date_plan, current_weight_kg),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    finally:
        conn.close()