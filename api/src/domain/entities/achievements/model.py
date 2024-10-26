from typing import Optional, List

from domain.entities.achievements.value_objects import AchievementID, FilePath, Title, Description


class Achievement:
    def init(
        self,
        title: Title,
        description: Description,
        file_path: FilePath,
    ):
        self._id: Optional[AchievementID] = None  # Изначально ID не задан
        self._title = title
        self._description = description
        self._file_path = file_path

    @property
    def id(self) -> Optional[int]:
        return self._id.value if self._id else None

    def set_id(self, achievement_id: int):
        """Устанавливает ID после сохранения в базу."""
        if self._id is not None:
            raise ValueError("ID уже установлен и не может быть изменен.")
        self._id = AchievementID(achievement_id)

    # Остальные свойства и методы остаются неизменными
    @property
    def title(self) -> str:
        return self._title.value

    @property
    def description(self) -> str:
        return self._description.value

    @property
    def file_path(self) -> str:
        return self._file_path.value
