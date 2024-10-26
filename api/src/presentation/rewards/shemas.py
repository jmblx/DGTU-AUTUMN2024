from pydantic import BaseModel


class RewardRead(BaseModel):
    id: int
    title: str
    file_path: str | None
    amount: int | None
    # event_id: int | None
    # achievement_id: int | None

