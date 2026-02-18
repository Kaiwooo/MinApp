from fastapi import APIRouter
from aiogram import Bot, Dispatcher, types
from application.config import BOT_TOKEN
from application.storage import BITRIX_AUTH
import httpx
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

telegram_router = APIRouter()

@telegram_router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    await dp.feed_raw_update(bot, update)
    return {"ok": True}


async def get_telegram_openline_id(auth: dict):
    """Получаем ID open line для Telegram-коннектора"""
    url = auth["client_endpoint"] + "imconnector.list"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={"auth": auth["access_token"]})
        data = resp.json()

    # Находим Telegram-коннектор
    for connector in data.get("result", {}).values():  # <- исправлено
        if connector.get("CODE") == "telegrambot":
            logging.info(f"Найдена Telegram open line: {connector.get('ID')}")
            return connector.get("ID")

    logging.warning("Telegram-коннектор не найден")
    return None


async def send_message_to_openline(auth: dict, openline_id: str, message: str):
    """Отправляем сообщение в open line"""
    url = auth["client_endpoint"] + "imopenlines.message.add"

    payload = {
        "CHAT_ID": openline_id,
        "MESSAGE": message
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params={"auth": auth["access_token"]}, json=payload)
        logging.info(f"Ответ Bitrix: {resp.text}")


# Обработчик сообщений из Telegram
@dp.message()
async def handle_message(message: types.Message):
    auth = next(iter(BITRIX_AUTH.values()), None)

    if not auth:
        await message.answer("❌ Bitrix не подключён")
        return

    # Получаем ID Telegram open line
    openline_id = await get_telegram_openline_id(auth)
    if not openline_id:
        await message.answer("❌ Telegram open line не найдена")
        return

    # Отправляем сообщение
    await send_message_to_openline(auth, openline_id, message.text)
    await message.answer("✅ Отправлено в Bitrix open line")
