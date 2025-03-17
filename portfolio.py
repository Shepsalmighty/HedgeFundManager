import json
from game_state import GameState

class Portfolio:
    def __init__(self, player_game_state):
        #TODO add 4% APY interest on cash

        # self.cash = player_game_state.get_synced_data().setdefault('cash', {})
        self.__tracked_cash = player_game_state.get_synced_data().setdefault('cash', [100_000])
        self.holdings = player_game_state.get_synced_data().setdefault('holdings', {})

    @property
    def cash(self):
        return self.__tracked_cash[0]

    @cash.setter
    def cash(self, value):
        self.__tracked_cash[0] = value


    def __str__(self):
        return (f"you have $$${round(self.cash, 2)} burning a hole in your wallet, \n"
                f"and {self.holdings} stonks")



