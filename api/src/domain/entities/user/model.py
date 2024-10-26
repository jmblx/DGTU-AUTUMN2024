from _decimal import Decimal
from typing import Optional
from datetime import datetime

from domain.entities.user.value_objects import UserID, Email, Balance, Exp


class User:
    def __init__(
        self,
        user_id: UserID,
        first_name: str,
        last_name: str,
        role_id: int,
        email: Email,
        file_path: Optional[str],
        registered_at: datetime,
        balance: Balance,
        exp: Exp,
        address: Optional[str],
        district_id: Optional[int]
    ):
        self._id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._role_id = role_id
        self._email = email
        self._file_path = file_path
        self._registered_at = registered_at
        self._balance = balance
        self._exp = exp
        self._address = address
        self._district_id = district_id

    @property
    def id(self) -> str:
        return self._id.value

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def role_id(self) -> int:
        return self._role_id

    @property
    def email(self) -> str:
        return self._email.value

    @property
    def file_path(self) -> Optional[str]:
        return self._file_path

    @property
    def registered_at(self) -> datetime:
        return self._registered_at

    @property
    def balance(self) -> Decimal:
        return self._balance.value

    @property
    def exp(self) -> int:
        return self._exp.value

    @property
    def address(self) -> Optional[str]:
        return self._address

    @property
    def district_id(self) -> Optional[int]:
        return self._district_id
