from fastapi import APIRouter, Request
import logging, json
from application.storage import BITRIX_AUTH

logging.basicConfig(level=logging.INFO)

bitrix_app_router = APIRouter()

@bitrix_app_router.post("/install")
async def install(request: Request):
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

    auth = data.get("auth")
    logging.info("AUTH:")
    logging.info(auth)

    if auth:
        BITRIX_AUTH["default"] = auth

    return {"status": "ok"}