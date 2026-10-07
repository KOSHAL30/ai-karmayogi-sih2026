# AI Karmayogi — Architecture

## Transactional / Relational Architecture

The application follows a standard layered FastAPI pattern, backing a React frontend:

**Frontend** (`frontend/src/api.ts`, React components)
↓ (HTTP REST)
**API Routers** (`backend/app/api/v1/endpoints/`)
↓ (Pydantic parsing)
**Services** (`backend/services/`)
↓ (Business Logic & Orchestration)
**Repositories** (`backend/repositories/`)
↓ (Motor AsyncIO)
**MongoDB Atlas** (`ai_karmayogi` database)

Important notes:
- Repositories return raw dictionaries (`dict`), not Pydantic objects.
- Services handle object mapping if needed, or pass dicts back to the API layer where Pydantic serializes them.
- `recursive_vars` conversion is required in API routes when dealing with nested `types.SimpleNamespace` objects returned from MongoDB cursor lists.

## AI & Vector Architecture

The AI layer strictly integrates with Groq for LLM and a local Ollama instance for embeddings.

**Frontend** (Document Studio, Learning Path)
↓ (HTTP REST)
**API Routers** (`documents.py`, `recommendations.py`)
↓
**AI Services** (`rag_service.py`, `mcq_service.py`, `learning_path_service.py`)
↓
**LLMProvider** (`backend/ai/llm_provider.py` - Groq Qwen 3.8 27B) / **EmbeddingService** (`backend/ai/embedding_service.py` - Ollama nomic-embed-text)
↓
**MongoDB Atlas Vector Search** (`document_chunks` collection -> `vector_index` index)

## Important Runtime Paths
- **Config**: `backend/app/core/config.py`
- **Dependencies (Auth/DB)**: `backend/app/core/deps.py`
- **FastAPI App**: `backend/app/main.py`
- **Vite Config**: `frontend/vite.config.ts`
