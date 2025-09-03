"""
AGT Server - A tournament server for game theory competitions

This package provides a complete tournament server for running game theory lab competitions
including Rock Paper Scissors, Battle of the Sexes, Chicken, Prisoner's Dilemma, 
Lemonade Stand, Auctions, and more.

Quick Start:
    # Start the server
    from agt_server import AGTServer
    server = AGTServer({"game_type": "rps", "num_rounds": 100})
    asyncio.run(server.run())
    
    # Or use command line tools after installation:
    # agt-server --game rps
    # agt-dashboard
    # agt-both

For more information, see the documentation or run:
    agt-server --help
    agt-dashboard --help
"""

__version__ = "0.1.0"
__author__ = "AGT Server Team"

# Import main classes for easy access
from agt_server.server.server import AGTServer
from agt_server.core.engine import Engine as GameEngine

# Import game classes
from agt_server.core.game.RPSGame import RPSGame
from agt_server.core.game.BOSGame import BOSGame
from agt_server.core.game.BOSIIGame import BOSIIGame
from agt_server.core.game.ChickenGame import ChickenGame
from agt_server.core.game.PDGame import PDGame
from agt_server.core.game.LemonadeGame import LemonadeGame
from agt_server.core.game.AuctionGame import AuctionGame

__all__ = [
    "AGTServer",
    "GameEngine", 
    "RPSGame",
    "BOSGame",
    "BOSIIGame",
    "ChickenGame",
    "PDGame",
    "LemonadeGame",
    "AuctionGame",
]
