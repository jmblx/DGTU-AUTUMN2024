from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from domain.repositories.achievement.repo import AchievementRepository
from infrastructure.db_models.achievement.models import Achievement, user_achievement, reward_achievement
from infrastructure.db_models.reward.models import Reward
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

    async def get_user_achievements(self, user_id: str) -> List[dict[str, Any]]:
        """
        Получает список достижений пользователя с прогрессом и наградами.
        """
        query = (
            select(Achievement, user_achievement.c.progress)
            .join(user_achievement, user_achievement.c.achievement_id == Achievement.id)
            .where(user_achievement.c.user_id == user_id)
            .options(selectinload(Achievement.rewards_ach))
        )
        result = await self._session.execute(query)
        achievements = result.fetchall()

        enriched_achievements = []
        for achievement, progress in achievements:
            # Получаем награды с количеством для текущего достижения
            reward_query = (
                select(Reward, reward_achievement.c.amount)
                .join(reward_achievement, Reward.id == reward_achievement.c.reward_id)
                .where(reward_achievement.c.achievement_id == achievement.id)
            )
            rewards_with_amounts = await self._session.execute(reward_query)
            rewards = rewards_with_amounts.all()

            # Формируем достижение с прогрессом и наградами
            enriched_achievements.append({
                "achievement": achievement,
                "progress": progress,
                "rewards": [{"reward": reward, "amount": amount} for reward, amount in rewards]
            })

        return enriched_achievements

    async def get_user_achievement_by_id(self, user_id: str, achievement_id: int) -> dict[str, Any]:
        """
        Получает одно достижение пользователя по ID с прогрессом и наградами.
        """
        query = (
            select(Achievement, user_achievement.c.progress)
            .join(user_achievement, user_achievement.c.achievement_id == Achievement.id)
            .where(user_achievement.c.user_id == user_id)
            .where(Achievement.id == achievement_id)
            .options(selectinload(Achievement.rewards_ach))
        )
        result = await self._session.execute(query)
        achievement, progress = result.one_or_none()

        if not achievement:
            return None

        # Получаем награды с количеством для текущего достижения
        reward_query = (
            select(Reward, reward_achievement.c.amount)
            .join(reward_achievement, Reward.id == reward_achievement.c.reward_id)
            .where(reward_achievement.c.achievement_id == achievement.id)
        )
        rewards_with_amounts = await self._session.execute(reward_query)
        rewards = rewards_with_amounts.all()

        return {
            "achievement": achievement,
            "progress": progress,
            "rewards": [{"reward": reward, "amount": amount} for reward, amount in rewards]
        }
