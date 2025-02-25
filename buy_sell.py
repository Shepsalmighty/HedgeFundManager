from portfolio import Portfolio

class Buy_Sell():
    def __init__(self, stock):
        """
        :param stock: - from ``stock.py``
        :param int trade_size: the currency value/amount of the underlying to buy
        :param in_trade: tracks if a trade is currently live
        """
        self.trade_size = None
        self.portfolio = Portfolio()
        self.stock = stock
        self.in_trade = False

    def buy_to_open(self):
        """
        open a buy position, on the given underlying
        """
        pass

    def buy_to_close(self):
        """
        close a buy position, on the given underlying locking in PnL
        """
        pass

    def sell_to_open(self):
        """
        open a sell position, on the given underlying
        """
        pass
    
    def sell_to_close(self):
        """
        close a sell position, on the given underlying locking in PnL
        """
        pass


