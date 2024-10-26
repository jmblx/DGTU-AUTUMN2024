from abc import ABC

from infrastructure.db_models.user.models import User
from domain.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User], ABC): ...
