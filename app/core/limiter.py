from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from core.security import decode_access_token, InvalidTokenError


def get_user_or_ip_identifier(request: Request) -> str:
    """
    Identifies the requester:
    1. If an Authorization Bearer token is provided and valid, rate limit by user_id.
    2. Otherwise, fallback to remote IP address.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")
            if user_id:
                return f"user:{user_id}"
        except InvalidTokenError:
            pass

    return f"ip:{get_remote_address(request)}"


# Initialize Limiter
# For Redis in production: Limiter(key_func=..., storage_uri="redis://localhost:6379/0")
limiter = Limiter(
    key_func=get_user_or_ip_identifier,
    default_limits=["100/minute"],
)
