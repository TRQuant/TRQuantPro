# region imports
from AlgorithmImports import *
# endregion
def fine_selection(self, fine):
    for stock in fine:
        fcf = stock.FinancialStatements.CashFlowStatement.FreeCashFlow
        if fcf and fcf.TwelveMonths:
            self.Debug(f"{stock.Symbol.Value} | FCF: {fcf.TwelveMonths}")
    return [f.Symbol for f in fine]

