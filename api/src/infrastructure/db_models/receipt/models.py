import datetime
from sqlalchemy import String, Float, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db.db_types import intpk
from infrastructure.db_models.database import Base
from infrastructure.db_models.district.models import District


class Receipt(Base):
    __tablename__ = 'receipts'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    time: Mapped[datetime.datetime] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    carbon_print: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)

    items: Mapped[list["ReceiptItem"]] = relationship("ReceiptItem", back_populates="receipt")
    user_receipt = relationship(
        "User",
        uselist=False,
        back_populates="receipts",
    )

class ReceiptItem(Base):
    __tablename__ = 'receipt_items'

    id: Mapped[intpk]
    receipt_id: Mapped[str] = mapped_column(ForeignKey("receipts.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)

    receipt: Mapped["Receipt"] = relationship("Receipt", back_populates="items")
