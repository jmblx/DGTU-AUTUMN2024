from typing import List, Any, Dict

from sqlalchemy import select, func, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.repositories.event.repo import EventRepository
from domain.repositories.reward.repo import RewardRepository
from infrastructure.db_models.reward.models import Reward, user_reward
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class RewardRepositoryImpl(BaseRepositoryImpl[Reward], RewardRepository):
    def __init__(self, model: type[Reward], session: AsyncSession):
        super().__init__(model, session)

    async def get_user_inventory(self, user_id: str) -> list[dict[str, Any]]:
        """
        Возвращает список наград пользователя с количеством и статусами.
        """
        query = (
            select(Reward, user_reward.c.amount, user_reward.c.is_used, user_reward.c.received_date)
            .join(user_reward, Reward.id == user_reward.c.reward_id)
            .where(user_reward.c.user_id == user_id)
        )
        result = await self._session.execute(query)
        rewards = result.fetchall()

        # Формируем список наград с дополнительными данными
        return [
            {
                "reward": reward,
                "amount": amount,
                "is_used": is_used,
                "received_date": received_date,
            }
            for reward, amount, is_used, received_date in rewards
        ]
