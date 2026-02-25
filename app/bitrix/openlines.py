from app.bitrix.client import call

async def list_openlines():
    """
    Получить список открытых линий (open lines) из Bitrix24
    """
    return await call("imopenlines.config.list.get")
