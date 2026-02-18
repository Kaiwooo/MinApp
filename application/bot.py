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


# ===============================
# Telegram webhook endpoint
# ===============================
@telegram_router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    await dp.feed_raw_update(bot, update)
    return {"ok": True}


# ===============================
# Получаем Telegram Open Line ID
# ===============================
async def get_telegram_openline_id(auth: dict) -> int | None:
    url = auth["client_endpoint"] + "imopenlines.config.list"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            params={"auth": auth["access_token"]},
            timeout=10
        )

    data = resp.json()
    logging.info("OPENLINES RESPONSE:")
    logging.info(data)

    result = data.get("result", {})

    for line_id, line in result.items():
        connectors = line.get("CONNECTORS", {})
        if "telegrambot" in connectors:
            logging.info(f"Найдена Telegram Open Line: {line_id}")
            return int(line_id)

    logging.warning("Telegram Open Line не найдена")
    return None


# ===============================
# Отправка сообщения в Open Line
# ===============================
async def send_message_to_openline(
    auth: dict,
    openline_id: int,
    message: types.Message
):
    url = auth["client_endpoint"] + "imopenlines.message.add"

    payload = {
        "LINE_ID": openline_id,
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


# ===============================
# Telegram message handler
# ===============================
@dp.message()
async def handle_message(message: types.Message):
    auth = next(iter(BITRIX_AUTH.values()), None)

    if not auth:
        await message.answer("❌ Bitrix не подключён")
        return

    openline_id = await get_telegram_openline_id(auth)

    if not openline_id:
        await message.answer("❌ Telegram Open Line не найдена в Bitrix")
        return

    await send_message_to_openline(auth, openline_id, message)

    await message.answer("✅ Сообщение отправлено в открытую линию Bitrix")