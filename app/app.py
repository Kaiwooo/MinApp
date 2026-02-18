from fastapi import FastAPI, Request
import logging
import json

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "alive"}