import datetime
import uuid

from sqlalchemy import String, Table, Column, Integer, ForeignKey, Boolean, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.db_types import intpk, added_at, event_fk, achievement_fk, not_null_user_fk, reward_fk
from infrastructure.db_models.database import Base
from infrastructure.db_models.event.models import event_reward


class Reward(Base):
    __tablename__ = 'reward'

    id: Mapped[intpk]
    title: Mapped[str]
    users_rewards = relationship(
        "User",
        uselist=True,
        back_populates="rewards",
        secondary="user_reward",
    )
    file_path: Mapped[str] = mapped_column(nullable=True)
    achievements_rew = relationship("Achievement", uselist=True, back_populates="rewards_ach", secondary="reward_achievement")
    events_rew = relationship("Event", uselist=True, back_populates="rewards_ev", secondary=event_reward)
    is_market_available: Mapped[bool] = mapped_column(default=False)
    market_cost: Mapped[float] = mapped_column(nullable=True)


user_reward = Table(
    'user_reward', Base.metadata,
    Column('user_id', String, ForeignKey('user.id')),
    Column('reward_id', Integer, ForeignKey('reward.id')),
    Column('is_used', Boolean, default=False),
    Column('code', String, nullable=True),
    Column('amount', Integer, nullable=False),
    Column('received_date', DateTime, nullable=True, server_default=text("TIMEZONE('utc', now())")),
    Column('activated_date', DateTime, nullable=True),
    Column('is_bought', Boolean, default=False),
    Column('event_id', Integer, ForeignKey('event.id'), nullable=True),
    Column('achievement_id', Integer, ForeignKey('achievement.id'), nullable=True)
)
