from abc import ABC

from infrastructure.db_models.achievement.models import Reward
from domain.repositories.base_repo import BaseRepository


class RewardRepository(BaseRepository[Reward], ABC): ...
