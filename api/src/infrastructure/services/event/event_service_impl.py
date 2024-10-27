from typing import List, Dict, Any

from sqlalchemy import select, update, func, insert

from infrastructure.db_models.event.models import Event, UserEvent, event_reward
from infrastructure.db_models.reward.models import Reward, user_reward
from infrastructure.db_models.user.models import User
from infrastructure.repositories.event.event_repo_impl import EventRepository
from infrastructure.services.entity_service_impl import EntityServiceImpl

class EventServiceImpl(EntityServiceImpl[Event]):
    def __init__(self, base_repo: EventRepository):
        super().__init__(base_repo)

    async def fetch_filtered_events(
            self,
            user_id: int,
            count: int,
            old_event_ids: List[int],
            replace_event_ids: List[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Формирует и возвращает новый список событий с наградами и их количеством.
        Убедитесь, что у пользователя не более 3 активных (не завершенных) задач.
        """
        active_events_count = await self._base_repo.get_active_user_events_count(user_id)

        if old_event_ids:
            await self._base_repo.remove_user_events(user_id, old_event_ids)
            active_events_count -= len(old_event_ids)

        # Учитываем задачи, которые нужно заменить
        if replace_event_ids:
            await self._base_repo.remove_user_events(user_id, replace_event_ids)
            active_events_count -= len(replace_event_ids)

        if active_events_count >= 3:
            return []

        replacement_events = []
        if replace_event_ids:
            for event_id in replace_event_ids:
                old_event = await self._base_repo.get_by_id(event_id)
                if old_event and old_event.amount >= 50:
                    light_event = await self._base_repo.get_by_fields(
                        {"description": old_event.description, "amount": 10}
                    )
                    if light_event:
                        replacement_events.append(light_event)

        random_events_needed = min(count, 3 - active_events_count) - len(replacement_events)
        random_events = await self._base_repo.get_random_events(random_events_needed,
                                                                old_event_ids + (replace_event_ids or []))
        all_events = replacement_events + random_events

        await self._base_repo.add_user_events(user_id, [event.id for event in all_events])

        event_ids = [event.id for event in all_events]
        events_with_rewards = await self._base_repo.get_events_with_rewards(event_ids)

        return events_with_rewards

    async def get_task_by_id(self, task_id: int):
        """
        Получает данные о задании по ID.
        """
        return await self._base_repo.get_task_by_id(task_id)

    async def get_user_by_id(self, user_id: str):
        """
        Получает данные о пользователе по ID.
        """
        return await self._base_repo.get_user_by_id(user_id)

    async def mark_task_as_completed(self, task_id: int, user_id: str):
        """
        Отмечает задачу как завершенную, заполняет progress, и начисляет пользователю награды.
        """
        # Обновляем `is_completed` и `progress` в `UserEvent`
        update_query = (
            update(UserEvent)
            .where(UserEvent.event_id == task_id, UserEvent.user_id == user_id)
            .values(is_completed=True, progress=UserEvent.goal)  # Установка `progress` равным `goal`
        )
        await self._base_repo._session.execute(update_query)
        await self._base_repo._session.commit()

        # Получаем награды для задачи
        rewards_with_amounts = await self._base_repo.get_rewards_for_task(task_id)

        # Подготовка данных для начисления наград
        user_rewards = [
            {
                "user_id": user_id,
                "reward_id": reward.id,
                "amount": amount,
                "is_used": False,
                "received_date": func.now()
            }
            for reward, amount in rewards_with_amounts
        ]

        # Добавление наград пользователю
        if user_rewards:
            await self._base_repo.add_user_rewards(user_id, user_rewards)
