from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import llm

app = FastAPI(
    title="LLM API",
    description="API для работы Target AI Агента",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm.router, prefix="/llm")


@app.get("/")
def root() -> dict:
    return {"message": "LLM API is running"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
