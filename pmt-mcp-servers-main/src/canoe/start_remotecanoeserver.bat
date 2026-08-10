@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo CANoe Remote Server Startup Script
echo ====================================================
echo.

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check if virtual environment exists
if not exist "venv\" (
    echo [INFO] Virtual environment not found. Creating venv...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        echo [ERROR] Please ensure Python is installed and available in PATH.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully.
    echo.
) else (
    echo [INFO] Virtual environment already exists.
    echo.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install/Update dependencies
echo [INFO] Installing/Updating dependencies...
echo.
python -m pip install --upgrade pip
pip install fastapi==0.109.2 uvicorn==0.27.1 pydantic==2.6.1 pywin32==306

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All dependencies installed successfully.
echo.

:: Prompt for port number
set /p PORT_NUMBER="Enter port number to start CANoe Remote Server (default: 8037): "

:: Use default if user pressed Enter without input
if "%PORT_NUMBER%"=="" (
    set PORT_NUMBER=8037
    echo [INFO] Using default port: 8037
)

:: Validate port number is numeric
set "valid=0"
for /f "delims=0123456789" %%i in ("%PORT_NUMBER%") do set valid=1
if %valid%==1 (
    echo [ERROR] Invalid port number. Port must be numeric.
    pause
    exit /b 1
)

:: Check if port is in valid range
if %PORT_NUMBER% LSS 1 (
    echo [ERROR] Port number must be greater than 0.
    pause
    exit /b 1
)
if %PORT_NUMBER% GTR 65535 (
    echo [ERROR] Port number must be less than 65536.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo Starting CANoe Remote Server on 0.0.0.0:%PORT_NUMBER%
echo ====================================================
echo.
echo Press Ctrl+C to stop the server
echo.

:: Run the server
python remotecanoeserver.py --port %PORT_NUMBER%

:: Deactivate virtual environment on exit
deactivate

pause
