from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from domain.services.reward.ach_service_interface import RewardServiceInterface
from infrastructure.db_models.user.models import User
from presentation.rewards.shemas import RewardRead

router = APIRouter(tags=["rewards"], route_class=DishkaRoute)


@router.get("/inventory", response_model=list[RewardRead])
async def get_inventory(reward_service: FromDishka[RewardServiceInterface], user: FromDishka[User]):
    """
    Возвращает инвентарь текущего пользователя.
    """
    inventory = await reward_service.get_inventory(user.id)

    return [
        RewardRead(
            id=item["reward"].id,
            title=item["reward"].title,
            file_path=item["reward"].file_path,
            amount=item["amount"],
        )
        for item in inventory if not item["is_used"]  # Возвращаем только неиспользованные награды
    ]
