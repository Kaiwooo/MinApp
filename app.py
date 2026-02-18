from fastapi import FastAPI, Request
import logging
import json

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "alive"}

@app.post("/install")
async def install(request: Request):
    raw_body = await request.body()

    logging.info("RAW BODY:")
    logging.info(raw_body.decode("utf-8", errors="ignore"))

    data = None

    # пробуем JSON
    try:
        data = await request.json()
    except Exception:
        pass

    # если не JSON — читаем form-data
    if data is None:
        form = await request.form()
        data = dict(form)

    logging.info("PARSED DATA:")
    logging.info(json.dumps(data, indent=2, ensure_ascii=False))

    auth = data.get("auth")
    logging.info("AUTH:")
    logging.info(auth)

    return {"status": "ok"}
