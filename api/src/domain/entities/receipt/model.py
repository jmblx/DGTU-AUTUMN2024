import datetime
from typing import Optional

from _decimal import Decimal

from domain.entities.receipt.value_objects import ReceiptID, UserID, ReceiptTime, TotalPrice, CarbonPrint


class Receipt:
    def __init__(
        self,
        receipt_id: ReceiptID,
        user_id: UserID,
        time: ReceiptTime,
        total_price: TotalPrice,
        carbon_print: Optional[CarbonPrint] = None
    ):
        self._id = receipt_id
        self._user_id = user_id
        self._time = time
        self._total_price = total_price
        self._carbon_print = carbon_print

    @property
    def id(self) -> str:
        return self._id.value

    @property
    def user_id(self) -> str:
        return self._user_id.value

    @property
    def time(self) -> datetime.datetime:
        return self._time.value

    @property
    def total_price(self) -> Decimal:
        return self._total_price.value

    @property
    def carbon_print(self) -> Optional[Decimal]:
        return self._carbon_print.value
