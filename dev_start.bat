@echo off
REM ==============================================================================
REM AI KARMAYOGI — DUAL-SERVER QUICK LAUNCHER (Windows)
REM Launches both FastAPI Backend and Vite React Frontend in separate windows
REM ==============================================================================

echo ==============================================================================
echo   STARTING AI KARMAYOGI DEVELOPMENT SERVERS
echo   Mission Karmayogi Bharat | Smart India Hackathon 2026
echo ==============================================================================
echo.

REM Start FastAPI Backend on Port 8000 in a new window
echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "AI Karmayogi - Backend (FastAPI)" cmd /k "cd backend && python -m uvicorn app.main:app --port 8000 --reload"

REM Wait 2 seconds for backend to bind
timeout /t 2 /nobreak >nul

REM Start React 19 Frontend on Port 5173 in a new window
echo [2/2] Starting React 19 Frontend on http://localhost:5173 ...
start "AI Karmayogi - Frontend (Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo ==============================================================================
echo   SERVERS LAUNCHED SUCCESSFULLY!
echo ==============================================================================
echo.
echo   - Web Application UI:      http://localhost:5173
echo   - FastAPI OpenAPI Docs:    http://localhost:8000/api/v1/docs
echo   - Health Check:            http://localhost:8000/health
echo.
echo   EVALUATOR SHORTCUTS (in browser):
echo   - SIH Demo Cockpit:        Press Ctrl + Shift + D
echo   - Spotlight Command Palette: Press Ctrl + K
echo.
echo   DEMO CREDENTIALS:
echo   - Admin:   priya.nair@karmayogi.gov.in     | Karmayogi2026!
echo   - Learner: rajesh.kumar@gov.in             | Karmayogi2026!
echo   - Trainer: sunita.deshmukh@nic.in          | Karmayogi2026!
echo.
echo   Opening web browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5173
