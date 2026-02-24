from fastapi import APIRouter, Request
#import logging
import json

from app.storage import BITRIX_AUTH
from app.bitrix.connectors import list_connectors

#logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

router = APIRouter()


@router.post("/install")
async def install(request: Request):
    raw = await request.body()
    logging.info("RAW INSTALL:")
    logging.info(raw.decode(errors="ignore"))

    data = None
    try:
        data = await request.json()
    except:
        form = await request.form()
        data = dict(form)

    auth = {}
    for k, v in data.items():
        if k.startswith("auth[") and k.endswith("]"):
            auth[k[5:-1]] = v

    if auth:
        BITRIX_AUTH["default"] = auth
        logging.info("✅ OAuth сохранён")

        connectors = await list_connectors()
        logging.info("CONNECTORS:")
        logging.info(json.dumps(connectors, indent=2, ensure_ascii=False))

    return {"status": "ok"}