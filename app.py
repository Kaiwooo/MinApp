from fastapi import FastAPI, Request
import logging
import json

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/install")
async def install(request: Request):
    data = await request.json()

    # Bitrix присылает auth здесь
    auth = data.get("auth")

    logging.info("BITRIX INSTALL DATA:")
    logging.info(json.dumps(data, indent=2, ensure_ascii=False))

    logging.info("BITRIX AUTH:")
    logging.info(json.dumps(auth, indent=2, ensure_ascii=False))

    # ВАЖНО: вернуть 200 OK
    return {"status": "ok"}