from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.config import TELEGRAM_TOKEN
from app.bitrix.connectors import list_connectors

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Bot connected to Bitrix24 ✅")


@dp.message()
async def any_message(message: Message):
    connectors = await list_connectors()
    await message.answer(f"Connectors:\n{connectors}")