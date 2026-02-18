from fastapi import FastAPI, APIRouter
from app.bitrix import bitrix_router
from app.telegram_bot import dp, bot

app = FastAPI()

app.include_router(bitrix_router)
app.include_router(telegram_router)

@app.get("/")
async def root():
    return {"status": "alive"}