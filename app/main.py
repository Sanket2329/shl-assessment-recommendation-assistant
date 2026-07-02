from contextlib import asynccontextmanager

from fastapi import FastAPI

print("Loading app...", flush=True)

from app.api.chat import router as chat_router
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_service import VectorService

print("Imports complete", flush=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up all services once at startup so the first request is fast
    print("Warming up services...", flush=True)

    try:
        EmbeddingService.get_client()
        print("EmbeddingService ready", flush=True)
    except Exception as e:
        print(f"EmbeddingService warm-up failed: {e}", flush=True)

    print("All services warmed up", flush=True)

    yield

    print("App shutting down", flush=True)


app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0",
    lifespan=lifespan,
)

print("FastAPI created", flush=True)

app.include_router(chat_router)

print("Router attached", flush=True)


@app.get("/")
def root():
    return {"message": "SHL Assessment Recommender API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
