from fastapi import FastAPI
from app.api.install import router as install_router
from app.telegram.telegram_webhook import router as telegram_router

app = FastAPI()
app.include_router(install_router)
app.include_router(telegram_router)