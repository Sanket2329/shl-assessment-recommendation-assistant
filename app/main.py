from fastapi import FastAPI

print("Loading app...")

from app.api.chat import router as chat_router

print("Router imported")

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)

print("FastAPI created")

app.include_router(chat_router)

print("Router attached")

@app.get("/")
def root():
    print("Root endpoint called")
    return {"message": "SHL Assessment Recommender API"}

@app.get("/health")
def health():
    print("Health endpoint called")
    return {"status": "healthy"}