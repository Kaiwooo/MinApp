from app.bitrix.client import call


async def list_connectors():
    return await call("imconnector.list")


async def register_connector(code: str):
    return await call(
        "imconnector.register",
        {"CONNECTOR": code}
    )


async def activate_connector(connector_code: str, line_id: int, active: int = 1):
    payload = {
        "CONNECTOR": connector_code,
        "LINE": line_id,
        "ACTIVE": active
    }
    return await call("imconnector.activate", payload)

async def deactivate_connector(connector_code: str, line_id: int, active: int = 1):
    payload = {
        "CONNECTOR": connector_code,
        "LINE": line_id,
        "ACTIVE": active
    }
    return await call("imconnector.activate", payload)


async def connector_status(code: str):
    return await call(
        "imconnector.status",
        {"CONNECTOR": code}
    )