from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from infrastructure.db_models.user.models import User
from infrastructure.external_services.receipt.service import ExternalAPIService
from presentation.receipts.schemas import Receipt

router = APIRouter(tags=["Receipts API"], route_class=DishkaRoute)

@router.post("/purchasers/verify_and_request_code", response_model=dict)
async def verify_and_request_code(
        user: FromDishka[User],
        external_service: FromDishka[ExternalAPIService],
):
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    purchaser = await external_service.get_purchaser(email=user.email)

    if purchaser:
        await external_service.grant_access(purchaser.id)
        return {"message": "Код подтверждения отправлен на email покупателя"}
    else:
        raise HTTPException(status_code=404, detail="Покупатель не найден")


@router.post("/purchasers/confirm_code_and_fetch_receipts", response_model=List[Receipt])
async def confirm_code_and_fetch_receipts(
        purchaser_id: str,
        code: str,
        from_time: str,
        to_time: str,
        external_service: FromDishka[ExternalAPIService]
):
    """
    Эндпоинт для подтверждения кода и получения чеков.
    """
    # Подтверждаем код доступа
    await external_service.confirm_access(purchaser_id, code)

    # Получаем чеки
    receipts = await external_service.get_receipts(purchaser_id, from_time, to_time)

    # Здесь вы можете добавить логику для загрузки чеков в базу данных
    # Например:
    # await save_receipts_to_db(receipts)

    return receipts

# import requests
#
# # Базовый URL API (проверьте, чтобы он соответствовал вашему конфигурационному значению)
# base_url = "http://localhost:8000"
#
# # Параметры запроса
# params = {
#     "purchaser_id": "2",  # ID покупателя
#     "code": "034752",      # Код подтверждения
#     "from_time": "1729686754",  # Начало временного диапазона
#     "to_time": "1729686760"     # Конец временного диапазона
# }
#
# # Выполнение запроса к API
# response = requests.post(f"{base_url}/purchasers/confirm_code_and_fetch_receipts", params=params)
#
# # Обработка ответа
# if response.status_code == 200:
#     receipts = response.json()
#     print("Полученные чеки:", receipts)
# else:
#     print(f"Ошибка {response.status_code}: {response.json().get('detail')}")

