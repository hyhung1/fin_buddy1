@echo off
title Start FinancialBuddy Dev Server
echo ===================================
echo    Starting Financial Analysis Buddy Dev Server
echo ===================================

cd /d "%~dp0"

:: Start the backend server in background of current window
cd python_backend
start /b python -m uvicorn main:app --reload --port 8000
cd ..

:: Start the client in dev mode
cd client
npm run dev

pause 