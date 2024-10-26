import re


class AchievementID:
    def __init__(self, id_value: int):
        if id_value <= 0:
            raise ValueError("ID достижения должен быть положительным числом.")
        self._value = id_value

    @property
    def value(self) -> int:
        return self._value


class Title:
    def __init__(self, title: str):
        if not title or len(title) > 255:
            raise ValueError("Название достижения не может быть пустым или слишком длинным.")
        self._value = title

    @property
    def value(self) -> str:
        return self._value


class Description:
    def __init__(self, description: str):
        if len(description) > 1000:
            raise ValueError("Описание достижения не может быть длиннее 1000 символов.")
        self._value = description

    @property
    def value(self) -> str:
        return self._value


class FilePath:
    def __init__(self, path: str):
        # Проверка, что путь является допустимым URL с использованием http/https и заданного формата
        pattern = r"^https?://[a-zA-Z0-9.-]+(:[0-9]+)?/rewards/.+"
        if not re.match(pattern, path):
            raise ValueError("Путь к файлу должен быть допустимым URL-адресом MinIO в формате 'http://localhost:9000/rewards/...'")
        self._value = path

    @property
    def value(self) -> str:
        return self._value

