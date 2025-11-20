from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="AI System Agent",
    description="AI agent for DB + File System Operations",
    version="1.0.0",
)

app.include_router(router)
