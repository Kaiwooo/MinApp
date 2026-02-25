from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
import json
from app.config import BOT_TOKEN
from app.bitrix.connectors import list_connectors, activate_connector, deactivate_connector, status_connector, create_connector
from app.bitrix.openlines.openlines import list_openlines

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message()
async def handle_message(message: Message):
    text = (message.text or "").strip().lower()

    if text == "get connectors":
        connectors = await list_connectors()
        await message.answer(f"Connectors:\n{json.dumps(connectors, indent=2, ensure_ascii=False)}")

    elif text.startswith("connector status "):
        # Извлекаем название коннектора
        connector_code = text.replace("connector status ", "").strip()
        status = await status_connector(connector_code)
        await message.answer(f"Статус коннектора '{connector_code}':\n{json.dumps(status, indent=2, ensure_ascii=False)}")


    elif text.startswith("activate connector "):
        parts = text.split()
        if len(parts) < 4:
            await message.answer(
                "Использование:\nactivate connector {код} {LINE_ID}"
            )
            return
        connector_code = parts[2]
        try:
            line_id = int(parts[3])
        except ValueError:
            await message.answer("LINE_ID должен быть числом")
            return
        result = await activate_connector(connector_code=connector_code, line_id=line_id)
        await message.answer(f"Результат активации:\n{json.dumps(result, indent=2, ensure_ascii=False)}")

    elif text.startswith("deactivate connector "):
        parts = text.split()
        if len(parts) < 4:
            await message.answer(
                "Использование:\ndeactivate connector {код} {LINE_ID}"
            )
            return
        connector_code = parts[2]
        try:
            line_id = int(parts[3])
        except ValueError:
            await message.answer("LINE_ID должен быть числом")
            return

        result = await deactivate_connector(connector_code=connector_code, line_id=line_id)
        await message.answer(
            f"Коннектор '{connector_code}' деактивирован для линии {line_id}:\n"
            f"{json.dumps(result, indent=2, ensure_ascii=False)}")

    elif text == "openlines":
        openlines = await list_openlines()
        if openlines and "result" in openlines:
            # Сокращаем вывод до ключевых полей
            simplified = [
                {k: v for k, v in line.items() if k in ["ID", "LINE_NAME", "ACTIVE"]}
                for line in openlines["result"]
            ]
            await message.answer(f"Openlines:\n{json.dumps(simplified, indent=2, ensure_ascii=False)}")
        else:
            await message.answer("Нет открытых линий")

    elif text.startswith("new connector "):
        parts = message.text.split(maxsplit=3)

        if len(parts) < 4:
            await message.answer(
                "Использование:\nnew connector {id} {name}"
            )
            return

        connector_id = parts[2]
        name = parts[3]
        result = await create_connector(connector_id, name)
        await message.answer(
            f"Создание коннектора:\n"
            f"{json.dumps(result, indent=2, ensure_ascii=False)}"
        )

    else:
        await message.answer(
            "Напиши:\n"
            "— 'get connectors' — список коннекторов;\n"
            "— 'connector status {название}' — статус коннектора;\n"
            "— 'activate connector {название}' — активировать коннектор;\n"
            "— 'deactivate connector {название}' — деактивировать коннектор;\n"
            "— 'openlines' — список открытых линий."
        )