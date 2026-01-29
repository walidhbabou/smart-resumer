@echo off
REM SmartResume Analyzer - Windows Setup Script

echo ================================================
echo SmartResume Analyzer - Setup Script (Windows)
echo ================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is installed

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed.
    pause
    exit /b 1
)
echo [OK] Docker Compose is installed

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo [OK] .env file created. Please edit it with your API keys.
) else (
    echo [OK] .env file already exists
)

REM Create backend .env if it doesn't exist
if not exist backend\.env (
    echo Creating backend\.env file...
    copy backend\.env.example backend\.env
    echo [OK] backend\.env file created
) else (
    echo [OK] backend\.env file already exists
)

REM Create frontend .env if it doesn't exist
if not exist frontend\.env (
    echo Creating frontend\.env file...
    copy frontend\.env.example frontend\.env
    echo [OK] frontend\.env file created
) else (
    echo [OK] frontend\.env file already exists
)

echo.
echo ================================================
echo Setup complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env files with your configuration
echo 2. Run: docker-compose up --build
echo 3. Access application at http://localhost:3000
echo 4. Access API docs at http://localhost:8000/api/docs
echo.
echo For local development without Docker:
echo   Backend:  cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt ^&^& uvicorn app.main:app --reload
echo   Frontend: cd frontend ^&^& npm install ^&^& npm run dev
echo.
pause
