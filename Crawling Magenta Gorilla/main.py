from AlgorithmImports import *

class PLTR_FCF_VS_PRICE(QCAlgorithm):

    def initialize(self):
        # —— 回测区间 & 现金（Python API 是小写）——
        # 文档：set_start_date / set_end_date（Python）:contentReference[oaicite:0]{index=0}
        self.set_start_date(2018, 1, 1)
        self.set_end_date(2025, 8, 1)
        self.set_cash(100000)

        # —— 订阅 PLTR（Python：add_equity 返回 Symbol）——
        # 文档：requesting-data / add_equity（Python）:contentReference[oaicite:1]{index=1}
        equity = self.add_equity("PLTR", Resolution.DAILY)
        equity.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
        self.symbol = equity.symbol

        # —— 归一化基准：首见价格即基准（避免 history 索引 KeyError）——
        self._price_base = None

        # —— 月频调度（Python：self.schedule.on + date_rules/time_rules）——
        # 文档：Scheduled Events（Python 用法）:contentReference[oaicite:2]{index=2}
        self.schedule.on(
            self.date_rules.month_start(self.symbol),
            self.time_rules.after_market_open(self.symbol, 10),
            self._record_snapshot
        )

        # 仅可视化
        # 文档：set_benchmark（Python）:contentReference[oaicite:3]{index=3}
        self.set_benchmark("SPY")

    # —— 安全转数：把 None/NaN 过滤掉 —— 
    def _num(self, x):
        try:
            v = float(x)
            if v != v:  # NaN
                return None
            return v
        except Exception:
            return None

    def _record_snapshot(self):
        sec = self.securities[self.symbol]
        if not sec.has_data:
            return

        # 价格归一化：首次拿到价格时设基准
        px = self._num(sec.price)
        if px is None or px <= 0:
            return
        if self._price_base is None:
            self._price_base = px
        norm_px = px / self._price_base if self._price_base else None

        # —— 取 TTM 自由现金流（正确的 Python 属性路径）——
        # 文档：Corporate Fundamentals → 直接访问 Fundamentals（Python）
        # 以及 Python 示例中 financial_statements.xxx 的访问方式:contentReference[oaicite:4]{index=4}
        f = sec.fundamentals
        fcf_ttm = None

        # 先判断是否有基本面数据（has_fundamental_data）:contentReference[oaicite:5]{index=5}
        if f and f.has_fundamental_data and f.financial_statements and f.financial_statements.cash_flow_statement:
            cfs = f.financial_statements.cash_flow_statement
            # Python 属性名为 snake_case：operating_cash_flow / capital_expenditure / twelve_months
            # 类参考：OperatingCashFlowCashFlowStatement / CashFlowStatement（C# 类，但字段同名）:contentReference[oaicite:6]{index=6}
            ocf_ttm   = self._num(getattr(cfs.operating_cash_flow,  "twelve_months", None))
            capex_raw = self._num(getattr(cfs.capital_expenditure, "twelve_months", None))
            if ocf_ttm is not None and capex_raw is not None:
                # CapEx 常为负，取绝对值后计算 FCF
                fcf_ttm = ocf_ttm - abs(capex_raw)

        # —— 绘图：Python 用 self.plot；如果未先建图/序列，会自动创建 —— 
        # 文档：Charting / self.plot 自动创建 chart & series（Python）:contentReference[oaicite:7]{index=7}
        if fcf_ttm is not None:
            self.plot("PLTR FCF vs Price", "FCF_TTM", fcf_ttm)
        if norm_px is not None:
            self.plot("PLTR FCF vs Price", "Price_Norm", norm_px)

