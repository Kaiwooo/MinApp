from app.bitrix.client import call

async def connector_status(code: str):
    return await call(
        "imconnector.status",
        {"CONNECTOR": code}
    )