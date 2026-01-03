# JQData Query PDF文档内容

=== 第 1 页 ===
 
 
 
 
 
如何调出目录索引： 
Word 文档：点击【视图】-勾选【导航窗格】 
PDF 文档：如使用WPS，页面左侧查看文档书签 
 
 
 
 
目录 
 
使用方法 ............................................................................. 4 
（1）基本的查询方式........................................................... 5 
（2）in_ 判断某个字段的值是否在列表之中（一般判断多个标的）................... 9 
（3）distinct 去重,用于查看数据库中某个字段都存在哪些值...................... 10 
（4）与或非.................................................................. 11 
（5）运算和命名(label)....................................................... 12 
（6）contains/like/ilike 数据库中的字符串模糊匹配............................ 12 
（7）简化计算的方法(sqlalchemy.sql.func)..................................... 14 
（8）run_offset_query,批量查询数据库......................................... 15 
 
 
 
 
财务数据表（get_fundamentals） ........................................................ 18 
valuation 估值数据 ............................................................. 18 
indicator 财务指标数据 ......................................................... 18 
cash flow 现金流量表 .......................................................... 19 
income 利润表 ................................................................ 21 
balance 资产负债表 ............................................................ 22 
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
农业......................................................................... 72 
国内贸易..................................................................... 75 
就业与工资................................................................... 79 
资源环境..................................................................... 86 
房地产行业................................................................... 94 
金融业...................................................................... 103 
财政政策.................................................................... 116 
固定资产投资................................................................ 126 
对外贸易.................................................................... 135 
景气指数.................................................................... 145 
工业........................................................................ 148 
保险业...................................................................... 158 
国民经济.................................................................... 164 
人民生活.................................................................... 173 
人口信息.................................................................... 182 
 
 


=== 第 4 页 ===
涉及到query 操作的数据有： 
 get_fundamentals (股票单季度财务数据) 
 finance (股票数据,基金数据等) 
 bond (债券数据)  
 macro (宏观数据) 
使用方法 
finance 库、opt 库、bond 库、macro 库 
from jqdatasdk import * 
q = query(库名.表名.字段名1, 
          库名.表名.字段名2, 
          库名.表名.字段名3 
         ).filter(库名.表名.字段名1.xxxxx, 
                  库名.表名.字段名2.xxxxx, 
                 ).order_by(库名.表名.字段名3.desc()).limit() 
df = 库名.run_query(q) #单次返回最多5000 条数据 
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
（1）基本的查询方式 
 query() 填写需要查询的对象,可以是整张表,也可以是表中的多个字段或计算出的
结果 
 filter 填写过滤条件,多个过滤条件可以用逗号隔开,或者用and,or 这样的语法  
 order_by 填写排序条件  
 
.desc() 降序排列 
 
.asc() 升序排列 
 limit 限制返回的个数(使用run_offset_query 时自己给Query 对象中传递的limit
及offset 参数不生效)  
 group_by 分组统计 
 
 # 查询 000001 2015 - 2017 年的整张合并利润表,且满足 net_profit(净利润) > 0 的条件 
from jqdatasdk import * 
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
    finance.STK_INCOME_STATEMENT.report_type == 0 
).order_by(finance.STK_INCOME_STATEMENT.end_date.desc())#根据end_date 降序排序 
df = finance.run_offset_query(q) 


=== 第 6 页 ===
 #查询平安银行2014 到2016 年的季报, 放到数组中并拼接为dataframe 
q = query( 
      income.statDate, 
      income.code, 
      income.basic_eps, 
      balance.cash_equivalents 
  ).filter( 
      income.code == '000001.XSHE') 
 
rets = [get_fundamentals(q, statDate=str(j) +'q'+str(i)) for i in range(1, 5) for j in range(2014,2016)] 
 
import pandas as pd 
df = pd.concat(rets) 
df = df.sort_values('statDate') 
 
 
statDate 
code 
basic_eps 
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
df = macro.run_offset_query(q) 
print(df[:4]) 
 
   id stat_quarter area_code area_name      total    farming  forestry  \ 
0   1      2015-06    350000       福建省  1240.1000   430.4000  101.2000    
1   2      2014-09    350000       福建省  2027.9000   830.8000  155.2000    
2   3      2015-03    350000       福建省   538.2000   148.2000   36.4000    
3   4      2014-12    350000       福建省  3522.3053  1529.5705  323.2506    
 
   animal_husbandry    fishery   
0          237.7000   417.6000   
1          368.4000   591.2000   
2          127.6000   197.9000   


=== 第 7 页 ===
3          522.8944  1025.1946  
 
 
 查询2022 年的分地区农林牧渔业总产值表(年度) 
#基本格式 
#query(macro.表名.字段名1，macro.表名.字段名2） 
# 查询2022 年的分地区农林牧渔业总产值表(年度) 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR  
          #设定表名为分地区农林牧渔业总产值表（年度） 
        ).filter(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2022' 
                 #设置查询的统计年份为2022 
                ). 
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
     id stat_year area_code area_name   total  farming  forestry  \ 
0  2884      2022    110000       北京市  268.18   129.77     86.52    
 
   animal_husbandry  fishery  total_idx farming_idx forestry_idx  \ 
0             42.29     3.85       98.0        None         None    
 
  animal_husbandry_idx fishery_idx   
0                 None        None   
 
 查询2022 年北京市以外的地区的农林牧渔业总产值表(年度) 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR  
        ).filter( 
    #设定查询时间为【2022】年 


=== 第 8 页 ===
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2022', 
    #设定查询的地区名称为【北京市】和【广东省】 
    #macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name.notin_(['北京市']) 
    ~macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name.in_(['北京市'])  
) 
 
df = macro.run_offset_query(q) 
#输出结果 
print(df[:5]) 
     id stat_year area_code area_name    total  farming  forestry  \ 
0  2895      2022    120000       天津市   521.44   276.80      8.86    
1  2900      2022    130000       河北省  7667.41  4035.67    266.56    
2  2890      2022    140000       山西省  2211.59  1288.41    174.52    
3  2898      2022    150000    内蒙古自治区  4316.76  2208.47    107.50    
4  2896      2022    210000       辽宁省  5180.03  2258.29    161.70    
 
   animal_husbandry  fishery  total_idx farming_idx forestry_idx  \ 
0            147.23    70.46      102.9        None         None    
1           2391.71   342.29      104.6        None         None    
2            615.81     9.06      105.0        None         None    
3           1876.28    31.30      104.9        None         None    
4           1694.61   881.26      103.2        None         None    
 
  animal_husbandry_idx fishery_idx   
0                 None        None   
1                 None        None   
2                 None        None   
3                 None        None   
4                 None        None   
 #查询2022 年,农林牧渔业总产值排名前5 的地区 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR  
        ).filter( 
    #设定查询时间为2022 年 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2022' 
                ).order_by(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.total.desc() 
                          ) #根据total 降序排序 .asc()代表升序排序，.desc() 降序排列 
 
df = macro.run_offset_query(q) 
#输出结果 
print(df[:5]) 
     id stat_year area_code area_name     total  farming  forestry  \ 


=== 第 9 页 ===
0  2902      2022    370000       山东省  12130.71  6206.54    227.29    
1  2881      2022    410000       河南省  10952.24  6948.30    149.55    
2  2880      2022    510000       四川省   9859.75  5528.76    438.22    
3  2904      2022    420000       湖北省   8939.33  4193.14    311.22    
4  2877      2022    440000       广东省   8892.29  4308.23    549.15    
 
   animal_husbandry  fishery  total_idx farming_idx forestry_idx  \ 
0           3003.54  1729.65      104.8        None         None    
1           2832.30   147.45      105.1        None         None    
2           3281.67   343.11      104.5        None         None    
3           2128.19  1584.34      104.4        None         None    
4           1680.24  1898.24      104.8        None         None    
 
  animal_husbandry_idx fishery_idx   
0                 None        None   
1                 None        None   
2                 None        None   
3                 None        None   
4                 None        None   
（2）in_ 判断某个字段的值是否在列表之中（一般判断多
个标的） 
stocks = ['000001.XSHE','600741.XSHG','600507.XSHG'] 
# 指定返回的字段只包括code,pubDate,statDate,total_assets 及total_sheet_owner_equities 
q = query(balance.code, 
          balance.pubDate, 
          balance.statDate,     
          balance.total_assets, 
          balance.total_sheet_owner_equities 
         ).filter(balance.code.in_(stocks))  #指定查询到的数据只包括code 在 stocks 中的数据 
 
get_fundamentals(q,date='2018-01-05')    #查询单季度数据中在2018-01-05 之前发布的数据,没有未来函数 
 
 查询【2022 年】指定多个地区的农林牧渔业总产值表(年度) 
#指定查询【2022 年】指定【北京市、广东省】的农林牧渔业总产值表(年度) 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR  
        ).filter( 
    #设定查询时间为【2022】年 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2022', 


=== 第 10 页 ===
    #设定查询的地区名称为【北京市】和【广东省】，使用in_ 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.area_name.in_(['北京市','广东省'])) 
df = macro.run_offset_query(q) 
#输出结果 
print(df) 
 
     id stat_year area_code area_name    total  farming  forestry  \ 
0  2884      2022    110000       北京市   268.18   129.77     86.52    
1  2877      2022    440000       广东省  8892.29  4308.23    549.15    
 
   animal_husbandry  fishery  total_idx farming_idx forestry_idx  \ 
0             42.29     3.85       98.0        None         None    
1           1680.24  1898.24      104.8        None         None    
 
  animal_husbandry_idx fishery_idx   
0                 None        None   
1                 None        None   
 
 
 
（3）distinct 去重,用于查看数据库中某个字段都存在哪
些值 
#  查看十大流通股东中都有哪些类别 
q = query( 
    finance.STK_SHAREHOLDER_FLOATING_TOP10.shareholder_class_id.distinct(),  #提取ID 不同的数据 
    finance.STK_SHAREHOLDER_FLOATING_TOP10.shareholder_class 
         ).order_by(finance.STK_SHAREHOLDER_FLOATING_TOP10.change_reason_id)   
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
 
 
 
（4）与或非 
与 "&" (在键盘数字7 上） 
或 "|" (在键盘回车和后退之间的斜杠上) 
非 "~" (在键盘tab 和esc 之间的点上) 反向查询符号 
q=query( 
        # 市值数据.股票代码valuation.code  
        # 市值数据.总市值,valuation.market_cap  
        # 利润数据.净利润,income.net_profit  
        # 筛选 总市值大于500 并且 净利润不大于0 或者 股票代码属'000001.XSHE','600000.XSHG'中 
        ).filter((valuation.market_cap > 500) 
                 &~ (income.net_profit > 0)  #要用括号把每个条件框起来 
                 |(valuation.code.in_(['000001.XSHE','600000.XSHG']))) 
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
 
or_的用法 
from sqlalchemy.sql.expression import or_ 
#筛选circulating_market_cap<7000 或volume<80000 
q = query( 
    finance.STK_EXCHANGE_TRADE_INFO 
         ).filter( 
                or_(finance.STK_EXCHANGE_TRADE_INFO. circulating_market_cap<7000, 
                    finance.STK_EXCHANGE_TRADE_INFO.volume<80000) 


=== 第 12 页 ===
                ) 
 
df = finance.run_offset_query(q) 
df 
 
（5）运算和命名(label) 
#label 的作用是命名获得数据的标签,一般用于直接运算后的重命名 
#尽量命名为英文 
q = query(indicator.code, 
         (income.total_operating_revenue - income.total_operating_cost).label('my_operating_profit') 
         ).filter(indicator.code=='600507.XSHG') 
get_fundamentals(q) 
 
code 
my_operating_profit 
0 
600507.XSHG 
143977984.0 
 
 
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
    finance.FINANCE_INCOME_STATEMENT 
).filter( 
    finance.FINANCE_INCOME_STATEMENT.code.in_(['000001.XSHE']), 
    finance.FINANCE_INCOME_STATEMENT.end_date.ilike('_____12-31') 
) 
df = finance.run_offset_query(q) 


=== 第 13 页 ===
df 
 #ilike，查询2019 年北京各季度的农林牧渔业总产值表 
#查找【宏观数据补充文档】 
#分地区农林牧渔业总产值表（季度累计）的表名为 
#【MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER】 
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER  
        ).filter( 
    #设定查询的地区名称为【北京市】 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER.area_name.in_(['北京市']), 
    #设定查询时间为2019 年 
    #使用ilike 模糊查询 
    #_ 下划线通配符:表示只能匹配单个字符,不能多也不能少,就是一个字符. 
    macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER.stat_quarter.ilike('2019___') 
).order_by(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER.stat_quarter.asc()) 
 
df = macro.run_offset_query(q) 
#输出结果 
print(df) 
     id stat_quarter area_code area_name   total  farming  forestry  \ 
0  2355      2019-03    110000       北京市   38.43    10.95     13.42    
1  2357      2019-06    110000       北京市  120.33    35.11     56.29    
2  2359      2019-09    110000       北京市  190.71    72.36     73.82    
3  2356      2019-12    110000       北京市  281.70   102.33    115.63    
 
   animal_husbandry  fishery   
0             12.80     0.29   
1             24.17     1.55   
2             36.36     2.90   
3             49.32     5.28   
 
 like 
#查询exchang_nameba 包含上海的行 
q = query(finance.STK_EXCHANGE_TRADE_INFO 
         ).filter(finance.STK_EXCHANGE_TRADE_INFO.exchange_name.like('%%上海%%')) 
df = finance.run_ offset_query(q) 
df[:5] 
 
id 
exchange_code 
exchange_name 
date 
total_market_cap 
circulating_market_cap volume
 
money 
deal_number 
pe_average turnover_ratio 


=== 第 14 页 ===
0 
1 
322002 
上海A 股 2005-01-04 25228.240618 
6941.067590 
80648.3466 43.888276
 
42.2473 
23.817 
0.6368 
1 
2 
322003 
上海B 股 2005-01-04 298.830614 298.830614 1019.3588 0.311245 
0.4442 
20.065
 
0.1018 
2 
3 
322001 
上海市场 
2005-01-04 25527.071233 
7239.898204 
81667.7054 44.199521
 
42.6915 
23.768 
0.5976 
3 
6 
322002 
上海A 股 2005-01-05 25408.493484 
7022.186703 
85238.5339 48.680153
 
52.7249 
23.978 
0.6731 
4 
7 
322003 
上海B 股 2005-01-05 306.795402 306.795402 1597.9846 0.500740 
0.6206 
20.629
 
0.1595 
 
#设置exchange_code 结尾是002 的 
q = query(finance.STK_EXCHANGE_TRADE_INFO 
         ).filter(finance.STK_EXCHANGE_TRADE_INFO.exchange_code.like('%%002')) 
df = finance.run_ offset_query(q) 
df[:5] 
 
id 
exchange_code 
exchange_name 
date 
total_market_cap 
circulating_market_cap volume
 
money 
deal_number 
pe_average turnover_ratio 
0 
1 
322002 
上海A 股 2005-01-04 25228.240618 
6941.067590 
80648.3466 43.888276
 
42.2473 
23.817 
0.6368 
1 
6 
322002 
上海A 股 2005-01-05 25408.493484 
7022.186703 
85238.5339 48.680153
 
52.7249 
23.978 
0.6731 
2 
11 
322002 
上海A 股 2005-01-06 25157.357575 
6967.940387 
78069.6818 43.413997
 
48.8350 
23.733 
0.6159 
3 
16 
322002 
上海A 股 2005-01-07 25266.082988 
6987.978945 
87711.4360 49.794987
 
56.1537 
23.834 
0.6920 
4 
21 
322002 
上海A 股 2005-01-10 25421.051133 
7050.466460 
71465.5220 40.869440
 
42.8602 
23.986 
0.5638 
 
 
 
 
（7）简化计算的方法(sqlalchemy.sql.func)  
关于query 的可导入函数,可以使用以下方法查看,配合官网文档使用: 
import sqlalchemy 
dir(sqlalchemy.sql.expression) 


=== 第 15 页 ===
 
from sqlalchemy.sql import func 
 
date= '2021-06-01' 
stocks = get_index_stocks('000300.XSHG' , date= date ) 
q = query(valuation.day, 
          func.sum(valuation.capitalization).label('capitalization'),  # 总股本 , 
          func.sum(valuation.circulating_cap).label('circulating_cap'),  # A 股流通股本  
          func.sum(valuation.market_cap).label('market_cap'),  # 总市值  
          func.sum(valuation.circulating_market_cap).label('circulating_market_cap'),   #流通市值,  
          (func.count()/func.sum(1/valuation.turnover_ratio)).label('avg_turnover_ratio'),  #直接sql 求平均 , 也可以使用成交量/流通股
本计算 
         ).filter( 
                valuation.code.in_(stocks)   #设置股票池,注释即为全市场 
                 ) 
df = get_fundamentals(q, date) 
df 
 
