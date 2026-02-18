from fastapi import APIRouter, Request

bitrix_router = APIRouter()

def extract_auth(data: dict) -> dict:
    auth = {}
    for k, v in data.items():
        if k.startswith("auth[") and k.endswith("]"):
            auth[k[5:-1]] = v
    return auth