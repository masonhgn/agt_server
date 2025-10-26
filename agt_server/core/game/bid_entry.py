from core.game.market_segment import MarketSegment
from dataclasses import dataclass

@dataclass
class SimpleBidEntry:
    market_segment: MarketSegment
    bid: float
    spending_limit: float 

    def to_dict(self) -> dict:
        return {
            "market_segment": self.market_segment.value,
            "bid": self.bid,
            "spending_limit": self.spending_limit
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SimpleBidEntry':
        """Create SimpleBidEntry from dictionary."""
        return cls(
            market_segment=MarketSegment(data['market_segment']),
            bid=data['bid'],
            spending_limit=data['spending_limit']
        )