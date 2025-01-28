from fastapi import APIRouter
import requests

router = APIRouter()

@router.post("/start", tags=["connections"])
def start():
    return {"success": False, "error": "Not implemented"}