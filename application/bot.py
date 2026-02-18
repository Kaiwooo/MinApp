import logging
import httpx
from fastapi import APIRouter
from aiogram import Bot, Dispatcher, types

from application.config import BOT_TOKEN
from application.storage import BITRIX_AUTH

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

telegram_router = APIRouter()

OPENLINE_ID = 2  # жёстко указываем ID открытой линии


@telegram_router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    await dp.feed_raw_update(bot, update)
    return {"ok": True}


async def send_message_to_openline(
    auth: dict,
    message: types.Message
):
    url = auth["client_endpoint"] + "imopenlines.message.add"

    payload = {
        "LINE_ID": OPENLINE_ID,
        "MESSAGE": message.text,
        "USER_ID": f"telegram_{message.from_user.id}",
        "SOURCE": "telegram",
        "SOURCE_ID": str(message.from_user.id),
        "AUTHOR_ID": 0
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            params={"auth": auth["access_token"]},
            json=payload,
            timeout=10
        )

    logging.info("SEND MESSAGE RESPONSE:")
    logging.info(resp.text)


@dp.message()
async def handle_message(message: types.Message):
    auth = next(iter(BITRIX_AUTH.values()), None)

    if not auth:
        await message.answer("❌ Bitrix не подключён")
        return

    await send_message_to_openline(auth, message)
    await message.answer("✅ Сообщение отправлено в открытую линию Bitrix")