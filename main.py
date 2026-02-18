from fastapi import FastAPI
from app.bitrix import bitrix_router
from app.telegram_bot import telegram_router

app = FastAPI()

app.include_router(bitrix_router)
app.include_router(telegram_router)

@app.get("/")
async def root():
    return {"status": "alive"}