from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    # Mocking simple auth for now; would connect to src.core.security in reality
    if request.username == "admin" and request.password == "admin":
        return {
            "token": "mock-jwt-token-12345",
            "user": {
                "name": "Admin User",
                "role": "Executive",
                "email": "admin@readynest.com"
            }
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/me")
def get_current_user():
    return {
        "user": {
            "name": "Admin User",
            "role": "Executive",
            "email": "admin@readynest.com"
        }
    }
