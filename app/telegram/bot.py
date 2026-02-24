from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import Router
import logging
import json

from app.config import BOT_TOKEN
from app.bitrix.connectors import list_connectors, connector_status, activate_connector
from app.bitrix.openlines import list_openlines

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message()
async def handle_message(message: Message):
    text = (message.text or "").strip().lower()

    if text == "get connectors":
        logging.info(f"Получен запрос от Telegram: {message.from_user.id} -> get connectors")
        connectors = await list_connectors()
        logging.info(f"Ответ Bitrix: {connectors}")
        await message.answer(f"Connectors:\n{json.dumps(connectors, indent=2, ensure_ascii=False)}")

    elif text.startswith("connector status "):
        # Извлекаем название коннектора
        connector_code = text.replace("connector status ", "").strip()
        logging.info(f"Запрос статуса коннектора: {connector_code} от {message.from_user.id}")
        status = await connector_status(connector_code)
        logging.info(f"Ответ Bitrix: {status}")
        await message.answer(f"Статус коннектора '{connector_code}':\n{json.dumps(status, indent=2, ensure_ascii=False)}")

    elif text.startswith("activate connector "):
        connector_code = text.replace("activate connector ", "").strip()
        logging.info(f"Запрос активации коннектора: {connector_code} от {message.from_user.id}")
        result = await activate_connector(connector_code)
        logging.info(f"Ответ Bitrix: {result}")
        await message.answer(f"Коннектор '{connector_code}' активирован:\n{json.dumps(result, indent=2, ensure_ascii=False)}")

    elif text == "openlines":
        logging.info(f"Запрос списка openlines от Telegram: {message.from_user.id}")
        openlines = await list_openlines()
        logging.info(f"Ответ Bitrix openlines: {openlines}")
        await message.answer(f"Openlines:\n{json.dumps(openlines, indent=2, ensure_ascii=False)}")

    else:
        await message.answer(
            "Напиши:\n"
            "— 'get connectors' — список коннекторов;\n"
            "— 'connector status {название}' — статус коннектора;\n"
            "— 'openlines' — список открытых линий."
        )