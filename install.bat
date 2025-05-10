@echo off
:: Check if the virtual environment exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Initialize the database
echo Initializing the database...
python database.py

echo Installation complete. You can now run the app using run_app.bat.