from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories.achievement.repo import AchievementRepository
from infrastructure.db_models.user.models import User
from domain.repositories.user.repo import UserRepository
from domain.services.user.user_service_interface import UserServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class UserServiceImpl(EntityServiceImpl[User], UserServiceInterface):
    def __init__(self, base_repo: UserRepository, achievement_repo: AchievementRepository):
        self.base_repo = base_repo
        super().__init__(base_repo)

        self.achievement_repo = achievement_repo

    async def create_user_with_achievements(self, user_data: dict[str, Any]) -> User:
        user_id = await self._base_repo.create(user_data)
        achievements = await self.achievement_repo.get_all_achievements()
        user_achievements = [
            {"user_id": user_id, "achievement_id": achievement.id, "progress": 0.0}
            for achievement in achievements
        ]
        await self._base_repo.add_user_achievements(user_achievements)
        return user_id
