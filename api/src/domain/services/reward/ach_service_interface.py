from domain.services.entity_service import EntityService
from infrastructure.db_models.achievement.models import Reward


class RewardServiceInterface(EntityService[Reward]): ...
