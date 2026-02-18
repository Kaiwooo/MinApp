from fastapi import APIRouter, Request
import logging
import json
import httpx

from application.storage import BITRIX_AUTH

logging.basicConfig(level=logging.INFO)

bitrix_app_router = APIRouter()


async def finish_install(auth: dict):
    """
    Завершение установки приложения Bitrix24
    https://apidocs.bitrix24.ru/settings/app-installation/installation-finish.html
    """
    url = auth["server_endpoint"] + "app.install.finish"

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            params={"auth": auth["access_token"]},
            timeout=10
        )

    logging.info("INSTALL FINISH RESPONSE:")
    logging.info(resp.text)


@bitrix_app_router.post("/install")
async def install(request: Request):
    # Получаем тело запроса
    raw_body = await request.body()
    logging.info("RAW BODY:")
    logging.info(raw_body.decode("utf-8", errors="ignore"))

    data = None
    try:
        data = await request.json()
    except Exception:
        pass

    if data is None:
        form = await request.form()
        data = dict(form)

    logging.info("PARSED DATA:")
    logging.info(json.dumps(data, indent=2, ensure_ascii=False))

    # Сбор auth
    auth = {}
    for k, v in data.items():
        if k.startswith("auth[") and k.endswith("]"):
            auth[k[5:-1]] = v

    logging.info("AUTH:")
    logging.info(auth)

    if auth:
        BITRIX_AUTH["default"] = auth
        logging.info("✅ Auth сохранён в BITRIX_AUTH")
        await finish_install(auth)

    return {"status": "ok"}
