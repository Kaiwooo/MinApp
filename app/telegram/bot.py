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
async def any_message(message: Message):
    connectors = await list_connectors()
    await message.answer(f"Connectors:\n{connectors}")