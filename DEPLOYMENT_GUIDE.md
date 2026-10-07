# AI Karmayogi — Complete Local Deployment Guide

**Smart India Hackathon 2026** | **Problem Statement:** `SIH26101`  
**Target:** Local, On-Premises, and Sovereign Air-Gapped Deployments

---

## 1. System Requirements & Prerequisites

### Hardware Specifications
| Specification | Minimum (CPU-Only) | Recommended (GPU Accelerated) |
| :--- | :--- | :--- |
| **Processor** | 8-Core Intel Core i7 / AMD Ryzen 7 | 8-Core Intel Core i7 / AMD Ryzen 7 |
| **RAM** | 16 GB DDR4/DDR5 | 16 GB – 32 GB DDR5 |
| **GPU / VRAM** | None (CPU inference supported) | NVIDIA RTX 3060 / 4060 / A100 (8GB+ VRAM) |
| **Storage** | 50 GB NVMe SSD | 100 GB NVMe SSD |
| **OS** | Windows 10/11, Ubuntu 22.04+, RHEL 9 | Ubuntu 22.04 LTS, Windows 11 with WSL2 |

### Software Prerequisites
- **Docker Desktop** (v24.0+) with Docker Compose v2.20+
- **NVIDIA Container Toolkit** (Optional, for GPU acceleration on Linux/WSL2)
- **Git** (for version control)

---

## 2. Fast-Track Deployment (Docker Compose)

The fastest and most reliable way to launch the entire multi-tier stack is via our automated one-command launchers.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Avengers-SIH/AI-Karmayogi.git
cd AI-Karmayogi
```

### Step 2: Launch the Sovereign Stack

#### On Windows:
Double-click `run.bat` or execute in PowerShell / Command Prompt:
```cmd
run.bat
```

#### On Linux / macOS:
```bash
chmod +x run.sh docker/init_models.sh
./run.sh
```

*Or manually using standard Docker Compose:*
```bash
docker compose up --build -d
```

### Step 3: Initialize Sovereign Cognitive Models
Once containers are running, pull the local embedding and reasoning models:

#### On Windows:
```cmd
docker\init_models.bat
```

#### On Linux / macOS:
```bash
./docker/init_models.sh
```

This will download:
- `nomic-embed-text`: 768-dimensional local embedding model (~270MB).
- `qwen3:8b`: Sovereign instruction-following & scenario LLM (~4.7GB).

---

## 3. Verifying the Deployment

### Service Endpoints
Once running, verify each tier:

| Service | URL | Expected Response |
| :--- | :--- | :--- |
| **Web Portal** | `http://localhost` | AI Karmayogi Sovereign Home Screen |
| **FastAPI Swagger Docs** | `http://localhost/api/v1/docs` | Interactive OpenAPI documentation |
| **System Health Probe** | `http://localhost/health` | `{"status": "healthy", ...}` |
| **Ollama Inference Engine** | `http://localhost:11434` | `Ollama is running` |

### Default SIH Evaluator Personas
Log in with any of the pre-seeded official civil service accounts:

| Role | Account Email | Default Password | Designation |
| :--- | :--- | :--- | :--- |
| **Admin** | `priya.nair@karmayogi.gov.in` | `Karmayogi2026!` | Director, Capacity Building |
| **Learner** | `rajesh.kumar@gov.in` | `Karmayogi2026!` | Under Secretary, DoPT |
| **Trainer** | `sunita.deshmukh@nic.in` | `Karmayogi2026!` | Senior Faculty, ISTM |

### Keyboard Shortcuts
- Press **`Ctrl + Shift + D`** anywhere in the app to open the **SIH Evaluator Demo Cockpit** for instant 1-click persona switching and telemetry synchronization.
- Press **`Ctrl + K`** to open the **Spotlight Command Palette** for instant universal navigation.

---

## 4. Alternative Bare-Metal Local Setup (Without Docker)

