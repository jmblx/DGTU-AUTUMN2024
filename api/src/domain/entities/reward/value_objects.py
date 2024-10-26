from typing import Optional
from decimal import Decimal, InvalidOperation


class RewardID:
    def __init__(self, id_value: int):
        if id_value <= 0:
            raise ValueError("ID награды должен быть положительным числом.")
        self._value = id_value

    @property
    def value(self) -> int:
        return self._value


class Title:
    def __init__(self, title: str):
        if not title or len(title) > 255:
            raise ValueError("Название награды не может быть пустым или слишком длинным.")
        self._value = title

    @property
    def value(self) -> str:
        return self._value


class FilePath:
    def __init__(self, path: Optional[str]):
        if path and not path.startswith("http://") and not path.startswith("https://"):
            raise ValueError("Путь к файлу должен быть допустимым URL-адресом.")
        self._value = path

    @property
    def value(self) -> Optional[str]:
        return self._value


class MarketCost:
    def __init__(self, cost: Optional[float]):
        if cost is not None:
            try:
                cost_value = Decimal(cost).quantize(Decimal("0.01"))
                if cost_value < Decimal("0"):
                    raise ValueError("Стоимость на рынке должна быть положительным числом.")
            except (InvalidOperation, ValueError):
                raise ValueError("Стоимость на рынке должна быть допустимым числом с двумя десятичными знаками.")
            self._value = cost_value
        else:
            self._value = None

    @property
    def value(self) -> Optional[Decimal]:
        return self._value


class IsMarketAvailable:
    def __init__(self, is_available: bool):
        if not isinstance(is_available, bool):
            raise ValueError("Поле доступности должно быть булевым значением.")
        self._value = is_available

    @property
    def value(self) -> bool:
        return self._value
