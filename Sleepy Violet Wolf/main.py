from AlgorithmImports import *

class FreeCashFlowFineFundamentalAlgorithm(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2021, 7, 1)
        self.set_end_date(2021, 7, 1)
        self.set_cash(100000)

        self.selected_tickers = ["NVDA", "SMCI"]

        # 添加Universe：Coarse + Fine
        self.add_universe(self.coarse_selection_function, self.fine_selection_function)

    def coarse_selection_function(self, coarse):
        return [Symbol.create(ticker, SecurityType.EQUITY, Market.USA) for ticker in self.selected_tickers]

    def fine_selection_function(self, fine):
        for stock in fine:
            if stock.Symbol.Value in self.selected_tickers:
                fcf = stock.FinancialStatements.CashFlowStatement.FreeCashFlow
                if fcf and fcf.TwelveMonths:
                    self.debug(f"{self.time} - {stock.Symbol.Value} | FCF (TTM): {fcf.TwelveMonths}")
        return [f.Symbol for f in fine if f.Symbol.Value in self.selected_tickers]

    def on_data(self, data):
        pass  # 本例中我们不做交易，只看数据打印

