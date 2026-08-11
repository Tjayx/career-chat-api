from fastapi import FastAPI

from api.auth import router as auth_router
from api.conversations import router as conversations_router
from api.chat import router as chat_router

app = FastAPI(
    title="Career Guidance AI API",
    version="1.0.0",
)

app.include_router(conversations_router)
app.include_router(chat_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "Career Guidance AI API",
        "status": "running",
    }