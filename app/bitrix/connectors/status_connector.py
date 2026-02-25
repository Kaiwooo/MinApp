from app.bitrix.client import call

async def status_connector(code: str):
    return await call(
        "imconnector.status",
        {"CONNECTOR": code}
    )