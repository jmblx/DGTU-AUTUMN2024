from pydantic import BaseModel

from presentation.rewards.shemas import RewardRead


class EventRead(BaseModel):
    id: int
    description: str
    rewards: list[RewardRead]
    file_path: str | None
