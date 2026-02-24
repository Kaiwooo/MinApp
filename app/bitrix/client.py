import httpx
import logging

from app.storage import BITRIX_AUTH
from app.bitrix.oauth import refresh_token


async def call(method: str, payload: dict | None = None):
    auth = BITRIX_AUTH.get("default")

    if not auth:
        logging.error("❌ Bitrix not installed")
        return None

    # Чистый OAuth — используем только server_endpoint
    base_url = auth.get("server_endpoint")
    if not base_url:
        logging.error("❌ server_endpoint not found in auth")
        return None

    url = base_url.rstrip("/") + f"/{method}.json"

    logging.info(f"[BITRIX URL] {url}")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            params={"auth": auth["access_token"]},
            json=payload or {},
            timeout=10
        )

    data = resp.json()
    logging.info(f"[BITRIX] {method} → {data}")

    # Автообновление токена
    if data.get("error") == "expired_token":
        logging.info("🔄 Token expired. Refreshing...")
        await refresh_token(auth)
        return await call(method, payload)

    return data