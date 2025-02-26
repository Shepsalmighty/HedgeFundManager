class Portfolio():
    def __init__(self):
        #TODO add 4% APY interest on cash
        self.cash = 10000000
        self.holdings = {}

    def __str__(self):
        return (f"you have $$${round(self.cash, 2)} burning a hole in your wallet, \n"
                f"and {self.holdings} stonks")



