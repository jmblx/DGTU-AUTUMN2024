from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories.achievement.repo import AchievementRepository
from domain.services.achievement.ach_service_interface import AchievementServiceInterface
from infrastructure.db_models.achievement.models import Achievement
from infrastructure.db_models.user.models import User
from domain.repositories.user.repo import UserRepository
from domain.services.user.user_service_interface import UserServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class AchievementServiceImpl(EntityServiceImpl[Achievement], AchievementServiceInterface):
    def __init__(self, base_repo: AchievementRepository):
        super().__init__(base_repo)

    async def get_user_achievements(self, user_id: str) -> list[Achievement]:
        """
        Возвращает список достижений с прогрессом для конкретного пользователя.
        """
        return await self._base_repo.get_user_achievements(user_id)

    async def get_user_achievement_by_id(self, user_id: str, achievement_id: int) -> Achievement:
        """
        Возвращает одно достижение с прогрессом для конкретного пользователя по ID.
        """
        return await self._base_repo.get_user_achievement_by_id(user_id, achievement_id)
