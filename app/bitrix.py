from fastapi import APIRouter, Request
import logging
import json
from urllib.parse import parse_qs
from app.storage import BITRIX_AUTH

bitrix_router = APIRouter()

def extract_auth(data: dict) -> dict:
    auth = {}
    for k, v in data.items():
        if k.startswith("auth[") and k.endswith("]"):
            auth[k[5:-1]] = v
    return auth

@bitrix_router.post("/install")
async def install(request: Request):
    body = (await request.body()).decode("utf-8", errors="ignore")
    parsed = parse_qs(body)
    data = {k: v[0] for k, v in parsed.items()}

    auth = extract_auth(data)
    member_id = auth.get("member_id")

    if member_id:
        BITRIX_AUTH[member_id] = auth
        logging.info(f"Bitrix installed: {member_id}")

    return {"status": "ok"}