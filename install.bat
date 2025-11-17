@echo off
echo ===============================================
echo AI-Based Question Paper Moderation System
echo Installation Script for Windows
echo ===============================================
echo.

echo Step 1: Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Creating necessary directories...
if not exist "data" mkdir data
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

echo.
echo Step 3: Initializing database...
python -c "from core.database import Database; db = Database(); db.initialize(); print('Database initialized successfully')"

echo.
echo ===============================================
echo Backend installation complete!
echo ===============================================
echo.
echo To install the frontend, run:
echo   cd frontend
echo   npm install
echo   npm run build
echo.
echo To start the application:
echo   python run.py
echo.
pause
