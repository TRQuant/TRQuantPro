# region imports
from AlgorithmImports import *
# endregion

class CasualYellowGreenDog(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2024, 1, 27)
        self.set_cash(10000)
        self.add_equity("NVDA", Resolution.MINUTE)
        self.add_equity("APP", Resolution.MINUTE)
        self.add_equity("PLTR", Resolution.MINUTE)

    def on_data(self, data: Slice):
        if not self.portfolio.invested:
            self.set_holdings("NVDA", 0.34)
            self.set_holdings("APP", 0.33)
            self.set_holdings("PLTR", 0.33)
