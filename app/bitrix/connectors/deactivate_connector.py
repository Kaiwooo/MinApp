from app.bitrix.client import call

async def deactivate_connector(connector_code: str, line_id: int):
    payload = {
        "CONNECTOR": connector_code,
        "LINE": line_id,
        "ACTIVE": 0
    }
    return await call("imconnector.activate", payload)