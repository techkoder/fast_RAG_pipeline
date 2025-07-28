import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv
load_dotenv()

VALID_TOKEN = os.getenv("API_AUTH_TOKEN")

def verify_bearer_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    token = authorization.replace("Bearer ", "").strip()
    if token != VALID_TOKEN:
        raise HTTPException(status_code=403, detail=f"Invalid token: {token}")
    return True
