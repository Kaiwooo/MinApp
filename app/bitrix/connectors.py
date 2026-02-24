from app.bitrix.client import call


async def list_connectors():
    return await call("imconnector.list")


async def register_connector(code: str):
    return await call(
        "imconnector.register",
        {"CONNECTOR": code}
    )


async def activate_connector(code: str):
    return await call(
        "imconnector.activate",
        {"CONNECTOR": code}
    )


async def connector_status(code: str):
    return await call(
        "imconnector.status",
        {"CONNECTOR": code}
    )