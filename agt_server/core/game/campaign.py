from core.game.market_segment import MarketSegment
from dataclasses import dataclass

@dataclass
class Campaign:
    id: int
    market_segment: MarketSegment
    reach: int
    budget: float
    start_day: int = 1
    end_day: int = 1 