For environments where Docker cannot be used, run the stack natively:

### Step 1: MongoDB Atlas Vector Search
1. Install MongoDB Atlas and the `Atlas Vector Search` extension.
2. Create database and user:
```sql
CREATE DATABASE karmayogi_db;
CREATE USER karmayogi_admin WITH PASSWORD 'KarmayogiSecure2026';
GRANT ALL PRIVILEGES ON DATABASE karmayogi_db TO karmayogi_admin;
\c karmayogi_db;
CREATE EXTENSION IF NOT EXISTS vector;
```
3. Initialize the schema and seed data:
```bash
psql -U karmayogi_admin -d karmayogi_db -f database/schema.sql
psql -U karmayogi_admin -d karmayogi_db -f database/seed_data.sql
```

### Step 2: Ollama Local Inference
1. Install Ollama from [https://ollama.ai](https://ollama.ai).
2. Start the Ollama server: `ollama serve`.
3. Pull the required models:
```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

### Step 3: FastAPI Backend
```bash
cd backend
python -m venv venv
# Activate virtualenv:
# Windows: venv\Scripts\activate | Linux: source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: React 19 Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`, proxying API requests to `http://localhost:8000`.

---

## 5. Automated Verification & Testing

Verify that all backend unit, integration, RAG, and analytics suites pass:
```bash
cd backend
python run_all_tests.py
```
**Expected Result:**
```
======================================================================
 EXECUTIVE TEST EXECUTION SUMMARY
======================================================================
SUITE                                    | TESTS  | FAIL  | STATUS
----------------------------------------------------------------------
Authentication & Security                | 4      | 0     | [PASS]
Assessment & FRAC Diagnostics            | 4      | 0     | [PASS]
Recommendation Engine & Path             | 2      | 0     | [PASS]
Sovereign RAG & PDF Intelligence         | 4      | 0     | [PASS]
Admin Telemetry, Certificates & Router   | 6      | 0     | [PASS]
----------------------------------------------------------------------
TOTAL TESTS: 20 | TOTAL FAILURES: 0 | ERRORS: 0
======================================================================
>>> ALL VERIFICATION CHECKS PASSED PERFECTLY! [RELEASE CANDIDATE READY] <<<
```

Verify frontend production bundle build:
```bash
cd frontend
npm run build
```
**Expected Result:**
`✓ built in ~58s` with modular chunked assets in `dist/`.

---

## 6. Air-Gapped & Offline Deployment Protocol

For high-security government installations (e.g., defense institutes, air-gapped data centers):
1. **Pre-Package Container Images:** On an internet-connected staging machine:
```bash
docker save Atlas Vector Search/Atlas Vector Search:pg16 ollama/ollama:latest nginx:alpine -o sovereign_images.tar
```
2. **Pre-Cache Ollama Models:** Copy the `~/.ollama` or `karmayogi_ollamadata` volume directory to an encrypted physical medium.
3. **Transfer to Air-Gapped Target:** Load images via `docker load -i sovereign_images.tar` and place the Ollama models in the container volume path.
4. **Boot Stack:** Execute `run.bat` or `./run.sh`. The entire platform runs without requesting a single external DNS packet or cloud token.

---

## 7. Troubleshooting & Common Questions

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| **Port 80 Already in Use** | Local IIS, Apache, or Skype occupying port 80 | Edit `docker-compose.yml` line 28 to map `"8080:80"`. Access UI at `http://localhost:8080`. |
| **Ollama Model Download Slow** | High network latency during initial pull | Models are persistent; they only download once into `karmayogi_ollamadata`. Once cached, boot is instantaneous. |
| **CUDA Out of Memory** | High batch size or insufficient GPU VRAM | Ollama automatically falls back to system RAM (CPU mode) if VRAM is saturated. |
| **MongoDB Atlas Connection Refused** | Container initialization lag | Backend has automated healthcheck waiting for `pg_isready` before starting application server. |
