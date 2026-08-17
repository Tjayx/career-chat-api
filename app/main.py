from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from api.auth import router as auth_router
from api.conversations import router as conversations_router
from api.chat import router as chat_router
from core.limiter import limiter

app = FastAPI(
    title="Career Guidance AI API",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(conversations_router)
app.include_router(chat_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "Career Guidance AI API",
        "status": "running",
    }