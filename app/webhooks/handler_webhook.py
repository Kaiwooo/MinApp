from fastapi import FastAPI, Request
import logging

app = FastAPI()


@app.post("/bitrix/webhook")
async def bitrix_webhook(request: Request):
    data = await request.json()

    logging.info("Получен webhook от Bitrix")
    logging.info(data)

    # Здесь позже будем обрабатывать события
    return {"status": "ok"}