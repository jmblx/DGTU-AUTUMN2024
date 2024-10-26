from _decimal import Decimal
from typing import Optional

from domain.entities.reward.value_objects import MarketCost, IsMarketAvailable, FilePath, Title, RewardID


class Reward:
    def __init__(
        self,
        reward_id: RewardID,
        title: Title,
        file_path: Optional[FilePath],
        is_market_available: IsMarketAvailable,
        market_cost: Optional[MarketCost] = None
    ):
        self._id = reward_id
        self._title = title
        self._file_path = file_path
        self._is_market_available = is_market_available
        self._market_cost = market_cost

    @property
    def id(self) -> int:
        return self._id.value

    @property
    def title(self) -> str:
        return self._title.value

    @property
    def file_path(self) -> Optional[str]:
        return self._file_path.value

    @property
    def is_market_available(self) -> bool:
        return self._is_market_available.value

    @property
    def market_cost(self) -> Optional[Decimal]:
        return self._market_cost.value
