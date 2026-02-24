from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import Router

from app.config import BOT_TOKEN
from app.bitrix.connectors import list_connectors

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message()
async def handle_message(message: Message):
    text = (message.text or "").strip().lower()

    if text == "get connectors":
        connectors = await list_connectors()
        # Преобразуем в красивый JSON для отображения
        import json
        await message.answer(f"Connectors:\n{json.dumps(connectors, indent=2, ensure_ascii=False)}")
    else:
        await message.answer("Напиши 'get connectors', чтобы получить список коннекторов Bitrix24")