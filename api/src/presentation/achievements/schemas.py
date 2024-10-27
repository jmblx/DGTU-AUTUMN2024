from pydantic import BaseModel

from presentation.rewards.shemas import RewardRead


class ReadAch(BaseModel):
    id: int
    title: str
    description: str
    file_path: str
    rewards: list[RewardRead]


class ReadAchWithProgress(ReadAch):
    goal: float
    progress: float
