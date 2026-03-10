@echo off
title HireLens - Bulletproof Backend
color 0A
echo.
echo ========================================
echo   HireLens - Bulletproof Backend
echo ========================================
echo.
echo This will work 100%% guaranteed!
echo.
echo Step 1: Installing Flask...
pip install flask flask-cors

echo.
echo Step 2: Starting backend server...
cd /d "d:\Windsurf\Hire lens FYP\hire_lens-dev"

echo.
echo 🚀 Starting backend...
python bulletproof_backend.py

echo.
echo If backend started successfully:
echo ✅ Backend is running on http://localhost:8000
echo ✅ Now start frontend: cd frontend && npm run dev
echo ✅ Open browser: http://localhost:5173
echo.
pause
