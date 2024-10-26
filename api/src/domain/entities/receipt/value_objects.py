from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional


class ReceiptID:
    def __init__(self, id_value: str):
        if not id_value or len(id_value) > 50:
            raise ValueError("Идентификатор чека не может быть пустым и должен быть короче 50 символов.")
        self._value = id_value

    @property
    def value(self) -> str:
        return self._value


class UserID:
    def __init__(self, user_id: str):
        if not user_id or len(user_id) > 50:
            raise ValueError("Идентификатор пользователя не может быть пустым и должен быть короче 50 символов.")
        self._value = user_id

    @property
    def value(self) -> str:
        return self._value


class ReceiptTime:
    def __init__(self, time: datetime):
        if not isinstance(time, datetime):
            raise ValueError("Дата и время должны быть допустимым значением datetime.")
        self._value = time

    @property
    def value(self) -> datetime:
        return self._value


class TotalPrice:
    def __init__(self, price: float):
        try:
            price_value = Decimal(price).quantize(Decimal("0.01"))
            if price_value <= 0:
                raise ValueError("Общая цена должна быть положительным числом.")
        except (InvalidOperation, ValueError):
            raise ValueError("Цена должна быть допустимым числом с двумя десятичными знаками.")
        self._value = price_value

    @property
    def value(self) -> Decimal:
        return self._value


class CarbonPrint:
    def __init__(self, carbon: Optional[float]):
        if carbon is not None:
            try:
                carbon_value = Decimal(carbon).quantize(Decimal("0.01"))
                if carbon_value < Decimal("0"):
                    raise ValueError("Углеродный след должен быть положительным числом.")
            except (InvalidOperation, ValueError):
                raise ValueError("Углеродный след должен быть допустимым числом с двумя десятичными знаками.")
            self._value = carbon_value
        else:
            self._value = None

    @property
    def value(self) -> Optional[Decimal]:
        return self._value
