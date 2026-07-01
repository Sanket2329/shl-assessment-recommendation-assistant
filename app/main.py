from fastapi import FastAPI

print("Loading app...", flush=True)

from app.api.chat import router as chat_router

print("Router imported", flush=True)

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)

print("FastAPI created", flush=True)

app.include_router(chat_router)

print("Router attached", flush=True)


@app.get("/")
def root():
    print("Root endpoint called", flush=True)
    return {"message": "SHL Assessment Recommender API"}


@app.get("/health")
def health():
    print("Health endpoint called", flush=True)
    return {"status": "healthy"}