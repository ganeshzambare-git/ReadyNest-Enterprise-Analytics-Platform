from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, data, executive

app = FastAPI(title="ReadyNest Analytics API")

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(executive.router, prefix="/api/executive", tags=["executive"])

@app.get("/")
def read_root():
    return {"message": "Welcome to ReadyNest Analytics API"}
