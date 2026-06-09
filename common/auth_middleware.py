import os
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ignore well-known A2A agent card endpoints or local test endpoints if needed
        # but let's strictly check everything except docs.
        path = request.url.path
        if path in ["/docs", "/openapi.json"]:
            return await call_next(request)

        expected_key = os.getenv("A2A_API_KEY", "my-secret-a2a-key")
        
        # Lấy từ header
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != expected_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Invalid or missing X-API-Key header"},
            )
            
        response = await call_next(request)
        return response
