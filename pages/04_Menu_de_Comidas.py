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

# Load the content of the markdown file
file_path = "documentation/COMIDAS.markdown"
with open(file_path, "r", encoding="utf-8") as file:
    markdown_content = file.read()

# Streamlit page to display the content
st.markdown(markdown_content, unsafe_allow_html=True)