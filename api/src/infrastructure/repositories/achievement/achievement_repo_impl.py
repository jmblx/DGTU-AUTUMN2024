from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from domain.repositories.achievement.repo import AchievementRepository
from infrastructure.db_models.achievement.models import Achievement, user_achievement
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class AchievementRepositoryImpl(BaseRepositoryImpl[Achievement], AchievementRepository):
    def __init__(self, model: type[Achievement], session: AsyncSession):
        super().__init__(model, session)

    async def get_all_achievements(self) -> List[Achievement]:
        """
        Возвращает список всех достижений.
        """
        query = select(Achievement)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_user_achievements(self, user_id: str) -> List[Achievement]:
        """
        Получает список достижений пользователя с прогрессом.
        """
        query = (
            select(Achievement)
            .join(user_achievement)
            .where(user_achievement.c.user_id == user_id)
            .options(
                selectinload(Achievement.rewards_ach)
            )
        )
        result = await self._session.execute(query)
        achievements = result.scalars().all()

        # Добавляем прогресс из user_achievement для каждого достижения
        for achievement in achievements:
            achievement.progress = (
                await self._session.execute(
                    select(user_achievement.c.progress)
                    .where(user_achievement.c.user_id == user_id)
                    .where(user_achievement.c.achievement_id == achievement.id)
                )
            ).scalar()

        return achievements

    async def get_user_achievement_by_id(self, user_id: str, achievement_id: int) -> Achievement:
        """
        Получает одно достижение пользователя по ID с прогрессом.
        """
        query = (
            select(Achievement)
            .join(user_achievement)
            .where(user_achievement.c.user_id == user_id)
            .where(Achievement.id == achievement_id)
            .options(
                selectinload(Achievement.rewards_ach)
            )
        )
        result = await self._session.execute(query)
        achievement = result.scalar_one_or_none()

        # Добавляем прогресс
        if achievement:
            achievement.progress = (
                await self._session.execute(
                    select(user_achievement.c.progress)
                    .where(user_achievement.c.user_id == user_id)
                    .where(user_achievement.c.achievement_id == achievement_id)
                )
            ).scalar()

        return achievement
