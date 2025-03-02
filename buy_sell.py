from portfolio import Portfolio
from stock import Stock

class Buy_Sell:
    def __init__(self, stock):
        """
        :param stock: - from ``stock.py``
        :param int trade_size: number of shares of the underlying to buy
        :param in_trade: tracks if a trade is currently live
        """
        self.portfolio = Portfolio()
        self.stock = stock


#TODO add stop loss and TP
    def buy_to_open(self, trade_size):
        """
        open a buy position, on the given underlying - without Margin currently
        """

        trade_cost = trade_size * self.stock.opens[self.stock.index]

        if self.portfolio.cash < trade_cost:
            return "Not enough money to place trade"

        self.portfolio.cash -= trade_cost
        self.portfolio.holdings['cash'] = round(self.portfolio.cash, 2)
        self.portfolio.holdings[self.stock.ticker.ticker] = (self.portfolio.holdings.get(self.stock.ticker.ticker, 0)
                                                      + trade_size)


    def sell_to_close(self, trade_size):
        """
        close a sell position, on the given underlying locking in PnL
        """
        #not allowing players to sell more shares than they own
        if trade_size > self.portfolio.holdings.get(self.stock.ticker.ticker, 0):
            return f"Can't sell that many shares you only have {self.portfolio.holdings.get(self.stock.ticker.ticker, 0)}"

        self.portfolio.holdings[self.stock.ticker.ticker] = (self.portfolio.holdings.get(self.stock.ticker.ticker, 0)
                                                      - trade_size)

        self.portfolio.cash += trade_size * self.stock.opens[self.stock.index]



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

#TODO add a json so that portfolio changes are saved and persistant
#TODO add trade history


stock = Stock("GOOG", "2024-11-03", "2025-02-08")
test_trade = Buy_Sell(stock)

test_trade.buy_to_open(50)

print(test_trade.portfolio)