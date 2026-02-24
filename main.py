from fastapi import FastAPI
from app.api.install import router as install_router

app = FastAPI()

app.include_router(install_router)