@echo off
title HireLens Auto-Start
echo.
echo ========================================
echo     HireLens Auto-Start System
echo ========================================
echo.
echo This will automatically start the backend server
echo and keep it running in the background.
echo.

cd /d "d:\Windsurf\Hire lens FYP\hire_lens-dev"

:CHECK_BACKEND
echo Checking if backend is already running...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "uvicorn" >NUL
if %ERRORLEVEL% EQU 0 (
    echo ✅ Backend is already running!
    goto :FRONTEND
) else (
    echo ❌ Backend not running, starting it now...
    start "HireLens Backend" /MIN python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    echo ⏳ Waiting for backend to start...
    timeout /t 5 /nobreak >nul
    goto :CHECK_BACKEND
)

:FRONTEND
echo.
echo 🚀 Starting frontend...
cd frontend
start "HireLens Frontend" cmd /k "npm run dev"

echo.
echo ✅ HireLens is starting up!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause >nul
