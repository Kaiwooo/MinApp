from fastapi import APIRouter, Request
import logging, json
from application.storage import BITRIX_AUTH

logging.basicConfig(level=logging.INFO)

bitrix_app_router = APIRouter()

@bitrix_app_router.post("/install")
async def install(request: Request):
    # Получаем "сырое" тело запроса
    raw_body = await request.body()
    logging.info("RAW BODY:")
    logging.info(raw_body.decode("utf-8", errors="ignore"))

    data = None
    try:
        data = await request.json()  # пробуем JSON
    except Exception:
        pass

    if data is None:
        form = await request.form()  # если не JSON — читаем form-data
        data = dict(form)

    logging.info("PARSED DATA:")
    logging.info(json.dumps(data, indent=2, ensure_ascii=False))

    # Собираем auth из всех полей вида auth[...]
    auth = {}
    for k, v in data.items():
        if k.startswith("auth[") and k.endswith("]"):
            auth[k[5:-1]] = v

    logging.info("AUTH:")
    logging.info(auth)

    # Сохраняем в глобальное хранилище, чтобы Telegram-бот мог использовать
    if auth:
        BITRIX_AUTH["default"] = auth
        logging.info("✅ Auth сохранён в BITRIX_AUTH")

    return {"status": "ok"}