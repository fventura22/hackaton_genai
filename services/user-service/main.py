from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import hashlib

app = FastAPI(title="User Management Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

SECRET_KEY = "fraud_detection_secret_key"

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: str
    permissions: list

# Mock user database
users_db = {
    "fraud_analyst": {
        "user_id": "USER001",
        "username": "fraud_analyst",
        "password_hash": hashlib.sha256("analyst123".encode()).hexdigest(),
        "role": "analyst",
        "permissions": ["view_cases", "analyze_fraud", "create_reports"]
    },
    "admin": {
        "user_id": "USER002",
        "username": "admin",
        "password_hash": hashlib.sha256("1234".encode()).hexdigest(),
        "role": "admin",
        "permissions": ["view_cases", "analyze_fraud", "create_reports", "manage_users", "system_config"]
    }
}

def create_token(user_data: dict) -> str:
    payload = {
        "user_id": user_data["user_id"],
        "username": user_data["username"],
        "role": user_data["role"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
async def login(request: LoginRequest):
    user = users_db.get(request.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(verify_token)):
    user = users_db.get(current_user["username"])
    return UserResponse(
        user_id=user["user_id"],
        username=user["username"],
        role=user["role"],
        permissions=user["permissions"]
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)