import re
from typing import Union
from uuid import UUID
from decimal import Decimal, InvalidOperation


class UserID:
    def __init__(self, id_value: str):
        if not (5 <= len(id_value) <= 30) or not id_value.isalnum():
            raise ValueError("Неверный формат идентификатора Firebase для UserID")
        self._value = id_value

    @property
    def value(self) -> str:
        return self._value


class Email:
    def __init__(self, email: str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise ValueError("Некорректный формат email")
        self._value = email

    @property
    def value(self) -> str:
        return self._value


class Balance:
    def __init__(self, balance: Union[str, float, Decimal]):
        try:
            balance_value = Decimal(balance).quantize(Decimal("0.01"))
            if balance_value < Decimal("0"):
                raise ValueError("Баланс не может быть отрицательным")
        except (InvalidOperation, ValueError):
            raise ValueError("Баланс должен быть положительным числом с двумя десятичными знаками")
        self._value = balance_value

    @property
    def value(self) -> Decimal:
        return self._value


class Exp:
    def __init__(self, exp: int):
        if exp < 0:
            raise ValueError("Опыт не может быть отрицательным")
        self._value = exp

    @property
    def value(self) -> int:
        return self._value
