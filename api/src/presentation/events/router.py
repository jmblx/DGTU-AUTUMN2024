from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from domain.services.event.event_service_interface import EventServiceInterface
from infrastructure.db_models.user.models import User
from presentation.events.schemas import EventRead
from presentation.rewards.shemas import RewardRead

router = APIRouter(tags=["events"], route_class=DishkaRoute)


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
