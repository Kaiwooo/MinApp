from fastapi import APIRouter
from aiogram import Bot, Dispatcher, types
from app.config import BOT_TOKEN
from app.storage import BITRIX_AUTH
import httpx

telegram_router = APIRouter()

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    auth = next(iter(BITRIX_AUTH.values()), None)

    if not auth:
        await message.answer("❌ Bitrix не подключён")
        return

    url = auth["client_endpoint"] + "crm.lead.add"

    payload = {
        "fields": {
            "TITLE": "Сообщение из Telegram",
            "COMMENTS": message.text,
            "SOURCE_ID": "WEB"
        }
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            url,
            params={"auth": auth["access_token"]},
            json=payload,
            timeout=10
        )

    await message.answer("✅ Отправлено в Bitrix")

@telegram_router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    await dp.feed_raw_update(bot, update)
    return {"ok": True}
