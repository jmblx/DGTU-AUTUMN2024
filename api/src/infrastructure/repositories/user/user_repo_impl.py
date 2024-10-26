import logging
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlalchemy.sql import Select

from core.exceptions.user.delete import UserIsAdminOfOrgsException
from infrastructure.db_models.user.models import User
from domain.repositories.user.repo import UserRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class UserRepositoryImpl(BaseRepositoryImpl[User], UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)


