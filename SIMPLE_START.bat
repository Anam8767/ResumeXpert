@echo off
title HireLens - Simple Start
echo.
echo ========================================
echo       HireLens - Simple Start
echo ========================================
echo.
echo Starting backend server...
echo.

cd /d "d:\Windsurf\Hire lens FYP\hire_lens-dev"

echo Running: python app.py
python app.py

echo.
echo If backend started successfully:
echo 1. Open new terminal
echo 2. Run: cd frontend && npm run dev
echo 3. Open: http://localhost:5173
echo.
pause
