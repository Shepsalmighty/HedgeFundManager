from PySide6.QtWidgets import QInputDialog, QWidget

from portfolio import Portfolio
from stock import Stock
from game_state import GameState

class BuySell:
    def __init__(self, stock, player_game_state):
        """
        :param stock: - from ``stock.py``
        :param int trade_size: number of shares of the underlying to buy
        :param in_trade: tracks if a trade is currently live
        """
        self.portfolio = Portfolio(player_game_state)
        self.stock = stock
        self.state = player_game_state



#TODO add stop loss and TP


    def buy_to_open(self, trade_size):
        """
        open a buy position, on the given underlying - without Margin currently
        """

        trade_cost = trade_size * self.stock.opens[self.stock.index]

        if self.portfolio.cash < trade_cost:
            return "Not enough money to place trade"

        self.portfolio.cash -= trade_cost
        # self.portfolio.holdings['cash'] = round(self.portfolio.cash, 2)
        self.portfolio.holdings[self.stock.ticker.ticker] = (self.portfolio.holdings.get(self.stock.ticker.ticker, 0)
                                                      + trade_size)

        print(f"Bought {trade_size} shares")

        self.state.sync()

    def sell_shares(self):
        i, ok = QInputDialog.getInt(central_widget, "QInputDialog::getInt()",
                                    "Order Size:", 0, 1, 100000000, 10)
        if ok:
            return i

    def sell_to_close(self, trade_size):
        """
        close a sell position, on the given underlying locking in PnL
        """
        #not allowing players to sell more shares than they own
        #TODO this return does not print, instead we get the standard portfolio string
        if trade_size > self.portfolio.holdings.get(self.stock.ticker.ticker, 0):
            return f"Can't sell that many shares you only have {self.portfolio.holdings.get(self.stock.ticker.ticker, 0)}"

        self.portfolio.holdings[self.stock.ticker.ticker] = (self.portfolio.holdings.get(self.stock.ticker.ticker, 0)
                                                      - trade_size)

        self.portfolio.cash += trade_size * self.stock.opens[self.stock.index]

        self.state.sync()



    def sell_to_open(self, trade_size):
        """
        open a sell position, on the given underlying - without Margin currently
        """
        pass

    def buy_to_close(self, trade_size):
        """
        close a buy position, on the given underlying locking in PnL
        """
        pass


#TODO add trade history


stock = Stock("GOOG", "2024-11-03", "2025-02-08")
player_game_state = GameState('player_state.json')

test_trade = BuySell(stock, player_game_state)

test_trade.sell_to_close(200)

print(test_trade.portfolio)

#TODO: add logic for the below that doesn't mess stuff up without this if block we won't be notified
# that we can't sell more stock than we own
# if test_trade.sell_to_close(2) is None:
#     print(test_trade.portfolio)
# else:
#     print(test_trade.sell_to_close(200))