from fastapi import APIRouter, Request
from aiogram.types import Update

from app.telegram.bot import dp, bot

router = APIRouter()

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}