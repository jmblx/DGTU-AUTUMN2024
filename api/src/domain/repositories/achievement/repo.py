from abc import ABC

from infrastructure.db_models.achievement.models import Achievement
from domain.repositories.base_repo import BaseRepository


class AchievementRepository(BaseRepository[Achievement], ABC): ...
