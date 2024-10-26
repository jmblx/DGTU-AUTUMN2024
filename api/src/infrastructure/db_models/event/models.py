from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.testing.schema import Table

from core.db.db_types import intpk, reward_fk, event_fk, user_fk
from infrastructure.db_models.database import Base


event_reward = Table(
    'event_reward', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id'), primary_key=True),
    Column('reward_id', Integer, ForeignKey('reward.id'), primary_key=True)
)


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[intpk]
    description: Mapped[str]
    is_group: Mapped[bool] = mapped_column(default=False)
    users_events = relationship(
        "User",
        uselist=True,
        back_populates="events",
        secondary="user_event",
    )
    rewards_ev = relationship("Reward", uselist=True, back_populates="events_rew", secondary=event_reward)
    file_path: Mapped[str]


class UserEvent(Base):
    __tablename__ = 'user_event'

    id: Mapped[intpk]
    goal: Mapped[float] = mapped_column(default=0, nullable=False)
    user_id: Mapped[user_fk]
    event_id: Mapped[event_fk]
    progress: Mapped[float] = mapped_column(default=0, nullable=False)
    is_completed: Mapped[bool] = mapped_column(default=False)
