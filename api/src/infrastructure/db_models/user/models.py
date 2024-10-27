from uuid import UUID
from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db_models.receipt.models import Receipt  # Замените на правильный путь к Receipt
from infrastructure.db_models.achievement.models import user_achievement
from infrastructure.db_models.database import Base
from core.db.db_types import added_at


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)
    role = relationship("Role", back_populates="users_role", uselist=False)
    email: Mapped[str]
    file_path: Mapped[str] = mapped_column(nullable=True)
    registered_at: Mapped[added_at]
    achievements = relationship(
        "Achievement",
        uselist=True,
        back_populates="users_ach",
        secondary=user_achievement,
    )
    balance: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False, default=0.0)
    rewards = relationship(
        "Reward",
        uselist=True,
        back_populates="users_rewards",
        secondary="user_reward",
    )
    exp: Mapped[int] = mapped_column(nullable=True)
    receipts = relationship(
        "Receipt",
        back_populates="user_receipt",
        uselist=True,
        primaryjoin="User.id == foreign(Receipt.user_id)"
    )
    address: Mapped[str] = mapped_column(nullable=True)
    district_id: Mapped[int] = mapped_column(ForeignKey("district.id"), nullable=True)
    district = relationship("District", back_populates="users_d", uselist=False)
    events = relationship(
        "Event",
        uselist=True,
        back_populates="users_events",
        secondary="user_event",
    )
