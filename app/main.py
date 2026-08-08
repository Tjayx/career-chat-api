from fastapi import FastAPI

from app.api.auth import router as auth_router

app = FastAPI(
    title="Career Guidance AI API",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "Career Guidance AI API",
        "status": "running",
    }