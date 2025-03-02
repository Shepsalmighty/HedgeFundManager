import json
from game_state import GameState

class Portfolio:
    def __init__(self, player_game_state):
        #TODO add 4% APY interest on cash
        self.cash = 10000000
        self.holdings = player_game_state.get_synced_data().setdefault('holdings', {})


    def __str__(self):
        return (f"you have $$${round(self.cash, 2)} burning a hole in your wallet, \n"
                # round(self.holdings.get('cash'),2)
                f"and {self.holdings} stonks")


    def initialised(self):
        """returns False if no holdings - zero trades have been made"""
        return len(self.holdings) != 0




