from app.bitrix.client import call

async def list_connectors():
    return await call("imconnector.list")