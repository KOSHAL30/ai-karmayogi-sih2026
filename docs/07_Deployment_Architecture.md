# 07_Deployment_Architecture.md

# Deployment Architecture: AI Karmayogi

**Production Docker Compose Topology, Sovereign Containerization, Nginx Gateway Configuration, and Self-Hosted FOSS Infrastructure**

**Document Version:** 1.0.0  
**Target Program:** Smart India Hackathon 2026  
**Problem Statement ID:** SIH26101  
**Project Name:** AI Karmayogi  
**Classification:** Enterprise Government Specification — Phase 2 Deployment Architecture  

---

## Table of Contents
1. [Deployment Principles & Sovereign Hosting Strategy](#1-deployment-principles--sovereign-hosting-strategy)
2. [High-Level Container Topology](#2-high-level-container-topology)
3. [Complete Production `docker-compose.yml`](#3-complete-production-docker-composeyml)
4. [Production Nginx Reverse Proxy Configuration (`nginx.conf`)](#4-production-nginx-reverse-proxy-configuration-nginxconf)
5. [Ollama Local Model Initialization & Pull Script](#5-ollama-local-model-initialization--pull-script)
6. [Hardware Sizing, System Requirements & Resource Limits](#6-hardware-sizing-system-requirements--resource-limits)
7. [Step-by-Step Installation & Verification Guide](#7-step-by-step-installation--verification-guide)

---

## 1. Deployment Principles & Sovereign Hosting Strategy

In alignment with Government of India digital sovereignty mandates, **AI Karmayogi** is 100% self-contained and operates exclusively using Free and Open Source Software (FOSS).

### Sovereign Deployment Guardrails:
- **Zero Cloud API Dependencies:** No external calls to OpenAI, Anthropic, Pinecone, Firebase, or proprietary foreign cloud services.
- **Sovereign Boundary Confinement:** Deployed on standard Linux servers (Ubuntu 22.04 LTS / RHEL 9) empanelled under MeitY / NIC MeghRaj.
- **Full Offline Operability:** Once initial container images and open-weights models (`nomic-embed-text`, `llama3.1:8b` / `qwen2.5:7b`) are loaded, the entire cognitive capacity platform functions without internet access.

---

## 2. High-Level Container Topology

```mermaid
graph TB
    subgraph Host_Environment ["Sovereign Server Environment (MeitY / NIC Cloud)"]
        subgraph Ingress_Network ["Ingress Network (Publicly Accessible)"]
            Nginx["Nginx Reverse Proxy<br/>(Ports 80 / 443)"]
        end

        subgraph App_Network ["Internal Application Network (Bridge: karmayogi_net)"]
            Frontend["Frontend Service<br/>(React 19 + Vite Static Assets)"]
            Backend["Backend API Service<br/>(FastAPI + Uvicorn Async Workers)"]
            Redis["Redis 7 Service<br/>(Session Cache & Task Queue)"]
        end

        subgraph Secure_AI_Network ["Secure Storage & AI Network (Internal Only)"]
            Postgres[("MongoDB Atlas Vector Search<br/>(Port 5432 - Internal)")]
            Ollama["Ollama Local AI Engine<br/>(Port 11434 - Internal)<br/>* nomic-embed-text<br/>* Llama 3.1:8b / Qwen 2.5:7b"]
        end

        subgraph Persistent_Volumes ["Host Storage Volumes"]
            V_PGData[("pgdata_vol<br/>(Relational & Vector Data)")]
            V_RedisData[("redisdata_vol<br/>(Cache & Sessions)")]
            V_OllamaModels[("ollama_vol<br/>(Local AI Model Weights)")]
            V_Uploads[("uploads_vol<br/>(Ingested Government PDFs)")]
        end
    end

    UserBrowser["Civil Servant / Admin Browser"] -->|HTTPS (Port 443)| Nginx
    Nginx -->|Proxy Static /| Frontend
    Nginx -->|Proxy /api/v1| Backend

    Backend -->|Cache / Sessions| Redis
    Backend -->|SQL & Vector Search| Postgres
    Backend -->|Embeddings & LLM Inference| Ollama

    Postgres --> V_PGData
    Redis --> V_RedisData
    Ollama --> V_OllamaModels
    Backend --> V_Uploads
```

---

## 3. Complete Production `docker-compose.yml`

Save the following file as `docker-compose.yml` in the project root:

```yaml
version: '3.8'

networks:
  karmayogi_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

volumes:
  pgdata:
    name: karmayogi_pgdata
  redisdata:
    name: karmayogi_redisdata
  ollamadata:
    name: karmayogi_ollamadata
  document_uploads:
    name: karmayogi_uploads

services:
  # =========================================================================
  # 1. Reverse Proxy & Gateway (Nginx)
  # =========================================================================
  nginx:
    image: nginx:alpine
    container_name: karmayogi_gateway
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - frontend
      - backend
    networks:
      - karmayogi_net
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost/healthz || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3

  # =========================================================================
  # 2. Presentation Tier: React 19 Frontend
  # =========================================================================
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: karmayogi_frontend
    restart: unless-stopped
    environment:
      - VITE_API_BASE_URL=/api/v1
    networks:
      - karmayogi_net

  # =========================================================================
  # 3. Application Tier: FastAPI Backend Server
  # =========================================================================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: karmayogi_backend
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql+asyncpg://karmayogi_admin:KarmayogiSecure2026@postgres:5432/karmayogi_db
      - REDIS_URL=redis://redis:6379/0
      - OLLAMA_BASE_URL=http://ollama:11434
      - JWT_SECRET=sovereign_secret_key_sih2026_dopt_mission_karmayogi
      - JWT_ALGORITHM=HS256
      - UPLOAD_DIR=/app/uploads
      - EMBEDDING_MODEL=nomic-embed-text
      - LLM_MODEL=llama3.1:8b
    volumes:
      - document_uploads:/app/uploads
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      ollama:
        condition: service_started
    networks:
      - karmayogi_net
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4096M

  # =========================================================================
  # 4. In-Memory Cache & Task Queue: Redis 7
  # =========================================================================
  redis:
    image: redis:7-alpine
    container_name: karmayogi_redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redisdata:/data
    networks:
      - karmayogi_net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # =========================================================================
  # 5. Relational & Vector Persistence: MongoDB Atlas Vector Search
  # =========================================================================
  postgres:
    image: Atlas Vector Search/Atlas Vector Search:pg16
    container_name: karmayogi_postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=karmayogi_db
      - POSTGRES_USER=karmayogi_admin
      - POSTGRES_PASSWORD=KarmayogiSecure2026
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./03_Database_Schema.sql:/docker-entrypoint-initdb.d/01_init.sql:ro
    networks:
      - karmayogi_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U karmayogi_admin -d karmayogi_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8192M

  # =========================================================================
  # 6. Local Cognitive AI Inference Engine: Ollama
  # =========================================================================
  ollama:
    image: ollama/ollama:latest
    container_name: karmayogi_ollama
    restart: unless-stopped
    volumes:
      - ollamadata:/root/.ollama
    networks:
      - karmayogi_net
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
        limits:
          cpus: '8.0'
          memory: 16384M
```

---

## 4. Production Nginx Reverse Proxy Configuration (`nginx.conf`)

Save the following file as `nginx.conf`:

```nginx
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  4096;
    use epoll;
    multi_accept on;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    types_hash_max_size 2048;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;

    # Rate Limiting Zone (100 req/min for general, 10 req/min for AI endpoints)
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=ai_limit:10m rate=20r/m;

    upstream frontend_upstream {
        server frontend:80;
    }

    upstream backend_upstream {
        server backend:8000;
        keepalive 32;
    }

    server {
        listen 80;
        server_name _;

        # Client Body Limits for PDF Uploads
        client_max_body_size 50M;

        # Health Check
        location /healthz {
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # API Proxy Pass
        location /api/v1/ {
            limit_req zone=general_limit burst=20 nodelay;
            proxy_pass http://backend_upstream;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 180s;
            proxy_connect_timeout 60s;
        }

        # AI Generation Specific Rate Limit
        location /api/v1/quizzes/generate {
            limit_req zone=ai_limit burst=5 nodelay;
            proxy_pass http://backend_upstream;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 300s;
        }

        # Frontend Static Asset Delivery
        location / {
            proxy_pass http://frontend_upstream;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

---

## 5. Ollama Local Model Initialization & Pull Script

Once the containers are online, execute the following script to pull the mandatory open-weights models into the persistent Ollama volume:

```bash
#!/bin/bash
# ==============================================================================
# Model Initialization Script for AI Karmayogi
# Downloads 100% free, sovereign models into the Ollama container
# ==============================================================================

echo "Initializing AI Karmayogi Cognitive Models in Ollama..."

# 1. Pull nomic-embed-text for 768-dimensional semantic embeddings
echo "Pulling nomic-embed-text (Embedding Model)..."
docker exec -it karmayogi_ollama ollama pull nomic-embed-text

# 2. Pull Llama 3.1 8B (or Qwen 2.5 7B) for MCQ & scenario generation
echo "Pulling Llama 3.1 8B (Instruction-Tuned LLM)..."
docker exec -it karmayogi_ollama ollama pull llama3.1:8b

# Optional: Pull Qwen 2.5 7B for superior multilingual Indic capability
# docker exec -it karmayogi_ollama ollama pull qwen2.5:7b

echo "Model initialization complete! Active models in container:"
docker exec -it karmayogi_ollama ollama list
```

---

## 6. Hardware Sizing, System Requirements & Resource Limits

| Tier | Minimum Specification (Development / Demo) | Recommended Production (State / Central Pilot) |
| :--- | :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS / RHEL 9 (x86_64) | Ubuntu 22.04 LTS Enterprise Server |
| **Processor (CPU)** | 8 Cores (Intel Xeon / AMD EPYC) | 16 Cores |
| **Memory (RAM)** | 16 GB DDR4 | 32 GB – 64 GB DDR4 ECC |
| **GPU Acceleration** | CPU Only (Quantized 4-bit mode supported) | 1x NVIDIA Tesla T4 / A10 (16GB VRAM) |
| **Storage (SSD)** | 100 GB NVMe SSD | 500 GB NVMe SSD (Encrypted) |
| **Network Bandwidth** | 100 Mbps Ethernet | 1 Gbps DedicatedNIC Gateway |

---

## 7. Step-by-Step Installation & Verification Guide

Follow these steps to deploy AI Karmayogi on a fresh server:

### Step 1: Clone Repository & Prepare Directory Layout
```bash
git clone https://github.com/gov-tech/ai-karmayogi.git
cd ai-karmayogi
mkdir -p certs uploads
```

### Step 2: Launch Docker Compose Services
```bash
docker compose up -d --build
```

### Step 3: Verify Container Health Status
```bash
docker compose ps
```
Ensure all 6 services (`karmayogi_gateway`, `karmayogi_frontend`, `karmayogi_backend`, `karmayogi_redis`, `karmayogi_postgres`, `karmayogi_ollama`) report `Up` or `healthy`.

### Step 4: Pull Sovereign AI Models
```bash
chmod +x init_models.sh
./init_models.sh
```

### Step 5: Verify Schema & Database Initialization
```bash
docker exec -it karmayogi_postgres psql -U karmayogi_admin -d karmayogi_db -c "\dt"
```
Verify that all 17 tables from `03_Database_Schema.sql` are created and the `vector` extension is active.

### Step 6: Access the Application
Open a browser and navigate to:
- **Web Application:** `http://localhost/` (or server IP)
- **Interactive Swagger Docs:** `http://localhost/api/v1/docs`
- **Gateway Health Check:** `http://localhost/healthz`

---
*End of Deployment Architecture*
