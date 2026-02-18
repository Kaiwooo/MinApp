from fastapi import FastAPI
from application.app import bitrix_app_router
from application.bot import telegram_router
from application.bitrix import bitrix_router

app = FastAPI()

# Bitrix /install роутер
app.include_router(bitrix_app_router)

# Telegram webhook роутер
app.include_router(telegram_router)

# Другие Bitrix роутеры (на будущее)
app.include_router(bitrix_router)

@app.get("/")
async def root():
    return {"status": "alive"}