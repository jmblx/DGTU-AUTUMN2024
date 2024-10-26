from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db_models.database import Base
from core.db.db_types import intpk
from infrastructure.db_models.user.models import User


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON)
    users_role = relationship("User",
        back_populates="role", uselist=True
    )

from infrastructure.db_models.user.models import User  # Замените на корректный путь

Role.users_role = relationship("User", back_populates="role", uselist=True)
