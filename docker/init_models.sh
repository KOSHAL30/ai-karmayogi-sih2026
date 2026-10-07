#!/bin/bash
# ==============================================================================
# Model Initialization Script for AI Karmayogi
# Automatically pulls required open-weights models into the local Ollama service
# ==============================================================================

set -e

echo "=========================================================="
echo "AI Karmayogi — Sovereign Cognitive Model Initializer"
echo "=========================================================="

OLLAMA_CONTAINER="karmayogi_ollama"

echo "Checking Ollama container status..."
if ! docker ps --format '{{.Names}}' | grep -q "^${OLLAMA_CONTAINER}$"; then
    echo "Error: Container '${OLLAMA_CONTAINER}' is not running."
    echo "Please start the stack with: docker compose up -d"
    exit 1
fi

echo "1. Pulling nomic-embed-text (768-dimensional local embeddings)..."
docker exec -i ${OLLAMA_CONTAINER} ollama pull nomic-embed-text

echo "2. Pulling qwen3:8b (Sovereign reasoning & scenario generation LLM)..."
docker exec -i ${OLLAMA_CONTAINER} ollama pull qwen3:8b

echo "=========================================================="
echo "Active Sovereign Models in ${OLLAMA_CONTAINER}:"
docker exec -i ${OLLAMA_CONTAINER} ollama list
echo "=========================================================="
echo "AI Engine models successfully initialized!"
