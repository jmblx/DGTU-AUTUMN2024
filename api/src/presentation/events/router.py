from io import BytesIO

import qrcode
from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from starlette.responses import StreamingResponse

from config import SERVER_BASE_URL
from domain.services.event.event_service_interface import EventServiceInterface
from infrastructure.db_models.user.models import User
from presentation.events.schemas import EventRead
from presentation.rewards.shemas import RewardRead

router = APIRouter(tags=["events"], route_class=DishkaRoute)

templates = Jinja2Templates(directory="templates")


@router.get("/random-events", response_model=list[EventRead])
async def get_events(
    amount: int,
    event_service: FromDishka[EventServiceInterface],
    user: FromDishka[User],
    old_event_ids: list[int] = Query([]),

) -> list[EventRead]:
    """
    Эндпоинт для получения случайных событий с учетом отсеянных.
    """
    events = await event_service.fetch_filtered_events(user_id=user.id, count=amount, old_event_ids=old_event_ids)
    return [
        EventRead(
            id=event["event"].id,
            description=event["event"].description,
            file_path=event["event"].file_path,
            rewards=[
                RewardRead(
                    id=reward_data["reward"].id,
                    title=reward_data["reward"].title,
                    file_path=reward_data["reward"].file_path,
                    amount=reward_data["amount"],
                ) for reward_data in event["rewards"]
            ],
        ) for event in events
    ]


@router.get("/current-tasks", response_model=list[EventRead])
async def get_current_tasks(
    event_service: FromDishka[EventServiceInterface],
    user: FromDishka[User]
) -> list[EventRead]:
    """
    Возвращает список незавершенных задач текущего пользователя.
    """
    enriched_events = await event_service.get_current_user_events(user.id)

    return [
        EventRead(
            id=user_event["user_event"].event_id,  # Исправлено
            description=user_event["user_event"].event.description,
            file_path=user_event["user_event"].event.file_path,
            rewards=[
                RewardRead(
                    id=reward_data["reward"].id,
                    title=reward_data["reward"].title,
                    file_path=reward_data["reward"].file_path,
                    amount=reward_data["amount"],
                ) for reward_data in user_event["rewards"]
            ]
        ) for user_event in enriched_events
    ]

@router.get("/generate-qrcode")
async def generate_qr_code(task_id: int, user_id: str) -> StreamingResponse:
    confirm_url = f"{SERVER_BASE_URL}/confirm-task?task_id={task_id}&user_id={user_id}"

    # Генерация QR-кода
    qr = qrcode.make(confirm_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@router.get("/confirm-task")
async def confirm_task(
    request: Request,
    task_id: int,
    user_id: str,
    event_service: FromDishka[EventServiceInterface]
):
    """
    Подтверждает выполнение задания, начисляет награды и отображает информацию о задании и пользователе.
    """
    # Получаем данные о задании и пользователе через сервис
    task = await event_service.get_task_by_id(task_id)
    user = await event_service.get_user_by_id(user_id)

    if not task or not user:
        raise HTTPException(status_code=404, detail="Task or User not found")

    # Отмечаем задание как завершенное и начисляем награды
    await event_service.mark_task_as_completed(task_id, user_id)

    # Отображаем страницу подтверждения
    return templates.TemplateResponse("confirmation.html", {
        "request": request,
        "task": task,
        "user": user,
        "message": "Спасибо за заботу о планете! Вы получили награды за выполнение задания."
    })
