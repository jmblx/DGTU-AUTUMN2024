class EventID:
    def __init__(self, id_value: int):
        if id_value <= 0:
            raise ValueError("ID события должен быть положительным числом.")
        self._value = id_value

    @property
    def value(self) -> int:
        return self._value


class Description:
    def __init__(self, description: str):
        if not description or len(description) > 1000:
            raise ValueError("Описание события не может быть пустым или длиннее 1000 символов.")
        self._value = description

    @property
    def value(self) -> str:
        return self._value


class IsGroup:
    def __init__(self, is_group: bool):
        if not isinstance(is_group, bool):
            raise ValueError("Поле группового события должно быть булевым значением.")
        self._value = is_group

    @property
    def value(self) -> bool:
        return self._value


class FilePath:
    def __init__(self, path: str):
        if not path.startswith("http://") and not path.startswith("https://"):
            raise ValueError("Путь к файлу должен быть допустимым URL-адресом.")
        self._value = path

    @property
    def value(self) -> str:
        return self._value
