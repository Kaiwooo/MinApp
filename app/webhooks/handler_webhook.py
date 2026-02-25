from fastapi import APIRouter, Request
import logging

router = APIRouter()

@router.post("/bitrix/webhook")
async def bitrix_webhook(request: Request):
    data = await request.json()

    logging.info("Получен webhook от Bitrix")
    logging.info(data)

    return {"status": "ok"}