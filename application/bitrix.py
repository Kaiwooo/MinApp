from fastapi import APIRouter
import httpx
import logging
from application.storage import BITRIX_AUTH

bitrix_router = APIRouter()

def get_oauth_base(auth: dict) -> str:
    # https://oauth.bitrix24.tech/rest/ -> https://oauth.bitrix24.tech
    return auth["server_endpoint"].replace("/rest/", "")

def extract_auth(data: dict) -> dict:
    auth = {}
    for k, v in data.items():
        if k.startswith("auth[") and k.endswith("]"):
            auth[k[5:-1]] = v
    return auth

BITRIX_OAUTH_URL = "https://oauth.bitrix.info/oauth/token/"

async def refresh_access_token(auth: dict) -> dict:
    oauth_base = get_oauth_base(auth)
    url = f"{oauth_base}/oauth/token/"

    data = {
        "grant_type": "refresh_token",
        "client_id": auth["client_id"],
        "client_secret": auth["client_secret"],
        "refresh_token": auth["refresh_token"],
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=data, timeout=10)
        resp.raise_for_status()
        token_data = resp.json()

    auth["access_token"] = token_data["access_token"]
    auth["refresh_token"] = token_data.get("refresh_token", auth["refresh_token"])
    auth["expires_in"] = token_data.get("expires_in")

    logging.info("🔄 OAuth token refreshed")

    return auth

async def bitrix_api_call(auth: dict, method: str, payload: dict | None = None):
    url = auth["client_endpoint"].rstrip("/") + f"/{method}.json"

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            params={"auth": auth["access_token"]},
            json=payload,
            timeout=10
        )

    data = resp.json()
    logging.info(f"BITRIX API [{method}] RESPONSE:")
    logging.info(data)

    if data.get("error") == "expired_token":
        await refresh_access_token(auth)
        return await bitrix_api_call(auth, method, payload)

    return data


# ===== imconnector =====

async def get_connectors(auth: dict):
    return await bitrix_api_call(auth, "imconnector.list")