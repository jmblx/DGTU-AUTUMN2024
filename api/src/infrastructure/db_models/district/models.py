from sqlalchemy.orm import Mapped, relationship

from core.db.db_types import intpk
from infrastructure.db_models.database import Base


class District(Base):
    __tablename__ = 'district'

    id: Mapped[intpk]
    name: Mapped[str]
    users_d = relationship('User', back_populates='district', uselist=True)
