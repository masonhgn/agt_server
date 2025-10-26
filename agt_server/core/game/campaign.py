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


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "market_segment": self.market_segment.value,
            "reach": self.reach,
            "budget": self.budget,
            "start_day": self.start_day,
            "end_day": self.end_day
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Campaign':
        """Create a Campaign object from a dictionary."""
        return cls(
            id=data['id'],
            market_segment=MarketSegment(data['market_segment']),
            reach=data['reach'],
            budget=data['budget'],
            start_day=data.get('start_day', 1),
            end_day=data.get('end_day', 1)
        )