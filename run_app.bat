@echo off
:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Run the Streamlit app
streamlit run app.py