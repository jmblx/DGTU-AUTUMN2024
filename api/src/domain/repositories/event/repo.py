from abc import ABC

from infrastructure.db_models.event.models import Event
from domain.repositories.base_repo import BaseRepository


class EventRepository(BaseRepository[Event], ABC): ...
