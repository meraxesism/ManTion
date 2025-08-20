@echo off
echo Starting ManTion System...
echo.

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Starting API server...
start "ManTion API Server" cmd /k "python api_server.py"

echo [3/3] Starting frontend...
cd mantion-frontend
start "ManTion Frontend" cmd /k "npm start"

echo.
echo ManTion system is starting up!
echo - API Server: http://localhost:5000
echo - Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
