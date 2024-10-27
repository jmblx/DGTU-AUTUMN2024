from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories.achievement.repo import AchievementRepository
from domain.repositories.reward.repo import RewardRepository
from domain.services.achievement.ach_service_interface import AchievementServiceInterface
from domain.services.reward.ach_service_interface import RewardServiceInterface
from infrastructure.db_models.achievement.models import Achievement
from infrastructure.db_models.reward.models import Reward, user_reward
from infrastructure.services.entity_service_impl import EntityServiceImpl


class RewardServiceImpl(EntityServiceImpl[Reward], RewardServiceInterface):
    def __init__(self, base_repo: RewardRepository):
        super().__init__(base_repo)

    async def get_inventory(self, user_id: str) -> list[dict[str, Any]]:
        """
        Возвращает инвентарь пользователя.
        """
        return await self._base_repo.get_user_inventory(user_id)

