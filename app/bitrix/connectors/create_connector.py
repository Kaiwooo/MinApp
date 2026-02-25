from app.config import WEBHOOK_HANDLER, WIDGET_HANDLER
from app.bitrix.client import call

ICON_SVG = "data:image/svg+xml;charset=US-ASCII,%3Csvg%20version%3D..."

async def register_connector(connector_id: str, name: str):
    payload = {
        "CONNECTOR": connector_id,
        "NAME": name,
        "ICON": ICON_SVG,
        "HANDLER": WEBHOOK_HANDLER
    }
    return await call("imconnector.register", payload)


async def bind_connector_widget(name: str):
    payload = {
        "PLACEMENT": "OPEN_LINES",
        "HANDLER": WIDGET_HANDLER,
        "TITLE": name
    }
    return await call("placement.bind", payload)


async def create_connector(connector_id: str, name: str):
    register_result = await register_connector(connector_id, name)
    bind_result = await bind_connector_widget(name)

    return {
        "register": register_result,
        "placement": bind_result
    }