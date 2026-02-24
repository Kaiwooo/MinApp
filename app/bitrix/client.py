import httpx
import logging

from app.storage import BITRIX_AUTH
from app.bitrix.oauth import refresh_token

logging.basicConfig(level=logging.INFO)


async def call(method: str, payload: dict | None = None):
    auth = BITRIX_AUTH.get("default")

    if not auth:
        logging.error("❌ Bitrix not installed")
        return None

    url = auth["client_endpoint"].rstrip("/") + f"/{method}.json"

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            params={"auth": auth["access_token"]},
            json=payload or {},
            timeout=10
        )

    data = resp.json()
    logging.info(f"[BITRIX] {method} → {data}")

    if data.get("error") == "expired_token":
        logging.info("Token expired. Refreshing...")
        await refresh_token(auth)
        return await call(method, payload)

    return data