from core.game.market_segment import MarketSegment
from dataclasses import dataclass

@dataclass
class SimpleBidEntry:
    market_segment: MarketSegment
    bid: float
    spending_limit: float 