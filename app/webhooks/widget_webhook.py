from fastapi import APIRouter

router = APIRouter()

@router.get("/bitrix/widget")
async def bitrix_widget():
    return """
    <html>
        <body>
            <h3>Коннектор установлен</h3>
        </body>
    </html>
    """