"""Dependency injection helpers."""
from fastapi import Request, HTTPException, status

API_KEY_HEADER = "X-API-Key"

def verify_api_key(request: Request):
    api_key = request.headers.get(API_KEY_HEADER)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    # TODO: validate against tenant DB
    return api_key

def get_api_key(api_key: str = None):
    # Placeholder for actual dependency; we accept any string
    return api_key
