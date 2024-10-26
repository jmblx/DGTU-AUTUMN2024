from abc import abstractmethod, ABC

from domain.services.entity_service import EntityService
from infrastructure.db_models.event.models import Event


class EventServiceInterface(EntityService[Event], ABC):
    @abstractmethod
    async def fetch_filtered_events(self, user_id: int, count: int, old_event_ids: list[int]): ...
