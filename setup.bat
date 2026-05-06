@echo off
REM Installation and setup script for Uber Driver Profit Maximizer Dashboard (Windows)

echo ==================================
echo Uber Driver Profit Maximizer Setup
echo ==================================
echo.

REM Check Python version
echo Checking Python installation...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Run tests
echo.
echo Running pipeline tests...
python test_pipeline.py

echo.
echo ==================================
echo Setup complete!
echo ==================================
echo.
echo To run the dashboard:
echo   venv\Scripts\activate.bat
echo   streamlit run app.py
echo.
pause
