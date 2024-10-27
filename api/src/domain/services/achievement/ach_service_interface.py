from abc import abstractmethod

from domain.services.entity_service import EntityService
from infrastructure.db_models.achievement.models import Achievement


class AchievementServiceInterface(EntityService[Achievement]): ...
