from app.bitrix.client import call

async def activate_connector(connector_code: str, line_id: int, active: int = 1):
    payload = {
        "CONNECTOR": connector_code,
        "LINE": line_id,
        "ACTIVE": active
    }
    return await call("imconnector.activate", payload)