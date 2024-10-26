from domain.entities.event.value_objects import EventID, IsGroup, FilePath, Description


class Event:
    def __init__(
        self,
        event_id: EventID,
        description: Description,
        is_group: IsGroup,
        file_path: FilePath
    ):
        self._id = event_id
        self._description = description
        self._is_group = is_group
        self._file_path = file_path

    @property
    def id(self) -> int:
        return self._id.value

    @property
    def description(self) -> str:
        return self._description.value

    @property
    def is_group(self) -> bool:
        return self._is_group.value

    @property
    def file_path(self) -> str:
        return self._file_path.value
