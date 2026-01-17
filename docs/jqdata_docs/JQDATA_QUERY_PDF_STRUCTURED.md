# JQData Query 使用方式完整文档（PDF提取）

> **来源**: JQDataQuery.pdf  
> **提取时间**: 2025-12-20  
> **总字符数**: 195,909

---

## 📚 目录结构

1. [基本查询方式](#基本查询方式)
2. [in_判断](#in_判断)
3. [distinct去重](#distinct去重)
4. [与或非逻辑](#与或非逻辑)
5. [运算和命名](#运算和命名)
6. [字符串匹配](#字符串匹配)
7. [简化计算](#简化计算)
8. [批量查询](#批量查询)
9. [财务数据表](#财务数据表)
10. [finance库](#finance库)

---

## 基本查询

（1）基本的查询方式........................................................... 5 
（1）基本的查询方式 
 query() 填写需要查询的对象,可以是整张表,也可以是表中的多个字段或计算出的
结果 

---

## in_判断

（2）in_ 判断某个字段的值是否在列表之中（一般判断多个标的）................... 9 
    #macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name.notin_(['北京市']) 
    ~macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name.in_(['北京市'])  
) 
 
（2）in_ 判断某个字段的值是否在列表之中（一般判断多
个标的） 
stocks = ['000001.XSHE','600741.XSHG','600507.XSHG'] 
# 指定返回的字段只包括code,pubDate,statDate,total_assets 及total_sheet_owner_equities 
         ).filter(balance.code.in_(stocks))  #指定查询到的数据只包括code 在 stocks 中的数据 
 
    #设定查询的地区名称为【北京市】和【广东省】，使用in_ 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name.in_(['北京市','广东省'])) 
                 |(valuation.code.in_(['000001.XSHE','600000.XSHG']))) 
    finance.FINANCE_INCOME_STATEMENT.code.in_(['000001.XSHE']), 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER.area_name.in_(['北京市']), 
    #设定查询时间为2019 年 
                valuation.code.in_(stocks)   #设置股票池,注释即为全市场 
                 ) 
net_increase_in_placements 
拆入资金净增加额(元) 
net_buyback 
回购业务资金净增加额(元) 
tax_levy_refund 
收到的税费返还(元) 
other_cashin_related_operate 
收到其他与经营活动有关的现金(元) 
net_deposit_in_cb_and_ib 
存放中央银行和同业款项净增加额(元) 
non_current_asset_in_one_year 
一年内到期的非流动资产(元) 
other_current_assets 
其他流动资产(元) 
total_current_assets 
流动资产合计(元) 
constru_in_process 
在建工程(元) 
construction_materials 
工程物资(元) 
fixed_assets_liquidation 
固定资产清理(元) 


=== 第 23 页 ===
biological_assets 
生产性生物资产(元) 
oil_gas_assets 
油气资产(元) 
intangible_assets 
无形资产(元) 
development_expenditure 
开发支出(元) 
good_will 
商誉(元) 
long_deferred_expense 
长期待摊费用(元) 
deferred_tax_assets 
递延所得税资产(元) 
other_non_current_assets 
其他非流动资产(元) 
total_non_current_assets 
非流动资产合计(元) 
total_assets 
资产总计(元) 
deposit_in_interbank 
吸收存款及同业存放(元) 
non_current_liability_in_one_year 
一年内到期的非流动负债(元) 
other_current_liability 
其他流动负债(元) 
total_current_liability 
流动负债合计(元) 
longterm_loan 
长期借款(元) 
bonds_payable 
应付债券(元) 
longterm_account_payable 
长期应付款(元) 
specific_account_payable 
专项应付款(元) 
estimate_liability 
预计负债(元) 
deferred_tax_liability 
递延所得税负债(元) 
other_non_current_liability 
其他非流动负债(元) 
total_non_current_liability 
非流动负债合计(元) 


=== 第 24 页 ===
total_liability 
负债合计(元) 
paidin_capital 
实收资本(或股本)(元) 
capital_reserve_fund 
资本公积金(元) 
treasury_stock 
库存股(元) 
specific_reserves 

---

## distinct去重

（3）distinct 去重,用于查看数据库中某个字段都存在哪些值...................... 10 
（3）distinct 去重,用于查看数据库中某个字段都存在哪
些值 
#  查看十大流通股东中都有哪些类别 
q = query( 
    finance.STK_SHAREHOLDER_FLOATING_TOP10.shareholder_class_id.distinct(),  #提取ID 不同的数据 
    finance.STK_SHAREHOLDER_FLOATING_TOP10.shareholder_class 

---

## 与或非

Word 文档：点击【视图】-勾选【导航窗格】 
PDF 文档：如使用WPS，页面左侧查看文档书签 
 
 
 
 
目录 
 
使用方法 ............................................................................. 4 
（4）与或非.................................................................. 11 
indicator 财务指标数据 ......................................................... 18 
bank indicator 银行业........................................................... 24 
security_indicator 券商 .......................................................... 25 
insurance indicator 保险 ......................................................... 26 
 
 
 
 
Query 使用方式 


=== 第 2 页 ===
finance 库 ............................................................................ 33 
股票............................................................................. 34 
沪深市场每日成交概况......................................................... 34 
申万一级行业指数日行情数据................................................... 34 
市场通交易日历............................................................... 34 
市场通AH 股价格对比 ......................................................... 35 
市场通合格证券变动记录....................................................... 35 
沪深港通持股数据............................................................. 35 
市场通十大成交活跃股......................................................... 36 
市场通成交与额度信息......................................................... 36 
市场通汇率................................................................... 37 
公司状态变动................................................................. 37 
上市公司......................................................................... 38 
上市公司基本信息............................................................. 38 
上市信息..................................................................... 39 
简称变更情况................................................................. 39 
员工情况..................................................................... 40 
公司管理人员任职情况......................................................... 40 
十大股东..................................................................... 41 
十大流通股东................................................................. 42 
股东股份质押................................................................. 42 
股东股份冻结................................................................. 43 
股东户数..................................................................... 44 
大股东增减持................................................................. 44 
上市公司股本变动............................................................. 45 
受限股份上市公告日期......................................................... 47 
受限股份实际解禁日期......................................................... 47 
上市公司分红送股 (除权除息)数据 .............................................. 48 
基金............................................................................. 51 
基金主体信息................................................................. 51 
基金持股信息................................................................. 51 
基金持有的债券信息........................................................... 52 
基金资产组合概况............................................................. 52 
基金财务指标................................................................. 53 
基金分红信息................................................................. 53 
场内基金份额数据............................................................. 54 
货币基金收益日报信息......................................................... 54 
基金净值信息................................................................. 55 
期货............................................................................. 56 
期货龙虎榜(会员持仓) ......................................................... 56 
期货仓单数据................................................................. 56 
外盘日行情数据............................................................... 57 
舆情数据......................................................................... 58 
舆情数据..................................................................... 58 
 
 
 
 
 


=== 第 3 页 ===
opt 库（期权） ....................................................................... 59 
期权合约资料................................................................. 59 
期权日行情(查表) ............................................................. 60 
期权风险指标................................................................. 61 
期权交易和持仓排名统计....................................................... 62 
期权行权交收信息............................................................. 63 
期权合约调整记录............................................................. 63 
期权每日盘前静态文件......................................................... 64 
 
 
 
 
bond 库（债券&可转债） .............................................................. 66 
债券基本信息................................................................. 66 
债券票面利率................................................................. 67 
债券付息事件................................................................. 67 
国债逆回购日行情数据......................................................... 68 
可转债基本资料............................................................... 68 
可转债转股价格调整........................................................... 69 
可转债每日转股统计........................................................... 70 
可转债日行情 (查表) .......................................................... 70 
 
 
 
 
macro 库（宏观经济） ................................................................. 72 

---

## 运算和命名

（5）运算和命名(label)....................................................... 12 
（5）运算和命名(label) 
#label 的作用是命名获得数据的标签,一般用于直接运算后的重命名 
#尽量命名为英文 
         (income.total_operating_revenue - income.total_operating_cost).label('my_operating_profit') 
          func.sum(valuation.capitalization).label('capitalization'),  # 总股本 , 
          func.sum(valuation.circulating_cap).label('circulating_cap'),  # A 股流通股本  
          func.sum(valuation.market_cap).label('market_cap'),  # 总市值  
          func.sum(valuation.circulating_market_cap).label('circulating_market_cap'),   #流通市值,  
          (func.count()/func.sum(1/valuation.turnover_ratio)).label('avg_turnover_ratio'),  #直接sql 求平均 , 也可以使用成交量/流通股
本计算 
         ).filter( 
    func.year(finance.STK_EXCHANGE_TRADE_INFO.date).label('year'), 
    func.month(finance.STK_EXCHANGE_TRADE_INFO.date).label('month'), 
    func.day(finance.STK_EXCHANGE_TRADE_INFO.date).label('day'), 
    finance.STK_EXCHANGE_TRADE_INFO.exchange_name, 
    finance.STK_EXCHANGE_TRADE_INFO.exchange_code, 
    finance.STK_EXCHANGE_TRADE_INFO.date 
          ).limit(5) 
finance.run_query(q) 
year 
month 
day 
exchange_name 
exchange_code 
date 
0 
2005 
1 
4 
上海A 股 322002 
2005-01-04 
1 
2005 
1 
4 
上海B 股 322003 
2005-01-04 
2 
2005 
1 
4 
上海市场 
322001 
2005-01-04 
3 
2005 
1 
4 
中小企业板 322006 
2005-01-04 
4 
2005 
1 
4 
深圳市场 
322004 
2005-01-04 
 
 

---

## 字符串匹配

（6）contains/like/ilike 数据库中的字符串模糊匹配............................ 12 
（6）contains/like/ilike 数据库中的字符串模糊匹配 
 
% 百分号通配符: 表示任何字符出现任意次数(可以是0 次). 
%模糊匹配含有“北京”的数据 
.like(“%%北京%%”) 
%模糊匹配“北京”开头的数据 
.like(“北京%%”) 
%模糊匹配“北京”结尾的数据 
.like(“%%北京”) 
 
 
_ 下划线通配符:表示只能匹配单个字符,不能多也不能少,就是一个字符. 
 
sqlalchemy 的版本,数据库的构建等问题可能导致查询报错,报错的话可以尝试另外两个方式 
 ilike 
# 获取000001.XSHG 每一年的年报    
q = query( 
    finance.FINANCE_INCOME_STATEMENT.end_date.ilike('_____12-31') 
) 
 #ilike，查询2019 年北京各季度的农林牧渔业总产值表 
#查找【宏观数据补充文档】 
#分地区农林牧渔业总产值表（季度累计）的表名为 
#【MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER】 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER  
        ).filter( 
    #设定查询的地区名称为【北京市】 
    #使用ilike 模糊查询 
    #_ 下划线通配符:表示只能匹配单个字符,不能多也不能少,就是一个字符. 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER.stat_quarter.ilike('2019___') 
 like 
#查询exchang_nameba 包含上海的行 
q = query(finance.STK_EXCHANGE_TRADE_INFO 
         ).filter(finance.STK_EXCHANGE_TRADE_INFO.exchange_name.like('%%上海%%')) 
         ).filter(finance.STK_EXCHANGE_TRADE_INFO.exchange_code.like('%%002')) 

---

## 简化计算

（7）简化计算的方法(sqlalchemy.sql.func)..................................... 14 
（7）简化计算的方法(sqlalchemy.sql.func)  
关于query 的可导入函数,可以使用以下方法查看,配合官网文档使用: 
    query(func.count('*') 
         ).filter( 
        finance.CCTV_NEWS.day<'2012-01-01') 
                ).iloc[0,0]  #先查询总共有多少条数据 
 

---

## 批量查询

（8）run_offset_query,批量查询数据库......................................... 15 
 
 
 
 
df = 库名.run_offset_query(q) #单次返回最多20 万条数据 
 因为run_query 有单次调取最大返回5000 条的限制，run_offset_query 函数利用MySql 的
offset 方法循环获取数据，便于提取超过5000 条的数据集 
 因为随着offset 值的增大，查询性能是递减的 ,因此此方法仍然设置了查询上限, 最多返回20
万条数据，如查询超过此上限返回数据可能不完整，请注意控制查询范围，可利用数据的日期,标的
代码等字段限制查询范围, 分批查询 
 因为该方法是通过指定limit 和offset 来实现分页查询的，因此用户自己给Query 对象中传递的
limit 及offset 参数将不生效 
 查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如
果命中索引返回就会较快 


=== 第 5 页 ===
综合案例： 
 limit 限制返回的个数(使用run_offset_query 时自己给Query 对象中传递的limit
及offset 参数不生效)  
 group_by 分组统计 
 
df = finance.run_offset_query(q) 


=== 第 6 页 ===
 #查询平安银行2014 到2016 年的季报, 放到数组中并拼接为dataframe 
q = query( 
df = macro.run_offset_query(q) 
print(df[:4]) 
 
df = macro.run_offset_query(q) 
#输出结果 
print(df) 
 
 
 查询【2022 年】【北京市】的分地区农林牧渔业总产值表(年度) 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR  
        ).filter( 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2022', 
    #设定查询的地区名称为【北京市】 
    #查找【宏观数据补充文档】，字段【area_name】代表地区名称 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name=='北京市' 
) 
df = macro.run_offset_query(q) 
#输出结果 
print(df) 
df = macro.run_offset_query(q) 
#输出结果 
print(df[:5]) 
df = macro.run_offset_query(q) 
#输出结果 
print(df[:5]) 
df = macro.run_offset_query(q) 
#输出结果 
print(df) 
 
df = finance.run_offset_query(q) 
df.tail() 
 
 
shareholder_class_id 
shareholder_class 
25 
307024.0 
上市公司和银行 
26 
307025.0 
信托投资管理公司和上市公司 
27 
307029.0 
期货经纪机构 
28 
307022.0 
上市公司和券商 
29 
307025.0 
上市公司和信托投资管理公司 


=== 第 11 页 ===
 
 
 
df = finance.run_offset_query(q) 
df 
 
df = finance.run_offset_query(q) 


=== 第 13 页 ===
df 
df = macro.run_offset_query(q) 
#输出结果 
print(df) 
df = finance.run_ offset_query(q) 
df[:5] 
 
id 

---

## 财务数据表

财务数据表（get_fundamentals） ........................................................ 18 
 get_fundamentals (股票单季度财务数据) 
 finance (股票数据,基金数据等) 
 bond (债券数据)  
 macro (宏观数据) 
使用方法 
finance 库、opt 库、bond 库、macro 库 
get_fundamentals(q,date='2018-01-05')    #查询单季度数据中在2018-01-05 之前发布的数据,没有未来函数 
 
 查询【2022 年】指定多个地区的农林牧渔业总产值表(年度) 
#指定查询【2022 年】指定【北京市、广东省】的农林牧渔业总产值表(年度) 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR  
        ).filter( 
    #设定查询时间为【2022】年 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2022', 


=== 第 10 页 ===
df=get_fundamentals(q, date='2016-10-15') 
print(df) 
 
code 
market_cap net_profit 
0 
000001.XSHE 
1560.7904 6.206000e+09 
1 
000725.XSHE 
896.4032 
-6.899237e+08 
2 
600000.XSHG 
3558.3689 1.300500e+10 
3 
600871.XSHG 
561.4636 
-2.824294e+09 
4 
601808.XSHG 
584.9972 
-7.476815e+09 
5 
601919.XSHG 
530.2246 
-2.425796e+09 
 
get_fundamentals(q) 
 
code 
my_operating_profit 
0 
600507.XSHG 
143977984.0 
 
 
df = get_fundamentals(q, date) 
df 
 
#提取年月日 
速,get_fundamentals 的限制为10000 条) 
财务数据表（get_fundamentals） 

---

## valuation

valuation 估值数据 ............................................................. 18 
valuation 估值数据 
列名 
列的含义 
code 
股票代码 
day 
日期 
capitalization 
总股本(万股) 
circulating_cap 
流通股本(万股) 
market_cap 
总市值(亿元) 
circulating_market_cap 
流通市值(亿元) 
turnover_ratio 
换手率(%) 
pe_ratio 
市盈率(PE, TTM) 
pe_ratio_lyr 
市盈率(PE) 
pb_ratio 
市净率(PB) 
ps_ratio 
市销率(PS, TTM) 
pcf_ratio 
市现率(PCF, 现金净流量TTM) 

---

## cashflow

cash flow 现金流量表 .......................................................... 19 
      balance.cash_equivalents 
  ).filter( 
cash_equivalents 
0 
2014-03-31 000001.XSHE 
0.53 
2.581100e+11 
0 
2014-06-30 000001.XSHE 
0.35 
2.596040e+11 
0 
2014-09-30 000001.XSHE 
0.49 
2.773250e+11 
0 
2014-12-31 000001.XSHE 
0.36 
3.062980e+11 
0 
2015-03-31 000001.XSHE 
0.41 
2.667050e+11 
0 
2015-06-30 000001.XSHE 
0.43 
2.986180e+11 
0 
2015-09-30 000001.XSHE 
0.43 
2.972230e+11 
0 
2015-12-31 000001.XSHE 
0.29 
2.917150e+11 
 
 # 查询分地区农林牧渔业总产值表(季度累计) 的数据 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER) 
经营活动产生的现金流量净额/营业收入(%) 
ocf_to_operating_profit 
经营活动产生的现金流量净额/经营活动净收益(%) 
inc_total_revenue_year_on_year 
营业总收入同比增长率(%) 
inc_total_revenue_annual 
营业总收入环比增长率(%) 
inc_revenue_year_on_year 
营业收入同比增长率(%) 
inc_revenue_annual 
营业收入环比增长率(%) 
inc_operation_profit_year_on_year 
cash flow 现金流量表 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
net_cash_received_from_reinsurance_busines
s 
收到再保险业务现金净额(元) 
net_insurer_deposit_investment 
保户储金及投资款净增加额(元) 
net_deal_trading_assets 
处置交易性金融资产净增加额(元) 
subtotal_operate_cash_inflow 
经营活动现金流入小计(元) 
policy_dividend_cash_paid 
支付保单红利的现金(元) 
staff_behalf_paid 
支付给职工以及为职工支付的现金(元) 
tax_payments 
支付的各项税费(元) 
other_operate_cash_paid 
支付其他与经营活动有关的现金(元) 
subtotal_operate_cash_outflow 
经营活动现金流出小计(元) 
net_operate_cash_flow 
经营活动产生的现金流量净额(元) 
invest_withdrawal_cash 
收回投资收到的现金(元) 
invest_proceeds 
取得投资收益收到的现金(元) 
fix_intan_other_asset_dispo_cash 
处置固定资产、无形资产和其他长期资产收回的现金净额(元) 
net_cash_deal_subcompany 
处置子公司及其他营业单位收到的现金净额(元) 
other_cash_from_invest_act 
收到其他与投资活动有关的现金(元) 
subtotal_invest_cash_inflow 
投资活动现金流入小计(元) 
fix_intan_other_asset_acqui_cash 
购建固定资产、无形资产和其他长期资产支付的现金(元) 
invest_cash_paid 
投资支付的现金(元) 
impawned_loan_net_increase 
质押贷款净增加额(元) 
net_cash_from_sub_company 

---

## income

income 利润表 ................................................................ 21 
 # 查询 000001 2015 - 2017 年的整张合并利润表,且满足 net_profit(净利润) > 0 的条件 
q = query(finance.STK_INCOME_STATEMENT).filter( 
    #选定股票  000783.XSHE 
    finance.STK_INCOME_STATEMENT.code=='000001.XSHE',  
    #指定查询时间段大于2005 年1 月1 日 
    finance.STK_INCOME_STATEMENT.end_date > '2005-01-01', 
    #指定查询时间段小于2018 年1 月1 日 
    finance.STK_INCOME_STATEMENT.end_date < '2018-01-01',         
    #指定查询到的数据中net_profit 为负 
    finance.STK_INCOME_STATEMENT.net_profit >0, 
    #指定报告期类型为本期 
      income.statDate, 
      income.code, 
      income.basic_eps, 
      income.code == '000001.XSHE') 
 
        # 利润数据.净利润,income.net_profit  
        # 筛选 总市值大于500 并且 净利润不大于0 或者 股票代码属'000001.XSHE','600000.XSHG'中 
        ).filter((valuation.market_cap > 500) 
                 &~ (income.net_profit > 0)  #要用括号把每个条件框起来 
    finance.FINANCE_INCOME_STATEMENT 
).filter( 
扣除非经常损益后的净利润(元) 
operating_profit 
经营活动净收益(元) 
value_change_profit 
价值变动净收益(元) 
roe 
净资产收益率ROE(%) 
inc_return 
净资产收益率(扣除非经常损益)(%) 
roa 
总资产净利率ROA(%) 
net_profit_margin 
销售净利率(%) 
gross_profit_margin 
销售毛利率(%) 
expense_to_total_revenue 
营业总成本/营业总收入(%) 
operation_profit_to_total_revenue 
营业利润/营业总收入(%) 
net_profit_to_total_revenue 
净利润/营业总收入(%) 
operating_expense_to_total_revenue 
营业费用/营业总收入(%) 
ga_expense_to_total_revenue 
管理费用/营业总收入(%) 


=== 第 19 页 ===
financing_expense_to_total_revenue 
财务费用/营业总收入(%) 
operating_profit_to_profit 
经营活动净收益/利润总额(%) 
invesment_profit_to_profit 
价值变动净收益/利润总额(%) 
adjusted_profit_to_profit 
扣除非经常损益后的净利润/归属于母公司所有者的净利润(%) 
营业利润同比增长率(%) 
inc_operation_profit_annual 
营业利润环比增长率(%) 
inc_net_profit_year_on_year 
净利润同比增长率(%) 
inc_net_profit_annual 
净利润环比增长率(%) 
inc_net_profit_to_shareholders_year_on_year 
归属母公司股东的净利润同比增长率(%) 
inc_net_profit_to_shareholders_annual 
归属母公司股东的净利润环比增长率(%) 
分配股利、利润或偿付利息支付的现金(元) 
proceeds_from_sub_to_mino_s 
子公司支付给少数股东的股利、利润(元) 
other_finance_act_payment 
支付其他与筹资活动有关的现金(元) 
income 利润表 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
total_operating_revenue 
营业总收入(元) 
operating_revenue 
营业收入(元) 
interest_income 
利息收入(元) 
premiums_earned 
已赚保费(元) 
commission_income 
手续费及佣金收入(元) 
total_operating_cost 
营业总成本(元) 
operating_cost 
营业成本(元) 
interest_expense 
利息支出(元) 

---

## balance

balance 资产负债表 ............................................................ 22 
q = query(balance.code, 
          balance.pubDate, 
          balance.statDate,     
          balance.total_assets, 
          balance.total_sheet_owner_equities 
balance 资产负债表 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
mid_term_loan_annualized_average_balance 
中长期贷款-平均余额 
mid_term_loan_annualized_average_interest_rate 
中长期贷款-年平均利率 
enterprise_deposits_average_balance 
企业存款-平均余额 
enterprise_deposits_average_interest_rate 
企业存款-年平均利率 
savings_deposit_average_balance 
储蓄存款-平均余额 
savings_deposit_average_interest_rate 
储蓄存款-年平均利率 
金融机构人民币信贷资金平衡表（年度）：MAC_CREDIT_BALANCE_YEAR 
货币供应量(月度)：MAC_MONEY_SUPPLY_MONTH 
货币供应量(年度)：MAC_MONEY_SUPPLY_YEAR 
货币当局资产负债表（年度）：MAC_CURRENCY_STATE_YEAR 
其他存款性公司资产负债表（年度）：MAC_OTHER_DEPOSIT 
社会融资规模及构成（年度）：MAC_SOCIAL_SCALE_FINANCE 
证券市场基本情况（年度）：MAC_STK_MARKET 
中央财政与地方财政收支及比重表（年度）：MAC_FISCAL_BALANCE_YEAR 
中央和地方财政主要收入项目情况表(年度)：MAC_FISCAL_CENTRAL_REVENUE_YEAR 
中央和地方财政主要支出项目情况表(年度)：MAC_FISCAL_CENTRAL_EXPENSE_YEAR 
各项税收表（年度）：MAC_FISCAL_TAX_YEAR 
预算外资金分项目收支表（年度）：MAC_FISCAL_EXTRA_REVENUE_EXPENSE_YEAR 
中央财政与地方财政预算外收支表（年度）：MAC_FISCAL_EXTRAL_BALANCE_YEAR 
外债余额表（年度）：MAC_FISCAL_EXTERNAL_DEBT_YEAR 
quota_balance 
总额度余额 
quota_daily 
每日额度 
quota_daily_balance 
每日额度余额 
市场通汇率 
STK_EXCHANGE_LINK_RATE 
字段 
名称 
day 
日期 
link_id 
市场通编码 
link_name 
市场通名称 
domestic_currency 本币 
表名：MAC_CREDIT_BALANCE_YEAR 
列名 
列的含义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_year 
统计年份 
文
本 
 
YYYY 
total_source 
金融机构
人民币信
贷资金来
源 
数
字 
 
信贷资金指金融机构以信用方式积聚和分配的货币资金。金融机构信
贷资金的来源有各项存款、金融债券、对国际金融机构负债、流通中
现金、其他项目等；信贷资金的运用有各项贷款、有价证券及投资、
金银占款、外汇占款、财政借款及在国际金融机构中的资产等。 
total_deposit 
金融机构
资金来源
各项存款 
数
字 
 
存款指企业、机关、团体或居民根据资金必须收回的原则，把货币资
金存入银行或其他信贷机构保管并取得一定利息的一种信用活动形
式。根据存款对象或性质的不同可划分为单位存款、个人存款、财政

---

