from typing import List, Dict, Any
from infrastructure.db_models.event.models import Event, UserEvent
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
        # Получаем текущее количество активных задач (is_completed = False)
        active_events_count = await self._base_repo.get_active_user_events_count(user_id)

        # Учитываем отвязку старых задач, если они заданы
        if old_event_ids:
            await self._base_repo.remove_user_events(user_id, old_event_ids)
            active_events_count -= len(old_event_ids)

        # Учитываем задачи, которые нужно заменить
        if replace_event_ids:
            await self._base_repo.remove_user_events(user_id, replace_event_ids)
            active_events_count -= len(replace_event_ids)

        # Проверяем, можно ли добавить новые задачи, с учетом лимита в 3 активные задачи
        if active_events_count >= 3:
            return []  # Возвращаем пустой список, так как новые задания не нужны

        # Подготовка новых событий с учетом условий (например, замена сложных событий на более легкие)
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

        # Рассчитываем количество новых событий, которые можно добавить
        random_events_needed = min(count, 3 - active_events_count) - len(replacement_events)
        random_events = await self._base_repo.get_random_events(random_events_needed,
                                                                old_event_ids + (replace_event_ids or []))
        all_events = replacement_events + random_events

        # Связываем новые события с пользователем в таблице user_event
        await self._base_repo.add_user_events(user_id, [event.id for event in all_events])

        # Получаем события с наградами и их количеством
        event_ids = [event.id for event in all_events]
        events_with_rewards = await self._base_repo.get_events_with_rewards(event_ids)

        return events_with_rewards
