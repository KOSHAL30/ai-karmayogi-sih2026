@echo off
REM ==============================================================================
REM AI KARMAYOGI — SOVEREIGN ONE-COMMAND LAUNCHER (Windows)
REM Smart India Hackathon 2026 (Problem Statement: SIH26101)
REM ==============================================================================

echo.
echo ==============================================================================
echo   AI KARMAYOGI -- SOVEREIGN CAPACITY BUILDING PLATFORM
echo   Mission Karmayogi Bharat ^| Smart India Hackathon 2026
echo ==============================================================================
echo.

REM 1. Check Docker Daemon
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH.
    echo Please install Docker Desktop for Windows: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM 2. Check Environment Configuration
if not exist .env (
    echo [SETUP] Creating local .env from .env.example...
    copy .env.example .env >nul
)

REM 3. Launch Docker Compose Stack
echo [DEPLOY] Building and starting sovereign containers...
docker compose up --build -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker containers.
    pause
    exit /b 1
)

echo.
echo ==============================================================================
echo   SOVEREIGN STACK INITIALIZED SUCCESSFULLY!
echo ==============================================================================
echo.
echo   - Web Application:         http://localhost
echo   - OpenAPI Documentation:   http://localhost/api/v1/docs
echo   - Health Endpoint:         http://localhost/health
echo.
echo   EVALUATOR SHORTCUTS:
echo   - SIH Demo Cockpit:        Press Ctrl + Shift + D anywhere on the portal
echo   - Command Palette:         Press Ctrl + K for universal search
echo.
echo   DEFAULT DEMO CREDENTIALS:
echo   - Admin:   priya.nair@karmayogi.gov.in     ^| Karmayogi2026!
echo   - Learner: rajesh.kumar@gov.in             ^| Karmayogi2026!
echo   - Trainer: sunita.deshmukh@nic.in          ^| Karmayogi2026!
echo.
echo ==============================================================================
pause
