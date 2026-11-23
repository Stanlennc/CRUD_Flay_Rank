from fastapi import APIRouter
from app.database import ping_redis

router = APIRouter()

@router.get("/hello")
def get_message():
    return {"message": "Hello World!"}

@router.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0.0",
        "endpoints": ["/tasks"],
    }

@router.get("/health")
def health():
    return {"status": "ok", "redis": ping_redis()}