#提取年月日 
from sqlalchemy import func 
q  = query( 
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
 
 
（8）run_offset_query 批量查询数据库 


=== 第 16 页 ===
 因为run_query 有单次调取finance,opt,macro 等表最大返回5000 条的限制(主要是为了提
速,get_fundamentals 的限制为10000 条) 
 所以当获取的数据超过这个限制时,可以用run_offset_query 这个新接口提取数据。此接口利用
MySql 的offset 方法循环获取数据，便于提取超过5000 条的数据集 
 因为随着offset 值的增大，查询性能是递减的 ,因此此方法仍然设置了查询上限, 最多返回20
万条数据，如查询超过此上限返回数据可能不完整，请注意控制查询范围，可利用数据的日期,标的
代码等字段限制查询范围, 分批查询 
 
from jqdatasdk import * 
from sqlalchemy.sql import func 
import pandas as pd 
import math 
 
#直接使用run_offset_query 提取超过5000 条的数据 
q = query(finance.CCTV_NEWS 
 
).filter(finance.CCTV_NEWS.day<'2012-01-01' 
       
 
 ).order_by( 
                    finance.CCTV_NEWS.day  #可以先按照一定规律排序 
                  
 
) 
df=finance.run_offset_query(q) 
 
# run_offset_query 利用MySql 的offset 方法循环获取数据的方法 
sum_count = finance.run_query( 
    query(func.count('*') 
         ).filter( 
        finance.CCTV_NEWS.day<'2012-01-01') 
                ).iloc[0,0]  #先查询总共有多少条数据 
 
print ('总共有{}条数据,需要获取{}次'.format(sum_count,int(math.ceil(sum_count/5000.0)))) 
 
l = [] 
for i in range(0,sum_count,5000): #以5000 为步长循环offset 的参数 
    q = query(finance.CCTV_NEWS 
             ).filter(finance.CCTV_NEWS.day<'2012-01-01' 
                    ).order_by( 
                                finance.CCTV_NEWS.day  #可以先按照一定规律排序 
                              ).offset(i)   #自第i 条数据之后进行获取 
     
    df=finance.run_query(q) 
    l.append(df) 
     


=== 第 17 页 ===
df = pd.concat(l).reset_index()  #数据拼接 
#print(df.shape) 
df.tail() 
 
index 
id 
day 
title 
content 
14904 
4904 
14715 
2011-12-31 国内联播快讯 
“十二五”期间工业领域重点行业淘汰落后产能目标任务日前
下达，与“十一五”相比，新增了铜冶... 
14905 
4905 
14702 
2011-12-31 胡锦涛主席发表2012 年新年贺词 2012 年新年来临之际，国家主席胡锦涛通过中国国
际广播电台、中央人民广播电台和中央电视台... 
14906 
4906 
14706 
2011-12-31 胡锦涛签署第五十二号、五十三号主席令 
本台消息，国家主席胡锦涛31 号在北
京签署了第五十二号和第五十三号主席令。\n  第五... 
14907 
4907 
14704 
2011-12-31 胡锦涛致电祝贺金正恩担任朝鲜人民军最高司令官 
本台消息，12 月31 日，中
华人民共和国中央军事委员会主席胡锦涛致电祝贺金正恩担任朝鲜... 
14908 
4908 
14717 
2011-12-31 金正恩成为朝鲜人民军最高司令官 据朝中社今天报道，朝鲜劳动党中央政治局会议30
号在平壤召开会议宣布，根据已故最高领导人金... 
 


=== 第 18 页 ===
财务数据表（get_fundamentals） 
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
indicator 财务指标数据 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
eps 
每股收益EPS(元) 
adjusted_profit 
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
goods_sale_and_service_to_revenue 
销售商品提供劳务收到的现金/营业收入(%) 
ocf_to_revenue 
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
cash flow 现金流量表 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
goods_sale_and_service_render_cash 
销售商品、提供劳务收到的现金(元) 
net_deposit_increase 
客户存款和同业存放款项净增加额(元) 
net_borrowing_from_central_bank 
向中央银行借款净增加额(元) 
net_borrowing_from_finance_co 
向其他金融机构拆入资金净增加额(元) 
net_original_insurance_cash 
收到原保险合同保费取得的现金(元) 
net_cash_received_from_reinsurance_busines
s 
收到再保险业务现金净额(元) 
net_insurer_deposit_investment 
保户储金及投资款净增加额(元) 
net_deal_trading_assets 
处置交易性金融资产净增加额(元) 
interest_and_commission_cashin 
收取利息、手续费及佣金的现金(元) 
net_increase_in_placements 
拆入资金净增加额(元) 
net_buyback 
回购业务资金净增加额(元) 
tax_levy_refund 
收到的税费返还(元) 
other_cashin_related_operate 
收到其他与经营活动有关的现金(元) 
subtotal_operate_cash_inflow 
经营活动现金流入小计(元) 
goods_and_services_cash_paid 
购买商品、接受劳务支付的现金(元) 


=== 第 20 页 ===
net_loan_and_advance_increase 
客户贷款及垫款净增加额(元) 
net_deposit_in_cb_and_ib 
存放中央银行和同业款项净增加额(元) 
original_compensation_paid 
支付原保险合同赔付款项的现金(元) 
handling_charges_and_commission 
支付利息、手续费及佣金的现金(元) 
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
取得子公司及其他营业单位支付的现金净额(元) 
other_cash_to_invest_act 
支付其他与投资活动有关的现金(元) 
subtotal_invest_cash_outflow 
投资活动现金流出小计(元) 
net_invest_cash_flow 
投资活动产生的现金流量净额(元) 
cash_from_invest 
吸收投资收到的现金(元) 
cash_from_mino_s_invest_sub 
子公司吸收少数股东投资收到的现金(元) 
cash_from_borrowing 
取得借款收到的现金(元) 
cash_from_bonds_issue 
发行债券收到的现金(元) 
other_finance_act_cash 
收到其他与筹资活动有关的现金(元) 
subtotal_finance_cash_inflow 
筹资活动现金流入小计(元) 
borrowing_repayment 
偿还债务支付的现金(元) 
dividend_interest_payment 
分配股利、利润或偿付利息支付的现金(元) 
proceeds_from_sub_to_mino_s 
子公司支付给少数股东的股利、利润(元) 
other_finance_act_payment 
支付其他与筹资活动有关的现金(元) 
subtotal_finance_cash_outflow 
筹资活动现金流出小计(元) 
net_finance_cash_flow 
筹资活动产生的现金流量净额(元) 
exchange_rate_change_effect 
汇率变动对现金及现金等价物的影响 
cash_equivalent_increase 
现金及现金等价物净增加额 
cash_equivalents_at_beginning 
期初现金及现金等价物余额(元) 
cash_and_equivalents_at_end 
期末现金及现金等价物余额(元) 


=== 第 21 页 ===
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
commission_expense 
手续费及佣金支出(元) 
refunded_premiums 
退保金(元) 
net_pay_insurance_claims 
赔付支出净额(元) 
withdraw_insurance_contract_reserve 
提取保险合同准备金净额(元) 
policy_dividend_payout 
保单红利支出(元) 
reinsurance_cost 
分保费用(元) 
operating_tax_surcharges 
营业税金及附加(元) 
sale_expense 
销售费用(元) 
administration_expense 
管理费用(元) 
financial_expense 
财务费用(元) 
asset_impairment_loss 
资产减值损失(元) 
fair_value_variable_income 
公允价值变动收益(元) 
investment_income 
投资收益(元) 
invest_income_associates 
对联营企业和合营企业的投资收益(元) 
exchange_income 
汇兑收益(元) 
operating_profit 
营业利润(元) 
non_operating_revenue 
营业外收入(元) 
non_operating_expense 
营业外支出(元) 
disposal_loss_non_current_liability 
非流动资产处置净损失(元) 
total_profit 
利润总额(元) 
income_tax_expense 
所得税费用(元) 
net_profit 
净利润(元) 
np_parent_company_owners 
归属于母公司股东的净利润(元) 
minority_profit 
少数股东损益(元) 
basic_eps 
基本每股收益(元) 


=== 第 22 页 ===
diluted_eps 
稀释每股收益(元) 
other_composite_income 
其他综合收益(元) 
total_composite_income 
综合收益总额(元) 
ci_parent_company_owners 
归属于母公司所有者的综合收益总额(元) 
ci_minority_owners 
归属于少数股东的综合收益总额(元) 
balance 资产负债表 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
cash_equivalents 
货币资金(元) 
settlement_provi 
结算备付金(元) 
lend_capital 
拆出资金(元) 
trading_assets 
交易性金融资产(元) 
bill_receivable 
应收票据(元) 
account_receivable 
应收账款(元) 
advance_payment 
预付款项(元) 
insurance_receivables 
应收保费(元) 
reinsurance_receivables 
应收分保账款(元) 
reinsurance_contract_reserves_receivable 
应收分保合同准备金(元) 
interest_receivable 
应收利息(元) 
dividend_receivable 
应收股利(元) 
other_receivable 
其他应收款(元) 
bought_sellback_assets 
买入返售金融资产(元) 
inventories 
存货(元) 
non_current_asset_in_one_year 
一年内到期的非流动资产(元) 
other_current_assets 
其他流动资产(元) 
total_current_assets 
流动资产合计(元) 
loan_and_advance 
发放委托贷款及垫款(元) 
hold_for_sale_assets 
可供出售金融资产(元) 
hold_to_maturity_investments 
持有至到期投资(元) 
longterm_receivable_account 
长期应收款(元) 
longterm_equity_invest 
长期股权投资(元) 
investment_property 
投资性房地产(元) 
fixed_assets 
固定资产(元) 
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
shortterm_loan 
短期借款(元) 
borrowing_from_centralbank 
向中央银行借款(元) 
deposit_in_interbank 
吸收存款及同业存放(元) 
borrowing_capital 
拆入资金(元) 
trading_liability 
交易性金融负债(元) 
notes_payable 
应付票据(元) 
accounts_payable 
应付账款(元) 
advance_peceipts 
预收款项(元) 
sold_buyback_secu_proceeds 
卖出回购金融资产款(元) 
commission_payable 
应付手续费及佣金(元) 
salaries_payable 
应付职工薪酬(元) 
taxs_payable 
应交税费(元) 
interest_payable 
应付利息(元) 
dividend_payable 
应付股利(元) 
other_payable 
其他应付款(元) 
reinsurance_payables 
应付分保账款(元) 
insurance_contract_reserves 
保险合同准备金(元) 
proxy_secu_proceeds 
代理买卖证券款(元) 
receivings_from_vicariously_sold_securities 
代理承销证券款(元) 
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
专项储备(元) 
surplus_reserve_fund 
盈余公积金(元) 
ordinary_risk_reserve_fund 
一般风险准备(元) 
retained_profit 
未分配利润(元) 
foreign_currency_report_conv_diff 
外币报表折算差额(元) 
equities_parent_company_owners 
归属于母公司股东权益合计(元) 
minority_interests 
少数股东权益(元) 
total_owner_equities 
股东权益合计(元) 
total_sheet_owner_equities 
负债和股东权益合计 
bank indicator 银行业 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
total_loan 
贷款总额 
total_deposit 
存款总额 
interest_earning_assets 
生息资产 
non_interest_earning_assets 
非生息资产 
interest_earning_assets_yield 
生息资产收益率 
interest_bearing_liabilities 
计息负债 
non_interest_bearing_liabilities 
非计息负债 
interest_bearing_liabilities_interest_rate 
计息负债成本率 
non_interest_income 
非利息收入 
non_interest_income_ratio 
非利息收入占比 
net_interest_margin 
净息差 
net_profit_margin 
净利差 
core_level_capital 
核心一级资本(2013) 
net_core_level_capital 
核心一级资本净额(2013) 
core_level_capital_adequacy_ratio 
核心一级资本充足率(2013) 
net_level_1_capital 
一级资本净额(2013) 
level_1_capital_adequacy_ratio 
一级资本充足率(2013) 
net_capital 
资本净额(2013) 
capital_adequacy_ratio 
资本充足率（2013） 
weighted_risky_asset 
风险加权资产合计（2013） 


=== 第 25 页 ===
deposit_loan_ratio 
存贷款比例 
short_term_asset_liquidity_ratio_CNY 
短期资产流动性比例（人民币） 
short_term_asset_liquidity_ratio_FC 
短期资产流动性比例（外币） 
Nonperforming_loan_rate 
不良贷款率 
single_largest_customer_loan_ratio 
单一最大客户贷款比例 
top_ten_customer_loan_ratio 
最大十家客户贷款比例 
bad_debts_reserve 
贷款呆账准备金 
non_performing_loan_provision_coverage 
不良贷款拨备覆盖率 
cost_to_income_ratio 
成本收入比 
former_core_capital 
核心资本 (旧) 
former_net_core_capital 
核心资本净额（旧） 
former_net_core_capital_adequacy_ratio 
核心资本充足率 (旧) 
former_net_capital 
资本净额 (旧) 
former_capital_adequacy_ratio 
资本充足率 (旧) 
former_weighted_risky_asset 
加权风险资产净额（旧） 
银行贷款的五级分类指标 
 
normal_amount 
正常-金额 
normal_amount_ratio 
正常金额占比 
concerned_amount 
关注-金额 
concerned_amount_ratio 
关注金额占比 
secondary_amount 
次级-金额 
secondary_amount_ratio 
次级金额占比 
suspicious_amount 
可疑-金额 
suspicious_amount_ratio 
可疑金额占比 
loss_amount 
损失-金额 
loss_amount_ratio 
损失金额占比 
平均贷款利率 
 
short_term_loan_average_balance 
短期贷款-平均余额 
short_term_loan_annualized_average_interest_rate 
短期贷款-年平均利率 
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
security_indicator 券商 
列名 
列的含义 
code 
股票代码 


=== 第 26 页 ===
pubDate 
日期 
statDate 
日期 
net_capital 
净资本 
net_assets 
净资产 
net_capital_to_reserve 
净资本/各项风险准备之和 
net_capital_to_net_asset 
净资本/净资产 
net_capital_to_debt 
净资本/负债 
net_asset_to_debt 
净资产/负债 
net_capital_to_sales_department_number 
净资本/营业部家数 
own_stock_to_net_capital 
自营股票规模/净资本 
own_security_to_net_capital 
证券自营业务规模/净资本 
operational_risk_reserve 
营运风险堆备 
broker_risk_reserve 
经纪业务风险堆备 
own_security_risk_reserve 
证券自营业务风险准备 
security_underwriting_reserve 
证券承消业务风险准备 
asset_management_reserve 
证券资产菅理业务风险准备 
own_equity_derivatives_to_net_capital 
自营权益类证券及证券衍生品/净资本 
own_fixed_income_to_net_capital 
自营固定收益类证券/净资本 
margin_trading_reserve 
融资融券业务风险资本准备 
branch_risk_reserve 
分支机构风险资本堆备 
insurance indicator 保险 
列名 
列的含义 
code 
股票代码 
pubDate 
日期 
statDate 
日期 
investment_assets 
投资资产 
total_investment_rate_of_return 
总投资收益率 
net_investment_rate_of_return 
净投资收益率 
earned_premium 
己赚保费 
earned_premium_growth_rate 
己赚保费增长率 
payoff_cost 
赔付支出 
compensation_rate 
退保率(寿险业务) 
not_expired_duty_reserve 
未到期责任准备金（产险业务） 
outstanding_claims_reserve 
未决赔款准备金（产险业务） 
comprehensive_cost_ratio 
综台成本率（产险业务） 
comprehensive_compensation_rate 综台赔付率（产险业务） 
solvency_adequacy_ratio 
偿付能力充足率 
actual_capital 
实际资本 


=== 第 27 页 ===
minimum_capital 
最低资本 
 
finance 库 
中文含义 
表名 
沪深市场每日成交概况 
STK_EXCHANGE_TRADE_INFO 
申万一级行业指数日行情数据 
SW1_DAILY_PRICE 
市场通交易日历 
STK_EXCHANGE_LINK_CALENDAR 
市场通AH 股价格对比 
STK_AH_PRICE_COMP 
市场通合格证券变动记录 
STK_EL_CONST_CHANGE 
沪深港通持股数据 
STK_HK_HOLD_INFO 
市场通十大成交活跃股 
STK_EL_TOP_ACTIVATE 
市场通成交与额度信息 
STK_ML_QUOTA 
市场通汇率 
STK_EXCHANGE_LINK_RATE 
公司状态变动 
STK_STATUS_CHANGE 
上市公司基本信息 
STK_COMPANY_INFO 
上市信息 
STK_LIST 
简称变更情况 
STK_NAME_HISTORY 
员工情况 
STK_EMPLOYEE_INFO 
公司管理人员任职情况 
STK_MANAGEMENT_INFO 
十大股东 
STK_SHAREHOLDER_TOP10 
十大流通股东 
STK_SHAREHOLDER_FLOATING_TOP10 
股东股份质押 
STK_SHARES_PLEDGE 
股东股份冻结 
STK_SHARES_FROZEN 
股东股份冻结 
 
股东户数 
STK_HOLDER_NUM 
大股东增减持 
STK_SHAREHOLDERS_SHARE_CHANGE 
上市公司股本变动 
STK_CAPITAL_CHANGE 
受限股份上市公告日期 
STK_LIMITED_SHARES_LIST 
受限股份实际解禁日期 
STK_LIMITED_SHARES_UNLIMIT 
上市公司分红送股 (除权除息)数据 
STK_XR_XD 
基金主体信息 
FUND_MAIN_INFO 
基金持股信息 
FUND_PORTFOLIO_STOCK 
基金持有的债券信息 
FUND_PORTFOLIO_BOND 
基金资产组合概况 
FUND_PORTFOLIO 
基金财务指标 
FUND_FIN_INDICATOR 
基金分红信息 
FUND_DIVIDEND 
场内基金份额数据 
FUND_SHARE_DAILY 
货币基金收益日报信息 
FUND_MF_DAILY_PROFIT 
基金净值信息 
FUND_NET_VALUE 
期货龙虎榜(会员持仓) 
FUT_MEMBER_POSITION_RANK 
期货仓单数据 
FUT_WAREHOUSE_RECEIPT 
外盘日行情数据 
FUT_GLOBAL_DAILY 


=== 第 28 页 ===
期权合约资料 
OPT_CONTRACT_INFO 
期权日行情(查表) 
OPT_DAILY_PRICE 
期权风险指标 
OPT_RISK_INDICATOR 
期权交易和持仓排名统计 
OPT_TRADE_RANK_STK 
期权行权交收信息 
OPT_EXERCISE_INFO 
期权合约调整记录 
OPT_ADJUSTMENT 
期权每日盘前静态文件 
OPT_DAILY_PREOPEN 
舆情数据 
CCTV_NEWS 
 
bond 库 
中文含义 
表名 
债券基本信息 
BOND_BASIC_INFO 
债券票面利率 
BOND_COUPON 
债券付息事件 
BOND_INTEREST_PAYMENT 
国债逆回购日行情数据 
REPO_DAILY_PRICE 
可转债基本资料 
CONBOND_BASIC_INFO 
可转债转股价格调整 
CONBOND_CONVERT_PRICE_ADJUST 
可转债每日转股统计 
CONBOND_DAILY_CONVERT 
可转债日行情 (查表) 
CONBOND_DAILY_PRICE 
 
macro 库 
分类 
表名 
农业 
分地区农林牧渔业总产值表(季度累计)：
MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER 
分地区农林牧渔业总产值表(年度)：
MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR 
全国农产品生产价格指数表(季度)：MAC_INDUSTRY_AGR_PRODUCT_IDX_QUARTER 
国内贸易 
社会消费品销售总额（月度）：MAC_SALE_RETAIL_MONTH 
限额以上零售分类表（月度）： MAC_SALE_SCALE_RETAIL_MONTH 
分地区消费品零售总额（年度）：MAC_AREA_RETAIL_SALE 
亿元以上商品交易市场基本情况（年度）：MAC_SALE_MARKET 
分地区亿元以上商品交易市场基本情况（年度）：MAC_AREA_SALE_MARKET 
就业与工
资 
分地区城镇登记失业率（年度）：MAC_AREA_UNEMPLOY 
就业情况基本表(年度)：MAC_EMPLOY_YEAR 
分地区城镇单位就业人员情况表(年度)：MAC_AREA_WAGEIDX_YEAR 
分地区分行业城镇单位就业人员工资情况表(年度)：


=== 第 29 页 ===
MAC_AREA_INDUSTRY_WAGE_YEAR 
分行业城镇单位就业人员工资情况表(年度)：MAC_INDUSTRY_WAGE_YEAR 
分地区按注册类型分城镇单位就业人员工资情况表(年度)：
MAC_AREA_REGISTERED_WAGE_YEAR 
分地区按行业分城镇单位就业人员情况表（年度）：
MAC_AREA_INDUSTRY_EMPLOY_YEAR 
资源环境 
各地区森林资源情况表（年度）：MAC_RESOURCES_AREA_FOREST 
生态环境情况信息表（年度）：MAC_RESOURCES_ECOLOGICAL_ENVIRONMENT 
水资源情况表（年度）：MAC_RESOURCES_AREA_WATER_RESOURCES 
全国水资源量年度信息表（年度）：MAC_RESOURCES_WATER_RESOURCES_YEAR 
各地区供水用水情况表（年度）：MAC_RESOURCES_AREA_WATER_SUPPLY_USE 
供水用水情况表（年度）：MAC_RESOURCES_WATER_SUPPLY_USE_YEAR 
水环境情况信息表（年度）：MAC_RESOURCES_WATER_ENVIRONMENT 
各地区废气排放及处理情况表（年度）：
MAC_RESOURCES_AREA_WASTE_GAS_EMISSION 
自然灾害情况信息表（年度）：MAC_RESOURCES_NATURAL_DISASTER 
环境污染治理投资情况信息表（年度）：
MAC_RESOURCES_ENVIRONMENT_TREAT_INVEST 
房地产行
业 
房地产开发投资情况表(月度累计)：MAC_INDUSTRY_ESTATE_INVEST_MONTH 
分地区房地产开发投资情况表(月度累计)：
MAC_INDUSTRY_AREA_ESTATE_INVEST_MONTH 
房地产开发投资资金来源情况表(月度累计)：
MAC_INDUSTRY_ESTATE_FUND_SOURCE_MONTH 
各地区房地产开发规模与开、竣工面积增长情况表(月度累计)：
MAC_INDUSTRY_AREA_ESTATE_BUILD_MONTH 
70 个大中城市房屋销售价格指数(月度)：
MAC_INDUSTRY_ESTATE_70CITY_INDEX_MONTH 
金融业 
人民币外汇牌价(日级)：MAC_RMB_EXCHANGE_RATE 
银行间拆借利率表（日级）：MAC_LEND_RATE 
金融机构人民币信贷资金平衡表（年度）：MAC_CREDIT_BALANCE_YEAR 
货币供应量(月度)：MAC_MONEY_SUPPLY_MONTH 
货币供应量(年度)：MAC_MONEY_SUPPLY_YEAR 
货币当局资产负债表（年度）：MAC_CURRENCY_STATE_YEAR 
其他存款性公司资产负债表（年度）：MAC_OTHER_DEPOSIT 
社会融资规模及构成（年度）：MAC_SOCIAL_SCALE_FINANCE 
证券市场基本情况（年度）：MAC_STK_MARKET 
黄金和外汇储备（月度）：MAC_GOLD_FOREIGN_RESERVE 
股票发行量和筹资额（年度）：MAC_STK_ISSUE 
股票市场统计表（年度）：MAC_STK_TRADE 


=== 第 30 页 ===
财政政策 
国家财政收支总额及增长速度表（年度）：MAC_FISCAL_TOTAL_YEAR 
中央财政与地方财政收支及比重表（年度）：MAC_FISCAL_BALANCE_YEAR 
中央和地方财政主要收入项目情况表(年度)：MAC_FISCAL_CENTRAL_REVENUE_YEAR 
中央和地方财政主要支出项目情况表(年度)：MAC_FISCAL_CENTRAL_EXPENSE_YEAR 
各项税收表（年度）：MAC_FISCAL_TAX_YEAR 
预算外资金分项目收支表（年度）：MAC_FISCAL_EXTRA_REVENUE_EXPENSE_YEAR 
中央财政与地方财政预算外收支表（年度）：MAC_FISCAL_EXTRAL_BALANCE_YEAR 
外债余额表（年度）：MAC_FISCAL_EXTERNAL_DEBT_YEAR 
外债风险指标表（年度）：MAC_FISCAL_RISK_INDICATOR_YEAR 
各地区财政收入表（年度）：MAC_AREA_FISCAL_REVENUE_YEAR 
各地区财政支出表（年度）：MAC_AREA_FISCAL_EXPENSE_YEAR 
固定资产
投资 
固定资产投资情况（月度）：MAC_FIXED_INVESTMENT 
分地区固定资产投资情况（月度）：MAC_AREA_FIXED_INVESTMENT 
分行业固定资产投资情况（月度）：MAC_INDUSTRY_FIXED_INVEST 
按注册类型登记分固定资产投资（月度）：MAC_REGISTERED_FIXED_INVESTMENT 
固定资产投资情况表(年度)：MAC_FIXED_INVESTMENT_YEAR 
对外贸易 
货物进出口总额表（年度）：MAC_TRADE_VALUE_YEAR 
海关进出口货物分类金额表（年度）：MAC_TRADE_VALUE_SITC_YEAR 
地区按经营单位所在地分货物进出口总额表（年度）：
MAC_TRADE_VALUE_LOCATION_YEAR 
各地区按境内目的地和货源地分货物进出口总额表（年度）：
MAC_TRADE_VALUE_DESTINATION_YEAR 
利用外资情况表（月度）：MAC_FOREIGN_CAPITAL_MONTH 
利用外资概况表（年度）：MAC_FOREIGN_CAPITAL_YEAR 
按行业分对外直接投资情况表（年度）：MAC_INDUSTRY_OFDI_YEAR 
分国别对外外直接投资情况表（年度）：MAC_NATION_OFDI 
分地区外商投资企业年底注册登记情况表（年度）：MAC_AREA_FOREIGN_REGISTER 
按行业分外商投资企业年底注册登记情况表（年度）：
MAC_INDUSTRY_FOREIGN_REGISTER 
对外经济合作表（年度）：MAC_FOREIGN_COOPERATE_YEAR 
按国别对外经济合作表（年度）：MAC_NATION_COOPERATE_YEAR 
景气指数 
宏观经济景气指数（月度）：MAC_ECONOMIC_BOOM_IDX 
消费者景气指数（月度）：MAC_CONSUMER_BOOM_IDX 
宏观经济景气预警指数（月度）：MAC_BOOM_WARNING_IDX 
企业景气及企业家信心指数（季度）：MAC_ENTERPRISE_BOOM_CONFIDENCE_IDX 
制造业采购经理指数（月度）：MAC_MANUFACTURING_PMI 
非制造业采购经理指数（月度）：MAC_NONMANUFACTURING_PMI 
分地区居民消费价格指数（月度）：MAC_AREA_CPI_MONTH 
全国居民消费价格指数（月度）：MAC_CPI_MONTH 


=== 第 31 页 ===
工业 
全国工业增长速度（月度）：MAC_INDUSTRY_GROWTH 
全国工业分行业增长速度（月度）：MAC_INDUSTRY_CATEGORY_GROWTH 
全国工业企业主要经济指标（月度）：MAC_INDUSTRY_INDICATOR 
保险业 
全国各地区保险业务统计表(年度)：MAC_INSURANCE_AREA_YEAR 
保险公司保费金额表(年度)：MAC_INSURANCE_PREMIUM_YEAR 
保险公司赔款及给付表(年度)：MAC_INSURANCE_PAYMENT_YEAR 
保险公司资产情况（年度）：MAC_INSURANCE_ASSETS_YEAR 
保险公司原保费收入和赔付支出情况（年度）：
MAC_INSURANCE_REVENUE_EXPENSE_YEAR 
国民经济 
全国各地区的行政划分（年度）：MAC_AREA_DIV 
分地区国内生产总值表(季度)：MAC_AREA_GDP_QUARTER 
分地区国内生产总值表(年度)：MAC_AREA_GDP_YEAR 
分地区国内生产总值指数表(上年=100，年度)：MAC_AREA_GDP_YEAR_IDX 
分地区国内生产总值指数表（年度）：MAC_AREA_GDP_YEAR_IDX_1978 
分地区支出法国内生产总值表(年度)：MAC_AREA_GDP_EXPEND_YEAR 
分地区收入法国内生产总值表(年度)：MAC_AREA_GDP_INCOME_YEAR 
国家统计局发布经济信息的日程表（年度）：MAC_STATS_REPORT_CALENDAR 
人民生活 
各地区居民消费水平表(年度)：MAC_AREA_CONSUME_YEAR 
居民人均收入支出表(年度)：MAC_REVENUE_EXPENSE_YEAR 
城乡居民家庭人均收入及恩格尔系数(年度)：MAC_ENGEL_COEFFICIENT_YEAR 
城乡居民人民币储蓄存款表(年度)：MAC_RESIDENT_SAVING_DEPOSIT_YEAR 
分地区城镇居民家庭平均每人全年收入来源表(年度)：
MAC_AREA_URBAN_INCOME_YEAR 
分地区城镇及农村居民家庭平均每人全年消费性支出表(年度)：
MAC_AREA_URBAN_RURAL_EXPENSE_YEAR 
农村居民家庭平均每人纯收入(年度)：MAC_RURAL_NET_INCOME_YEAR 
各地区按来源分农村居民家庭人均纯收入(年度)：
MAC_AREA_RURAL_NET_INCOME_YEAR 
分地区农村居民家庭住房情况表(年度)：MAC_AREA_RURAL_HOUSE_YEAR 
人口信息 
人口基本情况表(年度)：：MAC_POPULATION_YEAR 
各地区人口平均预期寿命表（年度）：MAC_LIFE_EXPECT 
按年龄和性别分人口数表（年度）：MAC_POPULATION_AGE 
各地区户数、人口数、性别比和户规模表（年度）：MAC_AREA_HOUSEHOLD_SIZE 
户口登记状况（年度）：MAC_AREA_HOUSEHOLD_REGISTER 
各地区人口年龄结构和抚养比例表（年度）：MAC_AREA_POP_DEPENDENCY 
各地区按性别和婚姻状况分的人口表（年度）：MAC_AREA_POP_MARITAL 
各地区按性别和受教育程度分人口情况表（年度）：MAC_AREA_POP_EDUCATION 
各地区按性别分的15 岁及以上文盲人口表（年度）：MAC_AREA_POP_ILLITERATE 
各地区按家庭户规模分的户数表（年度）：MAC_AREA_FAMILY_HOUSEHOLD 


=== 第 32 页 ===
育龄妇女分年龄生育状况表（年度）：MAC_POP_FERTILITY_RATE 
人口年龄结构和抚养比例（年度）：MAC_POPULATION_DEPENDENCY 
 
 
 
 
 
 
 
 
 


=== 第 33 页 ===
finance 库 


=== 第 34 页 ===
股票 
沪深市场每日成交概况 
表名：STK_EXCHANGE_TRADE_INFO 
字段名称 
中文名称 
exchange_code 
市场编码 
exchange_name 
市场名称 
date 
交易日期 
total_market_cap 
市价总值 
circulating_market_cap 
流通市值 
volume 
成交量 
money 
成交金额 
deal_number 
成交笔数 
pe_average 
平均市盈率 
turnover_ratio 
换手率 
 
申万一级行业指数日行情数据 
表名：SW1_DAILY_PRICE 
 
字段名称 
中文名称 
date 
交易日 
code 
指数编码 
name 
指数名称 
open 
开盘指数 
high 
最高指数 
low 
最低指数 
close 
收盘指数 
volume 
成交量 
money 
成交额 
change_pct 
涨跌幅 
 
市场通交易日历 
STK_EXCHANGE_LINK_CALENDAR 
 


=== 第 35 页 ===
字段 
名称 
day 
交易日期 
link_id 
市场通编码 
link_name 
市场通名称 
type_id 
交易日类型编码 
type 
交易日类型 
 
市场通AH 股价格对比 
STK_AH_PRICE_COMP 
 
字段 
名称 
类型 
day 
日期 
date 
name 
股票简称 
varchar(32) 
a_code 
a 股代码 
varchar(12) 
h_code 
h 股代码 
varchar(12) 
a_price 
a 股收盘价 
decimal(10,4) 
h_price 
h 股收盘价 
decimal(10,4) 
a_quote_change 
a 股涨跌幅 
decimal(10,4) 
h_quote_change 
h 股涨跌幅 
decimal(10,4) 
h_a_comp 
比价(H/A) 
decimal(10,4) 
 
市场通合格证券变动记录 
STK_EL_CONST_CHANGE 
字段 
名称 
link_id 
交易类型编码 
link_name 
交易类型名称 
code 
证券代码 
name_ch 
中文简称 
name_en 
英文简称 
exchange 
该股票所在的交易所 
change_date 变更日期 
direction 
变更方向 
沪深港通持股数据 


=== 第 36 页 ===
STK_HK_HOLD_INFO 
字段名称 
中文名称 
day 
日期 
link_id 
市场通编码 
link_name 
市场通名称 
code 
股票代码 
name 
股票名称 
share_number 持股数量 
share_ratio 
持股比例 
市场通十大成交活跃股 
STK_EL_TOP_ACTIVATE 
字段 
名称 
link_id 
交易类型编码 
link_name 
交易类型名称 
code 
证券代码 
name_ch 
中文简称 
name_en 
英文简称 
exchange 
该股票所在的交易所 
change_date 变更日期 
direction 
变更方向 
 
市场通成交与额度信息 
STK_ML_QUOTA 
字段 
名称 
day 
交易日期 
link_id 
市场通编码 
link_name 
市场通名称 
currency_id 
货币编码 
currency 
货币名称 
buy_amount 
买入成交额 
buy_volume 
买入成交数 
sell_amount 
卖出成交额 
sell_volume 
卖出成交数 
sum_amount 
累计成交额 
sum_volume 
累计成交数目 
quota 
总额度 


=== 第 37 页 ===
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
foreign_currency 
外币 
refer_bid_rate 
买入参考汇率 
refer_ask_rate 
卖出参考汇率 
settle_bid_rate 
买入结算汇率 
settle_ask_rate 
卖出结算汇率 
 
 
公司状态变动 
STK_STATUS_CHANGE 
字段名称 
中文名称 
company_id 
机构ID 
code 
股票代码 
name 
股票名称 
pub_date 
公告日期 
change_date 
变更日期（实际） 
public_status_id 
上市状态编码 
public_status 
上市状态 
change_reason 
变更原因 
change_type_id 
变更类型编码 
change_type 
变更类型 
comments 
备注 


=== 第 38 页 ===
上市公司 
上市公司基本信息 
STK_COMPANY_INFO 
字段名称 
中文名称 
company_id 
公司ID 
code 
证券代码 
full_name 
公司名称 
short_name 
公司简称 
a_code 
A 股股票代码 
b_code 
B 股股票代码 
h_code 
H 股股票代码 
fullname_en 
英文名称 
shortname_en 
英文简称 
legal_representative 
法人代表 
register_location 
注册地址 
office_address 
办公地址 
zipcode 
邮政编码 
register_capital 
注册资金 
currency_id 
货币编码 
currency 
货币名称 
establish_date 
成立日期 
website 
机构网址 
email 
电子信箱 
contact_number 
联系电话 
fax_number 
联系传真 
main_business 
主营业务 
business_scope 
经营范围 
description 
机构简介 
tax_number 
税务登记号 
license_number 
法人营业执照号 
pub_newspaper 
指定信息披露报刊 
pub_website 
指定信息披露网站 
secretary 
董事会秘书 
secretary_number 
董秘联系电话 
secretary_fax 
董秘联系传真 
secretary_email 
董秘电子邮箱 
security_representative 
证券事务代表 


=== 第 39 页 ===
province_id 
所属省份编码 
province 
所属省份 
city_id 
所属城市编码 
city 
所属城市 
industry_id 
行业编码 
industry_1 
行业一级分类 
industry_2 
行业二级分类 
cpafirm 
会计师事务所 
lawfirm 
律师事务所 
ceo 
总经理 
comments 
备注 
 
上市信息 
STK_LIST 
字段名称 
中文名称 
code 
证券代码 
name 
证券简称 
short_name 
拼音简称 
category 
证券类别 
exchange 
交易所 
start_date 
上市日期 
end_date 
终止上市日期 
company_id 
公司ID 
company_name 
公司名称 
ipo_shares 
初始上市数量 
book_price 
发行价格 
par_value 
面值 
state_id 
上市状态编码 
state 
上市状态 
 
简称变更情况 
STK_NAME_HISTORY 
字段名称 
中文名称 
字段类型 
code 
股票代码 
varchar(12) 
company_id 
公司ID 
int 
new_name 
新股票简称 
varchar(40) 


=== 第 40 页 ===
new_spelling 
新英文简称 
varchar(40) 
org_name 
原证券简称 
varchar(40) 
org_spelling 
原证券英文简称 
varchar(40) 
start_date 
开始日期 
date 
pub_date 
公告日期 
date 
reason 
变更原因 
varchar(255) 
 
员工情况 
STK_EMPLOYEE_INFO 
字段名称 
中文名称 
字段类型 
备注/代码示例： 
company_id 
公司ID 
int 
 
code 
证券代码 
varchar(12) 
'600276.XSHG'，
'000001.XSHE' 
name 
证券名称 
varchar(64) 
 
end_date 
报告期截止日 
date 
统计截止该报告期
的员工信息 
pub_date 
公告日期 
date 
 
employee 
在职员工总数 
int 
人 
retirement 
离退休人员 
int 
人 
graduate_rate 
研究生以上人员比例 
decimal(10,4) 
% 
college_rate 
大学专科以上人员比例 
decimal(10,4) 
% 
middle_rate 
中专及以下人员比例 
decimal(10,4) 
% 
 
公司管理人员任职情况 
STK_MANAGEMENT_INFO 
字段名称 
中文名称 
字段类型 
备注/代码示例： 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 
pub_date 
公告日期 
date 
 
person_id 
个人ID 
int 
 
name 
姓名 
varchar(40) 
 
title_class_id 
职务类别编码 
int 
 
title_class 
职务类别 
varchar(60) 
 
title 
职务名称 
varchar(60) 
 
start_date 
任职日期 
date 
 


=== 第 41 页 ===
leave_date 
离职日期 
date 
 
leave_reason 
离职原因 
varchar(255) 
 
on_job 
是否在职 
char(1) 
0-否，1-是 
gender 
性别 
char(1) 
F-女；M-男 
birth_year 
出生年份 
varchar(8) 
 
highest_degree_id 
最高学历编码 
int 
 
highest_degree 
最高学历 
varchar(60) 
 
title_level_id 
职级编码 
int 
 
titile_level 
职级 
varchar(120) 
职级代表工作的难易程度、责
任轻重以及所需的资格条件相
同或充分相似的职系的集合。
如初级、中级、高级。 
profession_certificate 
专业技术资格 
varchar(120) 
 
profession_certificate 
专业技术资格 
varchar(120) 
 
nationality 
国籍 
varchar(60) 
 
security_career_start_year 
从事证券业开始年份 
varchar(8) 
 
resume 
个人简历 
varchar(3000) 
 
 
十大股东 
STK_SHAREHOLDER_TOP10 
字段名称 
中文名称 
字段类型 
备注/代码示例： 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
在此是指上市公司的名称 
code 
股票代码 
varchar(12) 
 
end_date 
截止日期 
date 
公告中统计的十大股东截止到某一日期
的更新情况。 
pub_date 
公告日期 
date 
公告中会提到十大股东的更新情况。 
change_reason_id 
变动原因编码 
int 
 
change_reason 
变动原因 
varchar(120) 
 
shareholder_rank 
股东名次 
int 
 
shareholder_name 
股东名称 
varchar(200) 
 
shareholder_name_en 
股东名称（英文） 
varchar(200) 
 
shareholder_id 
股东ID 
int 
 
shareholder_class_id 
股东类别编码 
int 
 
shareholder_class 
股东类别 
varchar(150) 
包括:券商、社保基金、证券投资基金、
保险公司、QFII、其它机构、个人等 
share_number 
持股数量 
decimal(10,4) 
股 
share_ratio 
持股比例 
decimal(10,4) 
% 


=== 第 42 页 ===
sharesnature_id 
股份性质编码 
int 
 
sharesnature 
股份性质 
varchar(120) 
包括:国家股、法人股、个人股外资股、
流通A 股、流通B 股、职工股、发起人
股、转配股等 
share_pledge_freeze 
股份质押冻结数量 
decimal(10,4) 
如果股份质押数量和股份冻结数量任意
一个字段有值，则等于后两者之和 
share_pledge 
股份质押数量 
decimal(10,4) 
 
share_freeze 
股份冻结数量 
decimal(10,4) 
 
 
十大流通股东 
STK_SHAREHOLDER_FLOATING_TOP10 
字段名称 
中文名称 
字段类型 
备注/代码示
例： 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 
end_date 
截止日期 
date 
 
pub_date 
公告日期 
date 
 
change_reason_id 
变动原因编码 
int 
 
change_reason 
变动原因 
varchar(120) 
 
shareholder_rank 
股东名次 
int 
 
shareholder_id 
股东ID 
int 
 
shareholder_name 
股东名称 
varchar(200) 
 
shareholder_name_en 
股东名称（英文） 
varchar(150) 
 
shareholder_class_id 
股东类别编码 
int 
 
shareholder_class 
股东类别 
varchar(150) 
 
share_number 
持股数量 
int 
股 
share_ratio 
持股比例 
decimal(10,4) 
% 
sharesnature_id 
股份性质编码 
int 
 
sharesnature 
股份性质 
varchar(120) 
 
 
股东股份质押 
STK_SHARES_PLEDGE 
字段名称 
中文名称 
字段类型 
备注/代码示例： 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 


=== 第 43 页 ===
pub_date 
公告日期 
date 
 
pledgor_id 
出质人ID 
int 
 
pledgor 
出质人 
varchar(100) 
将资产质押出去的人成为出质人 
pledgee 
质权人 
varchar(100) 
 
pledge_item 
质押事项 
varchar(500) 
质押原因，记录借款人、借款金额、
币种等内容 
pledge_nature_id 
质押股份性质编码 
int 
 
pledge_nature 
质押股份性质 
varchar(120) 
 
pledge_number 
质押数量 
int 
股 
pledge_total_ratio 
占总股本比例 
decimal(10,4) 
% 
start_date 
质押起始日 
date 
 
end_date 
质押终止日 
date 
 
unpledged_date 
质押解除日 
date 
 
unpledged_number 
质押解除数量 
int 
 
unpledged _detail 
解除质押说明 
varchar(1000) 
 
is_buy_back 
是否质押式回购交易 
char(1) 
 
 
股东股份冻结 
STK_SHARES_FROZEN 
字段名称 
中文名称 
字段类型 
含义 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
pub_date 
公告日期 
date 
 
code 
股票代码 
varchar(12) 
 
frozen_person_id 
被冻结当事人ID 
int 
 
frozen_person 
被冻结当事人 
varchar(100) 
 
frozen_reason 
冻结事项 
varchar(600) 
 
frozen_share_nature_id 
被冻结股份性质编码 
int 
 
frozen_share_nature 
被冻结股份性质 
varchar(120) 
包括:国家股、法人股、个人股、
外资股、 
流通A 股、流通B 股、职工股、
发起人股、转配股 
frozen_number 
冻结数量 
int 
股 
frozen_total_ratio 
占总股份比例 
decimal(10,4) 
% 
freeze_applicant 
冻结申请人 
varchar(100) 
 
freeze_executor 
冻结执行人 
varchar(100) 
 
start_date 
冻结起始日 
date 
 
end_date 
冻结终止日 
date 
 


=== 第 44 页 ===
unfrozen_date 
解冻日期 
date 
分批解冻的为最近一次解冻日期 
unfrozen_number 
累计解冻数量 
int 
原解冻数量 
unfrozen_detail 
解冻处理说明 
varchar(1000) 
冻结过程及结束后的处理结果 
 
股东户数 
STK_HOLDER_NUM 
字段名称 
中文名称 
字段类型 
备注/代码示
例： 
code 
股票代码 
varchar(12) 
 
pub_date 
公告日期 
date 
 
end_date 
截止日期 
date 
 
share_holders 
股东总户数 
int 
 
a_share_holders 
A 股股东总户数 
int 
 
b_share_holders 
B 股股东总户数 
int 
 
h_share_holders 
H 股股东总户数 
int 
 
 
大股东增减持 
STK_SHAREHOLDERS_SHARE_CHANGE 
字段名称 
中文名称 
字段类型 
备注/代码示例： 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 
pub_date 
公告日期 
date 
 
end_date 
增（减）持截止日 
date 
变动截止日期 
type 
增（减）持类型 
int 
0--增持;1--减持 
shareholder_id 
股东ID 
int 
 
shareholder_name 
股东名称 
varchar(100) 
 
change_number 
变动数量 
int 
股 
change_ratio 
变动数量占总股本比例 
decimal(10,4) 
录入变动数量后，系统自动计
算变动比例， 
持股比例可以用持股数量除以
股本情况表中的总股本 
price_ceiling 
增（减）持价格上限 
varchar(100) 
公告里面一般会给一个增持或
者减持的价格区间，上限就是
增持价格或减持价格的最高
价。如果公告中只披露了平均


=== 第 45 页 ===
价，那price_ceiling 即为成交
均价 
after_change_ratio 
变动后占比 
decimal(10,4) 
%，变动后持股数量占总股本
比例 
 
上市公司股本变动 
STK_CAPITAL_CHANGE 
字段名称 
中文名称 
字段类型 
含义 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 
change_date 
变动日期 
date 
 
pub_date 
公告日期 
date 
 
change_reason_id 
变动原因编码 
int 
 
change_reason 
变动原因 
varchar(120) 
 
share_total 
总股本 
decimal(20,4) 
未流通股份+已流通股份，单位：
万股 
share_non_trade 
未流通股份 
decimal(20,4) 
发起人股份 + 募集法人股份 + 
内部职工股 + 优先股 +转配股+
其他未流通股+配售法人股+已发
行未上市股份 
share_start 
发起人股份 
decimal(20,4) 
国家持股 +国有法人持股+ 境内
法人持股 + 境外法人持股 + 自
然人持股 
share_nation 
国家持股 
decimal(20,4) 
单位:万股 
share_nation_legal 
国有法人持股 
decimal(20,4) 
单位:万股 
share_instate_legal 
境内法人持股 
decimal(20,4) 
单位:万股 
share_outstate_legal 
境外法人持股 
decimal(20,4) 
单位:万股 
share_natural 
自然人持股 
decimal(20,4) 
单位:万股 
share_raised 
募集法人股 
decimal(20,4) 
单位:万股 
share_inside 
内部职工股 
decimal(20,4) 
单位:万股 
share_convert 
转配股 
decimal(20,4) 
单位:万股 
share_perferred 
优先股 
decimal(20,4) 
单位:万股 
share_other_nontrade 
其他未流通股 
decimal(20,4) 
单位:万股 
share_limited 
流通受限股份 
decimal(20,4) 
单位:万股 
share_legal_issue 
配售法人股 
decimal(20,4) 
战略投资配售股份+证券投资基金
配售股份+一般法人配售股份 
share_strategic_investor 
战略投资者持股 
decimal(20,4) 
单位:万股 


=== 第 46 页 ===
share_fund 
证券投资基金持股 
decimal(20,4) 
单位:万股 
share_normal_legal 
一般法人持股 
decimal(20,4) 
单位:万股 
share_other_limited 
其他流通受限股份 
decimal(20,4) 
单位:万股 
share_nation_limited 
国家持股（受限） 
decimal(20,4) 
单位:万股 
share_nation_legal_limited 
国有法人持股（受
限） 
decimal(20,4) 
单位:万股 
other_instate_limited 
其他内资持股（受
限） 
decimal(20,4) 
单位:万股 
legal of 
other_instate_limited 
其他内资持股（受
限）中的境内法人持
股 
decimal(20,4) 
单位:万股 
natural of 
other_instate_limited 
其他内资持股（受
限）中的境内自然人
持股 
decimal(20,4) 
单位:万股 
outstate_limited 
外资持股（受限） 
decimal(20,4) 
单位:万股 
legal of outstate_limited 
外资持股（受限）中
的境外法人持股 
decimal(20,4) 
单位:万股 
natural of outstate_limited 
外资持股（受限）境
外自然人持股 
decimal(20,4) 
单位:万股 
share_trade_total 
已流通股份 
decimal(20,4) 
人民币普通股+ 境内上市外资股
(B 股)+ 境外上市外资股(H 股)+ 
高管股+ 其他流通股 
share_rmb 
人民币普通股 
decimal(20,4) 
单位:万股 
share_b 
境内上市外资股（B
股） 
decimal(20,4) 
单位:万股 
share_b_limited 
限售B 股 
decimal
（20,4） 
单位:万股 
share_h 
境外上市外资股（H
股） 
decimal(20,4) 
单位:万股 
share_h_limited 
限售H 股 
decimal(20,4) 
单位:万股 
share_management 
高管股 
decimal(20,4) 
单位:万股 
share_management_limited 
限售高管股 
decimal(20,4) 
单位:万股 
share_other_trade 
其他流通股 
decimal(20,4) 
单位:万股 
control_shareholder_limited 控股股东、实际控制
人(受限) 
decimal(20,4) 
单位:万股 
core_employee_limited 
核心员工(受限) 
decimal(20,4) 
单位:万股 
individual_fund_limited 
个人或基金(受限) 
decimal(20,4) 
单位:万股 
other_legal_limited 
其他法人(受限) 
decimal(20,4) 
单位:万股 
other_limited 
其他(受限) 
decimal(20,4) 
单位:万股 
 


=== 第 47 页 ===
受限股份上市公告日期 
STK_LIMITED_SHARES_LIST 
字段名称 
中文名称 
字段类型 
含义 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 
pub_date 
公告日期 
date 
上市流通方案公布日期 
shareholder_name 
股东名称 
varchar(100) 
 
expected_unlimited_date 
预计解除限售日期 
date 
 
expected_unlimited_number 预计解除限售数量 
int 
单位：股 
expected_unlimited_ratio 
预计解除限售比例 
decimal(10,4) 
单位：％；预计解除限售数量占总
股本比例 
actual_unlimited_date 
实际解除限售日期 
date 
 
actual_unlimited_number 
实际解除限售数量 
int 
单位：股 
actual_unlimited_ratio 
实际解除限售比例 
decimal(10,4) 
单位：％；实际解除限售数量占总
股本比例 
limited_reason_id 
限售原因编码 
int 
如下 限售原因编码 
limited_reason 
限售原因 
varchar(60) 
用户选择：股改限售；发行限售 
trade_condition 
上市交易条件 
varchar(500) 
股份上市交易的条件限制 
 
受限股份实际解禁日期 
STK_LIMITED_SHARES_UNLIMIT 
字段名称 
中文名称 
字段类型 
含义 
company_id 
公司ID 
int 
 
company_name 
公司名称 
varchar(100) 
 
code 
股票代码 
varchar(12) 
 
pub_date 
公告日期 
date 
 
shareholder_name 
股东名称 
varchar(100) 
 
actual_unlimited_date 
实际解除限售日期 
date 
 
actual_unlimited_number 
实际解除限售数量 
int 
股 
actual_unlimited_ratio 
实际解除限售比例 
decimal(10,4) 
实际解除限售
数量占总股本
比例，单位% 
limited_reason_id 
限售原因编码 
int 
 
limited_reason 
限售原因 
varchar(60) 
 
actual_trade_number 
实际可流通数量 
int 
 
 


=== 第 48 页 ===
上市公司分红送股 (除权除息)数据 
STK_XR_XD 
字段名称 
中文名称 
字段类型 
含义 
code 
股票代码 
varchar(12) 
加后缀（不能为空） 
company_id 
机构ID 
int 
（不能为空） 
company_name 
机构名称 
varchar(100) 
 
report_date 
分红报告期 
date 
（不能为空） 
一般为：一季报:YYYY-03-31; 
中报:YYYY-06-30; 
三季报:YYYY-09-30; 
年报:YYYY-12-31 同时也可能存在其他日期 
bonus_type 
分红类型 
varchar(60) 
201102 新增,类型如下：年度分红 中期分红 
季度分红 特别分红 向公众股东赠送 股改分
红 
board_plan_pub_date 
董事会预案公
告日期 
date 
 
board_plan_bonusnote 
董事会预案分
红说明 
varchar(500) 
每10 股送XX 转增XX 派XX 元 
distributed_share_base
_board 
分配股本基数
（董事会） 
decimal(20,4) 
单位:万股 
shareholders_plan_pub
_date 
股东大会预案
公告日期 
date 
 
shareholders_plan_bon
usnote 
股东大会预案
分红说明 
varchar(200) 
 
distributed_share_base
_shareholders 
分配股本基数
（股东大会） 
decimal(20,4) 
单位:万股 
implementation_pub_d
ate 
实施方案公告
日期 
date 
 
implementation_bonus
note 
实施方案分红
说明 
varchar(200) 
维护规则: 每10 股送XX 转增XX 派XX 元 
或:不分配不转赠 
distributed_share_base
_implement 
分配股本基数
（实施） 
单位:万股 
 
dividend_ratio 
送股比例 
decimal(20,4) 
每10 股送XX 股 
transfer_ratio 
转增比例 
decimal(20,4) 
每10 股转增 XX 股 ； 
bonus_ratio_rmb 
派息比例(人民
币) 
decimal(20,4) 
每10 股派 XX。说明：这里的比例为最新的
分配比例，预案公布的时候，预案的分配基数
在此维护，如果股东大会或实施方案发生变
化，再次进行修改，保证此处为最新的分配基
数 


=== 第 49 页 ===
bonus_ratio_usd 
派息比例（美
元） 
decimal(20,4) 
每10 股派 XX。说明：这里的比例为最新的
分配比例，预案公布的时候，预案的分配基数
在此维护，如果股东大会或实施方案发生变
化，再次进行修改，保证此处为最新的分配基
数 如果这里只告诉了汇率，没有公布具体的
外币派息，则要计算出； 
bonus_ratio_hkd 
派息比例（港
币） 
decimal(20,4) 
每10 股派 XX。说明：这里的比例为最新的
分配比例，预案公布的时候，预案的分配基数
在此维护，如果股东大会或实施方案发生变
化，再次进行修改，保证此处为最新的分配基
数 如果这里只告诉了汇率，没有公布具体的
外币派息，则要计算出； 
at_bonus_ratio_rmb 
税后派息比例
（人民币） 
decimal(20,4) 
 
exchange_rate 
汇率 
 
当日以外币（美元或港币）计价的B 股价格
兑换成人民币的汇率 
dividend_number 
送股数量 
decimal(20,4) 
单位：万股 
transfer_number 
转增数量 
decimal(20,4) 
单位：万股 
bonus_amount_rmb 
派息金额(人民
币) 
decimal(20,4) 
单位：万元 
a_registration_date 
A 股股权登记
日 
date 
 
b_registration_date 
B 股股权登记
日 
date 
B 股股权登记存在最后交易日，除权基准日以
及股权登记日三个日期，由于B 股实行T+3
制度，最后交易日持有的股份需要在3 个交易
日之后确定股东身份，然后在除权基准日进行
除权。 
a_xr_date 
A 股除权日 
date 
 
b_xr_baseday 
B 股除权基准
日 
date 
根据B 股实行T＋3 交收制度,则B 股的“股
权登记日”是“最后交易日”后的第 三个交
易日,直至“股权登记日”这一日为止,B 股投
资者的股权登记才告完成,也 就意味着B 股股
份至股权登记日为止,才真正划入B 股投资者
的名下。 
b_final_trade_date 
B 股最后交易
日 
date 
 
a_bonus_date 
派息日(A) 
date 
 
b_bonus_date 
派息日(B) 
date 
 
dividend_arrival_date 
红股到帐日 
date 
 


=== 第 50 页 ===
a_increment_listing_da
te 
A 股新增股份
上市日 
date 
 
b_increment_listing_da
te 
B 股新增股份
上市日 
date 
 
total_capital_before_tra
nsfer 
送转前总股本 
decimal(20,4) 
单位：万股 
total_capital_after_tran
sfer 
送转后总股本 
decimal(20,4) 
单位：万股 
float_capital_before_tra
nsfer 
送转前流通股
本 
decimal(20,4) 
单位：万股 
float_capital_after_tran
sfer 
送转后流通股
本 
decimal(20,4) 
单位：万股 
note 
备注 
varchar(500) 
 
a_transfer_arrival_date 
A 股转增股份
到帐日 
date 
 
b_transfer_arrival_date 
B 股转增股份
到帐日 
date 
 
b_dividend_arrival_dat
e 
B 股送红股到
帐日 
date 
20080801 新增 
note_of_no_dividend 
有关不分配的
说明 
varchar(1000) 
 
plan_progress_code 
方案进度编码 
int 
 
plan_progress 
方案进度 
varchar(60) 
董事会预案 实施方案 股东大会预案 取消分
红 公司预案 
bonus_cancel_pub_date 取消分红公告
日期 
date 
 
 


=== 第 51 页 ===
基金 
基金主体信息 
FUND_MAIN_INFO 
字段 
名称 
类型 
main_code 
基金主体代码 
varchar(12) 
name 
基金名称 
varchar(100) 
advisor 
基金管理人 
varchar(100) 
trustee 
基金托管人 
varchar(100) 
operate_mode_id 
基金运作方式编
码 
int 
operate_mode 
基金运作方式 
varchar(32) 
underlying_asset_type_id 投资标的类型编
码 
int 
underlying_asset_type 
投资标的类型 
varchar(32) 
start_date 
成立日期 
date 
pub_date 
发行日期 
date 
end_date 
结束日期 
date 
invest_style_id 
投资风格编码 
int 
invest_style 
投资风格 
varchar(32) 
statistics_main_code 
基金统计主代码
（仅多份额基金
存在此字段） 
varchar(32) 
 
基金持股信息 
FUND_PORTFOLIO_STOCK 
字段名称 
中文名称 
字段类型 
code 
基金代码 
varchar(12) 
period_start 
开始日期 
date 
period_end 
报告期 
date 
pub_date 
公告日期 
date 
report_type_id 
报告类型编码 
int 
report_type 
报告类型 
varchar(32) 
rank 
持仓排名 
int 
symbol 
股票代码 
varchar(32) 
name 
股票名称 
varchar(100) 
shares 
持有股票 
decimal(20,4) 


=== 第 52 页 ===
market_cap 
持有股票的市值 
decimal(20,4) 
proportion 
占净值比例 
decimal(10,4) 
 
基金持有的债券信息 
FUND_PORTFOLIO_BOND 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
基金资产组合概况 
FUND_PORTFOLIO 
字段名称 
中文名称 
字段类型 
code 
基金代码 
varchar(12) 
name 
基金名称 
varchar(80) 
period_start 
开始日期 
date 
period_end 
报告期 
date 
pub_date 
公告日期 
date 
report_type_id 
报告类型编码 
int 
report_type 
报告类型 
varchar(32) 
equity_value 
权益类投资金额 
decimal(20,4) 
equity_rate 
权益类投资占比 
decimal(10,4) 
stock_value 
股票投资金额 
decimal(20,4) 
stock_rate 
股票投资占比 
decimal(10,4) 
fixed_income_value 
固定收益投资金额 
decimal(20,4) 
fixed_income_rate 
固定收益投资占比 
decimal(10,4) 
字段名称 
中文名称 
字段类型 
code 
基金代码 
varchar(12) 
period_start 
开始日期 
date 
period_end 
报告期 
date 
pub_date 
公告日期 
date 
report_type_id 
报告类型编码 
int 
report_type 
报告类型 
varchar(32) 
rank 
持仓排名 
int 
symbol 
股票代码 
varchar(32) 
name 
股票名称 
varchar(100) 
shares 
持有股票 
decimal(20,4) 
market_cap 
持有股票的市值 
decimal(20,4) 
proportion 
占净值比例 
decimal(10,4) 


=== 第 53 页 ===
precious_metal_value 贵金属投资金额 
decimal(20,4) 
precious_metal_rate 
贵金属投资占比 
decimal(10,4) 
derivative_value 
金融衍生品投资金额 
decimal(20,4) 
derivative_rate 
金融衍生品投资占比 
decimal(10,4) 
buying_back_value 
买入返售金融资产金额 
decimal(20,4) 
buying_back_rate 
买入返售金融资产占比 
decimal(10,4) 
deposit_value 
银行存款和结算备付金合计 
decimal(20,4) 
deposit_rate 
银行存款和结算备付金合计占比 
decimal(10,4) 
others_value 
其他资产 
decimal(20,4) 
others_rate 
其他资产占比 
decimal(10,4) 
total_asset 
总资产合计 
decimal(20,4) 
 
基金财务指标 
FUND_FIN_INDICATOR 
字段 
名称 
类型 
code 
基金代码 
varchar(12) 
name 
基金名称 
varchar(80) 
period_start 
开始日期 
date 
period_end 
结束日期 
date 
pub_date 
公告日期 
date 
report_type_id 
报告类型编码 
int 
report_type 
报告类型 
varchar(32) 
profit 
本期利润 
 
adjust_profit 
本期利润扣减本期公允价值变动损益后的净额 
 
avg_profit 
加权平均份额本期利润 
 
avg_roe 
加权平均净值利润率 
 
profit_available 
期末可供分配利润 
 
profit_avaialbe_per_share 期末可供分配份额利润 
 
total_tna 
期末基金资产净值 
 
nav 
期末基金份额净值 
 
adjust_nav 
期末还原后基金份额累计净值 
 
nav_growth 
本期净值增长率 
 
acc_nav_growth 
累计净值增长率 
 
adjust_nav_growth 
扣除配售新股基金净值增长率 
 
 
基金分红信息 


=== 第 54 页 ===
FUND_DIVIDEND 
字段 
名称 
类型 
code 
基金代码 
varchar(12) 
name 
基金名称 
varchar(80) 
pub_date 
公布日期 
date 
event_id 
事项类别 
int 
event 
事项名称 
varchar(100) 
distribution_date 
分配收益日 
date 
process_id 
方案进度编码 
int 
process 
方案进度 
varchar(100) 
proportion 
派现比例 
decimal(20,8) 
split_ratio 
分拆（合并、赠送）比例 
decimal(20,8) 
record_date 
权益登记日 
date 
ex_date 
除息日 
date 
fund_paid_date 
基金红利派发日 
date 
redeem_date 
再投资赎回起始日 
date 
dividend_implement_date 分红实施公告日 
dated 
dividend_cancel_date 
取消分红公告日 
date 
otc_ex_date 
场外除息日 
date 
pay_date 
红利派发日 
date 
new_share_code 
新增份额基金代码 
varchar(10) 
new_share_name 
新增份额基金名称 
varchar(100) 
 
场内基金份额数据 
FUND_SHARE_DAILY 
名称 
类型 
描述： 
code 
varchar(12) 
基金代码 
name 
varchar(50） 
基金简称 
exchange_code 
varchar(12) 
交易市场编码 
XSHG-上海证券交易所； 
XSHE-深圳证券交易所 
date 
date 
日期 
shares 
bigint 
基金份额（份） 
 
货币基金收益日报信息 


=== 第 55 页 ===
FUND_MF_DAILY_PROFIT 
字段 
名称 
类型 
code 
基金代码 
varchar(12) 
name 
基金名称 
varchar(80) 
end_date 
收益日期 
date 
weekly_yield 
7 日年化收益率(%) 
decimal(10,4) 
daily_profit 
每万份基金单位当日
收益(元) 
decimal(10,4 
 
基金净值信息 
FUND_NET_VALUE 
字段 
名称 
类型 
注释 
code 
基金代码 
varchar(12) 
 
day 
交易日 
date 
 
net_value 
单位净值 
decimal(20,6) 
基金单位净值=（基金资产总值－基
金负债）÷ 基金总份额 
sum_value 
累计净值 
decimal(20,6) 
累计单位净值＝单位净值＋成立以来
每份累计分红派息的金额 
factor 
复权因子 
decimal(20,6) 
交易日最近一次分红拆分送股的复权
因子 
acc_factor 
累计复权因子 
decimal(20,6) 
基金从上市至今累计分红拆分送股的
复权因子 
refactor_net_value 
累计复权净值 
decimal(20,6) 
复权单位净值＝单计净值＋成立以来
每份累计分红派息的金额（1+涨跌
幅） 
 


=== 第 56 页 ===
期货 
期货龙虎榜(会员持仓) 
FUT_MEMBER_POSITION_RANK 
字段名称 
中文名称 
字段类型 
含义 
day 
交易日 
date 
 
code 
合约编码 
varchar(12) 
同一商品根据交割日的不同对应不同的期货合
约，比如：'CU1807.XSGE' 
exchange 
交易所编码 
varchar(10) 
见下表 
exchange_name 
交易所名称 
varchar(30) 
 
underlying_code 
标的编码 
varchar(10) 
 
underlying_name 
标的名称 
varchar(50) 
 
rank_type_ID 
排名类别编码 
int 
501001-成交量排名, 501002-持买单量排名， 
501003-持卖单量排名 
rank_type 
排名类别 
varchar(50) 
包含:成交量排名，持买单量排名，持卖单量排
名 
rank 
排名 
int 
 
member_name 
会员简称 
varchar(50) 
 
indicator 
统计指标 
int 
统计指标根据排名类别确定，分别代表：成交
量，持买单量，持卖单量。单位：手 
indicator_increase 
统计指标比上
交易日增减 
int 
单位：手 
 
期货仓单数据 
FUT_WAREHOUSE_RECEIPT 
字段名称 
中文名称 
字段类型 
注释 
day 
日期 
date 
 
exchange 
交易所编码 
varchar(10) 
英文编码 
exchange_name 
交易所名称 
varchar(30) 
上海期货交易所 
大连商品交易所 
郑州商商品交易所 
中国金融期货交易所 
underlying_code 
品种编码 
varchar(10) 
 
product_name 
品种名称 
varchar(20) 
 


=== 第 57 页 ===
warehouse_name 
仓库名称 
varchar(20) 
上期所：将地区和仓库数据合并
成一条，仓库名称=“地区”+
“仓库”。 
大商所：仓库名称存在多个不同
的名字的，取第一个字体加粗的
仓库名称。 
郑商所：不区分品牌，对每个仓
库取仓库小计值 
warehouse_receipt_number 
今日期货仓
单 
int 
 
unit 
单位 
varchar(10) 
 
warehouse_receipt_number_increase 比昨日增减 
int 
 
 
外盘日行情数据 
FUT_GLOBAL_DAILY 
字段 
名称 
类型 
非空 
含义 
code 
期货代码 
varchar(64) 
Y 
代码列表详见下方期货代码名称
对照表 
name 
期货名称 
varchar(64) 
 
 
day 
日期 
date 
Y 
 
open 
开盘价 
decimal(20,6) 
 
 
close 
收盘价 
decimal(20,6) 
 
 
low 
最低价 
decimal(20,6) 
 
 
high 
最高价 
decimal(20,6) 
 
 
volume 
成交量 
decimal(20,6) 
 
 
change_pct 
涨跌幅（%） 
decimal(20,4) 
 
（当日收盘价-前收价）/前收价 
amplitude 
振幅（%） 
decimal(20,6) 
 
（当日最高点的价格－当日最低
点的价格）/前收价 
pre_close 
前收价 
decimal(20,6) 
 
 
 


=== 第 58 页 ===
舆情数据 
舆情数据 
CCTV_NEWS 
字段名称 中文名称 字段类型 
非空 描述 
day 
日期 
date 
Y 
 
title 
标题 
varchar(200) 
Y 
 
content 
正文 
varchar(5000)  
 
 


=== 第 59 页 ===
opt 库（期权） 
期权合约资料 
OPT_CONTRACT_INFO 
名称 
类型 
描述： 
代码示例： 
备注 
code 
str 
合约代码 
10001313.XSHG；
CU1901C46000.XSG
E；
SR903C4700.XZCE；
M1707-C-2400.XDCE 
注意：合约代码使用大写字
母 
trading_code 
int 
合约交易代码 
510050C1810M02800 
合约调整会产生新的交易代
码 
name 
str 
合约简称 
50ETF 购10 月2800
豆粕购7 月2400 
合约调整会产生新的合约简
称 
contract_type 
str 
合约类型。CO-认购
期权，PO-认沽期权 
CO 
 
exchange_code 
str 
证券市场编码，
XSHG：上海证券交
易所；XSGE：上海
期货交易所；
XZCE：郑州商品交
易所；XDCE：大连
商品交易所 
XSHG 
 
currency_id 
str 
货币代码CNY-人民
币 
CNY 
 
underlying_sym
bol 
str 
标的代码 
510050.XSHG 
 
underlying_nam
e 
str 
标的简称 
华夏上证50ETF 
 
underlying_exch
ange 
str 
标的交易市场 
XSHG 
 
underlying_type 
str 
标的品种类别。ETF-
交易型开放式指数基
金FUTURE-期货 
ETF 
 
exercise_price 
float 
行权价格 
2.8 
合约调整会产生新的行权价
格 
contract_unit 
int 
合约单位 
10000 
合约调整会产生新的合约单
位 


=== 第 60 页 ===
contract_status 
str 
合约状态：LIST-上
市、DELIST-退市。
SUSPEND-停牌 
DELIST 
新期权上市由交易所公布
LIST：挂牌日期<=当前日期
<=最后交易日DELIST：当
前日期>最后交易日 
list_date 
str 
挂牌日期 
2018/9/25 
 
list_reason 
str 
合约挂牌原因 
 
 
list_price 
decim
al(20,
4) 
开盘参考价 
 
合约挂牌当天交易所会公布 
high_limit 
decim
al(20,
4) 
挂牌涨停价 
 
合约挂牌当天交易所会公布 
low_limit 
decim
al(20,
4) 
挂牌跌停价 
 
合约上市当天交易所会公布 
expire_date 
str 
到期日 
2018/10/24 
 
last_trade_date 
str 
最后交易日 
2018/10/24 
 
exercise_date 
str 
行权日 
2018/10/24 
50ETF，铜期权是欧式期
权，行权日固定。白糖期权
和豆粕期权是美式期权，到
期日之前都可以行权，行权
日不固定，可为空。 
delivery_date 
str 
交收日期 
2018/10/25  
is_adjust 
int 
是否调整 
 
原合约调整为新的合约会发
生合约资料的变化1-是，0-
否 
delist_date 
str 
摘牌日期 
2018/10/24 通联数据和交易所有出入,交
易所公布的是2018/10/25 摘
牌日期=最后交易日T+1 
delist_reason 
str 
合约摘牌原因 
 
 
 
期权日行情(查表) 
OPT_DAILY_PRICE 


=== 第 61 页 ===
名称 
类型 
描述： 
注释 
code 
str 
合约代码 
10001313.XSHG；
CU1901C46000.XSGE；
SR903C4700.XZCE；M1707-C-
2400.XDCE 
合约代码使用大写字母 
exchange_code 
str 
证券市场编码， 
XSHG 
XSHG：上海证券交易所； 
XSGE：上海期货交易所； 
XZCE：郑州商品交易所； 
XDCE：大连商品交易所 
date 
str 
交易日期 
2018/10/25 
pre_settle 
float 
前结算价 
0.1997 
pre_close 
float 
前收价 
0.1997 
open 
float 
今开盘 
0.1683 
high 
float 
最高价 
0.2072 
low 
float 
最低价 
0.1517 
close 
float 
收盘价 
0.2035 
change_pct_close 
float 
收盘价涨跌幅(%） 
收盘价/前结算价 
settle_price 
float 
结算价 
0.204 
change_pct_settle float 
结算价涨跌幅(%) 
结算价/前结算价 
volume 
float 
成交量（张） 
3126 
money 
float 
成交金额（元） 
5620827 
position 
int 
持仓量 
5095 
 
期权风险指标 
OPT_RISK_INDICATOR 
名称 
类型 
描述： 
代码示例： 
备注 
code 
str 
合约代码 
10001313.XSHG；
CU1901C46000.XSGE；
SR903C4700.XZCE；M1707-C-
2400.XDCE 
合约代码使用大写字
母 


=== 第 62 页 ===
exchange_code 
str 
证券市场编码 
XSHG 
 
date 
str 
交易日期 
10/19/2018  
delta 
float 
DELTA 
0.906 Delta=期权价格变化/
期货变化 
theta 
float 
THETA 
-0.249 Theta＝期权价格的
变化／距离到期日时
间的变化 
gamma 
float 
GAMMA 
0.669 Gamma=delta 的变化
／期货价格的变化 
vega 
float 
VEGA 
0.138 Vega=期权价格变化/
波动率的变化 
rho 
float 
RHO 
0.213 Rho=期权价格的变
化／无风险利率的变
化 
 
期权交易和持仓排名统计 
OPT_TRADE_RANK_STK 
名称 
类型 
描述： 
underlying_symbol 
str 
标的代码 
underlying_name 
str 
标的简称 
underlying_exchange str 
证券市场编码：XSHG-上海证券交易所； 
date 
str 
交易日期 
rank 
int 
排名 
volume 
int 
数量(张） 
option_agency 
str 
期权经营机构 
rank_type 
str 
排名统计类型601001：最活跃三个合约的认购交易排名；601002：
最活跃三个合约的认沽交易排名；601003：持仓最大3 个合约的认购
持仓量排名；601004：持仓最大3 个合约的认沽持仓量排名 


=== 第 63 页 ===
 
期权行权交收信息 
OPT_EXERCISE_INFO 
名称 
类型 
描述： 
代码示例： 
underlying_symbol 
str 
标的代码 
510050.XSHG 
underlying_name 
str 
标的名称 
 
exercise_date 
str 
行权日 
10/24/2018 
constract_type 
str 
合约类型，CO-认购
期权，PO-认沽期权 
CO 
exercise_number 
int 
行权数量 
12520 
 
期权合约调整记录 
OPT_ADJUSTMENT 
名称 
类型 
描述： 
代码示例： 
备注 
code 
str 
合约代码 
10001313.XSHG; 
 
adj_date 
date 
调整日期 
 
 
contract_type 
str 
合约类型。
CO-认购期
权，PO-认沽
期权 
CO 
 
ex_trading_code 
int 
原交易代码 
10001465Nan 
合约调整会产生新
的交易代码 
ex_name 
str 
原合约简称 
50ETF 购10 月2800 豆粕购7
月2400 
合约调整会产生新
的合约简称 
ex_exercise_price 
float 
原行权价 
 
 


=== 第 64 页 ===
ex_contract_unit 
int 
原合约单位 
 
 
new_trading_code 
str 
新交易代码 
 
 
new_name 
str 
新合约简称 
 
 
new_exercise_price 
float 
新行权价 
 
 
new_contract_unit 
int 
新合约单位 
 
 
adj_reason 
str 
调整原因 
 
 
expire_date 
str 
到期日 
10/24/2018  
last_trade_date 
str 
最后交易日 
10/24/2018  
exercise_date 
str 
行权日 
10/24/2018 50ETF 期权是欧式
期权，行权日固定 
delivery_date 
str 
交收日期 
10/25/2018  
position 
int 
合约持仓 
 
 
期权每日盘前静态文件 
OPT_DAILY_PREOPEN 
名称 
类型 
描述： 
date 
str 
交易日期 
code 
str 
合约代码 
trading_code 
str 
合约交易代码 
name 
str 
合约简称 
exchange_code 
str 
证券市场编码XSHG:上海证券交易所 
underlying_symbol 
str 
标的代码 
underlying_name 
str 
标的名称 
underlying_exchange 
str 
标的交易市场 
underlying_type 
str 
标的品种类别，STOCK：股票；ETF：交易型开放式指数基金；
FUTURE：期货 
exercise_type 
str 
期权履约方式:A 美式;E 欧式 
contract_type 
str 
合约类型。CO-认购期权，PO-认沽期权 
contract_unit 
int 
合约单位 
exercise_price 
float 
行权价格 
list_date 
str 
挂牌日期 
last_trade_date 
str 
最后交易日 
exercise_date 
str 
行权日 
delivery_date 
str 
交收日期 
expire_date 
str 
到期日 
contract_version 
str 
合约版本号 
position 
int 
持仓量 
pre_close 
float 
前收盘价 
pre_settle 
float 
前结算价 


=== 第 65 页 ===
pre_close_underlying float 
标的证券前收盘 
is_limit 
str 
涨跌幅限类型，“N”为有涨跌幅限制,深交所无此字段 
high_limit 
float 
涨停价 
low_limit 
float 
跌停价 
margin_unit 
float 
单位保证金 
margin_ratio_1 
float 
保证金计算比例参数一 
margin_ratio_2 
float 
保证金计算比例参数二 
round_lot 
int 
整手数 
limit_order_min 
int 
单笔限价申报下限,深交所无此字段 
limit_order_max 
int 
单笔限价申报上限,深交所无此字段 
market_order_min 
int 
单笔市价申报下限,深交所无此字段 
marker_order_max 
int 
单笔市价申报上限,深交所无此字段 
quote_change_min 
float 
最小报价变动(数值) 
contract_status 
str 
合约状态信息,深交所无此字段 
 


=== 第 66 页 ===
bond 库（债券&可转债） 
库名是bond 
bond.表名 
债券基本信息 
BOND_BASIC_INFO 
名称 
类型 
描述： 
code 
str 
债券代码(不加后缀） 
short_name 
str 
债券简称 
short_name_spelling str 
债券简称拼音 
full_name 
str 
债券全称 
list_status_id 
int 
上市状态编码，见下表上市状态编码对照表 
list_status 
str 
上市状态 
issuer 
str 
发行人 
company_code 
str 
发行人股票代码 
exchange_code  
int 
交易市场编码，见下表交易市场编码 
exchange 
str 
交易市场 
currency_id 
str 
货币代码。CNY-人民币 
coupon_type_id 
int 
计息方式编码，见下表计息方式编码 
coupon_type 
str 
计息方式 
coupon_frequency 
int 
付息频率，单位：月/次。按年付息是12 月/次；半年付息是6 月/次 
payment_type_id 
int 
兑付方式编码，见下表兑付方式编码表 
payment_type 
str 
兑付方式 
par 
float 
债券面值(元) 
repayment_period 
int 
偿还期限(月） 
bond_type_id 
int 
债券分类编码 
bond_type 
str 
债券分类 
bond_form_id 
int 
债券形式编码，见下表债券形式编码表 
bond_form 
str 
债券形式 
list_date 
date 
上市日期 
delist_Date 
date 
退市日期 
interest_begin_date 
date 
起息日 
maturity_date 
date 
到期日 
interest_date 
str 
付息日 
last_cash_date 
date 
最终兑付日 
cash_comment 
str 
兑付说明 


=== 第 67 页 ===
债券票面利率 
BOND_COUPON 
名称 
类型 
描述： 
code 
str 
债券代码（不加后缀） 
short_name 
str 
债券简称 
pub_date 
date 
信息发布日期 
coupon_type_id 
int 
计息方式编码，见下表计息方式编
码 
coupon_type 
str 
计息方式 
coupon 
float(5) 
票面年利率(%) 
coupon_start_date 
date 
票面利率起始适用日期 
coupon_end_date 
date 
票面利率终止适用日期 
reference_rate 
float 
浮息债参考利率(%) 
reference_rate_comment str 
浮息债参考利率说明 
margin_rate 
float 
浮息债利差(%)-(等于票面利率减
参考利率） 
coupon_upper_limit 
float 
利率上限 
coupon_lower_limit 
float 
利率下限 
债券付息事件 
BOND_INTEREST_PAYMENT 
名称 
类型 
描述： 
code 
str 
债券代码(不加后缀） 
name 
str 
债券简称 
pub_date 
date 
公告日期 
event_type 
str 
事件类型 
interest_start_date 
date 
年度计息起始日 
coupon 
float 
票面利率（%） 
interest_end_date 
date 
年度计息终止日 
autual_interest 
float 
实际付息利率（%） 
interest_per_unit 
float 
每手付息数（单位：元，每1000 元付息金额） 
register_date 
date 
债权登记日 
dividend_date 
date 
除息日 
interest_pay_start_date 
date 
付息起始日（债务人实际付息开始日期） 
interest_pay_end_date 
date 
付息终止日（债务人实际付息截止日期） 
payment_date 
date 
兑付日（债券到期兑付） 
payment_per_unit 
float 
每百元面值的到期兑付资金（元） 
tax_rate 
float 
代扣所得税率（%） 


=== 第 68 页 ===
tax_channel 
str 
扣税渠道 
 
国债逆回购日行情数据 
REPO_DAILY_PRICE 
名称 
类型 
描述： 
date 
date 
交易日期 
code 
varchar(12) 
回购代码，如 '204001.XSHG' 
name 
varchar(20) 
回购简称，如 'GC001' 
exchange_code 
varchar(12) 
证券市场编码。XSHG-上海证券
交易所；XSHE-深圳证券交易所 
pre_close 
decimal(10,4) 
前收盘利率(%) 
open 
decimal(10,4) 
开盘利率(%) 
high 
decimal(10,4) 
最高利率(%) 
low 
decimal(10,4) 
最低利率(%) 
close 
decimal(10,4) 
收盘利率(%) 
volume 
bigint 
成交量（手） 
money 
decimal（20,2） 
成交额（元） 
deal_number 
int 
成交笔数（笔） 
 
可转债基本资料 
CONBOND_BASIC_INFO 
名称 
类型 
描述： 
code 
str 
债券代码 
short_name 
str 
债券简称 
full_name 
str 
债券全称 
list_status_id 
int 
上市状态编码，见下表上市状
态编码对照表 
list_status 
str 
上市状态 
issuer 
str 
发行人 
company_code 
str 
发行人股票代码（带后缀） 
issue_start_date 
date 
发行起始日 
issue_end_date 
date 
发行终止日 
plan_raise_fund 
decimal(20,4) 
计划发行总量（万元） 
actual_raise_fund 
decimal(20,4) 
实际发行总量（万元） 
issue_par 
int 
发行面值 
issue_price 
decimal(10,3) 
发行价格 


=== 第 69 页 ===
is_guarantee 
int 
是否有担保(1-是，0-否） 
fund_raising_purposes 
varchar(200) 
募资用途说明 
list_date list_declare_date 
date 
上市公告日期 
convert_price_reason 
varchar(300) 
初始转股价确定方式 
convert_price 
decimal(10,3) 
初始转股价格 
convert_start_date 
start_date 
转股开始日期 
convert_end_date 
end_date 
转股终止日期 
convert_code 
varchar(10) 
转股代码（不带后缀） 
coupon 
decimal(10,3) 
初始票面利率 
exchange_code 
int 
交易市场编码，见下表交易市
场编码 
exchange 
str 
交易市场 
currency_id 
str 
货币代码。CNY-人民币 
coupon_type_id 
int 
计息方式编码，见下表计息方
式编码 
coupon_type 
str 
计息方式 
coupon_frequency 
int 
付息频率，单位：月/次。按年
付息是12 月/次；半年付息是6
月/次 
payment_type_id 
int 
兑付方式编码，见下表兑付方
式编码表 
payment_type 
str 
兑付方式 
par 
float 
债券面值(元) 
repayment_period 
int 
偿还期限(月） 
bond_type_id 
int 
债券分类编码，见下表债券分
类编码 
bond_type 
str 
债券分类 
bond_form_id 
int 
债券形式编码，见下表债券形
式编码表 
bond_form 
str 
债券形式 
list_date 
date 
上市日期 
delist_Date 
date 
退市日期 
interest_begin_date 
date 
起息日 
maturity_date 
date 
到期日 
interest_date 
str 
付息日 
last_cash_date 
date 
最终兑付日 
cash_comment 
str 
兑付说明 
 
可转债转股价格调整 


=== 第 70 页 ===
CONBOND_CONVERT_PRICE_ADJUST 
名称 
类型 
描述： 
code 
str 
债券代码 
name 
str 
债券名称 
pub_date 
date 
公告日期 
adjust_date 
date 
调整生效日期 
new_convert_price 
float 
调整后转股价格 
adjust_reason 
str 
调整原因 
 
可转债每日转股统计 
CONBOND_DAILY_CONVERT 
名称 
类型 
描述： 
date 
date 
交易日期（以YYYY-MM-DD 表示） 
code 
str 
债券代码 
name 
str 
债券简称 
exchange_code 
str 
证券市场编码（XSHG-上海证券交易所；XSHE-深圳
证券交易所） 
issue_number 
int 
发行总量（单位：张） 
convert_price 
float 
转股价格 
daily_convert_number 
int 
当日转股数量（深交所披露为债券转换量 单位：张，
上交所披露为股票转换量 单位 :股） 
acc_convert_number 
int 
累计转股数量（深交所披露为债券转换量 单位：张，
上交所披露为股票转换量 单位 :股） 
acc_convert_ratio 
float 
累计转股比例（单位：% ， 因上交所只披露转股股
数，因此计算剩余转股张数时公式应为 : 发行总量 
*(1 -累计转股比例) ） 
convert_premium 
float 
转股溢价，从2018-09-13 开始计算（每张可转债转股
后可以获得的收益，单位：元。转股溢价=可转债收盘
价-（100/转股价格）*正股收盘价） 
convert_premium_rate 
float 
转股溢价率 
 
可转债日行情 (查表) 
CONBOND_DAILY_PRICE 
名称 
类型 
描述： 
date 
date 
交易日期（以YYYY-MM-DD 表示） 
code 
str 
债券代码 
name 
str 
债券简称 


=== 第 71 页 ===
exchange_code 
str 
证券市场编码（XSHG-上交所；XSHE-深交所） 
pre_close 
float 
昨收价 
open 
float 
开盘价，以人民币计 
high 
float 
最高价，以人民币计 
low 
float 
最低价，以人民币计 
close 
float 
收盘价，以人民币计 
volume 
float 
成交量（手），1 手为10 张债券 
money 
float 
成交额，以人民币计 
deal_number 
int 
成交笔数 
change_pct 
float 
涨跌幅，单位：% 
 


=== 第 72 页 ===
macro 库（宏观经济） 
农业 
分地区农林牧渔业总产值表(季度累计) 
表名：MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_quarter 
统计季度 
文本 
 
YYYY-MM(03、06、09、12 分别代表第1、2、3、4 季度) 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
total 
农林牧渔业
总产值_累
计值 
数字 
亿元 
农林牧渔业总产值指以货币表现的农、林、牧、渔业全部产品和对农
林牧渔业生产活动进行的各种支持性服务活动的价值总量，它反映一
定时期内农林牧渔业生产总规模和总成果。 
farming 
农业总产值
_累计值 
数字 
亿元 
 
forestry 
林业总产值
_累计值 
数字 
亿元 
 
animal_husbandry 
牧业总产值
_累计值 
数字 
亿元 
 
fishery 
渔业总产值
_累计值 
数字 
亿元 
 
分地区农林牧渔业总产值表(年度) 
表名：MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
total 
农林牧渔业
总产值 
数字 
亿元 
农林牧渔业总产值指以货币表现的农、林、牧、渔业全部产品和
对农林牧渔业生产活动进行的各种支持性服务活动的价值总量，
它反映一定时期内农林牧渔业生产总规模和总成果。 
farming 
农业总产值 
数字 
亿元 
 
forestry 
林业总产值 
数字 
亿元 
 
animal_husbandry 
牧业总产值 
数字 
亿元 
 
fishery 
渔业总产值 
数字 
亿元 
 


=== 第 73 页 ===
total_idx 
农林牧渔业
总产值指数 
数字 
% 
上年=100，按可比价格 
farming_idx 
农业总产值
指数 
数字 
% 
上年=100 
forestry_idx 
林业总产值
指数 
数字 
% 
上年=100 
animal_husbandry_idx 
牧业总产值
指数 
数字 
% 
上年=100 
fishery_idx 
渔业总产值
指数 
数字 
% 
上年=100 
全国农产品生产价格指数表(季度) 
表名：MAC_INDUSTRY_AGR_PRODUCT_IDX_QUARTER 
列名 
列的含义 
类型 
单
位 
说明 
id 
id 
数字 
 
 
stat_quarter 
统计季度 
文本 
 
YYYY-MM(03、06、09、12 分别代表第1、2、3、4 季度) 
agricultural_products 
农产品生产价
格指数_当季值 
数字 
 
农产品生产价格指数是反映一定时期内，农产品生产者出售农产
品价格水平变动趋势及幅度的相对数。该指数可以客观反映全国
农产品生产价格水平和结构变动情况，满足农业与国民经济核算
需要。其中某代表品生产价格指数是通过对全部有出售该产品行
为的调查单位的个体指数进行几何平均求得的，类价格指数是通
过对其所属的类（或代表品）的价格指数进行加权平均求得的。
季度累计价格指数的计算方法与分季指数的计算方法相同 
crop_products 
种植业产品生
产价格指数_当
季值 
数字 
 
 
food 
粮食生产价格
指数_当季值 
数字 
 
粮食指人们用作主食的各种成品粮及其加工品，包括大米、面
粉、粗杂粮以及各种粗、细粮制品，不包括薯类、豆类及糕点食
品 
grain 
谷物生产价格
指数_当季值 
数字 
 
 
wheat 
小麦生产价格
指数_当季值 
数字 
 
 
rice 
稻谷生产价格
指数_当季值 
数字 
 
 
corn 
玉米生产价格
指数_当季值 
数字 
 
 
bean 
豆类生产价格
指数_当季值 
数字 
 
 
soybean 
大豆生产价格
指数_当季值 
数字 
 
 
potato 
薯类生产价格
指数_当季值 
数字 
 
 


=== 第 74 页 ===
oil_plants 
油料生产价格
指数_当季值 
数字 
 
 
cotton 
棉花生产价格
指数_当季值 
数字 
 
 
sugar 
糖料生产价格
指数_当季值 
数字 
 
 
tobacco 
烟叶生产价格
指数_当季值 
数字 
 
 
vegetable 
蔬菜生产价格
指数_当季值 
数字 
 
 
fruit 
水果生产价格
指数_当季值 
数字 
 
 
tea 
茶叶生产价格
指数_当季值 
数字 
 
 
forestry_products 
林业产品生产
价格指数_当季
值 
数字 
 
 
wood 
木材生产价格
指数_当季值 
数字 
 
 
bamboo 
竹材生产价格
指数_当季值 
数字 
 
 
pectin 
胶脂和果实类
林产品生产价
格指数_当季值 
数字 
 
 
animal_husbandry_products 
畜牧业产品生
产价格指数_当
季值 
数字 
 
 
pig 
猪(毛重)生产
价格指数_当季
值 
数字 
 
 
cow 
牛(毛重)生产
价格指数_当季
值 
数字 
 
 
sheep 
羊(毛重)生产
价格指数_当季
值 
数字 
 
 
poultry 
肉禽(毛重)生
产价格指数_当
季值 
数字 
 
 
egg 
禽蛋生产价格
指数_当季值 
数字 
 
 
milk 
奶类生产价格
指数_当季值 
数字 
 
 
wool 
毛绒类生产价
格指数_当季值 
数字 
 
 
fishery 
渔业产品生产
价格指数_当季
值 
数字 
 
 


=== 第 75 页 ===
marine_fishery_products 
海水捕捞产品
生产价格指数_
当季值 
数字 
 
 
marine_farm_products 
海水养殖产品
生产价格指数_
当季值 
数字 
 
 
fresh_fishery_products 
淡水捕捞产品
生产价格指数_
当季值 
数字 
 
 
fresh_farm_products 
淡水养殖产品
生产价格指数_
当季值 
数字 
 
 
国内贸易 
社会消费品销售总额（月度） 
表名：MAC_SALE_RETAIL_MONTH  
列名 
列的含义 
类型 
单
位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
retail_sin 
社会消费品零售
总额_当期值 
数字 
亿
元 
社会消费品零售总额指企业（单位、个体户）通过交易直接售给个
人、社会集团非生产、非经营用的实物商品金额，以及提供餐饮服
务所取得的收入金额。个人包括城乡居民和入境人员，社会集团包
括机关、社会团体、部队、学校、企事业单位、居委会或村委会
等。 
retail_acc 
社会消费品零售
总额_累计值 
数字 
亿
元 
 
retail_sin_yoy 
社会消费品零售
总额_同比增长 
数字 
% 
 
retail_acc_yoy 
社会消费品零售
总额_累计增长 
数字 
% 
 
scale_retail_sin 
限上单位消费品
零售额_当期值 
数字 
亿
元 
 
scale_retail_acc 
限上单位消费品
零售额_累计值 
数字 
亿
元 
 
scale_retail_sin_yoy 
限上单位消费品
零售额_同比增
长 
数字 
% 
 
scale_retail_acc_yoy 
限上单位消费品
零售额_累计增
长 
数字 
% 
 


=== 第 76 页 ===
city_retail_sin 
城镇社会消费品
零售总额_当期
值 
数字 
亿
元 
 
city_retail_acc 
城镇社会消费品
零售总额_累计
值 
数字 
亿
元 
 
city_retail_sin_yoy 
城镇社会消费品
零售总额_同比
增长 
数字 
% 
 
city_retail_acc_yoy 
城镇社会消费品
零售总额_累计
增长 
数字 
% 
 
rural_retail_sin 
乡村社会消费品
零售总额_当期
值 
数字 
亿
元 
 
rural_retail_acc 
乡村社会消费品
零售总额_累计
值 
数字 
亿
元 
 
rural_retail_sin_yoy 
乡村社会消费品
零售总额_同比
增长 
数字 
% 
 
rural_retail_acc_yoy 
乡村社会消费品
零售总额_累计
增长 
数字 
% 
 
hotel_retail_sin 
餐饮收入_当期
值 
数字 
亿
元 
 
hotel_retail_acc 
餐饮收入_累计
值 
数字 
亿
元 
 
hotel_retail_sin_yoy 
餐饮收入_同比
增长 
数字 
% 
 
hotel_retail_acc_yoy 
餐饮收入_累计
增长 
数字 
% 
 
hotel_scale_retail_sin 
限上单位餐饮收
入_当期值 
数字 
亿
元 
 
hotel_scale_retail_acc 
限上单位餐饮收
入_累计值 
数字 
亿
元 
 
hotel_scale_retail_sin_yoy 
限上单位餐饮收
入_同比增长 
数字 
% 
 
hotel_scale_retail_acc_yoy 
限上单位餐饮收
入_累计增长 
数字 
% 
 
sale_retail_sin 
商品零售_当期
值 
数字 
亿
元 
 
sale_retail_acc 
商品零售_累计
值 
数字 
亿
元 
 
sale_retail_sin_yoy 
商品零售_同比
增长 
数字 
% 
 
sale_retail_acc_yoy 
商品零售_累计
增长 
数字 
% 
 


=== 第 77 页 ===
sale_scale_retail_sin 
限上单位商品零
售类值_当期值 
数字 
亿
元 
 
sale_scale_retail_acc 
限上单位商品零
售类值_累计值 
数字 
亿
元 
 
sale_scale_retail_sin_yoy 
限上单位商品零
售类值_同比增
长 
数字 
% 
 
sale_scale_retail_acc_yoy 
限上单位商品零
售类值_累计增
长 
数字 
% 
 
限额以上零售分类表（月度） 
表名： MAC_SALE_SCALE_RETAIL_MONTH  
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
item_name 
条目名称 
文本 
 
 
item_sale_sin 
该条目所对应的零售-当前值 
数字 
亿元 
 
item_sale_acc 
该条目所对应的零售-累计值 
数字 
亿元 
 
item_sale_sin_rate 
该条目所对应的零售_累计增长 
数字 
% 
 
item_sale_acc_rate 
该条目所对应的零售_当期值 
数字 
亿元 
 
分地区消费品零售总额（年度） 
表名：MAC_AREA_RETAIL_SALE 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
retail 
社会消费品零售总额 
数字 
亿元 
 
retail_yoy 
社会消费品零售总额同比增长 
数字 
% 
 
city_retail 
社会消费品零售总额-市 
数字 
亿元 
 
city_county_retail 
社会消费品零售总额-县 
数字 
亿元 
 
city_county_below_retail 
社会消费品零售总额-县以下 
数字 
亿元 
 
city_whole_sale_retail 
社会消费品零售总额-批发和零售业 
数字 
亿元 
 
hotels_retail 
社会消费品零售总额-住宿和餐饮业 
数字 
亿元 
 
manufacturing_retail 
社会消费品零售总额-制造业 
数字 
亿元 
 
agricultural_retail 
社会消费品零售总额-农业生产 
数字 
亿元 
 
others_retail 
社会消费品零售总额-其他 
数字 
亿元 
 


=== 第 78 页 ===
亿元以上商品交易市场基本情况（年度） 
表名：MAC_SALE_MARKET 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
market_id 
市场编码 
数字 
 
 
market_name 
市场名称 
数字 
 
 
market_num 
市场数量 
数字 
 
亿元以上商品交易市场指年成交额在亿元及以上的商品交易市场。商品
交易市场是指经有关部门和组织批准设立，有固定场所、设施，有经营
管理部门和监管人员，若干市场经营者入内，常年或实际开业三个月以
上，集中、公开、独立地进行生活消费品、生产资料等现货商品交易以
及提供相关服务的交易场所，包括各类消费品市场、生产资料市场等。 
stall_num 
摊位数量 
数字 
 
 
operation_area 
营业面积 
数字 
 
商品交易市场年末营业面积指市场经营场地、仓库等营业用建筑面积，
不包括为市场经营提供服务的办公室和附设的旅馆、招待所、餐馆、停
车场等的面积，按年末实际面积统计。 
turnover 
成交额 
数字 
 
成交额指该市场所有摊位的全年商品交易额之合计。 
turnover_wholesale 
成交额-批
发 
数字 
 
成交额指该市场所有摊位的全年商品交易额之合计。 
turnover_retail 
成交额-零
售 
数字 
 
成交额指该市场所有摊位的全年商品交易额之合计。 
分地区亿元以上商品交易市场基本情况（年度） 
表名：MAC_AREA_SALE_MARKET 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
market_num 
市场数量 
数字 
 
亿元以上商品交易市场指年成交额在亿元及以上的商品交易市场。商品交易市
场是指经有关部门和组织批准设立，有固定场所、设施，有经营管理部门和监
管人员，若干市场经营者入内，常年或实际开业三个月以上，集中、公开、独
立地进行生活消费品、生产资料等现货商品交易以及提供相关服务的交易场
所，包括各类消费品市场、生产资料市场等。 
stall_num 
摊位数量 
数字 
 
 
operation_area 
营业面积 
数字 
 
商品交易市场年末营业面积指市场经营场地、仓库等营业用建筑面积，不包括
为市场经营提供服务的办公室和附设的旅馆、招待所、餐馆、停车场等的面
积，按年末实际面积统计。 
turnover 
成交额 
数字 
 
成交额指该市场所有摊位的全年商品交易额之合计。 


=== 第 79 页 ===
turnover_wholesale 
成交额-
批发 
数字 
 
成交额指该市场所有摊位的全年商品交易额之合计。 
turnover_retail 
成交额-
零售 
数字 
 
成交额指该市场所有摊位的全年商品交易额之合计。 
就业与工资 
分地区城镇登记失业率（年度） 
表名：MAC_AREA_UNEMPLOY 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 
unemploy 
城镇
登记
失业
人数 
数
字 
万
人 
城镇登记失业人员指有非农业户口，在一定的劳动年龄内(16 周岁至退休年龄)，有劳
动能力，无业而要求就业，并在当地劳动保障部门进行失业登记的人员 
unemploy_rate 
城镇
登记
失业
率 
数
字 
% 
城镇登记失业率城镇登记失业人员与城镇单位就业人员(扣除使用的农村劳动力、聘
用的离退休人员、港澳台及外方人员)、城镇单位中的不在岗职工、城镇私营业主、
个体户主、城镇私营企业和个体就业人员、城镇登记失业人员之和的比。 
就业情况基本表(年度) 
表名：MAC_EMPLOY_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
population 
经济活
动人口 
数
字 
万
人 
 


=== 第 80 页 ===
employ 
就业人
员 
数
字 
万
人 
 
employ_primary 
第一产
业就业
人员 
数
字 
万
人 
 
employ_secondary 
第二产
业就业
人员 
数
字 
万
人 
 
employ_tertiary 
第三产
业就业
人员 
数
字 
万
人 
 
employ_urban 
城镇就
业人员 
数
字 
万
人 
城镇单位就业人员指在各级国家机关、政党机关、社会团体及企
业、事业单位中工作，取得工资或其他形式的劳动报酬的全部人
员。包括在岗职工、再就业的离退休人员、民办教师以及在各单位
中工作的外方人员和港澳台方人员、兼职人员、借用的外单位人员
和第二职业者。不包括离开本单位仍保留劳动关系的职工。 
employ_urban_state_owned 
国有单
位城镇
就业人
员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。就业人员包括：(1)职工、(2)再就业的离退
休人员、(3)私营业主、(4)个体户主、(5)私营企业和个体就业人
员、(6)乡镇企业就业人员、(7)农村就业人员、(8)其他就业人员。 
employ_urban_collective 
城镇集
体单位
城镇就
业人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。就业人员包括：(1)职工、(2)再就业的离退
休人员、(3)私营业主、(4)个体户主、(5)私营企业和个体就业人
员、(6)乡镇企业就业人员、(7)农村就业人员、(8)其他就业人员。 
employ_urban_stock_cooperate 
股份合
作单位
城镇就
业人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_urban_joint_ownership 
联营单
位城镇
就业人
员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_urban_limited 
有限责
任公司
城镇就
业人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_urban_stock 
股份有
限公司
城镇就
业人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_urban_private 
私营企
业城镇
就业人
员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_urban_hkmt 
港澳台
商投资
单位城
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 


=== 第 81 页 ===
镇就业
人员 
employ_urban_foreign 
外商投
资单位
城镇就
业人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_urban_individual 
个体城
镇就业
人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_rural 
乡村就
业人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_rural_private 
私营企
业乡村
就业人
员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
employ_rural_individual 
个体乡
村就业
人员 
数
字 
万
人 
就业人员数是指在16 周岁及以上，从事一定社会劳动并取得劳动
报酬或经营收入的人员。 
unemploy_num 
城镇登
记失业
人数 
数
字 
万
人 
 
unemploy_rate 
城镇登
记失业
率 
数
字 
% 
 
分地区城镇单位就业人员情况表(年度) 
表名：MAC_AREA_WAGEIDX_YEAR 
列名 
列的含
义 
类
型 
单
位 
说明 
id 
id 
文
本 
 
 
stat_year 
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
wage 
城镇单
位就业
人员工
资总额 
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_state_owned 
国有城
镇单位
就业人
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工


=== 第 82 页 ===
员工资
总额 
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。。 
wage_collective 
城镇集
体单位
就业人
员工资
总额 
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_others 
其他城
镇单位
就业人
员工资
总额 
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。。 
wage_yoy 
其他城
镇单位
就业人
员工资
总额 
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_state_owned_yoy 
国有城
镇单位
就业人
员工资
总额指
数 
数
字 
 
上年=100 
wage_collective_yoy 
城镇集
体单位
就业人
员工资
总额指
数 
数
字 
 
上年=100 
wage_others_yoy 
其他城
镇单位
就业人
员工资
总额指
数 
数
字 
 
上年=100 
wage_avg 
城镇单
位就业
人员平
均工资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。
它表明一定时期职工工资收入的高低程度，是反映就业人员工资水平
的主要指标。计算公式为:平均工资=报告期实际支付的全部就业人员
工资总额/报告期全部就业人员平均人数。 
wage_employ_avg 
城镇单
位在岗
职工平
均工资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。
它表明一定时期职工工资收入的高低程度，是反映就业人员工资水平
的主要指标。计算公式为:平均工资=报告期实际支付的全部就业人员
工资总额/报告期全部就业人员平均人数。 
wage_state_owned_avg 
城镇国
有单位
就业人
员平均
工资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。
它表明一定时期职工工资收入的高低程度，是反映就业人员工资水平
的主要指标。计算公式为:平均工资=报告期实际支付的全部就业人员
工资总额/报告期全部就业人员平均人数。 


=== 第 83 页 ===
wage_collective_avg 
城镇集
体单位
就业人
员平均
工资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。
它表明一定时期职工工资收入的高低程度，是反映就业人员工资水平
的主要指标。计算公式为:平均工资=报告期实际支付的全部就业人员
工资总额/报告期全部就业人员平均人数。 
wage_others_avg 
城镇其
他单位
就业人
员平均
工资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。
它表明一定时期职工工资收入的高低程度，是反映就业人员工资水平
的主要指标。计算公式为:平均工资=报告期实际支付的全部就业人员
工资总额/报告期全部就业人员平均人数。 
wage_avg_yoy 
城镇单
位就业
人员平
均货币
工资指
数 
数
字 
 
上年=100 
wage_employ_avg_yoy 
城镇单
位在岗
职工平
均货币
工资指
数 
数
字 
 
上年=100 
wage_state_owned_avg_yoy 
国有城
镇单位
就业人
员平均
货币工
资指数 
数
字 
 
上年=100 
wage_collective_avg_yoy 
城镇集
体单位
就业人
员平均
货币工
资指数 
数
字 
 
上年=100 
wage_others_avg_yoy 
其他城
镇单位
就业人
员平均
货币工
资指数 
数
字 
 
上年=100 
分地区分行业城镇单位就业人员工资情况表(年度) 
表名：MAC_AREA_INDUSTRY_WAGE_YEAR 


=== 第 84 页 ===
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 
industry_id 
行业
编号 
文
本 
 
 
industry_name 
行业
名称 
文
本 
 
 
wage 
该行
业工
资总
额 
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的房费、水费、电
费、住房公积金和社会保险基金个人缴纳部分等。工资总额不论是计入成本的还是不
计入成本的，不论是以货币形式支付的还是以实物形式支付的，均应列入工资总额的
计算范围。 
wage_avg 
该行
业平
均工
资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。它表明一定时期
职工工资收入的高低程度，是反映就业人员工资水平的主要指标。计算公式为:平均工
资=报告期实际支付的全部就业人员工资总额/报告期全部就业人员平均人数。 
分行业城镇单位就业人员工资情况表(年度) 
表名：MAC_INDUSTRY_WAGE_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
industry_id 
行业编
号 
文
本 
 
 
industry_name 
行业名
称 
文
本 
 
 
wage 
该行业
工资总
额 
数
字 
亿
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的房费、水费、
电费、住房公积金和社会保险基金个人缴纳部分等。工资总额不论是计入成本的还
是不计入成本的，不论是以货币形式支付的还是以实物形式支付的，均应列入工资
总额的计算范围。 
wage_avg 
该行业
平均工
资 
数
字 
元 
平均工资指单位就业人员在一定时期内平均每人所得的货币工资额。它表明一定时
期职工工资收入的高低程度，是反映就业人员工资水平的主要指标。计算公式为:平
均工资=报告期实际支付的全部就业人员工资总额/报告期全部就业人员平均人数。 


=== 第 85 页 ===
employ 
该行业
就业人
员数量 
数
字 
万
人 
 
分地区按注册类型分城镇单位就业人员工资情况表(年度) 
表名：MAC_AREA_REGISTERED_WAGE_YEAR 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
wage_avg 
城镇单位
就业人员
平均工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_state_owned 
国有单位
就业人员
平均工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_collective 
城镇集体
单位就业
人员平均
工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_stock_cooperate 
股份合作
单位就业
人员平均
工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_joint_ownership 
联营单位
就业人员
平均工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_limited 
有限责任
公司就业
人员平均
工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_stock 
股份有限
公司就业
人员平均
工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 


=== 第 86 页 ===
wage_avg_private 
其他单位
就业人员
平均工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_hkmt 
港、澳、
台商投资
单位就业
人员平均
工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
wage_avg_foreign 
外商投资
单位就业
人员平均
工资 
数
字 
元 
工资总额是税前工资，包括单位从个人工资中直接为其代扣或代缴的
房费、水费、电费、住房公积金和社会保险基金个人缴纳部分等。工
资总额不论是计入成本的还是不计入成本的，不论是以货币形式支付
的还是以实物形式支付的，均应列入工资总额的计算范围。 
分地区按行业分城镇单位就业人员情况表（年度） 
表名：MAC_AREA_INDUSTRY_EMPLOY_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
industry_id 
行业编号 
文本 
 
 
industry_name 
行业名称 
文本 
 
 
employ 
该行业就业人数 
数字 
万人 
 
资源环境 
各地区森林资源情况表（年度） 
表名：MAC_RESOURCES_AREA_FOREST 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 


=== 第 87 页 ===
area_name 
地区
名称 
文
本 
 
 
forestry_land_area 
林业
用地
面积 
数
字 
万
公
顷 
人工林面积指由人工播种、植苗或扦插造林形成的生长稳定，(一般造
林3-5 年后或飞机播种5-7 年后)每公顷保存株数大于或等于造林设计
植树株数80%或郁闭度0.20 以上(含0.20)的林分面积。 
forest_area 
森林
面积 
数
字 
万
公
顷 
森林面积包括郁闭度0.2 以上的乔木林地面积和竹林面积，国家特别
规定的灌木林地面积，农田林网以及村旁、路旁、水旁、宅旁林木的
覆盖面积。 
man_made_forest_area 
人工
林面
积 
数
字 
万
公
顷 
 
forest_cover_rate 
森林
覆盖
率 
数
字 
% 
森林覆盖率指以行政区域为单位的森林面积占区域土地总面积的百分
比。计算公式为：森林覆盖率=森林面积/土地总面积×100%。 
standing_forest_stock_volume 
活立
木总
蓄积
量 
数
字 
亿
立
方
米 
活立木总蓄积量指一定范围土地上全部树木蓄积的总量，包括森林蓄
积、疏林蓄积、散生木蓄积和四旁树蓄积。 
forest_stand_volume 
森林
蓄积
量 
数
字 
亿
立
方
米 
森林蓄积量指一定森林面积上存在着的林木树干部分的总材积。 
生态环境情况信息表（年度） 
表名：MAC_RESOURCES_ECOLOGICAL_ENVIRONMENT 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
forest_area 
森林
面积 
数
字 
万
公
顷 
2001、2002 年为第五次全国森林资源清查数 (1994-1998 年)，包括台湾省数
据；2003-2006 年为第六次清查数(1999-2003 年)，包括香港、澳门特别行政
区和台湾省数据。 
forest_cover_rate 
森林
覆盖
率 
数
字 
% 
森林覆盖率指以行政区域为单位的森林面积占区域土地总面积的百分比。计
算公式为：森林覆盖率=森林面积/土地总面积×100%。 
man_made_forest_area 
造林
总面
积 
数
字 
千
公
顷 
造林面积指在宜林荒山荒地、宜林沙荒地、无立木林地、疏林地和退耕地等
其他宜林地上通过人工措施形成或恢复森林、林木、灌木林的过程。 
nature_reserves_num 
自然
保护
区个
数 
数
字 
个 
自然保护区指为了保护自然环境和自然资源，促进国民经济的持续发展，将
一定面积的陆地和水体划分出来，并经各级人民政府批准而进行特殊保护和
管理的区域个数。根据保护对象，自然保护区分为自然生态系统类、野生生
物类、自然遗迹类。风景名胜区、文物保护区不计在内。 


=== 第 88 页 ===
nature_reserves_area 
自然
保护
区面
积 
数
字 
万
公
顷 
 
水资源情况表（年度） 
表名：MAC_RESOURCES_AREA_WATER_RESOURCES 
列名 
列的含义 
类
型 
单位 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
total_amount 
水资源总
量 
数
字 
亿立
方米 
水资源总量指当地降水形成的地表和地下产水总量，即地表径流量
与降水入渗补给量之和。 
surface 
地表水资
源量 
数
字 
亿立
方米 
地表水资源量指河流、湖泊以及冰川等地表水体中可以逐年更新的
动态水量，即天然河川径流量。 
ground 
地下水资
源量 
数
字 
亿立
方米 
地表水资源量指河流、湖泊以及冰川等地表水体中可以逐年更新的
动态水量，即天然河川径流量。 
duplicated_measurement 
地表水与
地下水资
源重复量 
数
字 
亿立
方米 
地表水与地下水重复计算量指地表水和地下水相互转化的部分，即
天然河川径流量中的地下水排泄量和地下水补给量中来源于地表水
的入渗补给量。 
per_amount 
人均水资
源量 
数
字 
立方
米/
人 
 
全国水资源量年度信息表（年度） 
表名：MAC_RESOURCES_WATER_RESOURCES_YEAR 
列名 
列的含义 
类
型 
单位 
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
total_amount 
水资源总量 
数
字 
亿立
方米 
水资源总量指当地降水形成的地表和地下产水总量，即地表径流
量与降水入渗补给量之和。 


=== 第 89 页 ===
surface 
地表水资源
量 
数
字 
亿立
方米 
地表水资源量指河流、湖泊以及冰川等地表水体中可以逐年更新
的动态水量，即天然河川径流量。 
ground 
地下水资源
量 
数
字 
亿立
方米 
地表水资源量指河流、湖泊以及冰川等地表水体中可以逐年更新
的动态水量，即天然河川径流量。 
duplicated_measurement 
地表水与地
下水资源重
复量 
数
字 
亿立
方米 
地表水与地下水重复计算量指地表水和地下水相互转化的部分，
即天然河川径流量中的地下水排泄量和地下水补给量中来源于地
表水的入渗补给量。 
per_amount 
人均水资源
量 
数
字 
立方
米/人 
 
各地区供水用水情况表（年度） 
表名：MAC_RESOURCES_AREA_WATER_SUPPLY_USE 
列名 
列
的
含
义 
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
统
计
年
份 
文
本 
 
YYYY 
area_code 
地
区
代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地
区
名
称 
文
本 
 
 
water_supply 
供
水
总
量 
数
字 
亿
立
方
米 
供水总量指各种水源为用水户提供的包括输水损失在内的毛水量。 
surface_water 
地
表
水
供
水
总
量 
数
字 
亿
立
方
米 
地表水源供水量指地表水体工程的取水量，按蓄、引、提、调四种形式统计。从水
库、塘坝中引水或提水，均属蓄水工程供水量；从河道或湖泊中自流引水的，无论
有闸或无闸，均属引水工程供水量；利用扬水站从河道或湖泊中直接取水的，属提
水工程供水量；跨流域调水指水资源一级区或独立流域之间的跨流域调配水量，不
包括在蓄、引、提水量中。 
ground_water 
地
下
水
数
字 
亿
立
地下水源供水量指水井工程的开采量，按浅层淡水、深层承压水和微咸水分别统
计。城市地下水源供水量包括自来水厂的开采量和工矿企业自备井的开采量 


=== 第 90 页 ===
供
水
总
量 
方
米 
others 
其
他
供
水
总
量 
数
字 
亿
立
方
米 
其他水源供水量包括污水处理再利用、集雨工程、海水淡化等水源工程的供水量。 
water_use 
用
水
总
量 
数
字 
亿
立
方
米 
用水总量指各类用水户取用的包括输水损失在内的毛水量。 
agriculture 
农
业
用
水
总
量 
数
字 
亿
立
方
米 
农业用水包括农田灌溉用水、林果地灌溉用水、草地灌溉用水、鱼塘补水和畜禽用
水。 
industry 
工
业
用
水
总
量 
数
字 
亿
立
方
米 
工业用水指工矿企业在生产过程中用于制造、加工、冷却、空调、净化、洗涤等方
面的用水，按新水取用量计，不包括企业内部的重复利用水量。 
daily_consumption 
生
活
用
水
总
量 
数
字 
亿
立
方
米 
生活用水包括城镇生活用水和农村生活用水。城镇生活用水由居民用水和公共用水
（含第三产业及建筑业等用水）组成；农村生活用水指居民生活用水。 
ecology 
生
态
用
水
总
量 
数
字 
亿
立
方
米 
 
per_amount 
人
均
用
水
量 
数
字 
立
方
米/
人 
 
供水用水情况表（年度） 
表名：MAC_RESOURCES_WATER_SUPPLY_USE_YEAR 


=== 第 91 页 ===
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
water_supply 
供水
总量 
数
字 
亿
立
方
米 
供水总量指各种水源为用水户提供的包括输水损失在内的毛水量。 
surface_water 
地表
水供
水总
量 
数
字 
亿
立
方
米 
地表水源供水量指地表水体工程的取水量，按蓄、引、提、调四种形式统计。从
水库、塘坝中引水或提水，均属蓄水工程供水量；从河道或湖泊中自流引水的，
无论有闸或无闸，均属引水工程供水量；利用扬水站从河道或湖泊中直接取水
的，属提水工程供水量；跨流域调水指水资源一级区或独立流域之间的跨流域调
配水量，不包括在蓄、引、提水量中。 
ground_water 
地下
水供
水总
量 
数
字 
亿
立
方
米 
地下水源供水量指水井工程的开采量，按浅层淡水、深层承压水和微咸水分别统
计。城市地下水源供水量包括自来水厂的开采量和工矿企业自备井的开采量 
others 
其他
供水
总量 
数
字 
亿
立
方
米 
其他水源供水量包括污水处理再利用、集雨工程、海水淡化等水源工程的供水
量。 
water_use 
用水
总量 
数
字 
亿
立
方
米 
用水总量指各类用水户取用的包括输水损失在内的毛水量。 
agriculture 
农业
用水
总量 
数
字 
亿
立
方
米 
农业用水包括农田灌溉用水、林果地灌溉用水、草地灌溉用水、鱼塘补水和畜禽
用水。 
industry 
工业
用水
总量 
数
字 
亿
立
方
米 
工业用水指工矿企业在生产过程中用于制造、加工、冷却、空调、净化、洗涤等
方面的用水，按新水取用量计，不包括企业内部的重复利用水量。 
daily_consumption 
生活
用水
总量 
数
字 
亿
立
方
米 
生活用水包括城镇生活用水和农村生活用水。城镇生活用水由居民用水和公共用
水（含第三产业及建筑业等用水）组成；农村生活用水指居民生活用水。 
ecology 
生态
用水
总量 
数
字 
亿
立
方
米 
 
per_amount 
人均
用水
量 
数
字 
立
方
米/
人 
 


=== 第 92 页 ===
水环境情况信息表（年度） 
表名：MAC_RESOURCES_WATER_ENVIRONMENT 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
waste_water_discharge 
废水
排放
总量 
数
字 
万
吨 
废水排放总量指工业废水排放量与生活污水排放量之和。 
COD_discharge 
化学
需氧
量排
放量 
数
字 
万
吨 
化学需氧量(COD)排放量指工业废水中COD 排放量与生活污水中COD 排放量
之和。化学需氧量指用化学氧化剂氧化水中有机污染物时所需的氧量。一般利
用化学氧化剂将废水中可氧化的物质(有机物、亚硝酸盐、亚铁盐、硫化物等)
氧化分解，然后根据残留的氧化剂的量计算出氧的消耗量，来表示废水中有机
物的含量，反映水体有机物污染程度。COD 值越高，表示水中有机污染物污染
越重。 
NH3_N2_discharge 
氨氮
排放
量 
数
字 
万
吨 
 
各地区废气排放及处理情况表（年度） 
表名：MAC_RESOURCES_AREA_WASTE_GAS_EMISSION 
列名 
列的含
义 
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
统计年
份 
文
本 
 
 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
SO2_discharged 
二氧化
硫排放
量 
数
字 
吨 
二氧化硫排放量指报告期内工业SO2 排放量与生活SO2 排放量之和。 
NO_discharged 
氮氧化
物排放
量 
数
字 
吨 
氮氧化物排放量指报告期内企业在燃料燃烧和生产工艺过程中排入大气的氮氧化
物总质量。 


=== 第 93 页 ===
soot_discharged 
烟(粉)
尘排放
量 
数
字 
吨 
烟(粉)尘排放量指报告期内企业在燃料燃烧和生产工艺过程中排入大气的烟尘及工
业粉尘的总质量之和。烟尘或工业粉尘排放量可以通过除尘系统的排风量和除尘
设备出口烟尘浓度相乘求得。 
自然灾害情况信息表（年度） 
表名：MAC_RESOURCES_NATURAL_DISASTER 
列名 
列的
含义 
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
统计
年份 
文
本 
 
 
geological_disaster_num 
发生
地质
灾害
起数 
数
字 
次 
地质灾害指滑坡、崩塌、泥石流、地面塌陷等突发性地质灾害与地裂缝、
地面沉降、海水入侵等缓变性地质灾害。地质灾害数量的计量单位统一用
“处”，对于难以区分确切数量的同一次降雨（或其他因素）引发的群发性
地质灾害归为1 处灾害。地裂缝、地面沉降、海水入侵数量只统计报告期
内发现的或报告期之前发现且报告期内继续发展的。 
earthquake_num 
地震
灾害
次数 
数
字 
次 
 
forest_fire_num 
森林
火灾
次数 
数
字 
次 
森林火灾次数指发生在城市市区外的一切森林、林木和林地的火灾次数。
按照受害森林面积和伤亡人数，森林火灾分为一般森林火灾、较大森林火
灾、重大森林火灾和特别重大森林火灾：1.一般森林火灾：受害森林面积
在1 公顷以下或者其他林地起火的，或者死亡1 人以上3 人以下的，或者
重伤1 人以上10 人以下的；2.较大森林火灾：受害森林面积在1 公顷以
上100 公顷以下的，或者死亡3 人以上10 人以下的，或者重伤10 人以
上50 人以下的；3.重大森林火灾：受害森林面积在100 公顷以上1000 公
顷以下的，或者死亡10 人以上30 人以下的，或者重伤50 人以上100 人
以下的；4.特别重大森林火灾：受害森林面积在1000 公顷以上的，或者
死亡30 人以上的，或者重伤100 人以上的。本条所称“以上”包括本数，
“以下”不包括本数。 
forest_fire_area 
火场
总面
积 
数
字 
万
公
顷 
 
forest_pest_affected_area 
森林
病虫
鼠害
发生
面积 
数
字 
万
公
顷 
森林病虫鼠害指对森林、林木、林木种苗及木材、竹材形成的病害、虫害
和鼠害。森林病害是指林木机体遭受真菌、细菌、病毒、寄生性种子植物
和线虫等的危害，而使林木在生理机能、细胞和组织结构以及外部形态等
方面发生的病理性变化。森林虫害是指林木机体遭受松毛虫、金花虫、竹
蝗、金龟子、蝼蛄等各种昆虫的危害，而造成一定面积森林的生长衰弱或
死亡。森林鼠害是指森林、林木、林木种苗遭受各种鼠类的危害，而造成
一定程度的损失或死亡。 
forest_pest_protected_area 
森林
病虫
鼠害
数
字 
万
公
顷 
 


=== 第 94 页 ===
防治
面积 
forest_pest_protected_rate 
森林
病虫
鼠害
防治
率 
数
字 
% 
 
环境污染治理投资情况信息表（年度） 
表名：MAC_RESOURCES_ENVIRONMENT_TREAT_INVEST 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
 
environment_pollution 
环境污染治理投资总额 
数字 
亿元 
 
infrastructure 
城市环境基础设施建设投资额 
数字 
亿元 
 
fuel_gas 
城市燃气建设投资额 
数字 
亿元 
 
centralized_heating 
城市集中供热建设投资额 
数字 
亿元 
 
drainage 
城市排水建设投资额 
数字 
亿元 
 
gardening 
城市园林绿化建设投资额 
数字 
亿元 
 
sanitation 
城市市容环境卫生建设投资额 
数字 
亿元 
 
industrial_pollution 
工业污染源治理投资 
数字 
万元 
 
three_simultaneities 
建设项目“三同时”环保投资额 
数字 
亿元 
 
房地产行业 
房地产开发投资情况表(月度累计) 
表名：MAC_INDUSTRY_ESTATE_INVEST_MONTH 
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
 
 
stat_month 
统计月份 
文
本 
 
YYY-MM 
invest 
房地产投资
_累计值 
数
字 
亿
元 
房地产开发投资指各种登记注册类型的房地产开发法人单位统一开发
的包括统代建、拆迁还建的住宅、厂房、仓库、饭店、宾馆、度假
村、写字楼、办公楼等房屋建筑物，配套的服务设施，土地开发工程
(如道路、给水、排水、供电、供热、通讯、平整场地等基础设施工
程)和土地购置的投资；不包括单纯的土地开发和交易活动。 


=== 第 95 页 ===
invest_yoy 
房地产投资
_累计增长 
数
字 
% 
 
auxiliary_project 
房地产配套
工程投资_
累计值 
数
字 
亿
元 
 
auxiliary_project_yoy 
房地产配套
工程投资_
累计增长 
数
字 
% 
 
resident 
房地产住宅
投资_累计
值 
数
字 
亿
元 
 
resident_yoy 
房地产住宅
投资_累计
增长 
数
字 
% 
 
below90_house 
90 平方米
及以下住房
投资_累计
值 
数
字 
亿
元 
 
below90_house_yoy 
90 平方米
及以下住房
投资_累计
增长 
数
字 
% 
 
above144_house 
144 平方米
以上住房投
资_累计值 
数
字 
亿
元 
 
above144_house_yoy 
144 平方米
以上住房投
资_累计增
长 
数
字 
% 
 
villa_flat 
别墅、高档
公寓投资_
累计值 
数
字 
亿
元 
 
villa_flat_yoy 
别墅、高档
公寓投资_
累计增长 
数
字 
% 
 
office 
房地产办公
楼投资_累
计值 
数
字 
亿
元 
 
office_yoy 
房地产办公
楼投资_累
计增长 
数
字 
% 
 
business 
房地产商业
营业用房投
资_累计值 
数
字 
亿
元 
 
business_yoy 
房地产商业
营业用房投
资_累计增
长 
数
字 
% 
 


=== 第 96 页 ===
other_house 
其它房地产
投资_累计
值 
数
字 
亿
元 
 
other_house_yoy 
其它房地产
投资_累计
增长 
数
字 
% 
 
construct 
房地产开发
建筑工程投
资_累计值 
数
字 
亿
元 
 
construct_yoy 
房地产开发
建筑工程投
资_累计增
长 
数
字 
% 
 
install 
房地产开发
安装工程投
资_累计值 
数
字 
亿
元 
 
install_yoy 
房地产开发
安装工程投
资_累计增
长 
数
字 
% 
 
equipment_purchase 
房地产设备
工器具购置
投资_累计
值 
数
字 
亿
元 
 
equipment_purchase_yoy 
房地产设备
工器具购置
投资_累计
增长 
数
字 
% 
 
other_expense 
房地产其它
费用投资_
累计值 
数
字 
亿
元 
 
other_expense_yoy 
房地产其它
费用投资_
累计增长 
数
字 
% 
 
land_purchase 
房地产土地
购置费_累
计值 
数
字 
亿
元 
 
land_purchase_yoy 
房地产土地
购置费_累
计增长 
数
字 
% 
 
plan_invest 
房地产开发
计划总投资
_累计值 
数
字 
亿
元 
 
plan_invest_yoy 
房地产开发
计划总投资
_累计增长 
数
字 
% 
 
new_fixed_assets 
房地产开发
新增固定资
数
字 
亿
元 
 


=== 第 97 页 ===
产投资_累
计值 
new_fixed_assets_yoy 
房地产开发
新增固定资
产投资_累
计增长 
数
字 
% 
 
分地区房地产开发投资情况表(月度累计) 
表名：MAC_INDUSTRY_AREA_ESTATE_INVEST_MONTH 
列名 
列的含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_month 
统计月
份 
文
本 
 
YYYY-MM 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
invest 
房地产
投资_
累计值 
数
字 
亿
元 
房地产开发投资指各种登记注册类型的房地产开发法人单位统一开发的包括统代建、拆
迁还建的住宅、厂房、仓库、饭店、宾馆、度假村、写字楼、办公楼等房屋建筑物，配
套的服务设施，土地开发工程(如道路、给水、排水、供电、供热、通讯、平整场地等
基础设施工程)和土地购置的投资；不包括单纯的土地开发和交易活动。 
invest_yoy 
房地产
投资_
累计增
长 
数
字 
% 
 
resident 
房地产
住宅投
资_累
计值 
数
字 
亿
元 
 
resident_yoy 
房地产
住宅投
资_累
计增长 
数
字 
% 
 
房地产开发投资资金来源情况表(月度累计) 
表名：MAC_INDUSTRY_ESTATE_FUND_SOURCE_MONTH 
列名 
列的含义 
类
型 
单
位 
说明 


=== 第 98 页 ===
id 
id 
数
字 
 
 
stat_month 
统计月份 
文
本 
 
YYY-MM 
total_invest 
房地产投
资资金来
源_累计
值 
数
字 
亿
元 
 
total_invest_yoy 
房地产投
资资金来
源_累计
增长 
数
字 
% 
 
surplus 
房地产投
资上年资
金结余_
累计值 
数
字 
亿
元 
上年末结余资金指上年资金来源中没有形成投资额而结余的资金。包括尚未用
到工程中的材料价值、未开始安装的需要安装设备价值及结存的现金和银行存
款等。 
surplus_yoy 
房地产投
资上年资
金结余_
累计增长 
数
字 
% 
 
invest 
房地产投
资本年资
金来源小
计_累计
值 
数
字 
亿
元 
 
invest_yoy 
房地产投
资本年资
金来源小
计_累计
增长 
数
字 
% 
 
domestic_loan 
房地产投
资国内贷
款_累计
值 
数
字 
亿
元 
 
domestic_loan_yoy 
房地产投
资国内贷
款_累计
增长 
数
字 
% 
国内贷款指报告期内向银行及非银行金融机构借入的各种国内借款，包括银行
利用自有资金及吸收存款发放的贷款、上级主管部门拨入的国内贷款、国家专
项贷款(包括煤代油贷款、劳改煤矿专项贷款等)，地方财政专项资金安排的贷
款、国内储备贷款、周转贷款等。 
foreign_capital 
房地产投
资利用外
资_累计
值 
数
字 
亿
元 
利用外资指报告期内收到的境外(包括外国及港澳台地区)资金(包括设备、材
料、技术在内)。包括对外借款(外国政府贷款、国际金融组织贷款、出口信
贷、外国银行商业贷款、对外发行债券和股票)、外商直接投资、外商其他投
资(包括补偿贸易、加工装配由外商提供的设备价款、国际租赁，外商投资收
益的再投资资金)。不包括我国自有外汇资金(国家外汇、地方外汇、留成外
汇、调剂外汇和中国境内银行自有资金发放的外汇贷款等)。各类外资按报告
期的外汇牌价(中间价)折成人民币计算。 
foreign_capital_yoy 
房地产投
资利用外
数
字 
% 
 


=== 第 99 页 ===
资_累计
增长 
self_financing 
房地产投
资自筹资
金_累计
值 
数
字 
亿
元 
自筹资金指各地区、各部门及企事业单位筹集用于房地产开发与经营的预算外
资金。 
self_financing_yoy 
房地产投
资自筹资
金_累计
增长 
数
字 
% 
 
other_capital 
房地产投
资其他资
金_累计
值 
数
字 
亿
元 
工程款指在房地产开发过程中应付未付给施工单位(乙方)的工程投资款。 
other_capital_yoy 
房地产投
资其他资
金_累计
增长 
数
字 
% 
 
payment 
房地产投
资各项应
付款_累
计值 
数
字 
亿
元 
 
payment_yoy 
房地产投
资各项应
付款_累
计增长 
数
字 
% 
 
project_funds 
房地产投
资工程款
_累计值 
数
字 
亿
元 
 
project_funds_yoy 
房地产投
资工程款
_累计增
长 
数
字 
% 
 
各地区房地产开发规模与开、竣工面积增长情况表(月度累计) 
表名：MAC_INDUSTRY_AREA_ESTATE_BUILD_MONTH 
列名 
列的含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_month 
统计月
份 
文
本 
 
YYYY-MM 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 


=== 第 100 页 ===
area_name 
地区名
称 
文
本 
 
 
construct_area 
房地产
施工面
积_累
计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
construct_area_yoy 
房地产
施工面
积_累
计增长 
数
字 
% 
 
new_start_area 
房地产
新开工
施工面
积_累
计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
new_start_area_yoy 
房地产
新开工
施工面
积_累
计增长 
数
字 
% 
 
complete_area 
房地产
竣工面
积_累
计值 
数
字 
万
平
方
米 
竣工面积指报告期内房屋建筑按照设计要求已全部完工，达到住人和
使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交使用的
各栋房屋建筑面积的总和。竣工面积以房屋单位工程(栋)为核算对象，
在整栋房屋符合竣工条件后按其全部建筑面积一次性计算，而不是按
各栋施工房屋中已完成的部分或层次分割计算。 
complete_area_yoy 
房地产
竣工面
积_累
计增长 
数
字 
% 
 
resident_construct_area 
商品住
宅施工
面积_
累计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
resident_construct_area_yoy 
商品住
宅施工
面积_
累计增
长 
数
字 
% 
 
resident_new_start_area 
商品住
宅新开
工施工
面积_
累计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
resident_new_start_area_yoy 
商品住
宅新开
工施工
面积_
数
字 
% 
 


=== 第 101 页 ===
累计增
长 
resident_complete_area 
商品住
宅竣工
面积_
累计值 
数
字 
万
平
方
米 
竣工面积指报告期内房屋建筑按照设计要求已全部完工，达到住人和
使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交使用的
各栋房屋建筑面积的总和。竣工面积以房屋单位工程(栋)为核算对象，
在整栋房屋符合竣工条件后按其全部建筑面积一次性计算，而不是按
各栋施工房屋中已完成的部分或层次分割计算。 
resident_complete_area_yoy 
商品住
宅竣工
面积_
累计增
长 
数
字 
% 
 
office_construct_area 
办公楼
施工面
积_累
计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
office_construct_area_yoy 
办公楼
施工面
积_累
计增长 
数
字 
% 
 
office_new_start_area 
办公楼
新开工
施工面
积_累
计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
office_new_start_area_yoy 
办公楼
新开工
施工面
积_累
计增长 
数
字 
% 
 
office_complete_area 
办公楼
竣工面
积_累
计值 
数
字 
万
平
方
米 
竣工面积指报告期内房屋建筑按照设计要求已全部完工，达到住人和
使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交使用的
各栋房屋建筑面积的总和。竣工面积以房屋单位工程(栋)为核算对象，
在整栋房屋符合竣工条件后按其全部建筑面积一次性计算，而不是按
各栋施工房屋中已完成的部分或层次分割计算。 
office_complete_area_yoy 
办公楼
竣工面
积_累
计增长 
数
字 
% 
竣工面积指报告期内房屋建筑按照设计要求已全部完工，达到住人和
使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交使用的
各栋房屋建筑面积的总和。竣工面积以房屋单位工程(栋)为核算对象，
在整栋房屋符合竣工条件后按其全部建筑面积一次性计算，而不是按
各栋施工房屋中已完成的部分或层次分割计算。 
business_construct_area 
商业营
业用房
施工面
积_累
计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
business_construct_area_yoy 
商业营
业用房
施工面
数
字 
% 
 


=== 第 102 页 ===
积_累
计增长 
business_new_start_area 
商业营
业用房
新开工
施工面
积_累
计值 
数
字 
万
平
方
米 
施工面积指报告期内施工的全部房屋建筑面积。包括本期新开工的房
屋建筑面积、上期跨入本期继续施工的房屋建筑面积、上期停缓建在
本期恢复施工的房屋建筑面积、本期竣工的房屋建筑面积以及本期施
工后又停缓建的房屋建筑面积。多层建筑应填各层建筑面积之和。 
business_new_start_area_yoy 
商业营
业用房
新开工
施工面
积_累
计增长 
数
字 
% 
 
business_complete_area 
商业营
业用房
竣工面
积_累
计值 
数
字 
万
平
方
米 
竣工面积指报告期内房屋建筑按照设计要求已全部完工，达到住人和
使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交使用的
各栋房屋建筑面积的总和。竣工面积以房屋单位工程(栋)为核算对象，
在整栋房屋符合竣工条件后按其全部建筑面积一次性计算，而不是按
各栋施工房屋中已完成的部分或层次分割计算。 
business_complete_area_yoy 
商业营
业用房
竣工面
积_累
计增长 
数
字 
% 
竣工面积指报告期内房屋建筑按照设计要求已全部完工，达到住人和
使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交使用的
各栋房屋建筑面积的总和。竣工面积以房屋单位工程(栋)为核算对象，
在整栋房屋符合竣工条件后按其全部建筑面积一次性计算，而不是按
各栋施工房屋中已完成的部分或层次分割计算。 
70 个大中城市房屋销售价格指数(月度) 
表名：MAC_INDUSTRY_ESTATE_70CITY_INDEX_MONTH 
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
 
 
stat_month 
统计月份 
文
本 
 
YYYY-MM 
area_code 
地区代码 
文
本 
 
关
联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
fixed_base_type 
指数定基类型 
文
本 
 
 
resident_idx 
新建住宅销售价格指数 
数
字 
 
 
commodity_house_idx 
新建商品住宅销售价格指数 
数
字 
 
 


=== 第 103 页 ===
second_hand_idx 
二手住宅销售价格指数 
数
字 
 
 
commodity_house_below90_idx 
90 平米及以下新建商品住宅销售
价格指数 
数
字 
 
 
second_hand_below90_idx 
90 平米及以下二手住宅销售价格
指数 
数
字 
 
 
commodity_house_between_90_140_idx 
90-144 平米新建商品住宅销售价
格指数 
数
字 
 
 
second_hand_between_90_140_idx 
90-144 平米二手住宅销售价格指
数 
数
字 
 
 
commodity_house_above140_idx 
144 平米以上新建商品住宅销售
价格指数 
数
字 
 
 
second_house_above140_idx 
144 平米以上二手住宅销售价格
指数 
数
字 
 
 
金融业 
人民币外汇牌价(日级) 
表名：MAC_RMB_EXCHANGE_RATE  
列名 
列
的
含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
day 
统
计
日
期 
文
本 
 
YYYY-MM-DD 
currency_id 
货
币
编
码 
文
本 
 
1-韩国元；2-土耳其里拉；3-澳大利亚元；4-瑞典克朗；5-泰国铢；6-比利时法郎；
8-丹麦克朗；10-荷兰盾；11-欧元；12-印度卢比；14-新西兰元；15-日本元；17-
西班牙比塞塔；20-挪威克朗；21-英镑；22-港币；24-法国法郎；26-新加坡元；
27-菲律宾比索；28-俄罗斯卢布；30-阿联酋迪拉姆；33-马来西亚林吉特；34-瑞士
法郎；35-新台币；36-澳门元；38-加拿大元；39-印尼卢比；40-美元；41-巴西里
亚尔；43-芬兰马克；44-南非兰特；51-沙特里亚尔 
cash_buy_rate 
现
汇
买
入
价 
数
字 
 
 
cash_buy 
现
钞
买
数
字 
 
 


=== 第 104 页 ===
入
价 
spot_sell 
现
汇
卖
出
价 
数
字 
 
 
cash_offer_prc 
现
钞
卖
出
价 
数
字 
 
 
safe_prc 
外
管
局
中
间
价 
数
字 
 
 
bank_reduced_prc 
中
行
折
算
价 
数
字 
 
 
currency_name 
货
币
名
称 
文
本 
 
 
银行间拆借利率表（日级）） 
表名：MAC_LEND_RATE 
列名 
列的
含义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
day 
日期 
文
本 
 
YYYY-MM-DD 
currency_id 
货币
编码 
文
本 
 
1-人民币；2-港币；3-美元USD；4-日本元JPY；5-英镑GBP；6-欧元；7-瑞士法郎；
16-新加坡元；20-德国马克；21-法国法郎；22-ECU；23-澳大利亚元；24-AUS 25-加
拿大元；26-西班牙比塞塔；27-意大利里拉；28-荷兰盾；29-PTE；30-XEU；31-丹麦
克朗；32-新西兰元；33-瑞典克朗 
market_id 
拆借
市场
编码 
文
本 
 
伦敦银行同业拆借利率 LIBOR；上海银行间同业拆放利率 SHIBOR；香港银行同业拆
借利率 HIBOR；新加坡银行同业拆借利率 SIBOR；中国银行同业拆借利率 CHIBOR。
宏观体系编码：1=HIBOR，2=LIBOR，3=CHIBOR，4=SIBOR，5=SHIBOR，录入值
为：1，2，3，4，5。 


=== 第 105 页 ===
term_id 
拆借
期限
编码 
文
本 
 
隔夜=20，一周=7，两周=14，三周=9，一月=1，两月=2，三月=3，四月=4,五月
=5，六月=6，七月=21，八月=22，九月=23,十月=24，十一月=25，一年=12。注意
不是每个拆借市场都支持所有的拆解周期 
interest_rate 
拆借
利率 
数
字 
 
 
currency_name 
货币
名称 
文
本 
 
 
金融机构人民币信贷资金平衡表（年度） 
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
性存款、临时性存款、委托存款、其他存款等科目。它是银行信贷资
金的主要来源。 
corporate_deposit 
金融机构
资金来源
各项存款
中单位存
款 
数
字 
 
 
personal_deposit 
金融机构
资金来源
各项存款
中个人存
款 
数
字 
 
 
fiscal_deposit 
金融机构
资金来源
各项存款
中财政性
存款 
数
字 
 
 
temporary_deposit 
金融机构
资金来源
各项存款
数
字 
 
 


=== 第 106 页 ===
中临时性
存款 
designated_deposit 
金融机构
资金来源
各项存款
中委托存
款 
数
字 
 
 
finance_bond 
金融机构
资金来源
金融债券 
数
字 
 
 
m0 
金融机构
资金来源
流通中货
币 
数
字 
 
 
finance_liability 
金融机构
资金来源
对国际金
融机构负
债 
数
字 
 
 
total_use 
金融机构
人民币信
贷资金运
用 
数
字 
 
 
total_loan 
金融机构
资金运用
各项贷款 
数
字 
 
贷款指银行或其他信贷机构根据资金必须归还的原则，按一定利率，
为企业、个人等提供资金的一种信用活动形式。我国银行贷款分为短
期贷款、中长期贷款、融资租赁、票据融资、各项垫款、境外贷款
等。 
domestic_loan 
金融机构
资金运用
各项贷款
境内贷款 
数
字 
 
 
short_term_loan 
金融机构
资金运用
各项贷款
中短期贷
款 
数
字 
 
 
medium_long_term_loan 
金融机构
资金运用
各项贷款
中中长期
贷款 
数
字 
 
 
finance_lease 
金融机构
资金运用
各项贷款
中融资租
赁 
数
字 
 
 
finance_bill 
金融机构
资金运用
数
字 
 
 


=== 第 107 页 ===
各项贷款
中票据租
赁 
advance 
金融机构
资金运用
各项贷款
中各项垫
款 
数
字 
 
 
oversea_loan 
金融机构
资金运用
各项贷款
境外贷款 
数
字 
 
 
security 
金融机构
资金运用
有价证券
及投资 
数
字 
 
 
othershare 
金融机构
资金运用
股权及其
他投资 
数
字 
 
 
bullion_purchase 
金融机构
资金运用
黄金占款 
数
字 
 
 
forex_purchase 
金融机构
资金运用
外汇占款 
数
字 
 
 
finance_assets 
金融机构
资金运用
在国际金
融机构资
产 
数
字 
 
 
货币供应量(月度) 
表名：MAC_MONEY_SUPPLY_MONTH 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
m2 
货币和准货币(M2)供应量 
数字 
 
 
m1 
货币(M1)供应量 
数字 
 
货币=流通中货币+单位活期存款 
m0 
流通中现金(M0)供应量 
数字 
 
 
m2_yoy 
货币和准货币(M2)供应量同比增长率 
数字 
 
 
m1_yoy 
货币(M1)供应量同比增长率 
数字 
 
 
m0_yoy 
流通中现金(M0)供应量同比增长率 
数字 
 
 


=== 第 108 页 ===
货币供应量(年度) 
表名：MAC_MONEY_SUPPLY_YEAR 
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
m2 
货币和准货币(M2)供应量 
数
字 
 
 
m1 
货币(M1)供应量 
数
字 
 
货币=流通中货币+单位活期存款 
m0 
流通中现金(M0)供应量 
数
字 
 
 
demond_deposit 
货币供应量中活期存款供应量 
数
字 
 
 
quosi 
准货币供应量 
数
字 
 
准货币=单位定期存款+个人存款+其他存
款 
time_deposit 
准货币供应量定期存款 
数
字 
 
 
saving_deposit 
准货币供应量储蓄存款 
数
字 
 
 
other_deposit 
准货币供应量其他存款 
数
字 
 
 
m2_yoy 
货币和准货币(M2)供应量同比增长率 
数
字 
 
 
m1_yoy 
货币(M1)供应量同比增长率 
数
字 
 
 
m0_yoy 
流通中现金(M0)供应量同比增长率 
数
字 
 
 
demond_deposit_yoy 
货币供应量中活期存款供应量同比增长
率 
数
字 
 
 
quosi_yoy 
准货币供应量同比增长率 
数
字 
 
 
time_deposit_yoy 
准货币供应量定期存款同比增长率 
数
字 
 
 
saving_deposit_yoy 
准货币供应量储蓄存款同比增长率 
数
字 
 
 
other_deposit_yoy 
准货币供应量其他存款同比增长率 
数
字 
 
 
货币当局资产负债表（年度）） 


=== 第 109 页 ===
表名：MAC_CURRENCY_STATE_YEAR 
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
total_assets 
货币当局
总资产 
数
字 
 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、
预期会给企业带来经济利益的资源。资产一般按流动性分为流动资
产和非流动资产。其中流动资产可分为货币资金、交易性金融资
产、应收票据、应收账款、预付款项、其他应收款、存货等；非流
动资产可分为长期股权投资、固定资产、无形资产及其他非流动资
产等。 
foreign_assets 
货币当局
国外资产 
数
字 
 
 
foreign_exchange 
货币当局
外汇 
数
字 
 
 
money_gold 
货币当局
货币黄金 
数
字 
 
 
other_foreign_assets 
货币当局
其他国外
资产 
数
字 
 
 
government_claim 
货币当局
对政府债
权 
数
字 
 
 
bank_claim 
货币当局
对存款货
币银行债
权 
数
字 
 
 
other_finance_claim 
货币当局
对其他金
融性公司
债权 
数
字 
 
 
non_finance_claim 
货币当局
对非金融
性公司债
权 
数
字 
 
 
other_assets 
货币当局
其他资产 
数
字 
 
 
total_liability 
货币当局
总负债 
数
字 
 
 
reserve_money 
货币当局
储蓄货币 
数
字 
 
 
currency_issue 
货币当局
储备货币
发行 
数
字 
 
 


=== 第 110 页 ===
finance_deposit 
货币当局
金融性公
司存款 
数
字 
 
 
bank_deposit 
货币当局
存款货币
银行存款 
数
字 
 
存款指企业、机关、团体或居民根据资金必须收回的原则，把货币
资金存入银行或其他信贷机构保管并取得一定利息的一种信用活动
形式。根据存款对象或性质的不同可划分为单位存款、个人存款、
财政性存款、临时性存款、委托存款、其他存款等科目。它是银行
信贷资金的主要来源。 
other_finance_deposit 
货币当局
其他金融
性公司存
款 
数
字 
 
 
non_reserve_finance_deposit 
货币当局
不计入储
备货币的
金融性公
司存款 
数
字 
 
 
bond_issue 
货币当局
发行债券 
数
字 
 
 
foreign_liability 
货币当局
国外负债 
数
字 
 
 
government_deposit 
货币当局
政府存款 
数
字 
 
 
owned_capital 
货币当局
自有资金 
数
字 
 
 
other_liability 
货币当局
其他负债 
数
字 
 
 
其他存款性公司资产负债表（年度） 
表名：MAC_OTHER_DEPOSIT 
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
total_assets 
其他存款性
公司总资产 
数
字 
 
资产指企业过去的交易或者事项形成的、由企业拥有或者控
制的、预期会给企业带来经济利益的资源。资产一般按流动
性分为流动资产和非流动资产。其中流动资产可分为货币资
金、交易性金融资产、应收票据、应收账款、预付款项、其
他应收款、存货等；非流动资产可分为长期股权投资、固定
资产、无形资产及其他非流动资产等。 


=== 第 111 页 ===
foreign_assets 
其他存款性
公司国外资
产 
数
字 
 
 
reserve_assets 
其他存款性
公司储备资
产 
数
字 
 
 
reserve_deposit 
其他存款性
公司准备金
存款 
数
字 
 
 
cash_in_vault 
其他存款性
公司库存现
金 
数
字 
 
 
government_claim 
其他存款性
公司对政府
债权 
数
字 
 
 
central_bank_claim 
其他存款性
公司对中央
银行债权 
数
字 
 
 
other_claim 
其他存款性
公司对其他
存款性公司
债权 
数
字 
 
 
other_finance_claim 
其他存款性
公司对其他
金融性公司
债权 
数
字 
 
 
non_finance_claim 
其他存款性
公司对非金
融性公司债
权 
数
字 
 
 
other_resident_claim 
其他存款性
公司对其他
居民部门债
权 
数
字 
 
 
other_assets 
其他存款性
公司其他资
产 
数
字 
 
 
total_liability 
其他存款性
公司总负债 
数
字 
 
 
non_finance_liability 
其他存款性
公司对非金
融机构及住
户负债 
数
字 
 
 
non_finance_include_broad_money 
其他存款性
公司纳入广
义货币的存
款 
数
字 
 
存款指企业、机关、团体或居民根据资金必须收回的原则，
把货币资金存入银行或其他信贷机构保管并取得一定利息的
一种信用活动形式。根据存款对象或性质的不同可划分为单
位存款、个人存款、财政性存款、临时性存款、委托存款、
其他存款等科目。它是银行信贷资金的主要来源。 


=== 第 112 页 ===
corporate_demand_deposit 
其他存款性
公司纳入广
义货币的企
业活期存款 
数
字 
 
 
corporate_time_deposit 
其他存款性
公司纳入广
义货币的企
业定期存款 
数
字 
 
 
personal_deposit 
其他存款性
公司纳入广
义货币的个
人存款 
数
字 
 
 
exclude_broad_money 
其他存款性
公司不纳入
广义货币的
存款 
数
字 
 
 
transfer_deposit 
其他存款性
公司不纳入
广义货币的
可转让存款 
数
字 
 
 
other_deposit 
其他存款性
公司不纳入
广义存款的
其他存款 
数
字 
 
 
other_non_finance_liability 
其他存款性
公司对非金
融机构及住
户负债其他
负债 
数
字 
 
 
central_bank_liability 
其他存款性
公司对中央
银行负债 
数
字 
 
 
other_deposit_liability 
其他存款性
公司对其他
存款性公司
负债 
数
字 
 
 
other_finance_liability 
其他存款性
公司对其他
金融性公司
负债 
数
字 
 
 
include_broad_money 
其他存款性
公司对其他
金融性公司
负债中计入
广义货币的
存款 
数
字 
 
 


=== 第 113 页 ===
foreign_liability 
其他存款性
公司国外负
债 
数
字 
 
 
bond_issue 
其他存款性
公司债券发
行 
数
字 
 
 
paid_in_capital 
其他存款性
公司实收资
本 
数
字 
 
 
other_liability 
其他存款性
公司其他负
债 
数
字 
 
 
社会融资规模及构成（年度） 
表名：MAC_SOCIAL_SCALE_FINANCE 
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
 
 
social_finance_scale 
社会融资规
模 
数
字 
 
社会融资规模指一定时期内实体经济从金融体系获得的资金总额，是增
量概念。主要包括：人民币贷款、外币贷款（折合人民币）、委托贷
款、信托贷款、未贴现的银行承兑汇票、企业债券、非金融企业境内股
票融资、投资性房地产、保险公司赔偿等。 
rmb_loan 
人民币贷款
社会融资规
模 
数
字 
 
 
foreign_loan 
外币贷款
(折合人民
币)社会融
资规模 
数
字 
 
 
entrust_loan 
委托贷款社
会融资规模 
数
字 
 
 
trust_loan 
信托贷款社
会融资规模 
数
字 
 
 
out_fulfilled_scale 
未贴现银行
承兑汇票社
会融资规模 
数
字 
 
 
corporate_bond_scale 
企业债券社
会融资规模 
数
字 
 
 
non_finance_scale 
非金融企业
境内股票社
会融资规模 
数
字 
 
 


=== 第 114 页 ===
证券市场基本情况（年度） 
表名：MAC_STK_MARKET 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
public_company 
境内上市公司数(A、B 股) 
数字 
 
 
public_b_company 
境内上市外资股公司数(B 股) 
数字 
 
 
public_h_company 
境外上市公司数(H 股) 
数字 
 
 
total_share 
股票总发行股本 
数字 
 
 
flow_share 
流通股本 
数字 
 
 
total_value 
股票市价总值 
数字 
 
 
flow_value 
股票流通市值 
数字 
 
 
total_trade_volume 
股票成交量 
数字 
 
 
total_trade_amount 
股票成交金额 
数字 
 
 
xshg_close 
上证综合指数 
数字 
 
 
xshe_close 
深证综合指数 
数字 
 
 
account_num 
股票有效账户数 
数字 
 
 
xshg_avg_pe 
上海平均市盈率 
数字 
 
 
xshe_avg_pe 
深圳平均市盈率 
数字 
 
 
xshg_avg_turnover 
上海平均换手率 
数字 
 
 
xshe_avg_turnover 
深圳平均换手率 
数字 
 
 
treasury_bond_issue 
国债发行额 
数字 
 
 
company_bond_issue 
企业债券发行额 
数字 
 
 
bond_amount 
债券成交额 
数字 
 
 
treasury_bond_spot_amount 
国债现货成交金额 
数字 
 
 
treasury_bond_repurchase_amount 
国债回购成交金额 
数字 
 
 
security_fund_num 
证券投资基金只数 
数字 
 
 
security_fund_cap 
证券投资基金规模 
数字 
 
 
security_fund_amount 
证券投资基金成交金额 
数字 
 
 
future_volume 
期货总成交量 
数字 
 
 
future_amount 
期货总成交额 
数字 
 
 
黄金和外汇储备（月度） 
表名：MAC_GOLD_FOREIGN_RESERVE 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_date 
统计年月 
文本 
 
YYYY-MM 
gold 
黄金储备 
数字 
 
 
foreign 
外汇储备 
数字 
 
 


=== 第 115 页 ===
股票发行量和筹资额（年度） 
表名：MAC_STK_ISSUE 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
shared_issued 
股票发行量 
数字 
 
 
a_shared_issued 
A 股发行量 
数字 
 
 
hn_shared_issued 
H 股,N 股发行量 
数字 
 
 
b_shared_issued 
B 股发行量 
数字 
 
 
stk_financing_amount 
股票筹资额 
数字 
 
 
a_stk_financing_amount 
A 股筹资额 
数字 
 
 
allot_financing_amount 
配股筹资额 
数字 
 
 
hn_stk_financing_amount 
H 股,N 股筹资额 
数字 
 
 
b_stk_financing_amount 
B 股筹资额 
数字 
 
 
股票市场统计表（年度） 
表名：MAC_STK_TRADE 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
public_company 
股票发行量 
数字 
 
 
stock_num 
上市股票数目 
数字 
 
 
a_stock_num 
A 股股票数目 
数字 
 
 
b_stock_num 
B 股股票只数 
数字 
 
 
total_share 
股票总发行股本 
数字 
亿元 
 
a_total_share 
A 股发行股本 
数字 
亿元 
 
b_total_share 
B 股发行股本 
数字 
亿元 
 
circulating_share 
流通股本 
数字 
亿元 
 
a_circulating_share 
A 股流通股本 
数字 
亿元 
 
b_circulating_share 
B 股流通股本 
数字 
亿元 
 
total_value 
股票市价总值 
数字 
亿元 
 
a_total_value 
A 股市价总值 
数字 
亿元 
 
b_total_value 
B 股市价总值 
数字 
亿元 
 
circulation_value 
股票流通市值 
数字 
亿元 
 
a_circulation_value 
A 股流通市值 
数字 
亿元 
 
b_circulation_value 
B 股流通市值 
数字 
亿元 
 
amount 
股票成交金额 
数字 
亿元 
 
a_amount 
A 股成交金额 
数字 
亿元 
 
b_amount 
B 股成交金额 
数字 
亿元 
 


=== 第 116 页 ===
volume 
总成交股数 
数字 
亿股 
 
a_volume 
A 股成交股数 
数字 
亿股 
 
b_volume 
B 股成交股数 
数字 
亿股 
 
sh_composite_index_high 
上证综合指数最高 
数字 
 
 
sh_composite_index_low 
上证综合指数最低 
数字 
 
 
sh_composite_index_close 
上证综合指数收盘 
数字 
 
 
sz_composite_index_high 
深证综合指数最高 
数字 
 
 
sz_composite_index_low 
深证综合指数最低 
数字 
 
 
sz_composite_index_close 
深证综合指数收盘 
数字 
 
 
财政政策 
国家财政收支总额及增长速度表（年度） 
表名：MAC_FISCAL_TOTAL_YEAR 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
revenue 
财政
收入 
数
字 
亿
元 
财政收入指国家财政参与社会产品分配所取得的收入，是实现国家职能的财力保证。主
要包括：（1）各项税收：包括国内增值税、国内消费税、进口货物增值税和消费税、出
口货物退增值税和消费税、营业税、企业所得税、个人所得税、资源税、城市维护建设
税、房产税、印花税、城镇土地使用税、土地增值税、车船税、船舶吨税、车辆购置
税、关税、耕地占用税、契税、烟叶税等。（2）非税收入：包括专项收入、行政事业性
收费、罚没收入和其他收入。财政收入按现行分税制财政体制划分为中央本级收入和地
方本级收入。 
expense 
财政
支出 
数
字 
亿
元 
财政支出指国家财政将筹集起来的资金进行分配使用，以满足经济建设和各项事业的需
要。主要包括：一般公共服务、外交、国防、公共安全、教育、科学技术、文化体育与
传媒、社会保障和就业、医疗卫生、环境保护、城乡社区事务、农林水事务、交通运
输、资源勘探电力信息等事务、商业服务等事务、金融监管支出、国土气象等事务、住
房保障支出、粮油物资储备管理等事务、国债付息支出等方面的支出。财政支出根据政
府在经济和社会活动中的不同职权，划分为中央财政支出和地方财政支出。 
revenue_yoy 
财政
收入
增长
速度 
数
字 
% 
 
expense_yoy 
财政
支出
增长
速度 
数
字 
% 
 


=== 第 117 页 ===
中央财政与地方财政收支及比重表（年度） 
表名：MAC_FISCAL_BALANCE_YEAR 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
revenue 
全国
财政
收入 
数
字 
亿
元 
财政收入指国家财政参与社会产品分配所取得的收入，是实现国家职能的财力保
证。主要包括：（1）各项税收：包括国内增值税、国内消费税、进口货物增值
税和消费税、出口货物退增值税和消费税、营业税、企业所得税、个人所得税、
资源税、城市维护建设税、房产税、印花税、城镇土地使用税、土地增值税、车
船税、船舶吨税、车辆购置税、关税、耕地占用税、契税、烟叶税等。（2）非
税收入：包括专项收入、行政事业性收费、罚没收入和其他收入。财政收入按现
行分税制财政体制划分为中央本级收入和地方本级收入。 
central_revenue 
中央
财政
收入 
数
字 
亿
元 
 
local_revenue 
地方
财政
收入 
数
字 
亿
元 
 
central_revenue_rate 
中央
财政
收入
比重 
数
字 
% 
 
local_revenue_rate 
地方
财政
收入
比重 
数
字 
% 
 
expense 
全国
财政
支出 
数
字 
亿
元 
财政支出指国家财政将筹集起来的资金进行分配使用，以满足经济建设和各项事
业的需要。主要包括：一般公共服务、外交、国防、公共安全、教育、科学技
术、文化体育与传媒、社会保障和就业、医疗卫生、环境保护、城乡社区事务、
农林水事务、交通运输、资源勘探电力信息等事务、商业服务等事务、金融监管
支出、国土气象等事务、住房保障支出、粮油物资储备管理等事务、国债付息支
出等方面的支出。财政支出根据政府在经济和社会活动中的不同职权，划分为中
央财政支出和地方财政支出。 
central_expense 
中央
财政
支出 
数
字 
亿
元 
 
local_expense 
地方
财政
支出 
数
字 
亿
元 
 
central_expense_rate 
中央
财政
数
字 
% 
 


=== 第 118 页 ===
支出
比重 
local_expense_rate 
地方
财政
支出
比重 
数
字 
% 
 
中央和地方财政主要收入项目情况表(年度) 
表名：MAC_FISCAL_CENTRAL_REVENUE_YEAR 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
item_id 
条目
ID 
文
本 
 
 
item_name 
条目
名称 
文
本 
 
 
revenue 
国家
财政
收入 
数
字 
亿
元 
财政收入指国家财政参与社会产品分配所取得的收入，是实现国家职能的财力保证。
主要包括：（1）各项税收：包括国内增值税、国内消费税、进口货物增值税和消费
税、出口货物退增值税和消费税、营业税、企业所得税、个人所得税、资源税、城市
维护建设税、房产税、印花税、城镇土地使用税、土地增值税、车船税、船舶吨税、
车辆购置税、关税、耕地占用税、契税、烟叶税等。（2）非税收入：包括专项收入、
行政事业性收费、罚没收入和其他收入。财政收入按现行分税制财政体制划分为中央
本级收入和地方本级收入。 
central_revenue 
中央
财政
收入 
数
字 
亿
元 
 
local_revenue 
地方
财政
收入 
数
字 
亿
元 
 
中央和地方财政主要支出项目情况表(年度) 
表名：MAC_FISCAL_CENTRAL_EXPENSE_YEAR 
列名 
列的
含义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 


=== 第 119 页 ===
stat_year 
统计
年份 
文
本 
 
YYYY 
item_id 
条目
ID 
文
本 
 
 
item_name 
条目
名称 
文
本 
 
 
expense 
国家
财政
支出 
数
字 
亿
元 
财政支出指国家财政将筹集起来的资金进行分配使用，以满足经济建设和各项事业的
需要。主要包括：一般公共服务、外交、国防、公共安全、教育、科学技术、文化体
育与传媒、社会保障和就业、医疗卫生、环境保护、城乡社区事务、农林水事务、交
通运输、资源勘探电力信息等事务、商业服务等事务、金融监管支出、国土气象等事
务、住房保障支出、粮油物资储备管理等事务、国债付息支出等方面的支出。财政支
出根据政府在经济和社会活动中的不同职权，划分为中央财政支出和地方财政支出。 
central_expense 
中央
财政
支出 
数
字 
亿
元 
 
local_expense 
地方
财政
支出 
数
字 
亿
元 
 
各项税收表（年度） 
表名：MAC_FISCAL_TAX_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
tax 
各项税收 
数字 
亿元 
 
add_value_tax 
国内增值税 
数字 
亿元 
 
business_tax 
营业税 
数字 
亿元 
 
consumption_tax 
国内消费税 
数字 
亿元 
 
tariff 
关税 
数字 
亿元 
 
individual_tax 
个人所得税 
数字 
亿元 
 
corporate_tax 
企业所得税 
数字 
亿元 
 
预算外资金分项目收支表（年度） 
表名：MAC_FISCAL_EXTRA_REVENUE_EXPENSE_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
revenue 
预算外资金收入 
数字 
亿元 
 
revenue_administration 
预算外资金收入中行政事业性收费 
数字 
亿元 
 


=== 第 120 页 ===
revenue_fund 
预算外资金收入中政府性基金收入 
数字 
亿元 
 
revenue_pool_fund 
预算外资金收入中乡镇自筹、统筹资金 
数字 
亿元 
 
revenue_local_finance 
预算外资金收入中地方财政收入 
数字 
亿元 
 
revenue_state_enterprise 
预算外资金收入中国有企业和主管部门收入 
数字 
亿元 
 
revenue_other 
预算外资金收入中其他收入 
数字 
亿元 
 
expense 
预算外资金支出 
数字 
亿元 
 
expense_pubic_service 
预算外一般公共服务资金支出 
数字 
亿元 
 
expense_education 
预算外教育资金支出 
数字 
亿元 
 
expense_security_employment 
预算外社会保障和就业资金支出 
数字 
亿元 
 
expense_transportation 
预算外交通运输资金支出 
数字 
亿元 
 
expense_community_affairs 
预算外城乡社区事务资金支出 
数字 
亿元 
 
expense_other 
预算外其他资金支出 
数字 
亿元 
 
中央财政与地方财政预算外收支表（年度） 
表名：MAC_FISCAL_EXTRAL_BALANCE_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
revenue 
全国预算外资金收入 
数字 
亿元 
 
central_revenue 
中央预算外资金收入 
数字 
亿元 
 
local_revenue 
地方预算外资金收入 
数字 
亿元 
 
expense 
全国预算外资金支出 
数字 
亿元 
 
central_expense 
中央预算外资金支出 
数字 
亿元 
 
local_expense 
地方预算外资金支出 
数字 
亿元 
 
外债余额表（年度） 
表名：MAC_FISCAL_EXTERNAL_DEBT_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
debt 
外债余额 
数字 
亿美元 
 
government_loan 
国家外债余额中外国政府贷款 
数字 
亿美元 
 
financial_organization_loan 
国家外债余额中国际金融组织贷款 
数字 
亿美元 
 
commerce_loan 
国家外债余额中国际商业贷款 
数字 
亿美元 
 
trade_credit 
国家外债余额中贸易信贷 
数字 
亿美元 
 
long_term_debt 
国家外债余额中长期债务余额 
数字 
亿美元 
 
short_term_debt 
国家外债余额中短期债务余额 
数字 
亿美元 
 


=== 第 121 页 ===
外债风险指标表（年度） 
表名：MAC_FISCAL_RISK_INDICATOR_YEAR 
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
debt_service_ratio 
国家外债偿债
率 
数
字 
% 
偿债率指偿还外债本息与当年贸易和非贸易外汇收入(国际收支口径)
之比。 
liability_ratio 
国家外债负债
率 
数
字 
% 
负债率指外债余额与当年国内生产总值之比。 
foreign_debt_ratio 
国家外债债务
率 
数
字 
% 
债务率指外债余额与当年贸易和非贸易外汇收入(国际收支口径)之
比。 
各地区财政收入表（年度） 
表名：MAC_AREA_FISCAL_REVENUE_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
general_budget 
地方财
政一般
预算收
入 
数
字 
亿
元 
地方财政一般预算收入包括增值税、营业税、企业所得税、个人所得
税、资源税、城市维护建设税、房产税、印花税、城镇土地使用税、
土地增值税、车船税、耕地占用税、契税、烟草税、其他各项税收等
税收收入和专项收入、行政事业性收费收入、罚没收入、国有资本经
营收入、国有资源（资产）有偿使用收入、其他收入等非税收入。 
tax 
地方财
政税收
收入 
数
字 
亿
元 
各项税收包括增值税、消费税、营业税、企业所得税、企业所得税退
税、个人所得税、资源税、固定资产投资方向调节税、城市维护建设
税、房产税、印花税、城镇土地使用税、土地增值税、车船税、耕地
占用税、契税、烟叶税、其他税收收入。 
add_value_tax 
地方财
政国内
增值税 
数
字 
亿
元 
 


=== 第 122 页 ===
business_tax 
地方财
政营业
税 
数
字 
亿
元 
 
corporate_income_tax 
地方财
政企业
所得税 
数
字 
亿
元 
企业所得税反映税务机关按《中华人民共和国企业所得税暂行条例》
征收的企业所得税及依照《中华人民共和国外商投资企业和外国企业
所得税法》征收的外商投资企业和外国企业所得税。税务机关对港澳
台商投资企业征收的企业所得税也包括在内。 
individual_income_tax 
地方财
政个人
所得税 
数
字 
亿
元 
个人所得税反映按照《中华人民共和国个人所得税法》、《对储蓄存
款利息所得征收个人所得税的实施办法》征收的个人所得税。 
resource_tax 
地方财
政资源
税 
数
字 
亿
元 
 
adjustment_tax 
地方财
政固定
资产投
资方向
调节税 
数
字 
亿
元 
 
maintenance_construction_tax 
地方财
政城市
维护建
设税 
数
字 
亿
元 
 
house_property_tax 
地方财
政房产
税 
数
字 
亿
元 
 
stamp_tax 
地方财
政印花
税 
数
字 
亿
元 
 
land_tax 
地方财
政城镇
土地使
用税 
数
字 
亿
元 
 
land_increment_tax 
地方财
政土地
增值税 
数
字 
亿
元 
 
vehicle_vessel_tax 
地方财
政车船
税 
数
字 
亿
元 
 
land_occupation_tax 
地方财
政耕地
占用税 
数
字 
亿
元 
 
contract_tax 
地方财
政契税 
数
字 
亿
元 
 
tobacco_tax 
地方财
政烟叶
税 
数
字 
亿
元 
 
other_tax 
地方财
政其他
数
字 
亿
元 
 


=== 第 123 页 ===
税收收
入 
non_tax 
地方财
政非税
收入 
数
字 
亿
元 
 
special 
地方财
政专项
收入 
数
字 
亿
元 
 
administration 
地方财
政行政
事业性
收费收
入 
数
字 
亿
元 
 
punishment 
地方财
政罚没
收入 
数
字 
亿
元 
 
capital_operation 
地方财
政国有
资本经
营收入 
数
字 
亿
元 
 
asset_use 
地方财
政国有
资源
(资产)
有偿使
用收入 
数
字 
亿
元 
 
other_non_tax 
地方财
政其他
非税收
入 
数
字 
亿
元 
 
各地区财政支出表（年度） 
表名：MAC_AREA_FISCAL_EXPENSE_YEAR 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 


=== 第 124 页 ===
general_budget 
地方
财政
一般
预算
支出 
数
字 
亿
元 
地方财政一般预算支出包括一般公共服务、国防、公共安全、教育、
科学技术、文化体育与传媒、社会保障就业、医疗卫生、环境保护、
城乡社区事务、农林水事务、交通运输等方面的支出。 
public_sevice 
地方
财政
一般
公共
服务
支出 
数
字 
亿
元 
一般性公共服务支出反映政府提供一般公共服务的支出。 
diplomacy 
地方
财政
外交
支出 
数
字 
亿
元 
 
defence 
地方
财政
国防
支出 
数
字 
亿
元 
 
public_security 
地方
财政
公共
安全
支出 
数
字 
亿
元 
 
education 
地方
财政
教育
支出 
数
字 
亿
元 
教育支出反映政府教育事务支出。有关具体教育事务包括教育行政管
理、学前教育、小学教育、初中教育、普通高中教育、普通高等教
育、初等职业教育、中专教育、技校教育、职业高中教育、高等职业
教育、广播电视教育、留学生教育、特殊教育、干部继续教育、教育
机关服务等。 
science_technology 
地方
财政
科学
技术
支出 
数
字 
亿
元 
科学技术支出反映用于科学技术方面的支出。 
cultural_sports_media 
地方
财政
文化
体育
与传
媒支
出 
数
字 
亿
元 
文化体育与传媒支出反映政府在文化、文物、体育、广播电视、新闻
出版等方面的支出。 
social_security_employment 
地方
财政
社会
保障
和就
业支
出 
数
字 
亿
元 
社会保障和就业支出反映政府在社会保障与就业方面的支出。有关事
项包括社会保障与就业管理事务、民政管理事务、财政对社会保险基
金的补助、补充全国社会保障基金、行政事业单位离退休、企业改革
补助、就业补助、抚恤、退役安置、社会福利、残疾人事业、城市居
民最低生活保障、其他城镇社会救济、农村社会救济、自然灾害生活
补助、红十字事务等。 


=== 第 125 页 ===
public_health 
地方
财政
医疗
卫生
支出 
数
字 
亿
元 
医疗卫生支出即地方财政一般预算内支出中的医疗卫生支出项目。指
政府医疗卫生方面的支出。具体包括医疗卫生管理事务支出、医疗服
务支出、医疗保障支出、疾病预防控制支出、卫生监督支出、妇幼保
健支出、农村卫生支出等。 
environmental_protection 
地方
财政
环境
保护
支出 
数
字 
亿
元 
 
community_affairs 
地方
财政
城乡
社区
事务
支出 
数
字 
亿
元 
城乡社区事务支出反映政府城乡社区事务支出。具体包括：城乡社区
管理事务支出、城乡社区规划与管理支出、城乡社区公共设施支出、
城乡社区住宅支出、城乡社区环境卫生支出、建设市场管理与监督支
出等。 
agriculture_forestry 
地方
财政
农林
水事
务支
出 
数
字 
亿
元 
农林水事务支出即地方财政一般预算支出中的农业支出项目。指政府
农林水事务支出，包括农业支出、林业支出、水利支出、扶贫支出、
农业综合开发支出等。 
transportation 
地方
财政
交通
运输
支出 
数
字 
亿
元 
交通运输支出反映政府交通运输方面的支出。包括公路运输支出、水
路运输支出、铁路运输支出、民用航空运输支出等。 
resource_exploration_power 
地方
财政
资源
勘探
电力
信息
等事
务支
出 
数
字 
亿
元 
 
business_service 
地方
财政
商业
服务
业等
事务
支出 
数
字 
亿
元 
 
financial_supervision 
地方
财政
金融
监管
支出 
数
字 
亿
元 
 


=== 第 126 页 ===
earthquake_reconstruction 
地方
财政
地震
灾后
重建
支出 
数
字 
亿
元 
 
land_resource_meteorology 
地方
财政
国土
资源
气象
等事
务支
出 
数
字 
亿
元 
 
housing_security 
地方
财政
住房
保障
支出
支出 
数
字 
亿
元 
 
material_reserve_management 
地方
财政
粮油
物资
储备
管理
等事
务 
数
字 
亿
元 
 
debt_interest 
地方
财政
国债
还本
付息
支出 
数
字 
亿
元 
 
other 
地方
财政
其他
支出 
数
字 
亿
元 
 
固定资产投资 
固定资产投资情况（月度） 
表名：MAC_FIXED_INVESTMENT 


=== 第 127 页 ===
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
 
 
stat_month 
统计月份 
文
本 
 
YYYY-MM 
fixed_assets_investment 
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
固定资产投资(不含农户)指城镇和农村各种登记注册类型的企业、事
业、行政单位及城镇个体户进行的计划总投资500 万元及500 万元
以上的建设项目投资和房地产开发投资，包含原口径的城镇固定资
产投资加上农村企事业组织项目投资，该口径自2011 年起开始使
用。 
state_owned 
国有及国
有控股固
定资产投
资额_累
计值 
数
字 
亿
元 
 
real_estate 
房地产开
发投资额
_累计值 
数
字 
亿
元 
房地产开发投资指各种登记注册类型的房地产开发法人单位统一开
发的包括统代建、拆迁还建的住宅、厂房、仓库、饭店、宾馆、度
假村、写字楼、办公楼等房屋建筑物，配套的服务设施，土地开发
工程(如道路、给水、排水、供电、供热、通讯、平整场地等基础设
施工程)和土地购置的投资；不包括单纯的土地开发和交易活动。 
primary 
第一产业
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
 
secondary 
第二产业
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
 
tertiary 
第三产业
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
 
centre_project 
中央项目
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
中央是指中共中央、人大常委会和国务院各部、委、局、总公司以
及直属机构直接领导的建设项目和企业、事业、行政单位。这些单
位的固定资产投资计划由国务院各部门直接编制和下达，统一组织
或委托下级实施。包括有中央垂直管理的部门(如国家统计局各级调
查队)和中央直属企业、事业单位(如工商银行、中国电信、中国石
油)等。 
local_project 
地方项目
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
地方是由省(自治区、直辖市)、地(区、市、州、盟)、县(区、市、
旗)三级政府及业务主管部门直接领导和管理的建设项目、企业、事
业、行政单位。地方项目还包括不隶属以上各级政府及主管部门的
建设项目和企业、事业单位，如外商投资企业和无主管部门的企业
等。 


=== 第 128 页 ===
new_construct 
新建固定
资产投资
完成额_
累计值 
数
字 
亿
元 
新建指从无到有“平地起家”开始建设的项目。现有企业、事业、行
政单位投资的项目一般不属于新建。但如有的单位原有基础很小，
经过建设后新增的固定资产价值超过该企业、事业、行政单位原有
固定资产价值(原值)三倍以上的，也应作为新建。 
expand 
扩建固定
资产投资
完成额_
累计值 
数
字 
亿
元 
扩建指在厂内或其他地点，为扩大原有产品的生产能力(或效益)或增
加新的产品生产能力，而增建的生产车间(或主要工程)、分厂、独立
的生产线的企业、事业单位。行政、事业单位在原单位增建业务性
用房(如学校增建教学用房、医院增建门诊部、病房等)也作为扩建。
现有企、事业单位为扩大原有主要产品生产能力或增加新的产品生
产能力，增建一个或几个主要生产车间(或主要工程)、分厂，同时进
行一些更新改造工程的，也应作为扩建。 
reconstruct 
改建固定
资产投资
完成额_
累计值 
数
字 
亿
元 
改建和技术改造指现有企业、事业单位对原有设施进行技术改造或
更新(包括相应配套的辅助性生产、生活福利设施)的建设项目。改建
项目包括现有企业、事业单位为适应市场变化的需要，而改变企业
的主要产品种类(如军工企业转民产品等)的建设项目，原有产品生产
作业线由于各工序(车间)之间能力不平衡，为填平补齐充分发挥原有
生产能力而增建不增加本企业主要产品设计能力的车间的建设项
目。技术改造是指企业、事业单位在现有基础上，用先进的技术代
替落后的技术，用先进的工艺和装备代替落后的工艺和装备，以改
变企业落后的技术经济面貌，实现以内涵为主的扩大再生产，达到
提高产品质量、促进产品更新换代、节约能源、降低消耗、扩大生
产规模、全面提高社会经济效益的目的。技术改造具体包括以下内
容：机器设备和工具的更新改造；生产工艺改革、节约能源和原材
料的改造；厂房建筑和公共设施的改造；保护环境进行的“三废”治
理改造；劳动条件和生产环境的改造等。 
construct_install 
建筑安装
工程固定
资产投资
完成额_
累计值 
数
字 
亿
元 
建筑工程指各种房屋、建筑物的建造工程，又称建筑工作量。这部
分投资额必须兴工动料，通过施工活动才能实现，是固定资产投资
额的重要组成部分。安装工程指各种设备、装置的安装工程，又称
安装工作量。在安装工程中，不包括被安装设备本身价值。 
equipment_purchase 
设备工器
具购置固
定资产投
资完成额
_累计值 
数
字 
亿
元 
设备工具器具购置指报告期内购置或自制的，达到固定资产标准的
设备、工具、器具的价值。新建单位及扩建单位的新建车间，按照
设计或计划要求购置或自制的全部设备、工具、器具，不论是否达
到固定资产标准均计入“设备工具器具购置”中。 
other_expense 
其他费用
固定资产
投资完成
额_累计
值 
数
字 
亿
元 
其他费用指在固定资产建造和购置过程中发生的，除建筑安装工程
和设备、工器具购置投资完成额以外的应当分摊计入固定资产投资
的费用，不指经营中财务上的其他费用。 
construct_area 
房屋施工
面积_累
计值(万平
方米) 
数
字 
万
平
方
米 
房屋施工面积指报告期内施工的全部房屋建筑面积。包括本期新开
工的面积、上期跨入本期继续施工的房屋面积、上期停缓建在本期
恢复施工的房屋面积、本期竣工的房屋面积以及本期施工后又停缓
建的房屋面积。多层建筑应填各层建筑面积之和。 
resident_complete_area 
房屋竣工
面积_累
计值(万平
方米) 
数
字 
万
平
方
米 
房屋竣工面积报告期内房屋建筑按照设计要求已全部完工，达到住
人和使用条件，经验收鉴定合格或达到竣工验收标准，可正式移交
使用的各栋房屋建筑面积的总和。 


=== 第 129 页 ===
new_fixed_assets 
新增固定
资产_累
计值 
数
字 
亿
元 
新增固定资产是指已经完成建造和购置过程，并已交付生产或使用
单位的固定资产的价值，包括已经建成投入生产或交付使用的工程
投资和达到固定资产标准的设备、工具、器具的投资及有关应摊入
的费用。该指标是表示固定资产投资成果的价值指标，也是反映建
设进度，计算固定资产投资效果的重要指标。 
fixed_assets_investment_yoy 
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
state_owned_yoy 
国有及国
有控股固
定资产投
资额_累
计增长 
数
字 
% 
 
real_estate_yoy 
房地产开
发投资额
_累计增
长 
数
字 
% 
 
primary_yoy 
第一产业
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
secondary_yoy 
第二产业
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
tertiary_yoy 
第三产业
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
centre_project_yoy 
中央项目
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
local_project_yoy 
地方项目
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
new_construct_yoy 
新建固定
资产投资
完成额_
累计增长 
数
字 
% 
 


=== 第 130 页 ===
expand_yoy 
扩建固定
资产投资
完成额_
累计增长 
数
字 
% 
 
reconstruct_yoy 
改建固定
资产投资
完成额_
累计增长 
数
字 
% 
 
construct_install_yoy 
建筑安装
工程固定
资产投资
完成额_
累计增长 
数
字 
% 
 
equipment_purchase_yoy 
设备工器
具购置固
定资产投
资完成额
_累计增
长 
数
字 
% 
 
other_expense_yoy 
其他费用
固定资产
投资完成
额_累计
增长 
数
字 
% 
 
construct_area_yoy 
房屋施工
面积_累
计增长 
数
字 
% 
 
resident_complete_area_yoy 
房屋竣工
面积_累
计增长 
数
字 
% 
 
new_fixed_assets_yoy 
新增固定
资产_累
计增长 
数
字 
% 
 
分地区固定资产投资情况（月度） 
表名：MAC_AREA_FIXED_INVESTMENT 
列名 
列的含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_month 
统计月
份 
文
本 
 
YYYY-MM 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 


=== 第 131 页 ===
area_name 
地区名
称 
文
本 
 
 
fixed_assets_investment 
固定资
产投资
完成额
_累计
值 
数
字 
亿
元 
固定资产投资(不含农户)指城镇和农村各种登记注册类型的企业、事
业、行政单位及城镇个体户进行的计划总投资500 万元及500 万元以上
的建设项目投资和房地产开发投资，包含原口径的城镇固定资产投资加
上农村企事业组织项目投资，该口径自2011 年起开始使用。 
construct_install 
建筑安
装工程
固定资
产投资
完成额
_累计
值 
数
字 
亿
元 
建筑工程指各种房屋、建筑物的建造工程，又称建筑工作量。这部分投
资额必须兴工动料，通过施工活动才能实现，是固定资产投资额的重要
组成部分。安装工程指各种设备、装置的安装工程，又称安装工作量。
在安装工程中，不包括被安装设备本身价值。 
equipment_purchase 
设备工
器具购
置固定
资产投
资完成
额_累
计值 
数
字 
亿
元 
设备工具器具购置指报告期内购置或自制的，达到固定资产标准的设
备、工具、器具的价值。新建单位及扩建单位的新建车间，按照设计或
计划要求购置或自制的全部设备、工具、器具，不论是否达到固定资产
标准均计入“设备工具器具购置”中。 
other_expense 
其他费
用固定
资产投
资完成
额_累
计值 
数
字 
亿
元 
其他费用指在固定资产建造和购置过程中发生的，除建筑安装工程和设
备、工器具购置投资完成额以外的应当分摊计入固定资产投资的费用，
不指经营中财务上的其他费用。 
resident_construct 
住宅建
设投资
额_累
计值 
数
字 
亿
元 
 
construct_area 
住宅施
工面积
_累计
值 
数
字 
亿
元 
住宅指专供居住的房屋，包括别墅、公寓、职工家属宿舍和集体宿舍
(包括职工单身宿舍和学生宿舍)等。但不包括住宅楼中作为人防用、不
住人的地下室等。住宅按照用途可以划分为经济适用住房和别墅、高档
公寓等。按照户型结构可以划分为90 平方米以下住房，144 平方米以
上住房等。房屋施工面积指报告期内施工的全部房屋建筑面积。包括本
期新开工的面积、上期跨入本期继续施工的房屋面积、上期停缓建在本
期恢复施工的房屋面积、本期竣工的房屋面积以及本期施工后又停缓建
的房屋面积。多层建筑应填各层建筑面积之和。 
resident_complete 
住宅竣
工面积
_累计
值 
数
字 
亿
元 
住宅指专供居住的房屋，包括别墅、公寓、职工家属宿舍和集体宿舍
(包括职工单身宿舍和学生宿舍)等。但不包括住宅楼中作为人防用、不
住人的地下室等。住宅按照用途可以划分为经济适用住房和别墅、高档
公寓等。按照户型结构可以划分为90 平方米以下住房，144 平方米以
上住房等。房屋施工面积指报告期内施工的全部房屋建筑面积。包括本
期新开工的面积、上期跨入本期继续施工的房屋面积、上期停缓建在本
期恢复施工的房屋面积、本期竣工的房屋面积以及本期施工后又停缓建
的房屋面积。多层建筑应填各层建筑面积之和。 


=== 第 132 页 ===
construct_num 
施工项
目项目
个数_
累计值 
数
字 
个 
 
new_construct_num 
新开工
项目项
目个数
_累计
值 
数
字 
个 
 
fixed_assets_investment_yoy 
固定资
产投资
完成额
_累计
增长 
数
字 
% 
 
construct_install_yoy 
建筑安
装工程
固定资
产投资
完成额
_累计
增长 
数
字 
% 
 
equipment_purchase_yoy 
设备工
器具购
置固定
资产投
资完成
额_累
计增长 
数
字 
% 
 
other_expense_yoy 
其他费
用固定
资产投
资完成
额_累
计增长 
数
字 
% 
 
resident_construct_yoy 
住宅建
设投资
额_累
计增长 
数
字 
% 
 
construct_area_yoy 
住宅施
工面积
_累计
增长 
数
字 
% 
 
resident_complete_yoy 
住宅竣
工面积
_累计
增长 
数
字 
% 
 
construct_num_yoy 
施工项
目项目
数
字 
% 
施工项目个数是指本年正式进行过建筑或安装施工活动的建设项目个
数。包括本年新开工项目，以前年度开工跨入本年继续施工项目，本年


=== 第 133 页 ===
个数_
累计增
减额 
全部建成投产项目、以前年度全部停缓建在本年恢复施工的项目，本年
进行过施工又在本年内全部停缓建的项目。施工项目个数可以反映一定
时期固定资产投资的实际规模，与同期全部建成投产项目个数相比，可
以从建设速度的角度反映固定资产投资的效果。 
new_construct_num_yoy 
新开工
项目项
目个数
_累计
增减额 
数
字 
% 
 
分行业固定资产投资情况（月度） 
表名：MAC_INDUSTRY_FIXED_INVEST 
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
 
 
stat_month 
统计月份 
文
本 
 
YYYY-MM 
item_name 
条目名称 
文
本 
 
 
investment_value 
该条目固
定资产投
资额_累计
值 
数
字 
亿
元 
固定资产投资(不含农户)指城镇和农村各种登记注册类型的企业、事业、行政
单位及城镇个体户进行的计划总投资500 万元及500 万元以上的建设项目投资
和房地产开发投资，包含原口径的城镇固定资产投资加上农村企事业组织项目
投资，该口径自2011 年起开始使用。 
investment_perc 
该条目固
定资产投
资额_累计
增长 
数
字 
% 
 
按注册类型登记分固定资产投资（月度） 
表名：MAC_REGISTERED_FIXED_INVESTMENT 
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
 
 
stat_month 
统计月份 
文
本 
 
YYYY-MM 
item_name 
条目名称 
文
本 
 
 


=== 第 134 页 ===
investment_value 
该条目固
定资产投
资额_累计
值 
数
字 
亿
元 
固定资产投资(不含农户)指城镇和农村各种登记注册类型的企业、事业、行政
单位及城镇个体户进行的计划总投资500 万元及500 万元以上的建设项目投资
和房地产开发投资，包含原口径的城镇固定资产投资加上农村企事业组织项目
投资，该口径自2011 年起开始使用。 
investment_perc 
该条目固
定资产投
资额_累计
增长 
数
字 
% 
 
固定资产投资情况表(年度) 
表名：MAC_FIXED_INVESTMENT_YEAR 
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
fixed_investment 
全社会固定
资产投资 
数
字 
亿
元 
固定资产投资(不含农户)指城镇和农村各种登记注册类型的企业、事
业、行政单位及城镇个体户进行的计划总投资500 万元及500 万元以
上的建设项目投资和房地产开发投资，包含原口径的城镇固定资产投
资加上农村企事业组织项目投资，该口径自2011 年起开始使用。 
urban_fixed_investment 
城镇固定资
产投资 
数
字 
亿
元 
 
mainland 
内资企业全
社会固定资
产投资 
数
字 
亿
元 
 
state_owned 
国有全社会
固定资产投
资 
数
字 
亿
元 
 
collective 
集体全社会
固定资产投
资 
数
字 
亿
元 
 
joint_stock 
股份合作全
社会固定资
产投资 
数
字 
亿
元 
 
joint_owned 
联营全社会
固定资产投
资 
数
字 
亿
元 
 
limited 
有限责任公
司全社会固
定资产投资 
数
字 
亿
元 
 
stock 
股份有限公
司全社会固
定资产投资 
数
字 
亿
元 
 


=== 第 135 页 ===
private 
私营全社会
固定资产投
资 
数
字 
亿
元 
 
individual 
个体全社会
固定资产投
资 
数
字 
亿
元 
 
others 
其他全社会
固定资产投
资 
数
字 
亿
元 
 
hkmt 
港、澳、台
商投资全社
会固定资产
投资 
数
字 
亿
元 
 
foreign 
外商投资全
社会固定资
产投资 
数
字 
亿
元 
 
state_budget 
全社会固定
资产投资中
国家预算内
资金 
数
字 
亿
元 
 
domestic_loan 
全社会固定
资产投资中
国内贷款 
数
字 
亿
元 
 
foreign_investment 
全社会固定
资产投资中
利用外资 
数
字 
亿
元 
 
self_raised_fund 
全社会固定
资产投资中
自筹资金 
数
字 
亿
元 
 
other_fund 
全社会固定
资产投资中
其他资金 
数
字 
亿
元 
 
construct_install 
全社会固定
资产投资中
建筑安装工
程 
数
字 
亿
元 
 
equipment_purchase 
全社会固定
资产投资中
设备工具器
具购置 
数
字 
亿
元 
 
other_expense 
全社会固定
资产投资中
其它费用 
数
字 
亿
元 
 
对外贸易 


=== 第 136 页 ===
货物进出口总额表（年度） 
表名：MAC_TRADE_VALUE_YEAR 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
total_rmb 
进出
口总
额(人
民币) 
数
字 
亿
元 
货物进出口总额指实际进出我国国境的货物总金额。包括对外贸易实际进出口货物，
来料加工装配进出口货物，国家间、联合国及国际组织无偿援助物资和赠送品，华
侨、港澳台同胞和外籍华人捐赠品，租赁期满归承租人所有的租赁货物，进料加工进
出口货物，边境地方贸易及边境地区小额贸易进出口货物(边民互市贸易除外)，中外
合资企业、中外合作经营企业、外商独资经营企业进出口货物和公用物品，到、离岸
价格在规定限额以上的进出口货样和广告品(无商业价值、无使用价值和免费提供出
口的除外)，从保税仓库提取在中国境内销售的进口货物，以及其他进出口货物。该
指标用以观察一个国家在对外贸易方面的总规模。我国规定出口货物按离岸价格统
计，进口货物按到岸价格统计。 
export_rmb 
出口
总额
(人民
币) 
数
字 
亿
元 
 
import_rmb 
进口
总额
(人民
币) 
数
字 
 
 
balance_rmb 
进出
口差
额(人
民币) 
数
字 
亿
元 
差额＝出口额-进口额 
total_dollar 
进出
口总
额(美
元) 
数
字 
百
万
美
元 
 
export_dollar 
出口
总额
(美元) 
数
字 
百
万
美
元 
 
import_dollar 
进口
总额
(美元) 
数
字 
百
万
美
元 
 
balance_dollar 
进出
口差
数
字 
百
万
差额＝出口额-进口额 


=== 第 137 页 ===
额(美
元) 
美
元 
海关进出口货物分类金额表（年度） 
表名：MAC_TRADE_VALUE_SITC_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
item_id 
条目ID 
文本 
 
 
item_name 
条目名称 
文本 
 
 
export_dollar 
出口总额 
数字 
百万美元 
 
import_dollar 
进口总额 
数字 
百万美元 
 
地区按经营单位所在地分货物进出口总额表（年度） 
表名：MAC_TRADE_VALUE_LOCATION_YEAR 
列名 
列的含义 
类
型 
单位 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
total_dollar 
经营单位所在地
进出口总额 
数
字 
千美
元 
商品经营单位所在地进出口额指在所在地海关注册登记的有进出口经营
权的企业实际进、出口额。 
export_dollar 
经营单位所在地
出口总额 
数
字 
千美
元 
 
import_dollar 
经营单位所在地
进口总额 
数
字 
千美
元 
 
各地区按境内目的地和货源地分货物进出口总额表（年度） 
表名：MAC_TRADE_VALUE_DESTINATION_YEAR 


=== 第 138 页 ===
列名 
列的含义 
类
型 
单位 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
total_dollar 
境内目的地和货源地进出口
总额 
数
字 
千美
元 
 
export_dollar 
境内目的地和货源地出口总
额 
数
字 
千美
元 
货源地出口额指出口货物的产地或原始发货地的实际出口
额。 
import_dollar 
境内目的地和货源地进口总
额 
数
字 
千美
元 
目的地进口额指进口货物的消费、使用或最终抵运地的实际
进口额 
利用外资情况表（月度） 
表名：MAC_FOREIGN_CAPITAL_MONTH 
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
 
 
stat_month 
统计月份 
文
本 
 
YYYY-MM 
num_acc 
外商直接投资
合同项目数_
累计值 
数
字 
个 
 
num_acc_yoy 
外商直接投资
合同项目数_
累计增长 
数
字 
% 
 
joint_num_acc 
合资经营企业
外商直接投资
合同项目数_
累计值 
数
字 
个 
中外合资经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合资经营企业法》及有关法律的规定，
按合同规定的比例投资设立，分享利润和分担风险的企业。 
joint_num_acc_yoy 
合资经营企业
外商直接投资
合同项目数_
累计增长 
数
字 
% 
中外合资经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合资经营企业法》及有关法律的规定，
按合同规定的比例投资设立，分享利润和分担风险的企业。 
cooperative_num_acc 
合作经营企业
外商直接投资
合同项目数_
累计值 
数
字 
个 
中外合作经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合作经营企业法》及有关法律的规定，
依照合作合同的约定进行投资或提供条件设立，分配利润、分
担风险和亏损的企业。 


=== 第 139 页 ===
cooperative_num_acc_yoy 
合作经营企业
外商直接投资
合同项目数_
累计增长 
数
字 
% 
中外合作经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合作经营企业法》及有关法律的规定，
依照合作合同的约定进行投资或提供条件设立，分配利润、分
担风险和亏损的企业。 
foreign_num_acc 
外资企业外商
直接投资合同
项目数_累计
值 
数
字 
个 
外商独资企业指依照《中华人民共和国外资企业法》及有关法
律的规定，在中国内地由外国投资者全额投资设立的企业 
foreign_num_acc_yoy 
外资企业外商
直接投资合同
项目数_累计
增长 
数
字 
% 
外商独资企业指依照《中华人民共和国外资企业法》及有关法
律的规定，在中国内地由外国投资者全额投资设立的企业 
foreign_share_num_acc 
外商投资股份
制企业外商直
接投资合同项
目数_累计值 
数
字 
个 
外商投资股份有限公司指根据国家有关规定，经商务部（原外
经贸部）批准设立，并且其中外资的股本占公司注册资本的比
例达25%以上的股份有限公司。凡其中外资股本占公司注册资
本的比例小于25%的，属于内资中的股份有限公司。 
foreign_share_num_acc_yoy 
外商投资股份
制企业外商直
接投资合同项
目数_累计增
长 
数
字 
% 
外商投资股份有限公司指根据国家有关规定，经商务部（原外
经贸部）批准设立，并且其中外资的股本占公司注册资本的比
例达25%以上的股份有限公司。凡其中外资股本占公司注册资
本的比例小于25%的，属于内资中的股份有限公司。 
value_acc 
实际利用外商
直接投资金额
_累计值 
数
字 
百
万
美
元 
外商直接投资指外国投资者在我国境内通过设立外商投资企
业、合伙企业、与中方投资者共同进行石油资源的合作勘探开
发以及设立外国公司分支机构等方式进行投资。外国投资者可
以用现金、实物、技术等投资，还可以用从外商投资企业获得
的利润进行再投资。 
value_acc_yoy 
实际利用外商
直接投资金额
_累计增长 
数
字 
% 
外商直接投资指外国投资者在我国境内通过设立外商投资企
业、合伙企业、与中方投资者共同进行石油资源的合作勘探开
发以及设立外国公司分支机构等方式进行投资。外国投资者可
以用现金、实物、技术等投资，还可以用从外商投资企业获得
的利润进行再投资。 
joint_value_acc 
合资经营企业
实际利用外商
直接投资金额
_累计值 
数
字 
百
万
美
元 
中外合资经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合资经营企业法》及有关法律的规定，
按合同规定的比例投资设立，分享利润和分担风险的企业。 
joint_value_acc_yoy 
合资经营企业
实际利用外商
直接投资金额
_累计增长 
数
字 
% 
中外合资经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合资经营企业法》及有关法律的规定，
按合同规定的比例投资设立，分享利润和分担风险的企业。 
cooperative_value_acc 
合作经营企业
实际利用外商
直接投资金额
_累计值 
数
字 
百
万
美
元 
中外合作经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合作经营企业法》及有关法律的规定，
依照合作合同的约定进行投资或提供条件设立，分配利润、分
担风险和亏损的企业。 
cooperative_value_acc_yoy 
合作经营企业
实际利用外商
直接投资金额
_累计增长 
数
字 
% 
中外合作经营企业指外国企业或外国人与中国内地企业依照
《中华人民共和国中外合作经营企业法》及有关法律的规定，
依照合作合同的约定进行投资或提供条件设立，分配利润、分
担风险和亏损的企业。 


=== 第 140 页 ===
foreign_value_acc 
外资企业实际
利用外商直接
投资金额_累
计值 
数
字 
百
万
美
元 
外商独资企业指依照《中华人民共和国外资企业法》及有关法
律的规定，在中国内地由外国投资者全额投资设立的企业。 
foreign_value_acc_yoy 
外资企业实际
利用外商直接
投资金额_累
计增长 
数
字 
% 
外商独资企业指依照《中华人民共和国外资企业法》及有关法
律的规定，在中国内地由外国投资者全额投资设立的企业。 
foreign_share_value_acc 
外商投资股份
制企业实际利
用外商直接投
资金额_累计
值 
数
字 
百
万
美
元 
外商投资股份有限公司指根据国家有关规定，经商务部（原外
经贸部）批准设立，并且其中外资的股本占公司注册资本的比
例达25%以上的股份有限公司。凡其中外资股本占公司注册资
本的比例小于25%的，属于内资中的股份有限公司。 
foreign_share_value_acc_yoy 
外商投资股份
制企业实际利
用外商直接投
资金额_累计
增长 
数
字 
% 
外商投资股份有限公司指根据国家有关规定，经商务部（原外
经贸部）批准设立，并且其中外资的股本占公司注册资本的比
例达25%以上的股份有限公司。凡其中外资股本占公司注册资
本的比例小于25%的，属于内资中的股份有限公司。 
利用外资概况表（年度） 
表名：MAC_FOREIGN_CAPITAL_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
total_invest_value 
实际利
用外资
额 
数
字 
万
美
元 
实际使用外资金额指批准的合同外资金额的实际执行数，外国投资者
根据批准外商投资企业的合同(章程)的规定实际缴付的出资额和企业投
资总额内外国投资者以自己的境外自有资金实际直接向企业提供的贷
款。 
invest_value 
实际利
用外商
直接投
资金额 
数
字 
万
美
元 
外商直接投资指外国投资者在我国境内通过设立外商投资企业、合伙
企业、与中方投资者共同进行石油资源的合作勘探开发以及设立外国
公司分支机构等方式进行投资。外国投资者可以用现金、实物、技术
等投资，还可以用从外商投资企业获得的利润进行再投资 
other_invest_value 
实际利
用外商
其他投
资额 
数
字 
万
美
元 
外商其他投资指除对外借款和外商直接投资以外的各种利用外资的形
式。包括企业在境内外股票市场公开发行的以外币计价的股票发行价
总额，国际租赁进口设备的应付款，补偿贸易中外商提供的进口设
备、技术、物料的价款，加工装配贸易中外商提供的进口设备、物料
的价款。 
total_contract_project_num 
合同利
用外资
项目 
数
字 
个 
 


=== 第 141 页 ===
total_contract_invest_value 
合同利
用外资
额 
数
字 
万
美
元 
 
contract_project_num 
合同利
用外商
直接投
资项目 
数
字 
个 
 
contract_invest_value 
合同利
用外商
直接投
资金额 
数
字 
万
美
元 
外商直接投资指外国投资者在我国境内通过设立外商投资企业、合伙
企业、与中方投资者共同进行石油资源的合作勘探开发以及设立外国
公司分支机构等方式进行投资。外国投资者可以用现金、实物、技术
等投资，还可以用从外商投资企业获得的利润进行再投资。 
contract_other_invest_value 
合同利
用外商
其他投
资额 
数
字 
万
美
元 
外商其他投资指除对外借款和外商直接投资以外的各种利用外资的形
式。包括企业在境内外股票市场公开发行的以外币计价的股票发行价
总额，国际租赁进口设备的应付款，补偿贸易中外商提供的进口设
备、技术、物料的价款，加工装配贸易中外商提供的进口设备、物料
的价款。 
按行业分对外直接投资情况表（年度） 
表名：MAC_INDUSTRY_OFDI_YEAR 
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
item_id 
条目ID 
文
本 
 
 
item_name 
条目名称 
文
本 
 
 
invest 
对外直接投资
额 
数
字 
万
美
元 
对外直接投资净额指境内投资主体对外直接投资额中扣除反向投资额后的
净额，当期对外直接投资净额简称流量，对外直接投资累计净额简称存
量。 
accumulation 
截至本年底对
外直接投资存
量 
数
字 
万
美
元 
对外直接投资净额指境内投资主体对外直接投资额中扣除反向投资额后的
净额，当期对外直接投资净额简称流量，对外直接投资累计净额简称存
量。 
分国别对外外直接投资情况表（年度） 
表名：MAC_NATION_OFDI 
列名 
列的含义 
类
型 
单
位 
说明 


=== 第 142 页 ===
id 
id 
数
字 
 
 
stat_year 
统计年份 
文
本 
 
YYYY 
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
invest 
对外直接投
资额 
数
字 
万
美
元 
对外直接投资净额指境内投资主体对外直接投资额中扣除反向投资额后的净
额，当期对外直接投资净额简称流量，对外直接投资累计净额简称存量。 
accumulation 
截至本年底
对外直接投
资存量 
数
字 
万
美
元 
对外直接投资净额指境内投资主体对外直接投资额中扣除反向投资额后的净
额，当期对外直接投资净额简称流量，对外直接投资累计净额简称存量。 
分地区外商投资企业年底注册登记情况表（年度） 
表名：MAC_AREA_FOREIGN_REGISTER 
列名 
列的含义 
类
型 
单位 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
enterprise_num 
外商投资企业
数 
数
字 
户 
外商投资指我国政府、部门、企业和其他经济组织通过吸收外商直接投
资以及其他方式筹措的境外现汇、技术、设备等。 
invest 
外商投资企业
投资总额 
数
字 
百万
美元 
 
registered_capital 
外商投资企业
注册资本 
数
字 
百万
美元 
 
foreign_registered 
外方外商投资
企业注册资本 
数
字 
百万
美元 
 
按行业分外商投资企业年底注册登记情况表（年度） 
表名：MAC_INDUSTRY_FOREIGN_REGISTER 
列名 
列的含义 
类
型 
单位 
说明 


=== 第 143 页 ===
id 
id 
数
字 
 
 
stat_year 
统计年份 
文
本 
 
YYYY 
item_id 
条目ID 
文
本 
 
 
item_name 
条目名称 
文
本 
 
 
enterprise_num 
外商投资企业数 
数
字 
户 
外商投资指我国政府、部门、企业和其他经济组织通过吸收外商直
接投资以及其他方式筹措的境外现汇、技术、设备等。 
invest 
外商投资企业投
资总额 
数
字 
百万
美元 
 
registered_capital 
外商投资企业注
册资本 
数
字 
百万
美元 
 
foreign_registered 
外方外商投资企
业注册资本 
数
字 
百万
美元 
 
对外经济合作表（年度） 
表名：MAC_FOREIGN_COOPERATE_YEAR 
列名 
列的
含义 
类
型 
单
位 
示
例 
说明 
id 
id 
数
字 
 
 
 
stat_year 
统计
年份 
文
本 
 
 
YYYY 
project_contract_num 
对外
承包
工程
合同
数 
数
字 
份 
 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是
指中国的企业或者其他单位承包境外建设工程项目的活动。对外
承包工程项目分为十一大类：房屋建筑项目、工业建设项目、制
造加工设施建设项目、水利建设项目、废水（物）处理项目、交
通运输建设项目、危险品处理项目、电力工程建设项目、石油化
工项目、通讯工程项目、其他。 
project_value 
对外
承包
工程
合同
金额 
数
字 
亿
美
元 
 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是
指中国的企业或者其他单位承包境外建设工程项目的活动。新签
合同额指企业在报告期内签订的合法有效的对外承包工程项目合
同的金额。 
project_turnover 
对外
承包
工程
完成
营业
额 
数
字 
亿
美
元 
 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是
指中国的企业或者其他单位承包境外建设工程项目的活动。完成
营业额指企业在报告期内完成的以货币形式表现的工作量。 
project_abroad_person_num 
对外
承包
数
字 
人 
 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是
指中国的企业或者其他单位承包境外建设工程项目的活动。期末


=== 第 144 页 ===
工程
年末
在外
人数 
在外人数指报告期末企业在国(境)外执行对外承包工程和劳务合作
项目的人数。 
labour_dispatch_num 
对外
劳务
合作
派出
劳务
人数 
数
字 
人 
 
对外劳务合作指组织劳务人员赴其他国家或地区为国外的企业或
机构工作的经营性活动。派出人数指企业在报告期内派往国(境)外
执行对外承包工程和劳务合作项目的人数。 
labour_abroad_person_num 
对外
劳务
合作
年末
在外
人数 
数
字 
人 
 
对外劳务合作指组织劳务人员赴其他国家或地区为国外的企业或
机构工作的经营性活动。期末在外人数指报告期末企业在国(境)外
执行对外承包工程和劳务合作项目的人数。 
按国别对外经济合作表（年度） 
表名：MAC_NATION_COOPERATE_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
project_turnover 
对外承
包工程
完成营
业额 
数
字 
万
美
元 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是指中
国的企业或者其他单位承包境外建设工程项目的活动。完成营业额指
企业在报告期内完成的以货币形式表现的工作量。 
project_dispatch_num 
对外承
包工程
派出劳
务人数 
数
字 
人 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是指中
国的企业或者其他单位承包境外建设工程项目的活动。期末在外人数
指报告期末企业在国(境)外执行对外承包工程和劳务合作项目的人
数。 
project_abroad_person_num 
对外承
包工程
年末在
外人数 
数
字 
人 
对外承包工程根据《对外承包工程管理条例》，对外承包工程是指中
国的企业或者其他单位承包境外建设工程项目的活动。期末在外人数
指报告期末企业在国(境)外执行对外承包工程和劳务合作项目的人
数。 
labour_dispatch_num 
对外劳
务合作
数
字 
人 
对外劳务合作指组织劳务人员赴其他国家或地区为国外的企业或机构
工作的经营性活动。派出人数指企业在报告期内派往国(境)外执行对
外承包工程和劳务合作项目的人数。 


=== 第 145 页 ===
派出劳
务人数 
labour_abroad_person_num 
对外劳
务合作
年末在
外人数 
数
字 
人 
对外劳务合作指组织劳务人员赴其他国家或地区为国外的企业或机构
工作的经营性活动。期末在外人数指报告期末企业在国(境)外执行对
外承包工程和劳务合作项目的人数。 
景气指数 
宏观经济景气指数（月度） 
表名：MAC_ECONOMIC_BOOM_IDX 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
early_warning_idx 
预警指数 
数字 
 
 
consistency_idx 
一致指数 
数字 
 
 
leading_idx 
先行指数 
数字 
 
 
lagging_idx 
滞后指数 
数字 
 
 
消费者景气指数（月度） 
表名：MAC_CONSUMER_BOOM_IDX 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
expectation_idx 
消费者预期指数 
数字 
 
 
satisfaction_idx 
消费者满意指数 
数字 
 
 
confidence_idx 
消费者信心指数 
数字 
 
 
宏观经济景气预警指数（月度） 
表名：MAC_BOOM_WARNING_IDX 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
warning_idx 
预警指数信号 
数字 
 
 


=== 第 146 页 ===
industry_idx_sgn 
工业生产指数信号 
数字 
 
 
fixed_assets_sgn 
固定资产投资信号 
数字 
 
 
rpi_sgn 
消费品零售总额信号 
数字 
 
 
import_export_sgn 
进出口总额信号 
数字 
 
 
gov_revenue_sgn 
财政收入信号 
数字 
 
 
industry_profit_sgn 
工业企业利润信号 
数字 
 
 
resident_dpi_sgn 
居民可支配收入信号 
数字 
 
 
loan_sgn 
金融机构各项贷款信号 
数字 
 
 
m2_sgn 
货币供应M2 信号 
数字 
 
 
cpi_sgn 
居民消费价格指数信号 
数字 
 
 
企业景气及企业家信心指数（季度）） 
表名：MAC_ENTERPRISE_BOOM_CONFIDENCE_IDX 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_quarter 
统计季度 
文本 
 
YYYY-MM 
boom_idx 
企业景气指数 
数字 
 
 
boom_idx_yoy 
企业景气指数同比增长 
数字 
 
 
boom_idx_mom 
企业景气指数环比增长 
数字 
 
 
confidence_idx 
企业家信心指数 
数字 
 
 
confidence_idx_yoy 
企业家信心指数同比增长 
数字 
 
 
confidence_idx_mom 
企业家信心指数环比增长 
数字 
 
 
制造业采购经理指数（月度） 
表名：MAC_MANUFACTURING_PMI 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
pmi 
制造业采购经理指数 
数字 
 
 
produce_idx 
生产指数 
数字 
 
 
new_orders_idx 
新订单指数 
数字 
 
 
new_export_orders_idx 
新出口订单指数 
数字 
 
 
order_in_hand_idx 
在手订单指数 
数字 
 
 
finished_produce_idx 
产成品库存指数 
数字 
 
 
purchase_quantity_idx 
采购量指数 
数字 
 
 
import_idx 
进口指数 
数字 
 
 
exfactory_idx 
出厂价格指数 
数字 
 
 
purchases_idx 
主要原材料购进价格指数 
数字 
 
 
raw_material_idx 
原材料库存指数 
数字 
 
 


=== 第 147 页 ===
employ_idx 
从业人员指数 
数字 
 
 
delivery_time_idx 
供应商配送时间指数 
数字 
 
 
production_expected_idx 
生产经营活动预期指数 
数字 
 
 
非制造业采购经理指数（月度） 
表名：MAC_NONMANUFACTURING_PMI 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_month 
统计月份 
文本 
 
YYYY-MM 
business_idx 
商务活动指数 
数字 
 
 
new_orders_idx 
新订单指数 
数字 
 
 
new_export_orders_idx 
新出口订单指数 
数字 
 
 
order_in_hand_idx 
在手订单指数 
数字 
 
 
inventory_idx 
存货指数 
数字 
 
 
input_idx 
投入品价格指数 
数字 
 
 
sell_idx 
销售价格指数 
数字 
 
 
employ_idx 
从业人员指数 
数字 
 
 
delivery_time_idx 
供应商配送时间指数 
数字 
 
 
bussiness_activity_expected_idx 
业务活动预期指数 
数字 
 
 
分地区居民消费价格指数（月度） 
表名：MAC_AREA_CPI_MONTH 
列名 
列
的
含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_month 
统
计
月
份 
文
本 
 
YYYY-MM 
area_code 
地
区
代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地
区
文
本 
 
 


=== 第 148 页 ===
名
称 
item_name 
条
目
名
称 
文
本 
 
 
item_value 
该
条
目
的
值 
数
字 
 
居民消费价格指数是反映一定时期内城乡居民所购买的生活消费品和服务项目价格变动趋
势和程度的相对数，是对城市居民消费价格指数和农村居民消费价格指数进行综合汇总计
算的结果。通过该指数可以观察和分析消费品的零售价格和服务项目价格变动对城乡居民
实际生活费支出的影响程度。 
全国居民消费价格指数（月度） 
表名：MAC_CPI_MONTH 
字段名称 
中文名称 
字段类型 
含义 
id 
主键 
 
 
stat_month 
日期 
str 
 
area_code 
统计范围代码 
str 
701001-全国，701002-城市，701003-农村 
area_name 
统计范围 
str 
 
cpi_month 
当月CPI 
decimal(10,4) 
(上年同月=100) 
yoy 
同比 
decimal(10,4) 
 
mom 
环比 
decimal(10,4) 
 
acc 
当年度累计 
decimal(10,4) 
当年度累计=当年度各个月份CPI 的加权平均 
工业 
全国工业增长速度（月度） 
表名：MAC_INDUSTRY_GROWTH 
列名 
列的含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_month 
统计月
份 
文
本 
 
YYYY-MM 
growth_yoy 
工业增
加值_同
比增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、


=== 第 149 页 ===
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
growth_acc 
工业增
加值_累
计增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
state_owned_yoy 
国有及
国有控
股企业
增加值_
同比增
长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
state_owned_acc 
国有及
国有控
股企业
增加值_
累计增
长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
private_yoy 
私营企
业增加
值_同比
增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
private_acc 
私营企
业增加
值_累计
增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
collective_yoy 
集体企
业增加
值_同比
增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
collective_acc 
集体企
业增加
值_累计
增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
stock_cooperate_yoy 
股份合
作企业
增加值_
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、


=== 第 150 页 ===
同比增
长 
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
stock_cooperate_acc 
股份合
作企业
增加值_
累计增
长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
joint_stock_yoy 
股份制
企业增
加值_同
比增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
joint_stock_acc 
股份制
企业增
加值_累
计增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
foreign_yoy 
外商及
港澳台
投资企
业增加
值_同比
增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
foreign_acc 
外商及
港澳台
投资企
业增加
值_累计
增长 
数
字 
% 
工业增加值是指工业企业在报告期内以货币形式表现的从事工业生产活动的
最终成果。工业增加值有两种计算方法：一是生产法，即工业总产出减去工
业中间投入加上应交增值税；二是收入法，即从收入的角度出发，根据生产
要素在生产过程中应得到的收入份额计算，具体构成项目有固定资产折旧、
劳动者报酬、生产税净额、营业盈余。工业增加值同比增长是指本月度工业
增加值相对上年同月数的变动趋势和程度。按不变价格计算。 
全国工业分行业增长速度（月度） 
表名：MAC_INDUSTRY_CATEGORY_GROWTH 
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
 
 
stat_month 
统计月份 
文
本 
 
YYYY-
MM 
coal_mining_yoy 
煤炭开采和洗选业增加值_同比增长 
数
字 
% 
 


=== 第 151 页 ===
oil_gas_mining_yoy 
石油和天然气开采业增加值_同比增长 
数
字 
% 
 
black_metal_mining_yoy 
黑色金属矿采选业增加值_同比增长 
数
字 
% 
 
nonferrous_metal_mining_yoy 
有色金属矿采选业增加值_同比增长 
数
字 
% 
 
nonmetal_mining_yoy 
非金属矿采选业增加值_同比增长 
数
字 
% 
 
mining_aid_yoy 
开采辅助活动增加值_同比增长 
数
字 
% 
 
other_mining_yoy 
其他采矿业增加值_同比增长 
数
字 
% 
 
agro_food_yoy 
农副食品加工业增加值_同比增长 
数
字 
% 
 
food_manu_yoy 
食品制造业增加值_同比增长 
数
字 
% 
 
drink_manu_yoy 
酒、饮料和精制茶制造业增加值_同比增长 
数
字 
% 
 
tobacco_manu_yoy 
烟草制品业增加值_同比增长 
数
字 
% 
 
textile_yoy 
纺织业增加值_同比增长 
数
字 
% 
 
cloth_manu_yoy 
纺织服装、服饰业增加值_同比增长 
数
字 
% 
 
leather_manu_yoy 
皮革、毛皮、羽毛及其制品和制鞋业增加值_同比增长 
数
字 
% 
 
wood_manu_yoy 
木材加工及木、竹、藤、棕、草制品业增加值_同比增
长 
数
字 
% 
 
furniture_manu_yoy 
家具制造业增加值_同比增长 
数
字 
% 
 
paper_manu_yoy 
造纸及纸制品业增加值_同比增长 
数
字 
% 
 
print_yoy 
印刷和记录媒介复制业增加值_同比增长 
数
字 
% 
 
refinery_yoy 
石油加工、炼焦及核燃料加工业增加值_同比增长 
数
字 
% 
 
chemical_manu_yoy 
化学原料及化学制品制造业增加值_同比增长 
数
字 
% 
 
medical_manu_yoy 
医药制造业增加值_同比增长 
数
字 
% 
 
chemical_fiber_yoy 
化学纤维制造业增加值_同比增长 
数
字 
% 
 
rubber_manu_yoy 
橡胶和塑料制品业增加值_同比增长 
数
字 
% 
 
nonmetal_manu_yoy 
非金属矿物制品业增加值_同比增长 
数
字 
% 
 
black_metal_manu_yoy 
黑色金属冶炼及压延加工业增加值_同比增长 
数
字 
% 
 


=== 第 152 页 ===
nonferrous_metal_manu_yoy 
有色金属冶炼及压延加工业增加值_同比增长 
数
字 
% 
 
metal_product_manu_yoy 
金属制品业增加值_同比增长 
数
字 
% 
 
general_equipment_manu_yoy 
通用设备制造业增加值_同比增长 
数
字 
% 
 
professional_equipment_manu_yoy 
专用设备制造业增加值_同比增长 
数
字 
% 
 
car_manu_yoy 
汽车制造业增加值_同比增长 
数
字 
% 
 
transport_manu_yoy 
铁路、船舶、航空航天和其他运输设备制造业增加值_
同比增长 
数
字 
% 
 
electrical_equipment_manu_yoy 
电气机械及器材制造业增加值_同比增长 
数
字 
% 
 
communication_equipment_manu_yoy 
通信设备、计算机及其他电子设备制造业增加值_同比
增长 
数
字 
% 
 
meter_manu_yoy 
仪器仪表制造业增加值_同比增长 
数
字 
% 
 
other_manu_yoy 
其他制造业增加值_同比增长 
数
字 
% 
 
reuse_manu_yoy 
废弃资源综合利用业增加值_同比增长 
数
字 
% 
 
repair_manu_yoy 
金属制品、机械和设备修理业增加值_同比增长 
数
字 
% 
 
power_yoy 
电力、热力的生产和供应业增加值_同比增长 
数
字 
% 
 
gas_yoy 
燃气生产和供应业增加值_同比增长 
数
字 
% 
 
water_yoy 
水的生产和供应业增加值_同比增长 
数
字 
% 
 
coal_mining_acc 
煤炭开采和洗选业增加值_累计增长 
数
字 
% 
 
oil_gas_mining_acc 
石油和天然气开采业增加值_累计增长 
数
字 
% 
 
black_metal_mining_acc 
黑色金属矿采选业增加值_累计增长 
数
字 
% 
 
nonferrous_metal_mining_acc 
有色金属矿采选业增加值_累计增长 
数
字 
% 
 
nonmetal_mining_acc 
非金属矿采选业增加值_累计增长 
数
字 
% 
 
mining_aid_acc 
开采辅助活动增加值_累计增长 
数
字 
% 
 
other_mining_acc 
其他采矿业增加值_累计增长 
数
字 
% 
 
agro_food_acc 
农副食品加工业增加值_累计增长 
数
字 
% 
 
food_manu_acc 
食品制造业增加值_累计增长 
数
字 
% 
 


=== 第 153 页 ===
drink_manu_acc 
酒、饮料和精制茶制造业增加值_累计增长 
数
字 
% 
 
tobacco_manu_acc 
烟草制品业增加值_累计增长 
数
字 
% 
 
textile_acc 
纺织业增加值_累计增长 
数
字 
% 
 
cloth_manu_acc 
纺织服装、服饰业增加值_累计增长 
数
字 
% 
 
leather_manu_acc 
皮革、毛皮、羽毛及其制品和制鞋业增加值_累计增长 
数
字 
% 
 
wood_manu_acc 
木材加工及木、竹、藤、棕、草制品业增加值_累计增
长 
数
字 
% 
 
furniture_manu_acc 
家具制造业增加值_累计增长 
数
字 
% 
 
paper_manu_acc 
造纸及纸制品业增加值_累计增长 
数
字 
% 
 
print_acc 
印刷和记录媒介复制业增加值_累计增长 
数
字 
% 
 
refinery_acc 
石油加工、炼焦及核燃料加工业增加值_累计增长 
数
字 
% 
 
chemical_manu_acc 
化学原料及化学制品制造业增加值_累计增长 
数
字 
% 
 
medical_manu_acc 
医药制造业增加值_累计增长 
数
字 
% 
 
chemical_fiber_acc 
化学纤维制造业增加值_累计增长 
数
字 
% 
 
rubber_manu_acc 
橡胶和塑料制品业增加值_累计增长 
数
字 
% 
 
nonmetal_manu_acc 
非金属矿物制品业增加值_累计增长 
数
字 
% 
 
black_metal_manu_acc 
黑色金属冶炼及压延加工业增加值_累计增长 
数
字 
% 
 
nonferrous_metal_manu_acc 
有色金属冶炼及压延加工业增加值_累计增长 
数
字 
% 
 
metal_product_manu_acc 
金属制品业增加值_累计增长 
数
字 
% 
 
general_equipment_manu_acc 
通用设备制造业增加值_累计增长 
数
字 
% 
 
professional_equipment_manu_acc 
专用设备制造业增加值_累计增长 
数
字 
% 
 
car_manu_acc 
汽车制造业增加值_累计增长 
数
字 
% 
 
transport_manu_acc 
铁路、船舶、航空航天和其他运输设备制造业增加值_
累计增长 
数
字 
% 
 
electrical_equipment_manu_acc 
电气机械及器材制造业增加值_累计增长 
数
字 
% 
 
communication_equipment_manu_acc 
通信设备、计算机及其他电子设备制造业增加值_累计
增长 
数
字 
% 
 


=== 第 154 页 ===
meter_manu_acc 
仪器仪表制造业增加值_累计增长 
数
字 
% 
 
other_manu_acc 
其他制造业增加值_累计增长 
数
字 
% 
 
reuse_manu_acc 
废弃资源综合利用业增加值_累计增长 
数
字 
% 
 
repair_manu_acc 
金属制品、机械和设备修理业增加值_累计增长 
数
字 
% 
 
power_acc 
电力、热力的生产和供应业增加值_累计增长 
数
字 
% 
 
gas_acc 
燃气生产和供应业增加值_累计增长 
数
字 
% 
 
water_acc 
水的生产和供应业增加值_累计增长 
数
字 
% 
 
全国工业企业主要经济指标（月度） 
表名：MAC_INDUSTRY_INDICATOR 
列名 
列的
含义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_month 
统计
月份 
文
本 
 
YYYY-MM 
enterprise_value_acc 
企业
单位
数_累
计值 
数
字 
个 
工业企业数包括独立核算法人工业企业和附营工业生产单位。独立核
算法人工业企业指从事生产经营活动的单位。它同时具备以下条件：
①依法成立，有自己的名称、组织机构和场所，能够独立承担民事责
任；②独立拥有和使用资产，承担负债，有权与其他单位签订合同；
③会计上独立核算，能够编制资产负债表 
loss_enterprise_value_acc 
亏损
企业_
累计
值 
数
字 
个 
工业企业数包括独立核算法人工业企业和附营工业生产单位。独立核
算法人工业企业指从事生产经营活动的单位。它同时具备以下条件：
①依法成立，有自己的名称、组织机构和场所，能够独立承担民事责
任；②独立拥有和使用资产，承担负债，有权与其他单位签订合同；
③会计上独立核算，能够编制资产负债表 
loss_enterprise_ratio_acc 
亏损
企业_
累计
增长 
数
字 
% 
工业企业数包括独立核算法人工业企业和附营工业生产单位。独立核
算法人工业企业指从事生产经营活动的单位。它同时具备以下条件：
①依法成立，有自己的名称、组织机构和场所，能够独立承担民事责
任；②独立拥有和使用资产，承担负债，有权与其他单位签订合同；
③会计上独立核算，能够编制资产负债表 
current_asset_value_acc 
流动
资产
合计_
累计
值 
数
字 
亿
元 
资产满足以下条件之一应归为流动资产：（1）预计在一个正常营业
周期中变现、出售或耗用，主要包括存货、应收账款等；（2）主要
为交易目的而持有；（3）预计在资产负债表日起一年内（含一年）
变现；（4）自资产负债日起一年内，交换其他资产或清偿负债的能
力不受限制的现金或现金等价物。包括货币资金、应收票据、应收账


=== 第 155 页 ===
款、存货等项目。根据会计“资产负债表”中“流动资产合计”项目的期
末余额数填报。 
current_asset_ratio_acc 
流动
资产
合计_
累计
增长 
数
字 
% 
资产满足以下条件之一应归为流动资产：（1）预计在一个正常营业
周期中变现、出售或耗用，主要包括存货、应收账款等；（2）主要
为交易目的而持有；（3）预计在资产负债表日起一年内（含一年）
变现；（4）自资产负债日起一年内，交换其他资产或清偿负债的能
力不受限制的现金或现金等价物。包括货币资金、应收票据、应收账
款、存货等项目。根据会计“资产负债表”中“流动资产合计”项目的期
末余额数填报。 
accounts_receivable_value_acc 
应收
账款_
累计
值 
数
字 
亿
元 
应收账款指企业因销售商品、提供劳务等经营活动，应向购货单位或
接受劳务单位收取的款项，主要包括企业销售商品或提供劳务等应向
有关债务人收取的价款及代购货单位垫付的包装费、运杂费等。根据
会计“资产负债表”中“应收账款”项目的期末余额数填报。 
accounts_receivable_ratio_acc 
应收
账款_
累计
增长 
数
字 
% 
应收账款指企业因销售商品、提供劳务等经营活动，应向购货单位或
接受劳务单位收取的款项，主要包括企业销售商品或提供劳务等应向
有关债务人收取的价款及代购货单位垫付的包装费、运杂费等。根据
会计“资产负债表”中“应收账款”项目的期末余额数填报。 
inventories_value_acc 
应收
账款_
累计
值 
数
字 
亿
元 
应收账款指企业因销售商品、提供劳务等经营活动，应向购货单位或
接受劳务单位收取的款项，主要包括企业销售商品或提供劳务等应向
有关债务人收取的价款及代购货单位垫付的包装费、运杂费等。根据
会计“资产负债表”中“应收账款”项目的期末余额数填报。 
inventories_ratio_acc 
存货_
累计
增长 
数
字 
% 
存货指企业在日常活动中持有以备出售的产成品或商品、处在生产过
程中的在产品、在生产过程或提供劳务过程中耗用的材料或物料等，
通常包括原材料、在产品、半成品、产成品、商品以及周转材料等。
根据会计“资产负债表”中“存货”项目的期末余额数填报。其中：“年初
存货”根据会计“资产负债表”中“存货”项目的年初余额数填报。注意：
“存货”具有实物形态，不属于无形资产，由于企业持有存货的最终目
的是为了出售，所以房地产开发企业（单位）购置的土地、尚未销售
的商品房等均计入“存货”。 
finished_product_value_acc 
产成
品存
货_累
计值 
数
字 
亿
元 
产成品指工业企业已经完成全部生产过程并验收入库，可以按照合同
规定的条件送交订货单位，或者可以作为商品对外销售的产品。根据
会计“产成品”科目的借方余额填报 
finished_product_ratio_acc 
产成
品存
货_累
计增
长 
数
字 
% 
产成品指工业企业已经完成全部生产过程并验收入库，可以按照合同
规定的条件送交订货单位，或者可以作为商品对外销售的产品。根据
会计“产成品”科目的借方余额填报 
total_assets_value_acc 
资产
总计_
累计
值 
数
字 
亿
元 
资产总计指企业过去的交易或者事项形成的、由企业拥有或者控制
的、预期会给企业带来经济利益的资源。资产一般按流动性分为流动
资产和非流动资产。其中流动资产可分为货币资金、交易性金融资
产、应收票据、应收账款、预付款项、其他应收款、存货等；非流动
资产可分为长期股权投资、固定资产、无形资产及其他非流动资产
等。根据会计“资产负债表”中“资产总计”项目的期末余额数填报。 
total_assets_ratio_acc 
资产
总计_
累计
增长 
数
字 
% 
资产总计指企业过去的交易或者事项形成的、由企业拥有或者控制
的、预期会给企业带来经济利益的资源。资产一般按流动性分为流动
资产和非流动资产。其中流动资产可分为货币资金、交易性金融资
产、应收票据、应收账款、预付款项、其他应收款、存货等；非流动


=== 第 156 页 ===
资产可分为长期股权投资、固定资产、无形资产及其他非流动资产
等。根据会计“资产负债表”中“资产总计”项目的期末余额数填报。 
liabilities_value_acc 
负债
合计_
累计
值 
数
字 
亿
元 
负债合计指企业过去的交易或者事项形成的，预期会导致经济利益流
出企业的现时义务。负债一般按偿还期长短分为流动负债和非流动负
债。根据会计“资产负债表”中“负债合计”项目的期末余额数填报。 
liabilities_ratio_acc 
负债
合计_
累计
增长 
数
字 
% 
负债合计指企业过去的交易或者事项形成的，预期会导致经济利益流
出企业的现时义务。负债一般按偿还期长短分为流动负债和非流动负
债。根据会计“资产负债表”中“负债合计”项目的期末余额数填报。 
main_business_value_acc 
主营
业务
收入_
累计
值 
数
字 
亿
元 
主营业务收入指企业确认的销售商品、提供劳务等主营业务的收入。
根据会计“主营业务收入”科目的期末贷方余额填报。 
main_business_ratio_acc 
主营
业务
收入_
累计
增长 
数
字 
% 
主营业务收入指企业确认的销售商品、提供劳务等主营业务的收入。
根据会计“主营业务收入”科目的期末贷方余额填报。 
main_business_tax_value_acc 
主营
业务
税金
及附
加_累
计值 
数
字 
亿
元 
主营业务税金及附加指企业经营主要业务应负担的营业税、消费税、
城市维护建设税、教育费附加等。根据会计“主营业务税金及附加”科
目的期末借方余额（结转前）填报。执行2006 年《企业会计准则》
的企业，如未设置该科目，以“营业税金及附加”代替填报。 
main_business_tax_ratio_acc 
主营
业务
税金
及附
加_累
计增
长 
数
字 
% 
主营业务税金及附加指企业经营主要业务应负担的营业税、消费税、
城市维护建设税、教育费附加等。根据会计“主营业务税金及附加”科
目的期末借方余额（结转前）填报。执行2006 年《企业会计准则》
的企业，如未设置该科目，以“营业税金及附加”代替填报。 
sale_expense_value_acc 
销售
费用_
累计
值 
数
字 
亿
元 
销售费用指企业在销售商品和材料、提供劳务的过程中发生的各种费
用，包括保险费、包装费、展览费和广告费、商品维修费、预计产品
质量保证损失、运输费、装卸费等以及为销售本企业商品而专设的销
售机构（含销售网点、售后服务网点等）的职工薪酬、业务费、折旧
费等经营费用。 
sale_expense_ratio_acc 
销售
费用_
累计
增长 
数
字 
% 
销售费用指企业在销售商品和材料、提供劳务的过程中发生的各种费
用，包括保险费、包装费、展览费和广告费、商品维修费、预计产品
质量保证损失、运输费、装卸费等以及为销售本企业商品而专设的销
售机构（含销售网点、售后服务网点等）的职工薪酬、业务费、折旧
费等经营费用。 
management_cost_value_acc 
管理
费用_
累计
值 
数
字 
亿
元 
管理费用指企业为组织和管理企业生产经营所发生的费用，包括企业
在筹建期间内发生的开办费、董事会和行政管理部门在企业经营管理
中发生的，或者应当由企业统一负担的公司经费等。根据会计“利润
表”中“管理费用”项目的本期金额数填报。 


=== 第 157 页 ===
management_cost_ratio_acc 
管理
费用_
累计
增长 
数
字 
% 
管理费用指企业为组织和管理企业生产经营所发生的费用，包括企业
在筹建期间内发生的开办费、董事会和行政管理部门在企业经营管理
中发生的，或者应当由企业统一负担的公司经费等。根据会计“利润
表”中“管理费用”项目的本期金额数填报。 
financial_expense_value_acc 
财务
费用_
累计
值 
数
字 
亿
元 
财务费用指企业为筹集生产经营所需资金等而发生的筹资费用，包括
企业生产经营期间发生的利息支出（减利息收入）、汇兑损失（减汇
兑收益）以及相关的手续费等。根据会计“利润表”中“财务费用”项目
的本期金额数填报。 
financial_expense_ratio_acc 
财务
费用_
累计
增长 
数
字 
% 
财务费用指企业为筹集生产经营所需资金等而发生的筹资费用，包括
企业生产经营期间发生的利息支出（减利息收入）、汇兑损失（减汇
兑收益）以及相关的手续费等。根据会计“利润表”中“财务费用”项目
的本期金额数填报。 
interest_expense_value_acc 
利息
支出_
累计
值 
数
字 
亿
元 
利息支出指企业短期借款利息、长期借款利息、应付票据利息、票据
贴现利息、应付债券利息、长期应付引进国外设备款利息等利息支
出。根据企业“财务费用明细账”中“财务费用——利息支出”科目的本
期发生额填报。如果企业没有单独设立“利息收入”科目，应填报利息
支出减去银行存款等的利息收入后的净额。 
interest_expense_ratio_acc 
利息
支出_
累计
增长 
数
字 
% 
利息支出指企业短期借款利息、长期借款利息、应付票据利息、票据
贴现利息、应付债券利息、长期应付引进国外设备款利息等利息支
出。根据企业“财务费用明细账”中“财务费用——利息支出”科目的本
期发生额填报。如果企业没有单独设立“利息收入”科目，应填报利息
支出减去银行存款等的利息收入后的净额。 
total_interest_value_acc 
利润
总额_
累计
值 
数
字 
亿
元 
利润总额指企业在一定会计期间的经营成果，是生产经营过程中各种
收入扣除各种耗费后的盈余，反映企业在报告期内实现的盈亏总额。
根据会计“利润表”中“利润总额”项目的本期金额数填报。 
total_interest_ratio_acc 
利润
总额_
累计
增长 
数
字 
% 
利润总额指企业在一定会计期间的经营成果，是生产经营过程中各种
收入扣除各种耗费后的盈余，反映企业在报告期内实现的盈亏总额。
根据会计“利润表”中“利润总额”项目的本期金额数填报。 
enterprise_total_loss_value_acc 
亏损
企业
亏损
总额_
累计
值 
数
字 
亿
元 
 
enterprise_total_loss_ratio_acc 
亏损
企业
亏损
总额_
累计
增长 
数
字 
% 
 
vat_value_acc 
应交
增值
税_累
计值 
数
字 
亿
元 
应交增值税指企业按税法规定，从事货物销售或提供加工、修理修配
劳务等增加货物价值的活动本期应交纳的税金。计算公式为：应交增
值税=销项税额-（进项税额-进项税额转出）-出口抵减内销产品应纳
税额-减免税款+出口退税，进项税额指企业在报告期内购入货物或接
受应税劳务而支付的、准予从销项税额中抵扣的增值税额。销项税额
指企业在报告期内销售货物或提供应税劳务应收取的增值税额。 


=== 第 158 页 ===
vat_ratio_acc 
应交
增值
税_累
计增
长 
数
字 
% 
应交增值税指企业按税法规定，从事货物销售或提供加工、修理修配
劳务等增加货物价值的活动本期应交纳的税金。计算公式为：应交增
值税=销项税额-（进项税额-进项税额转出）-出口抵减内销产品应纳
税额-减免税款+出口退税，进项税额指企业在报告期内购入货物或接
受应税劳务而支付的、准予从销项税额中抵扣的增值税额。销项税额
指企业在报告期内销售货物或提供应税劳务应收取的增值税额。 
保险业 
全国各地区保险业务统计表(年度) 
表名：MAC_INSURANCE_AREA_YEAR 
列名 
列
的
含
义 
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
统
计
年
份 
文
本 
 
YYYY 
area_code 
地
区
代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地
区
名
称 
文
本 
 
 
income 
原
保
险
保
费
收
入 
数
字 
亿
元 
原保险保费收入为本年累计数，保费指投保人为取得保险人在约定范围内所承担赔偿
责任而支付给保险人的费用。 
property_income 
财
产
险
保
费
收
入 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而支付给保险人的费用。 


=== 第 159 页 ===
personal_income 
人
身
险
保
费
收
入 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而支付给保险人的费用。 
expense 
原
保
险
赔
付
支
出 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金额。给
付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保险及长期健康
保险合同的规定，因被保险人在保险期内发生保险责任范围内的保险事故支付给被保
险人(或受益人)的金额。满期给付是指被保险人生存期满，保险人按人寿保险合同规
定支付给被保险人的满期保险金额。 
property_expense 
财
产
险
支
出 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金额。给
付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保险及长期健康
保险合同的规定，因被保险人在保险期内发生保险责任范围内的保险事故支付给被保
险人(或受益人)的金额。满期给付是指被保险人生存期满，保险人按人寿保险合同规
定支付给被保险人的满期保险金额。 
personal_expense 
人
身
险
支
出 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金额。给
付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保险及长期健康
保险合同的规定，因被保险人在保险期内发生保险责任范围内的保险事故支付给被保
险人(或受益人)的金额。满期给付是指被保险人生存期满，保险人按人寿保险合同规
定支付给被保险人的满期保险金额。 
保险公司保费金额表(年度) 
表名：MAC_INSURANCE_PREMIUM_YEAR 
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
total_income 
保险公司保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
property_income 
财产保险公司保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
enterprise 
企业财产保险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
family 
家庭财产保险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
vehicle 
机动车辆保险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 


=== 第 160 页 ===
project 
财产保险公司工程保险保
费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
liability 
财产保险公司责任保险保
费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
credit 
财产保险公司信用保险保
费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
guarantee 
财产保险公司保证保险保
费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
ship 
财产保险公司船舶保险保
费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
freight 
财产保险公司货物运输保
险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
special_risk 
财产保险公司特殊风险保
险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
farm 
财产保险公司农业保险保
费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
property_health 
财产保险公司健康险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
property_accident 
财产保险公司意外伤害保
险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
other 
财产保险公司其他险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
personal_income 
人寿保险公司保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
life 
人寿保险公司寿险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
health 
人寿保险公司健康险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
accident 
人寿保险公司人身意外伤
害险保费 
数
字 
亿
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而
支付给保险人的费用。 
保险公司赔款及给付表(年度) 
表名：MAC_INSURANCE_PAYMENT_YEAR 
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
total_expense 
保险公司
赔款及给
付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 


=== 第 161 页 ===
property_expense 
财产保险
公司赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
enterprise 
企业财产
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
family 
家庭财产
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
vehicle 
机动车辆
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
project 
财产保险
公司工程
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
liability 
财产保险
公司责任
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
credit 
财产保险
公司信用
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
guarantee 
财产保险
公司保证
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
ship 
财产保险
公司船舶
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
freight 
财产保险
公司货物
运输保险
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的


=== 第 162 页 ===
赔款及给
付 
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
special_risk 
财产保险
公司特殊
风险保险
赔款及给
付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
farm 
财产保险
公司农业
保险赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
property_health 
财产保险
公司健康
险赔款及
给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
property_accident 
财产保险
公司意外
伤害保险
赔款及给
付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
other 
财产保险
公司其他
险赔款及
给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
personal_expense 
人寿保险
公司赔款
及给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
life 
人寿保险
公司寿险
赔款及给
付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
health 
人寿保险
公司健康
险赔款及
给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 
accident 
人寿保险
公司人身
意外伤害
险赔款及
给付 
数
字 
亿
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金
额。给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保
险及长期健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的
保险事故支付给被保险人(或受益人)的金额。满期给付是指被保险人生存期
满，保险人按人寿保险合同规定支付给被保险人的满期保险金额。 


=== 第 163 页 ===
保险公司资产情况（年度） 
表名：MAC_INSURANCE_ASSETS_YEAR 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
total 
保险
业资
产总
额 
数
字 
亿
元 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、预期会给企业带
来经济利益的资源。资产一般按流动性分为流动资产和非流动资产。其中流动资产
可分为货币资金、交易性金融资产、应收票据、应收账款、预付款项、其他应收
款、存货等；非流动资产可分为长期股权投资、固定资产、无形资产及其他非流动
资产等。 
assets 
财产
险公
司资
产 
数
字 
亿
元 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、预期会给企业带
来经济利益的资源。资产一般按流动性分为流动资产和非流动资产。其中流动资产
可分为货币资金、交易性金融资产、应收票据、应收账款、预付款项、其他应收
款、存货等；非流动资产可分为长期股权投资、固定资产、无形资产及其他非流动
资产等。 
life 
寿险
公司
资产 
数
字 
亿
元 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、预期会给企业带
来经济利益的资源。资产一般按流动性分为流动资产和非流动资产。其中流动资产
可分为货币资金、交易性金融资产、应收票据、应收账款、预付款项、其他应收
款、存货等；非流动资产可分为长期股权投资、固定资产、无形资产及其他非流动
资产等。 
reinsurance 
再保
险公
司资
产 
数
字 
亿
元 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、预期会给企业带
来经济利益的资源。资产一般按流动性分为流动资产和非流动资产。其中流动资产
可分为货币资金、交易性金融资产、应收票据、应收账款、预付款项、其他应收
款、存货等；非流动资产可分为长期股权投资、固定资产、无形资产及其他非流动
资产等。 
china_invested 
中资
保险
公司
资产 
数
字 
亿
元 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、预期会给企业带
来经济利益的资源。资产一般按流动性分为流动资产和非流动资产。其中流动资产
可分为货币资金、交易性金融资产、应收票据、应收账款、预付款项、其他应收
款、存货等；非流动资产可分为长期股权投资、固定资产、无形资产及其他非流动
资产等。 
foreign_invested 
外资
保险
公司
资产 
数
字 
亿
元 
资产指企业过去的交易或者事项形成的、由企业拥有或者控制的、预期会给企业带
来经济利益的资源。资产一般按流动性分为流动资产和非流动资产。其中流动资产
可分为货币资金、交易性金融资产、应收票据、应收账款、预付款项、其他应收
款、存货等；非流动资产可分为长期股权投资、固定资产、无形资产及其他非流动
资产等。 
保险公司原保费收入和赔付支出情况（年度） 
表名：MAC_INSURANCE_REVENUE_EXPENSE_YEAR 


=== 第 164 页 ===
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
original_revenue 
原保
险保
费收
入 
数
字 
万
元 
原保险保费收入为本年累计数，保费指投保人为取得保险人在约定范围内所承担赔
偿责任而支付给保险人的费用。 
property_revenue 
财产
险保
费收
入 
数
字 
万
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而支付给保险人的费用。 
life_revenue 
人身
险保
费收
入 
数
字 
万
元 
保费指投保人为取得保险人在约定范围内所承担赔偿责任而支付给保险人的费用。 
original_expense 
原保
险赔
付支
出 
数
字 
万
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金额。
给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保险及长期
健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的保险事故支付
给被保险人(或受益人)的金额。满期给付是指被保险人生存期满，保险人按人寿保
险合同规定支付给被保险人的满期保险金额。 
property_expense 
财产
险支
出 
数
字 
万
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金额。
给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保险及长期
健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的保险事故支付
给被保险人(或受益人)的金额。满期给付是指被保险人生存期满，保险人按人寿保
险合同规定支付给被保险人的满期保险金额。 
life_expense 
人身
险支
出 
数
字 
万
元 
赔款指保险人根据保险合同的规定，向被保险人支付的赔偿保险责任损失的金额。
给付包括死伤医疗给付和满期给付。死伤医疗给付是指保险人根据人寿保险及长期
健康保险合同的规定，因被保险人在保险期内发生保险责任范围内的保险事故支付
给被保险人(或受益人)的金额。满期给付是指被保险人生存期满，保险人按人寿保
险合同规定支付给被保险人的满期保险金额。 
国民经济 
全国各地区的行政划分（年度） 
表名：MAC_AREA_DIV 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
province_name 
该地区所在省份名称 
文本 
 
 


=== 第 165 页 ===
city_name 
该地区所在城市名称 
文本 
 
 
分地区国内生产总值表(季度) 
表名：MAC_AREA_GDP_QUARTER 
列名 
列的含
义 
类
型 
单
位 
说明 
id 
id 
数
字 
 
 
stat_quarter 
统计的
季度 
文
本 
 
YYYY-MM(03、06、09、12 分别代表第1、2、3、4 季度) 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
gdp_acc 
国内生
产总值
(累计
值) 
数
字 
亿
元 
国内生产总值(GDP)指按市场价格计算的一个国家（或地区）所有常住单位
在一定时期内生产活动的最终成果。国内生产总值有三种表现形态，即价值
形态、收入形态和产品形态。从价值形态看，它是所有常住单位在一定时期
内生产的全部货物和服务价值与同期投入的全部非固定资产货物和服务价值
的差额，即所有常住单位的增加值之和；从收入形态看，它是所有常住单位
在一定时期内创造并分配给常住单位和非常住单位的初次收入之和；从产品
形态看，它是所有常住单位在一定时期内最终使用的货物和服务价值与货物
和服务净出口价值之和。在实际核算中，国内生产总值有三种计算方法，即
生产法、收入法和支出法。三种方法分别从不同的方面反映国内生产总值及
其构成。按当年价格计算。对于一个地区来说，称为地区生产总值或地区
GDP。 
gdp_primary_acc 
国内生
产总值
-第一
产业
(累计
值) 
数
字 
亿
元 
第一产业增加值是指按市场价格计算的一个国家（或地区）所有常住单位在
一定时期内从事第一产业生产活动的最终成果。第一产业是指农、林、牧、
渔业。 
gdp_secondary_acc 
国内生
产总值
-第二
产业
(累计
值) 
数
字 
亿
元 
第二产业增加值是指按市场价格计算的一个国家（或地区）所有常住单位在
一定时期内从事第二产业生产活动的最终成果。第二产业是指采矿业，制造
业，电力、煤气及水的生产和供应业，建筑业。 
gdp_tertiary_acc 
国内生
产总值
-第三
产业
(累计
值) 
数
字 
亿
元 
第三产业增加值是指按市场价格计算的一个国家（或地区）所有常住单位在
一定时期内从事第三产业生产活动的最终成果。第三产业是指除第一、二产
业以外的其他行业。 


=== 第 166 页 ===
gdp_sin 
国内生
产总值
(当前
值) 
数
字 
亿
元 
 
gdp_primary_sin 
国内生
产总值
-第一
产业
(当季
值) 
数
字 
亿
元 
 
gdp_secondary_sin 
国内生
产总值
-第二
产业
(当季
值) 
数
字 
亿
元 
 
gdp_tertiary_sin 
国内生
产总值
-第三
产业
(当季
值) 
数
字 
亿
元 
 
gdp_yoy_acc 
国内生
产总值
同比
(累计
值) 
数
字 
% 
 
gdp_primary_yoy_acc 
国内生
产总值
同比-
第一产
业(累
计值) 
数
字 
% 
 
gdp_secondary_yoy_acc 
国内生
产总值
同比-
第二产
业(累
计值) 
数
字 
% 
 
gdp_tertiary_yoy_acc 
国内生
产总值
同比-
第三产
业(累
计值) 
数
字 
% 
 
gdp_yoy_sin 
国内生
产总值
同比
数
字 
% 
 


=== 第 167 页 ===
(当季
值) 
gdp_primary_yoy_sin 
国内生
产总值
同比-
第一产
业(当
季值) 
数
字 
% 
 
gdp_secondary_yoy_sin 
国内生
产总值
同比-
第二产
业(当
季值) 
数
字 
% 
 
gdp_tertiary_yoy_sin 
国内生
产总值
同比-
第三产
业(当
季值) 
数
字 
% 
 
gdp_mom 
国内生
产总值
环比 
数
字 
% 
 
分地区国内生产总值表(年度) 
表名：MAC_AREA_GDP_YEAR 
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
统计的年度 
文
本 
 
YYYY 
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
gni 
该地区的总收入 
数
字 
亿
元 
 
gdp 
该地区的生产总值 
数
字 
亿
元 
 
gdp_primary 
该地区的第一产业生产总值 
数
字 
亿
元 
 
gdp_agro 
该地区的农林牧渔业生产总值 
数
字 
亿
元 
 


=== 第 168 页 ===
gdp_secondary 
该地区的第二产业生产总值 
数
字 
亿
元 
 
gdp_industry 
该地区的工业生产总值 
数
字 
亿
元 
 
gdp_construction 
该地区的建筑业生产总值 
数
字 
亿
元 
 
gdp_tertiary 
该地区的第三产业生产总值 
数
字 
亿
元 
 
gdp_transport 
该地区的交通运输、仓储和邮
政业生产总值 
数
字 
亿
元 
 
gdp_sale 
该地区的批发和零售业生产总
值 
数
字 
亿
元 
1952-2004 年报告披露为批发零售贸易及餐饮，现统一
记为批发零售 
gdp_hotel 
该地区的住宿和餐饮业生产总
值 
数
字 
亿
元 
 
gdp_financial 
该地区的金融业生产总值 
数
字 
亿
元 
1997-2004 年报告披露为金融保险业，现记为金融业 
gdp_estate 
该地区的房地产业生产总值 
数
字 
亿
元 
 
gdp_others 
该地区的其他行业生产总值 
数
字 
亿
元 
 
primary_percent 
该地区的第一产业占比 
数
字 
% 
 
secondary_percent 
该地区的第二产业占比 
数
字 
% 
 
tertiary_percent 
该地区的第三产业占比 
数
字 
% 
 
gpd_per_capita 
该地区人均国内生产总值 
数
字 
元 
 
分地区国内生产总值指数表(上年=100，年度) 
表名：MAC_AREA_GDP_YEAR_IDX 
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
统计的年度 
文
本 
 
YYYY 
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
gni_idx 
该地区总收入增长
指数 
数
字 
% 
上年=100 


=== 第 169 页 ===
gdp_idx 
该地区生产总值增
长指数 
数
字 
% 
上年=100，地区生产总值指数指反映一定时期内地区生产总值变
动趋势和程度的相对数，该指标是以上一年为基期计算的指数。
按不变价格计算。 
gdp_primary_idx 
该地区生产总值中
第一产业增长指数 
数
字 
% 
上年=100，第一产业增加值指数是指反映一定时期内第一产业增
加值变动趋势和程度的相对数，该指标是以上一年为基期计算的
指数。按不变价格计算。 
gdp_agro_idx 
该地区生产总值中
农林牧渔业增长指
数 
数
字 
% 
上年=100 
gdp_secondary_idx 
该地区生产总值中
第二产业增长指数 
数
字 
% 
上年=100，第二产业增加值指数是指反映一定时期内第二产业增
加值变动趋势和程度的相对数，该指标是以上一年为基期计算的
指数。按不变价格计算。 
gdp_industry_idx 
该地区生产总值中
工业增长指数 
数
字 
% 
上年=100 
gdp_construction_idx 
该地区生产总值中
建筑业增长指数 
数
字 
% 
上年=100 
gdp_tertiary_idx 
该地区生产总值中
第三产业增长指数 
数
字 
% 
上年=100，第三产业增加值指数是指反映一定时期内第三产业增
加值变动趋势和程度的相对数，该指标是以上一年为基期计算的
指数。按不变价格计算。 
gdp_sale_idx 
该地区生产总值中
批发和零售业增长
指数 
数
字 
% 
上年=100 
gdp_transport_idx 
该地区生产总值中
交通运输、仓储和
邮政业增长指数 
数
字 
% 
上年=100 
gdp_hotel_idx 
该地区生产总值中
住宿和餐饮业增长
指数 
数
字 
% 
上年=100 
gdp_financial_idx 
该地区生产总值中
金融业增长指数 
数
字 
% 
上年=100 
gdp_estate_idx 
该地区生产总值中
房地产业增长指数 
数
字 
% 
上年=100 
gdp_others_idx 
该地区生产总值中
其他行业增长指数 
数
字 
% 
上年=100 
gdp_per_capita_idx 
该地区人均生产总
值增长指数 
数
字 
% 
上年=100 
分地区国内生产总值指数表（年度） 
表名：MAC_AREA_GDP_YEAR_IDX_1978 
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
 
 


=== 第 170 页 ===
stat_year 
统计的年度 
文
本 
 
YYYY 
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
gni_idx 
该地区总收入增长
指数 
数
字 
% 
1978 年=100，地区生产总值指数指反映一定时期内地区生产总值
变动趋势和程度的相对数，该指标是以上一年为基期计算的指数。
按不变价格计算。 
gdp_idx 
该地区生产总值增
长指数 
数
字 
% 
1978 年=100 
gdp_primary_idx 
该地区生产总值中
第一产业增长指数 
数
字 
% 
1978 年=100，第一产业增加值指数是指反映一定时期内第一产业
增加值变动趋势和程度的相对数，该指标是以上一年为基期计算的
指数。按不变价格计算。 
gdp_agro_idx 
该地区生产总值中
农林牧渔业增长指
数 
数
字 
% 
1978 年=100 
gdp_secondary_idx 
该地区生产总值中
第二产业增长指数 
数
字 
% 
1978 年=100，第二产业增加值指数是指反映一定时期内第二产业
增加值变动趋势和程度的相对数，该指标是以上一年为基期计算的
指数。按不变价格计算。 
gdp_industry_idx 
该地区生产总值中
工业增长指数 
数
字 
% 
1978 年=100 
gdp_construction_idx 
该地区生产总值中
建筑业增长指数 
数
字 
% 
1978 年=100 
gdp_tertiary_idx 
该地区生产总值中
第三产业增长指数 
数
字 
% 
1978 年=100，第三产业增加值指数是指反映一定时期内第三产业
增加值变动趋势和程度的相对数，该指标是以上一年为基期计算的
指数。按不变价格计算。 
gdp_sale_idx 
该地区生产总值中
批发和零售业增长
指数 
数
字 
% 
1978 年=100 
gdp_transport_idx 
该地区生产总值中
交通运输、仓储和
邮政业增长指数 
数
字 
% 
1978 年=100 
gdp_hotel_idx 
该地区生产总值中
住宿和餐饮业增长
指数 
数
字 
% 
1978 年=100 
gdp_financial_idx 
该地区生产总值中
金融业增长指数 
数
字 
% 
1978 年=100 
gdp_estate_idx 
该地区生产总值中
房地产业增长指数 
数
字 
% 
1978 年=100 
gdp_others_idx 
该地区生产总值中
其他行业增长指数 
数
字 
% 
1978 年=100 
gdp_per_capita_idx 
该地区人均生产总
值增长指数 
数
字 
% 
1978 年=100 
分地区支出法国内生产总值表(年度) 


=== 第 171 页 ===
表名：MAC_AREA_GDP_EXPEND_YEAR 
列名 
列的
含义 
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
统计
的年
度 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 
gdp_expend 
支出
法该
地区
生产
总值 
数
字 
亿
元 
支出法国内生产总值是从最终使用的角度反映一个国家(或地区)一定时
期内生产活动最终成果的一种方法，包括最终消费支出、资本形成总额
及货物和服务净出口三部分。计算公式为：支出法国内生产总值=最终
消费支出+资本形成总额+货物和服务净出口 
gdp_fin_comsum_expend 
最终
消费
支出 
数
字 
亿
元 
最终消费支出指常住单位为满足物质、文化和精神生活的需要，从本国
经济领土和国外购买的货物和服务的支出。它不包括非常住单位在本国
经济领土内的消费支出。最终消费支出分为居民消费支出和政府消费支
出。 
gdp_household_expend 
居民
消费
支出 
数
字 
亿
元 
居民消费支出指常住住户在一定时期内对于货物和服务的全部最终消费
支出。居民消费支出除了直接以货币形式购买的货物和服务的消费支出
外，还包括以其他方式获得的货物和服务的消费支出，即所谓的虚拟消
费支出。居民虚拟消费支出包括如下几种类型：单位以实物报酬及实物
转移的形式提供给劳动者的货物和服务；住户生产并由本住户消费了的
货物和服务，其中的服务仅指住户的自有住房服务和付酬的家庭雇员提
供的家庭和个人服务；金融机构提供的金融媒介服务。 
gdp_ruarl_household_expend 
农村
居民
消费
支出 
数
字 
亿
元 
 
gdp_citizen_household_expend 
城镇
居民
消费
支出 
数
字 
亿
元 
 
gdp_gov_expend 
政府
消费
支出 
数
字 
亿
元 
政府消费支出指政府部门为全社会提供的公共服务的消费支出和免费或
以较低的价格向居民住户提供的货物和服务的净支出，前者等于政府服
务的产出价值减去政府单位所获得的经营收入的价值，后者等于政府部
门免费或以较低价格向居民住户提供的货物和服务的市场价值减去向住
户收取的价值。 
gdp_gross_capital_format 
资本
形成
总额 
数
字 
亿
元 
资本形成总额指常住单位在一定时期内获得减去处置的固定资产和存货
的净额，包括固定资本形成总额和存货增加两部分。 
gdp_gross_fixed_format 
固定
资本
数
字 
亿
元 
固定资本形成总额指常住单位在一定时期内获得的固定资产减处置的固
定资产的价值总额。固定资产是通过生产活动生产出来的，且其使用年


=== 第 172 页 ===
形成
总额 
限在一年以上、单位价值在规定标准以上的资产，不包括自然资产。可
分为有形固定资本形成总额和无形固定资本形成总额。有形固定资本形
成总额包括一定时期内完成的建筑工程、安装工程和设备工器具购置
(减处置)价值，以及土地改良、新增役、种、奶、毛、娱乐用牲畜和新
增经济林木价值。无形固定资本形成总额包括矿藏的勘探、计算机软件
等获得减处置。 
gdp_gross_inventory_format 
存货
增加 
数
字 
亿
元 
存货增加指常住单位在一定时期内存货实物量变动的市场价值，即期末
价值减期初价值的差额，再扣除当期由于价格变动而产生的持有收益。
存货增加可以是正值，也可以是负值，正值表示存货上升，负值表示存
货下降。存货包括生产单位购进的原材料、燃料和储备物资等存货，以
及生产单位生产的产成品、在制品和半成品等存货。 
gdp_net_export 
货物
和服
务净
出口 
数
字 
亿
元 
货物和服务净出口指货物和服务出口减货物和服务进口的差额。出口包
括常住单位向非常住单位出售或无偿转让的各种货物和服务的价值；进
口包括常住单位从非常住单位购买或无偿得到的各种货物和服务的价
值。由于服务活动的提供与使用同时发生，一般把常住单位从非常住单
位得到的服务作为进口，非常住单位从常住单位得到的服务作为出口。
货物的出口和进口都按离岸价格计算。 
final_consum_rate 
最终
消费
率 
数
字 
% 
最终消费率(消费率)=最终消费支出/支出法国内生产总值(除法) 
capital_format_rate 
资本
形成
率 
数
字 
% 
资本形成率(投资率)=资本形成总额/支出法国内生产总值(除法) 
分地区收入法国内生产总值表(年度) 
表名：MAC_AREA_GDP_INCOME_YEAR 
列名 
列的
含义 
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
统计
的年
度 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 
gdp_income 
收入
法该
地区
生产
总值 
数
字 
亿
元 
从收入角度计算的地区生产总值，等于劳动者报酬、生产税净额、固定资产
折旧和营业盈余之和。 


=== 第 173 页 ===
gdp_employee_payment 
劳动
者报
酬 
数
字 
亿
元 
劳动者报酬指劳动者因从事生产活动所获得的全部报酬。包括劳动者获得的
各种形式的工资、奖金和津贴，既包括货币形式的，也包括实物形式的，还
包括劳动者所享受的公费医疗和医药卫生费、上下班交通补贴、单位支付的
社会保险费、住房公积金等。 
gdp_net_tax_on_product 
生产
税净
额 
数
字 
亿
元 
生产税净额指生产税减生产补贴后的余额。生产税指政府对生产单位从事生
产、销售和经营活动以及因从事生产活动使用某些生产要素(如固定资产、
土地、劳动力)所征收的各种税、附加费和规费。生产补贴与生产税相反，
指政府对生产单位的单方面转移支出，因此视为负生产税，包括政策亏损补
贴、价格补贴等。 
gdp_fix_asset_depreciation 
固定
资产
折旧 
数
字 
亿
元 
固定资产折旧指一定时期内为弥补固定资产损耗按照规定的固定资产折旧率
提取的固定资产折旧，或按国民经济核算统一规定的折旧率虚拟计算的固定
资产折旧。它反映了固定资产在当期生产中的转移价值。各类企业和企业化
管理的事业单位的固定资产折旧是指实际计提的折旧费；不计提折旧的政府
机关、非企业化管理的事业单位和居民住房的固定资产折旧是按照统一规定
的折旧率和固定资产原值计算的虚拟折旧。原则上，固定资产折旧应按固定
资产的重置价值计算，但是目前我国尚不具备对全社会固定资产进行重估价
的基础，所以暂时只能采用上述办法。 
gdp_operate_profit 
营业
盈余 
数
字 
亿
元 
营业盈余指常住单位创造的增加值扣除劳动者报酬、生产税净额和固定资产
折旧后的余额。它相当于企业的营业利润加上生产补贴，但要扣除从利润中
开支的工资和福利等。 
国家统计局发布经济信息的日程表（年度） 
表名：MAC_STATS_REPORT_CALENDAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
report_date 
公告发布日期 
文本 
 
 
content 
公告的主题 
文本 
 
 
人民生活 
各地区居民消费水平表(年度) 
表名：MAC_AREA_CONSUME_YEAR 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
income 
居民人均可支配收入 
数字 
元 
 
income_yoy 
居民人均可支配收入_同比增长 
数字 
% 
 


=== 第 174 页 ===
urban_income 
城镇居民人均可支配收入 
数字 
元 
 
urban_income_yoy 
城镇居民人均可支配收入_同比增长 
数字 
% 
 
rural_income 
农村居民人均可支配收入 
数字 
元 
 
rural_income_yoy 
农村居民人均可支配收入_同比增长 
数字 
% 
 
expense 
居民人均消费支出 
数字 
元 
 
expense_yoy 
居民人均消费支出_同比增长 
数字 
% 
 
urban_expense 
城镇居民人均消费支出 
数字 
元 
 
urban_expense_yoy 
城镇居民人均消费支出_同比增长 
数字 
% 
 
rural_expense 
农村居民人均消费支出 
数字 
元 
 
rural_expense_yoy 
农村居民人均消费支出_同比增长 
数字 
% 
 
居民人均收入支出表(年度) 
表名：MAC_REVENUE_EXPENSE_YEAR 
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
category 
居民类型 
文
本 
 
 
income 
人均可支
配收入 
数
字 
元 
可支配收入指调查户可用于最终消费支出和其他非义务性支出以及
储蓄的总和，即居民家庭可以用来自由支配的收入。它是家庭总收
入扣除交纳的个人所得税、个人交纳的社会保障支出以及调查户的
记账补贴后的收入。计算公式为：可支配收入=家庭总收入-交纳
个人所得税-个人交纳的社会保障支出-记账补贴。 
wage_income 
人均可支
配工资性
收入 
数
字 
元 
工资收入指就业人员通过各种途径得到的全部劳动报酬，包括所从
事主要职业的工资以及从事第二职业、其他兼职和零星劳动得到的
其他劳动收入。 
business_income 
人均可支
配经营净
收入 
数
字 
元 
经营净收入指家庭成员从事生产经营活动所获得的净收入。是全部
生产经营收入中扣除生产成本和税金（但不扣除个人所得税）后所
得的收入。 
property_income 
人均可支
配财产净
收入 
数
字 
元 
财产性收入指家庭拥有的动产(如银行存款、有价证券)、不动产(如
房屋、土地等)所获得的收入。包括出让财产使用权所获得的利
息、租金、专利收入；财产营运所获得的红利收入、财产增值收益
等。 
transfer_income 
人均可支
配转移净
收入 
数
字 
元 
转移性收入指国家、单位、社会团体对居民家庭的各种转移支付和
居民家庭间的收入转移。包括政府对个人收入转移的离退休金、失
业救济金、赔偿等；单位对个人收入转移的辞退金、保险索赔、住
房公积金、家庭间的赠送和赡养等。 
expense 
人均消费
支出 
数
字 
元 
消费性支出指调查户用于本家庭日常生活的全部支出，包括食品、
衣着、居住、家庭设备用品及服务、医疗保健、交通和通信、教育
文化娱乐服务、其他商品和服务八大类等。包括用于赠送的商品或
服务。 


=== 第 175 页 ===
food_alcohol_expense 
人均食品
烟酒消费
支出 
数
字 
元 
食品消费支出指用于购买食品和在外饮食服务的相关支出，包括在
商店、集市、工作单位食堂和饮食业购买和直接消费的主食、副
食、烟草、酒、饮料以及干鲜瓜果、糖果、糕点、奶制品等。 
clothes_expense 
人均衣着
消费支出 
数
字 
元 
衣着消费支出指用于各种穿着用品及加工穿着品的各种材料的支
出，包括棉、麻、丝、毛和各种人造纤维、合成纤维纺织的各种布
匹、呢绒、绸缎及其加工的服装，各种鞋、袜、帽及其他零星穿着
用品等。 
resident_expense 
人均居住
消费支出 
数
字 
元 
居住消费支出指用于各种与居住有关的支出，包括住房、水、电、
燃料方面的支出。 
living_goods_expense 
人均生活
用品及服
务消费支
出 
数
字 
元 
 
traffic_expense 
人均交通
和通信消
费支出 
数
字 
元 
交通和通信指用于交通和通信工具及相关的各种服务费、维修费等
支出。 
education_recreation_expense 
人均教
育、文化
和娱乐消
费支出 
数
字 
元 
文教娱乐服务消费支出指用于教育和文化娱乐用品及服务的支出。 
healthcare_expense 
人均医疗
保健消费
支出 
数
字 
元 
医疗保健消费支出指用于医疗和保健的药品、用品和服务的支出。
包括医疗器具、保健用品、医药费、滋补保健品、医疗保健服务及
其他医疗保健费用。 
other_expense 
人均其他
用品及服
务消费支
出 
数
字 
元 
其他消费支出指除上述食品、衣着、居住、家庭设备及用品、医疗
保健、交通通信、文教娱乐支出以外的其他商品和服务现金支出。 
城乡居民家庭人均收入及恩格尔系数(年度) 
表名：MAC_ENGEL_COEFFICIENT_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
urban_income 
城镇居
民家庭
人均可
支配收
入 
数
字 
元 
可支配收入指调查户可用于最终消费支出和其他非义务性支出以及储蓄的总
和，即居民家庭可以用来自由支配的收入。它是家庭总收入扣除交纳的个人
所得税、个人交纳的社会保障支出以及调查户的记账补贴后的收入。计算公
式为：可支配收入=家庭总收入-交纳个人所得税-个人交纳的社会保障支出-
记账补贴。 
urban_income_index 
城镇居
民家庭
人均可
数
字 
 
1978=100，可支配收入指调查户可用于最终消费支出和其他非义务性支出
以及储蓄的总和，即居民家庭可以用来自由支配的收入。它是家庭总收入扣
除交纳的个人所得税、个人交纳的社会保障支出以及调查户的记账补贴后的


=== 第 176 页 ===
支配收
入指数 
收入。计算公式为：可支配收入=家庭总收入-交纳个人所得税-个人交纳的
社会保障支出-记账补贴。 
rural_income 
农村居
民家庭
人均纯
收入 
数
字 
元 
纯收入指农村住户当年从各个来源得到的总收入相应地扣除所发生的费用后
的收入总和。计算方法：纯收入=总收入-家庭经营费用支出-税费支出-生产
性固定资产折旧-调查补贴-赠送农村内部亲友支出。纯收入主要用于再生产
投入和当年生活消费支出，也可用于储蓄和各种非义务性支出。“农民人均
纯收入”按人口平均的纯收入水平，反映的是一个地区或一个农户农村居民
的平均收入水平。 
rural_income_index 
农村居
民家庭
人均纯
收入指
数 
数
字 
 
1978=100，纯收入指农村住户当年从各个来源得到的总收入相应地扣除所
发生的费用后的收入总和。计算方法：纯收入=总收入-家庭经营费用支出-
税费支出-生产性固定资产折旧-调查补贴-赠送农村内部亲友支出。纯收入
主要用于再生产投入和当年生活消费支出，也可用于储蓄和各种非义务性支
出。“农民人均纯收入”按人口平均的纯收入水平，反映的是一个地区或一个
农户农村居民的平均收入水平。 
urban_engel_coefficient 
城镇居
民家庭
恩格尔
系数 
数
字 
% 
 
rural_engel_coefficient 
农村居
民家庭
恩格尔
系数 
数
字 
% 
 
城乡居民人民币储蓄存款表(年度) 
表名：MAC_RESIDENT_SAVING_DEPOSIT_YEAR 
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
deposit 
城乡居民人民币储蓄存
款年底余额 
数
字 
亿
元 
人民币储蓄存款余额是指城乡居民在某一时点上在银行
和其他金融机构的人民币储蓄存款总额。 
time_deposit 
城乡居民人民币定期储
蓄存款年底余额 
数
字 
亿
元 
 
demand_deposit 
城乡居民人民币活期储
蓄存款年底余额 
数
字 
亿
元 
 
deposit_increase 
城乡居民人民币储蓄存
款年增加额 
数
字 
亿
元 
 
time_deposit_increase 
城乡居民人民币定期储
蓄存款年增加额 
数
字 
亿
元 
 
demand_deposit_increase 
城乡居民人民币活期储
蓄存款年增加额 
数
字 
亿
元 
 


=== 第 177 页 ===
分地区城镇居民家庭平均每人全年收入来源表(年度) 
表名：MAC_AREA_URBAN_INCOME_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
 
area_name 
地区名
称 
文
本 
 
 
disposable_income 
城镇居
民人均
可支配
收入 
数
字 
元 
可支配收入指调查户可用于最终消费支出和其他非义务性支出以及储蓄的总
和，即居民家庭可以用来自由支配的收入。它是家庭总收入扣除交纳的个人所
得税、个人交纳的社会保障支出以及调查户的记账补贴后的收入。计算公式
为：可支配收入=家庭总收入-交纳个人所得税-个人交纳的社会保障支出-记账
补贴。 
income 
城镇居
民人均
总收入 
数
字 
元 
家庭总收入指调查户中生活在一起的所有家庭成员在调查期得到的工资性收
入、经营净收入、财产性收入、转移性收入的总和，不包括出售财物和借贷收
入。收入的统计标准以实际发生的数额为准，无论收入是补发还是预发，只要
是调查期得到的都应如实计算，原则上不作分摊。 
wage_income 
城镇居
民人均
工资性
收入 
数
字 
元 
工资收入指就业人员通过各种途径得到的全部劳动报酬，包括所从事主要职业
的工资以及从事第二职业、其他兼职和零星劳动得到的其他劳动收入。 
business_income 
城镇居
民人均
经营净
收入 
数
字 
元 
经营净收入指家庭成员从事生产经营活动所获得的净收入。是全部生产经营收
入中扣除生产成本和税金（但不扣除个人所得税）后所得的收入。 
property_income 
城镇居
民人均
财产性
收入 
数
字 
元 
财产性收入指家庭拥有的动产(如银行存款、有价证券)、不动产(如房屋、土地
等)所获得的收入。包括出让财产使用权所获得的利息、租金、专利收入；财产
营运所获得的红利收入、财产增值收益等。 
transfer_income 
城镇居
民人均
转移性
收入 
数
字 
元 
转移性收入指国家、单位、社会团体对居民家庭的各种转移支付和居民家庭间
的收入转移。包括政府对个人收入转移的离退休金、失业救济金、赔偿等；单
位对个人收入转移的辞退金、保险索赔、住房公积金、家庭间的赠送和赡养
等。 
分地区城镇及农村居民家庭平均每人全年消费性支出表(年度) 
表名：MAC_AREA_URBAN_RURAL_EXPENSE_YEAR 


=== 第 178 页 ===
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
category 
居民类
型 
文
本 
 
 
expense 
家庭人
均现金
消费支
出 
数
字 
元 
消费性支出指调查户用于本家庭日常生活的全部支出，包括食
品、衣着、居住、家庭设备用品及服务、医疗保健、交通和通
信、教育文化娱乐服务、其他商品和服务八大类等。包括用于赠
送的商品或服务。 
food_expense 
家庭人
均食品
消费支
出 
数
字 
元 
食品消费支出指用于购买食品和在外饮食服务的相关支出，包括
在商店、集市、工作单位食堂和饮食业购买和直接消费的主食、
副食、烟草、酒、饮料以及干鲜瓜果、糖果、糕点、奶制品等。 
clothes_expense 
家庭人
均衣着
消费支
出 
数
字 
元 
衣着消费支出指用于各种穿着用品及加工穿着品的各种材料的支
出，包括棉、麻、丝、毛和各种人造纤维、合成纤维纺织的各种
布匹、呢绒、绸缎及其加工的服装，各种鞋、袜、帽及其他零星
穿着用品等。 
resident_expense 
家庭人
均居住
消费支
出 
数
字 
元 
居住消费支出指用于各种与居住有关的支出，包括住房、水、
电、燃料方面的支出。 
household_equipment_expense 
家庭人
均家庭
设备及
用品消
费支出 
数
字 
元 
家庭设备及用品消费支出指用于家庭各类日用消费品及家庭服务
的支出。包括日用耐用消费品、室内装饰品、床上用品、家庭日
用杂品、家具、家庭服务。 
healthcare_expense 
家庭人
均医疗
保健消
费支出 
数
字 
元 
医疗保健消费支出指用于医疗和保健的药品、用品和服务的支
出。包括医疗器具、保健用品、医药费、滋补保健品、医疗保健
服务及其他医疗保健费用。 
traffic_expense 
家庭人
均交通
和通信
消费支
出 
数
字 
元 
交通和通信指用于交通和通信工具及相关的各种服务费、维修费
等支出。 
education_recreation_expense 
家庭人
均文教
娱乐服
务消费
支出 
数
字 
元 
文教娱乐服务消费支出指用于教育和文化娱乐用品及服务的支
出。 


=== 第 179 页 ===
other_expense 
家庭人
均其它
消费支
出 
数
字 
元 
其他消费支出指除上述食品、衣着、居住、家庭设备及用品、医
疗保健、交通通信、文教娱乐支出以外的其他商品和服务现金支
出。 
农村居民家庭平均每人纯收入(年度) 
表名：MAC_RURAL_NET_INCOME_YEAR 
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
income 
农村居民家
庭平均每人
纯收入 
数
字 
元 
纯收入指农村住户当年从各个来源得到的总收入相应地扣除所发生
的费用后的收入总和。计算方法：纯收入=总收入-家庭经营费用支
出-税费支出-生产性固定资产折旧-调查补贴-赠送农村内部亲友支
出。纯收入主要用于再生产投入和当年生活消费支出，也可用于储
蓄和各种非义务性支出。“农民人均纯收入”按人口平均的纯收入水
平，反映的是一个地区或一个农户农村居民的平均收入水平。 
wage_income 
农村居民家
庭平均每人
工资性纯收
入 
数
字 
元 
 
business_income 
农村居民家
庭平均每人
家庭经营纯
收入 
数
字 
元 
 
property_income 
农村居民家
庭平均每人
财产性纯收
入 
数
字 
元 
 
transfer_income 
农村居民家
庭平均每人
转移性纯收
入 
数
字 
元 
 
farming_income 
农村居民家
庭平均每人
农业纯收入 
数
字 
元 
 
forestry_income 
农村居民家
庭平均每人
林业纯收入 
数
字 
元 
 
animal_husbandry_income 
农村居民家
庭平均每人
牧业纯收入 
数
字 
元 
 


=== 第 180 页 ===
fishery_income 
农村居民家
庭平均每人
渔业纯收入 
数
字 
元 
 
industry_income 
农村居民家
庭平均每人
工业纯收入 
数
字 
元 
 
construction_income 
农村居民家
庭平均每人
建筑业纯收
入 
数
字 
元 
 
traffic_income 
农村居民家
庭平均每人
交通运输
业、邮电业
纯收入 
数
字 
元 
 
wholesale_income 
农村居民家
庭平均每人
批发、零售
贸易及餐饮
业纯收入 
数
字 
元 
 
service_income 
农村居民家
庭平均每人
社会服务业
纯收入 
数
字 
元 
 
education_culture_income 
农村居民家
庭平均每人
文教卫生业
纯收入 
数
字 
元 
 
other_income 
农村居民家
庭平均每人
其他纯收入 
数
字 
元 
 
各地区按来源分农村居民家庭人均纯收入(年度) 
表名：MAC_AREA_RURAL_NET_INCOME_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 


=== 第 181 页 ===
income 
农村居
民家庭
人均纯
收入 
数
字 
元 
纯收入指农村住户当年从各个来源得到的总收入相应地扣除所发生的费用后的收入
总和。计算方法：纯收入=总收入-家庭经营费用支出-税费支出-生产性固定资产折
旧-调查补贴-赠送农村内部亲友支出。纯收入主要用于再生产投入和当年生活消费
支出，也可用于储蓄和各种非义务性支出。“农民人均纯收入”按人口平均的纯收入
水平，反映的是一个地区或一个农户农村居民的平均收入水平。 
wage_income 
农村居
民家庭
人均工
资性纯
收入 
数
字 
元 
工资性收入指农村住户成员受雇于单位或个人，靠出卖劳动力而获得的全部劳动报
酬和各种福利收入。 
business_income 
农村居
民家庭
人均家
庭经营
纯收入 
数
字 
元 
农村居民家庭经营收入指农村住户以家庭为生产经营单位进行生产筹划和管理而获
得的收入。家庭经营活动按行业划分为农业、林业、畜牧业、渔业、工业、建筑
业、交通运输和邮电业、批发和零售贸易餐饮业、社会服务业、文教卫生业和其他
家庭经营。 
property_income 
农村居
民家庭
人均财
产性纯
收入 
数
字 
元 
农村居民财产性收入指金融资产或有形非生产性资产的所有者向其他机构单位提供
资金或将有形非生产性资产供其支配，作为回报而从中获得的收入。 
transfer_income 
农村居
民家庭
人均转
移性纯
收入 
数
字 
元 
农村居民转移性收入指农村住户和住户成员无须付出任何对应物而获得的货物、服
务、资金或资产所有权等，不包括无偿提供的用于固定资本形成的资金。一般情况
下，指农村住户在二次分配中的所有收入。农村居民家庭平均每人转移性纯收入不
包括农村内部亲友赠送收入。 
分地区农村居民家庭住房情况表(年度) 
表名：MAC_AREA_RURAL_HOUSE_YEAR 
列名 
列的含
义 
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
统计年
份 
文
本 
 
YYYY 
area_code 
地区代
码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名
称 
文
本 
 
 
house_area 
农村居
民人均
住房面
积 
数
字 
平
方
米/
人 
住宅建筑面积是指房屋外墙勒脚以上的外围水平面积，包括阳台、走廊、室
外楼梯等的建筑面积。 
house_value 
农村居
民家庭
数
字 
元/
平
住房价值指农村住户期末居住的房屋当初购买或新建时的价值。新建房屋的
价值可按实际消耗的建筑材料和人工的报酬计算，有的地方，人工不要报


=== 第 182 页 ===
住房价
值 
方
米 
酬，只管吃喝，可将吃喝的费用，当作报酬，计入房价内。原有房屋，按房
屋质量和新旧程度，根据当地实际情况进行估价。对原有房屋进行大翻修
的，也应考虑在内。 
concrete_structure 
农村居
民家庭
住房钢
筋混凝
土结构 
数
字 
平
方
米/
人 
钢筋混凝土结构是指房屋的梁、柱、承重墙等主要部分是用钢筋混凝土建造
的住房。 
brick_wood_structure 
农村居
民家庭
住房砖
木结构 
数
字 
平
方
米/
人 
砖木结构是指梁、柱、承重墙等主要部分是用砖、石和木料建造的的住房。
以砖、石作墙基的土坯房不包括在内。 
人口信息 
人口基本情况表(年度) 
表名：MAC_POPULATION_YEAR 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
population 
年末常住
人口 
数
字 
 
年末人口数指每年12 月31 日24 时的人口数。年度统计的全国人口总数内未包括
香港、澳门特别行政区和台湾省以及海外华侨人数。 
male 
男性人口 
数
字 
 
 
female 
女性人口 
数
字 
 
 
urban 
城镇人口 
数
字 
 
城镇人口是指居住在城镇范围内的全部常住人口。 
rural 
乡村人口 
数
字 
 
乡村人口是除城镇人口以外的全部人口。 
birth_rate 
人口出生
率 
数
字 
‰ 
 
death_rate 
人口死亡
率 
数
字 
‰ 
 
growth_rate 
人口自然
增长率 
数
字 
‰ 
 


=== 第 183 页 ===
各地区人口平均预期寿命表（年度） 
表名：MAC_LIFE_EXPECT 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 
life_expect 
平均
预期
寿命 
数
字 
岁 
平均预期寿命是指已经活到一定岁数的人平均还能再活的年数。它是反映人类健康
水平、死亡水平的综合指标，其高低主要受社会经济条件和医疗水平等因素的制
约，不同社会、不同时期有很大差别。在不特别指明岁数的情况下，平均预期寿命
就是指0 岁人口的平均预期寿命。 
male_life_expect 
男性
平均
预期
寿命 
数
字 
岁 
平均预期寿命是指已经活到一定岁数的人平均还能再活的年数。它是反映人类健康
水平、死亡水平的综合指标，其高低主要受社会经济条件和医疗水平等因素的制
约，不同社会、不同时期有很大差别。在不特别指明岁数的情况下，平均预期寿命
就是指0 岁人口的平均预期寿命。 
female_life_expect 
女性
平均
预期
寿命 
数
字 
岁 
平均预期寿命是指已经活到一定岁数的人平均还能再活的年数。它是反映人类健康
水平、死亡水平的综合指标，其高低主要受社会经济条件和医疗水平等因素的制
约，不同社会、不同时期有很大差别。在不特别指明岁数的情况下，平均预期寿命
就是指0 岁人口的平均预期寿命。 
按年龄和性别分人口数表（年度） 
表名：MAC_POPULATION_AGE 
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
age 
年龄段 
文
本 
 
 
rate 
该年龄段占总抽样人口的比
例 
数
字 
 
 
population 
该年龄段的人口数 
数
字 
 
 


=== 第 184 页 ===
male 
该年龄段的男性人口数 
数
字 
 
 
female 
该年龄段的女性人口数 
数
字 
 
 
gender_ratio 
该年龄段的性别比 
数
字 
 
性别比指人口中男性与女性人口之比（以女性人口为
100）。 
各地区户数、人口数、性别比和户规模表（年度） 
表名：MAC_AREA_HOUSEHOLD_SIZE 
列名 
列的
含义 
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
统计
年份 
文
本 
 
YYYY 
area_code 
地区
代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区
名称 
文
本 
 
 
household 
总户
数(人
口抽
样调
查) 
数
字 
户 
 
family_household 
家庭
户户
数(人
口抽
样调
查) 
数
字 
户 
 
collective_household 
集体
户户
数(人
口抽
样调
查) 
数
字 
户 
 
family_household_population 
家庭
户人
口数
(人口
抽样
调查) 
数
字 
人 
家庭户是指以家庭成员关系为主的人口，或者还有其他人口，居住
一处共同生活的,作为一个家庭户。单身居住独自生活的也作为一个
家庭户。居住生活在同一家庭户的人，不论其工作性质如何，农业
户口还是非农业户口，有无正式户口，都应登记为一户。 
male_family 
家庭
户男
数
字 
人 
 


=== 第 185 页 ===
性人
口数
(人口
抽样
调查) 
female_family 
家庭
户女
性人
口数
(人口
抽样
调查) 
数
字 
人 
 
collective_household_population 
集体
户人
口数
(人口
抽样
调查) 
数
字 
人 
集体户是指相互之间没有家庭成员关系，集体居住在机关、团体、
学校、工厂、矿山、工地、农场、公司、商店、医院、托儿所、敬
老院、寺院、教堂等单位内集体宿舍及其他住所共同生活的人口，
作为集体户。从事各种流动作业、集体居住的人口，也作为集体户
登记。集体户以居住在同一房间的人作为一个集体户进行登记。 
male_collective 
集体
户男
性人
口数
(人口
抽样
调查) 
数
字 
人 
 
female_collective 
集体
户女
性人
口数
(人口
抽样
调查) 
数
字 
人 
 
户口登记状况（年度） 
表名：MAC_AREA_HOUSEHOLD_REGISTER 
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
area_code 
地区代码 
文
本 
 
关
联:MAC_AREA_DIV.area_code 


=== 第 186 页 ===
area_name 
地区名称 
文
本 
 
 
population 
人口数(人口抽样调查) 
数
字 
人 
 
male 
男性人口数(人口抽样调查) 
数
字 
人 
 
female 
女性人口数(人口抽样调查) 
数
字 
人 
 
residing 
住本乡、镇、街道，户口在本乡、镇、街道人
口数(人口抽样调查) 
数
字 
人 
 
male_residing 
住本乡、镇、街道，户口在本乡、镇、街道男
性人口数(人口抽样调查) 
数
字 
人 
 
female_residing 
住本乡、镇、街道，户口在本乡、镇、街道女
性人口数(人口抽样调查) 
数
字 
人 
 
residing_6months 
住本乡、镇、街道，户口在外乡、镇、街道，
离开户口登记地半年以上人口数(人口抽样调查) 
数
字 
人 
 
male_residing_6months 
住本乡、镇、街道，户口在外乡、镇、街道，
离开户口登记地半年以上男性人口数(人口抽样
调查) 
数
字 
人 
 
female_residing_6months 
住本乡、镇、街道，户口在外乡、镇、街道，
离开户口登记地半年以上女性人口数(人口抽样
调查) 
数
字 
人 
 
household_unsettle 
住本乡、镇、街道，户口待定人口数(人口抽样
调查) 
数
字 
人 
 
male_household_unsettle 
住本乡、镇、街道，户口待定男性人口数(人口
抽样调查) 
数
字 
人 
 
female_household_unsettle 
住本乡、镇、街道，户口待定女性人口数(人口
抽样调查) 
数
字 
人 
 
residing_abroad 
居住在港澳台或国外，户口在本乡、镇、街道
人口数(人口抽样调查) 
数
字 
人 
 
male_residing_abroad 
居住在港澳台或国外，户口在本乡、镇、街道
男性人口数(人口抽样调查) 
数
字 
人 
 
female_residing_abroad 
居住在港澳台或国外，户口在本乡、镇、街道
女性人口数(人口抽样调查) 
数
字 
人 
 
各地区人口年龄结构和抚养比例表（年度） 
表名：MAC_AREA_POP_DEPENDENCY 
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


=== 第 187 页 ===
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
population 
人口数
(人口抽
样调查) 
数
字 
人 
 
age_between_0_and_14 
0-14 岁
人口数
(人口抽
样调查) 
数
字 
人 
 
age_between_15_and_64 
15-64 岁
人口数
(人口抽
样调查) 
数
字 
人 
 
age_over_65 
65 岁及
以上人口
数(人口
抽样调
查) 
数
字 
人 
 
dependency_ratio 
总抚养比
(人口抽
样调查) 
数
字 
% 
总抚养比也称总负担系数。指人口总体中非劳动年龄人口数与劳动年
龄人口数之比。通常用百分比表示。说明每100 名劳动年龄人口大致
要负担多少名非劳动年龄人口。用于从人口角度反映人口与经济发展
的基本关系。 
children_dependency_ratio 
少年儿童
抚养比
(人口抽
样调查) 
数
字 
% 
少年儿童抚养比也称少年儿童抚养系数。指某一人口中少年儿童人口
数与劳动年龄人口数之比。通常用百分比表示。以反映每100 名劳动
年龄人口要负担多少名少年儿童。 
old_dependency_ratio 
老年人口
抚养比
(人口抽
样调查) 
数
字 
% 
老年人口抚养比也称老年人口抚养系数。指某一人口中老年人口数与
劳动年龄人口数之比。通常用百分比表示。用以表明每100 名劳动年
龄人口要负担多少名老年人。老年人口抚养比是从经济角度反映人口
老化社会后果的指标之一。 
各地区按性别和婚姻状况分的人口表（年度） 
表名：MAC_AREA_POP_MARITAL 
列名 
列的含义 
类
型 
单
位 
说明 
id 
id 
 
 
 
stat_year 
统计年份 
 
 
YYYY 
area_code 
地区代码 
 
 
关
联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
 
 
 
age_over_15 
15 岁及以上人口数(人口抽样调查) 
 
人 
 
male_age_over_15 
15 岁及以上男性人口数(人口抽样调查) 
 
人 
 


=== 第 188 页 ===
female_age_over_15 
15 岁及以上女性人口数(人口抽样调查) 
 
人 
 
never_married 
15 岁及以上未婚人口数(人口抽样调查) 
 
人 
 
male_never_married 
15 岁及以上男性未婚人口数(人口抽样调查) 
 
人 
 
female_never_married 
15 岁及以上女性未婚人口数(人口抽样调查) 
 
人 
 
first_married 
15 岁及以上初婚有配偶人口数(人口抽样调查) 
 
人 
 
male_first_married 
15 岁及以上男性初婚有配偶人口数(人口抽样调
查) 
 
人 
 
female_first_married 
15 岁及以上女性初婚有配偶人口数(人口抽样调
查) 
 
人 
 
remarried 
15 岁及以上再婚有配偶人口数(人口抽样调查) 
 
人 
 
male_remarried 
15 岁及以上男性再婚有配偶人口数(人口抽样调
查) 
 
人 
 
female_remarried 
15 岁及以上女性再婚有配偶人口数(人口抽样调
查) 
 
人 
 
divorced 
15 岁及以上离婚人口数(人口抽样调查) 
 
人 
 
male_divorced 
15 岁及以上男性离婚人口数(人口抽样调查) 
 
人 
 
female_divorced 
15 岁及以上女性离婚人口数(人口抽样调查) 
 
人 
 
widowed 
15 岁及以上丧偶人口数(人口抽样调查) 
 
人 
 
male_widowed 
15 岁及以上男性丧偶人口数(人口抽样调查) 
 
人 
 
female_widowed 
15 岁及以上女性丧偶人口数(人口抽样调查) 
 
人 
 
各地区按性别和受教育程度分人口情况表（年度） 
表名：MAC_AREA_POP_EDUCATION 
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
area_code 
地区代码 
文
本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文
本 
 
 
age_over_6 
6 岁及6 岁以
上人口数(人口
抽样调查) 
数
字 
人 
 
male_age_over_6 
6 岁及6 岁以
上男性人口数
(人口抽样调查) 
数
字 
人 
 
female_age_over_6 
6 岁及6 岁以
上女性人口数
(人口抽样调查) 
数
字 
人 
 


=== 第 189 页 ===
no_schooling 
6 岁及6 岁以
上未上过学人
口数(人口抽样
调查) 
数
字 
人 
 
male_no_schooling 
6 岁及6 岁以
上未上过学男
性人口数(人口
抽样调查) 
数
字 
人 
 
female_no_schooling 
6 岁及6 岁以
上未上过学女
性人口数(人口
抽样调查) 
数
字 
人 
 
primary_school 
6 岁及6 岁以
上小学人口数
(人口抽样调查) 
数
字 
人 
小学指接受的最高一级教育为小学,无论其是否在校、毕
业、肄业或辍学 
male_primary_school 
6 岁及6 岁以
上小学男性人
口数(人口抽样
调查) 
数
字 
人 
 
female_primary_school 
6 岁及6 岁以
上小学女性人
口数(人口抽样
调查) 
数
字 
人 
 
junior_secondary_school 
6 岁及6 岁以
上初中人口数
(人口抽样调查) 
数
字 
人 
初中指接受的最高一级教育为初中,无论其是否在校、毕
业、肄业或辍学。相当于初中程度的技工学校，也属于此
类。 
male_junior_secondary_school 
6 岁及6 岁以
上初中男性人
口数(人口抽样
调查) 
数
字 
人 
 
female_junior_secondary_school 
6 岁及6 岁以
上初中女性人
口数(人口抽样
调查) 
数
字 
人 
 
senior_secondary_school 
6 岁及6 岁以
上高中人口数
(人口抽样调查) 
数
字 
人 
高中指接受的最高一级教育为普通高中、职业高中和中等
专业学校，无论其是否在校、毕业、肄业或辍学。相当于
高中程度的技工学校，也属于此类。 
male_senior_secondary_school 
6 岁及6 岁以
上高中男性人
口数(人口抽样
调查) 
数
字 
人 
 
female_senior_secondary_school 
6 岁及6 岁以
上高中女性人
口数(人口抽样
调查) 
数
字 
人 
 
college 
6 岁及6 岁以
上大专及以上
数
字 
人 
大学专科指接受的最高一级教育为大学专科。在普通高等
学校学习大学专科的，无论其是否在校、毕业、肄业或辍
学，都属于此类。 


=== 第 190 页 ===
人口数(人口抽
样调查) 
male_college 
6 岁及6 岁以
上大专及以上
男性人口数(人
口抽样调查) 
数
字 
人 
 
female_college 
6 岁及6 岁以
上大专及以上
女性人口数(人
口抽样调查) 
数
字 
人 
 
各地区按性别分的15 岁及以上文盲人口表（年度） 
表名：MAC_AREA_POP_ILLITERATE 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
age_over_15 
15 岁及以上人口数(人口抽样调查) 
数字 
人 
 
male_age_over_15 
15 岁及以上男性人口数(人口抽样调查) 
数字 
人 
 
female_age_over_15 
15 岁及以上女性人口数(人口抽样调查) 
数字 
人 
 
illiterate 
15 岁及以上文盲人口数(人口抽样调查) 
数字 
人 
 
male_illiterate 
15 岁及以上男性文盲人口数(人口抽样调查) 
数字 
人 
 
female_illiterate 
15 岁及以上女性文盲人口数(人口抽样调查) 
数字 
人 
 
各地区按家庭户规模分的户数表（年度） 
表名：MAC_AREA_FAMILY_HOUSEHOLD 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
area_code 
地区代码 
文本 
 
关联:MAC_AREA_DIV.area_code 
area_name 
地区名称 
文本 
 
 
family_household 
家庭户户数(人口抽样调查) 
数字 
户 
 
one_persons 
一人户家庭户户数(人口抽样调查) 
数字 
户 
 
two_persons 
二人户家庭户户数(人口抽样调查) 
数字 
户 
 
three_persons 
三人户家庭户户数(人口抽样调查) 
数字 
户 
 
four_persons 
四人户家庭户户数(人口抽样调查) 
数字 
户 
 
five_persons 
五人户家庭户户数(人口抽样调查) 
数字 
户 
 
six_persons 
六人户家庭户户数(人口抽样调查) 
数字 
户 
 


=== 第 191 页 ===
seven_persons 
七人户家庭户户数(人口抽样调查) 
数字 
户 
 
eight_persons 
八人户家庭户户数(人口抽样调查) 
数字 
户 
 
nine_persons 
九人户家庭户户数(人口抽样调查) 
数字 
户 
 
over_ten_persons 
十人及以上户家庭户户数(人口抽样调查) 
数字 
户 
 
育龄妇女分年龄生育状况表（年度） 
表名：MAC_POP_FERTILITY_RATE 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
age 
年龄段 
文本 
 
 
rate 
该年龄段育龄妇女占抽样人数比例 
数字 
 
 
population 
该年龄段平均育龄妇女人数(人口抽样调查) 
数字 
人 
 
births 
该年龄段育龄妇女生育孩子的人数(人口抽样调查) 
数字 
人 
 
first_births 
该年龄段育龄妇女第一孩次出生人口数(人口抽样调查) 
数字 
人 
 
second_births 
该年龄段育龄妇女第二孩次出生人口数(人口抽样调查) 
数字 
人 
 
third_births 
该年龄段育龄妇女第三孩次及以上出生人口数(人口抽样调查) 
数字 
人 
 
fertility_rate 
该年龄段育龄妇女的生育率(人口抽样调查) 
数字 
‰ 
 
first_fertility_rate 
该年龄段育龄妇女第一孩次生育率(人口抽样调查) 
数字 
‰ 
 
second_fertility_rate 
该年龄段育龄妇女第二孩次生育率(人口抽样调查) 
数字 
‰ 
 
third_fertility_rate 
该年龄段育龄妇女第三孩次及以上生育率(人口抽样调查) 
数字 
‰ 
 
人口年龄结构和抚养比例表（年度） 
表名：MAC_POPULATION_DEPENDENCY 
列名 
列的含义 
类型 
单位 
说明 
id 
id 
数字 
 
 
stat_year 
统计年份 
文本 
 
YYYY 
population 
人口数(人口抽样调查) 
数字 
人 
 
age_between_0_and_14 
0-14 岁人口数(人口抽样调查) 
数字 
人 
 
age_between_15_and_64 
15-64 岁人口数(人口抽样调查) 
数字 
人 
 
age_over_65 
65 岁及以上人口数(人口抽样调查) 
数字 
人 
 
dependency_ratio 
总抚养比(人口抽样调查) 
数字 
% 
 
children_dependency_ratio 
少年儿童抚养比(人口抽样调查) 
数字 
% 
 
old_dependency_ratio 
老年人口抚养比(人口抽样调查) 
数字 
% 
 
  
 
 
 



## 图片

- /tmp/jqdata_query_pdf_images/page_1_img_1.png
- /tmp/jqdata_query_pdf_images/page_1_img_2.png
