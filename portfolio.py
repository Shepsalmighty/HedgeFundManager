import json

class Portfolio:
    def __init__(self):
        #TODO add 4% APY interest on cash
        self.cash = 10000000
        self.holdings = {}

    def __str__(self):
        return (f"you have $$${round(self.cash, 2)} burning a hole in your wallet, \n"
                # round(self.holdings.get('cash'),2)
                f"and {self.holdings} stonks")


    def initialised(self):
        """returns False if no holdings - zero trades have been made"""
        return len(self.holdings) is not 0

mytest = Portfolio()
print(mytest.initialised())


