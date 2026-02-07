from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class TitForTatAgent(BaseAgent):
    """
    tit-for-tat agent that copies opponent's previous action.

    plays a default action on the first move, then mirrors whatever
    the opponent played in the previous round. works for any game
    where observations include opponent_last_action.
    """

    def __init__(self, name: str = "TitForTat", default_action: int = 0):
        super().__init__(name)
        self.default_action = default_action

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """return action based on tit-for-tat strategy."""
        if obs is None:
            return self.default_action

        opponent_last_action = obs.get("opponent_last_action", None)

        if opponent_last_action is None:
            return self.default_action

        return opponent_last_action

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """update with the observation and reward received."""
        if reward is not None:
            self.reward_history.append(reward)
