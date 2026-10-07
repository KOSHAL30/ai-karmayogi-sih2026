#!/usr/bin/env bash
# ==============================================================================
# AI KARMAYOGI — SOVEREIGN ONE-COMMAND LAUNCHER (Linux / macOS)
# Smart India Hackathon 2026 (Problem Statement: SIH26101)
# ==============================================================================

set -e

echo ""
echo "=============================================================================="
echo "  AI KARMAYOGI — SOVEREIGN CAPACITY BUILDING PLATFORM"
echo "  Mission Karmayogi Bharat | Smart India Hackathon 2026"
echo "=============================================================================="
echo ""

# 1. Check Docker
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed or not in PATH."
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 2. Check Environment Configuration
if [ ! -f .env ]; then
    echo "[SETUP] Creating local .env from .env.example..."
    cp .env.example .env
fi

# 3. Launch Docker Compose Stack
echo "[DEPLOY] Building and starting sovereign containers..."
docker compose up --build -d

echo ""
echo "=============================================================================="
echo "  SOVEREIGN STACK INITIALIZED SUCCESSFULLY!"
echo "=============================================================================="
echo ""
echo "  - Web Application:         http://localhost"
echo "  - OpenAPI Documentation:   http://localhost/api/v1/docs"
echo "  - Health Endpoint:         http://localhost/health"
echo ""
echo "  EVALUATOR SHORTCUTS:"
echo "  - SIH Demo Cockpit:        Press Ctrl + Shift + D anywhere on the portal"
echo "  - Command Palette:         Press Ctrl + K for universal search"
echo ""
echo "  DEFAULT DEMO CREDENTIALS:"
echo "  - Admin:   priya.nair@karmayogi.gov.in     | Karmayogi2026!"
echo "  - Learner: rajesh.kumar@gov.in             | Karmayogi2026!"
echo "  - Trainer: sunita.deshmukh@nic.in          | Karmayogi2026!"
echo ""
echo "=============================================================================="
