import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = "https://minapp-8aca.onrender.com"
WEBHOOK_HANDLER = f"{BASE_URL}/bitrix/webhook"
WIDGET_HANDLER = f"{BASE_URL}/bitrix/widget"
BITRIX_CLIENT_ID = os.environ.get("BITRIX_CLIENT_ID")
BITRIX_CLIENT_SECRET = os.environ.get("BITRIX_CLIENT_SECRET")