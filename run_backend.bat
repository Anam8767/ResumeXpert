@echo off
title HireLens Backend Server
echo.
echo ========================================
echo       HireLens Backend Server
echo ========================================
echo.
echo Starting backend server...
echo Please wait for "Application startup complete" message
echo.

cd /d "d:\Windsurf\Hire lens FYP\hire_lens-dev"

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Backend server stopped!
pause
