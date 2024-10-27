from _decimal import Decimal

from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime, text, String, Float
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.db.db_types import intpk, added_at, achievement_fk, user_fk, reward_fk
from infrastructure.db_models.database import Base
from infrastructure.db_models.reward.models import Reward


user_achievement = Table(
    'user_achievement', Base.metadata,
    Column('id', Integer, primary_key=True),  # Основной ключ, если требуется
    Column('achievement_id', Integer, ForeignKey('achievement.id'), nullable=False),
    Column('user_id', String, ForeignKey('user.id'), nullable=False),
    Column('achieved_time', DateTime, nullable=True),
    Column('progress', Float, nullable=False, default=0.0),
)


class Achievement(Base):
    __tablename__ = 'achievement'

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    file_path: Mapped[str] = mapped_column(String, nullable=True)
    rewards_ach: Mapped[list[Reward]] = relationship('Reward', back_populates="achievements_rew", uselist=True, secondary="reward_achievement")
    users_ach = relationship('User', back_populates="achievements", uselist=True, secondary=user_achievement)
    goal: Mapped[float] = mapped_column(nullable=True)


reward_achievement = Table(
    'reward_achievement', Base.metadata,
    Column('reward_id', Integer, ForeignKey('reward.id')),
    Column('achievement_id', Integer, ForeignKey('achievement.id')),
    Column('amount', Integer, nullable=False)
)
