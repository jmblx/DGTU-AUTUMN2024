from typing import List, Any, Dict

from sqlalchemy import select, func, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.repositories.event.repo import EventRepository
from infrastructure.db_models.event.models import Event, UserEvent, event_reward
from infrastructure.db_models.reward.models import Reward
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class EventRepositoryImpl(BaseRepositoryImpl[Event], EventRepository):
    def __init__(self, model: type[Event], session: AsyncSession):
        super().__init__(model, session)

    async def remove_user_events(self, user_id: int, event_ids: List[int]):
        """
        Удаляет записи в таблице user_event, которые связывают пользователя с указанными событиями.
        """
        stmt = (
            delete(UserEvent)
            .where(UserEvent.user_id == user_id)
            .where(UserEvent.event_id.in_(event_ids))
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_random_events(self, amount: int, exclude_ids: List[int]) -> List[Event]:
        """
        Возвращает указанное количество случайных событий, исключая события с идентификаторами из exclude_ids.
        Предзагружает награды для каждого события.
        """
        query = (
            select(Event)
            .options(selectinload(Event.rewards_ev))  # Предзагрузка наград
            .filter(~Event.id.in_(exclude_ids))
            .order_by(func.random())
            .limit(amount)
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_events_with_rewards(self, event_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Получает события с наградами и их количеством из связанной таблицы event_reward.
        """
        # Получаем события с предзагруженными наградами
        query = (
            select(Event)
            .options(selectinload(Event.rewards_ev))  # Предзагрузка наград
            .where(Event.id.in_(event_ids))
        )
        result = await self._session.execute(query)
        events = result.scalars().all()

        # Составляем список наград с количеством для каждого события
        enriched_events = []

        for event in events:
            reward_query = (
                select(Reward, event_reward.c.amount)
                .join(event_reward, Reward.id == event_reward.c.reward_id)
                .where(event_reward.c.event_id == event.id)
            )
            rewards_with_amounts = await self._session.execute(reward_query)
            rewards_with_amounts = rewards_with_amounts.all()

            # Формируем список наград с учетом количества для каждого события
            enriched_events.append({
                "event": event,
                "rewards": [{"reward": reward, "amount": amount} for reward, amount in rewards_with_amounts]
            })

        return enriched_events

    async def get_active_user_events_count(self, user_id: int) -> int:
        """
        Возвращает количество активных (не завершенных) задач пользователя.
        """
        query = select(func.count()).select_from(UserEvent).where(
            UserEvent.user_id == user_id,
            UserEvent.is_completed == False  # Учитываем только незавершенные задачи
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def add_user_events(self, user_id: int, event_ids: List[int]):
        """
        Добавляет новые связи пользователя с задачами в таблицу user_event и копирует значение `amount` из Event в столбец `goal`.
        """
        # Получаем события с их значениями `amount`
        query = select(Event.id, Event.amount).where(Event.id.in_(event_ids))
        result = await self._session.execute(query)
        events = result.fetchall()

        # Подготавливаем данные для вставки в user_event, включая `goal`
        user_event_data = [
            {"user_id": user_id, "event_id": event_id, "goal": amount} for event_id, amount in events
        ]

        stmt = insert(UserEvent).values(user_event_data)
        await self._session.execute(stmt)
        await self._session.commit()
