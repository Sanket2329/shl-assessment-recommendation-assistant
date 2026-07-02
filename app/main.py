import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(__name__)

from app.api.chat import router as chat_router
from app.services.embedding_service import EmbeddingService

logger.info("Application modules loaded")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Warming up services...")
    try:
        EmbeddingService.get_client()
        logger.info("EmbeddingService client ready")
    except Exception as exc:
        logger.error("EmbeddingService warm-up failed: %s", exc)

    logger.info("Application startup complete")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="SHL Assessment Recommender",
    description=(
        "AI-powered SHL assessment recommendation API. "
        "Submit a hiring requirement or job description and receive "
        "ranked SHL assessment recommendations with explanations."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(chat_router)


@app.get("/", tags=["General"])
def root():
    return {"message": "SHL Assessment Recommender API", "docs": "/docs"}


@app.get("/health", tags=["General"])
def health():
    return {"status": "ok"}
