@echo off
REM ==============================================================================
REM Model Initialization Script for AI Karmayogi (Windows Batch)
REM Automatically pulls required open-weights models into the local Ollama service
REM ==============================================================================

echo ==========================================================
echo AI Karmayogi -- Sovereign Cognitive Model Initializer
echo ==========================================================

set OLLAMA_CONTAINER=karmayogi_ollama

echo 1. Pulling nomic-embed-text (768-dimensional local embeddings)...
docker exec -i %OLLAMA_CONTAINER% ollama pull nomic-embed-text

echo 2. Pulling qwen3:8b (Sovereign reasoning and scenario generation LLM)...
docker exec -i %OLLAMA_CONTAINER% ollama pull qwen3:8b

echo ==========================================================
echo Active Sovereign Models:
docker exec -i %OLLAMA_CONTAINER% ollama list
echo ==========================================================
echo AI Engine models successfully initialized!
pause
