# 3-Month Health Plan App

This project is a Streamlit application designed to help users follow a 3-month health plan for alleviating sciatica and increasing muscle mass. The app includes features such as user authentication, a daily dashboard, and progress tracking.

## Prerequisites

1. Install Python (version 3.8 or higher):
   - Download and install Python from [python.org](https://www.python.org/downloads/).
   - During installation, ensure you check the box to add Python to your system PATH.

2. Verify Python installation:
   ```bash
   python --version
   ```

3. Install `pip` (Python package manager) if not already installed:
   ```bash
   python -m ensurepip --upgrade
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd health_plan_vane
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python database.py
   ```

## Execution

Run the Streamlit app:
```bash
streamlit run app.py
```

Alternatively, use the provided `.bat` script to start the app:
```bash
run_app.bat
```