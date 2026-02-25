import logging
from fastapi import FastAPI
from app.webhooks.install_webhook import router as install_router
from app.webhooks.telegram_webhook import router as telegram_router
from app.webhooks.handler_webhook import router as bitrix_webhook_router
from app.webhooks.widget_webhook import router as widget_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
app = FastAPI()
app.include_router(install_router)
app.include_router(telegram_router)
app.include_router(bitrix_webhook_router)
app.include_router(widget_router)