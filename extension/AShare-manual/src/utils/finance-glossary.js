// 金融术语获取工具
// 支持多个数据源：Investopedia、Wikipedia、Alpha Vantage、本地缓存

const GLOSSARY_CACHE = new Map();
const API_CACHE_DURATION = 24 * 60 * 60 * 1000; // 24小时缓存

// 本地金融术语库（核心术语）
export const LOCAL_GLOSSARY = {
  'CAGR': {
    term: 'CAGR',
    fullName: 'Compound Annual Growth Rate',
    description: '复合年增长率，衡量投资或业务在特定时间段内的年均增长速度',
    category: '财务指标',
    example: '一家公司5年内从100万增长到200万，CAGR = (200/100)^(1/5) - 1 = 14.87%'
  },
  'TAM': {
    term: 'TAM',
    fullName: 'Total Addressable Market',
    description: '可寻址市场总规模，指产品或服务在特定市场中的最大潜在需求',
    category: '市场分析',
    example: '电动汽车TAM = 全球汽车市场 × 电动化渗透率'
  },
  'ROE': {
    term: 'ROE',
    fullName: 'Return on Equity',
    description: '净资产收益率，衡量公司利用股东投资创造利润的效率',
    category: '财务指标',
    example: 'ROE = 净利润 / 股东权益，通常>15%为优秀'
  },
  'PEG': {
    term: 'PEG',
    fullName: 'Price/Earnings to Growth',
    description: '市盈率相对盈利增长比率，用于评估成长股的估值合理性',
    category: '估值指标',
    example: 'PEG = PE / 盈利增长率，<1通常认为被低估'
  },
  'EBITDA': {
    term: 'EBITDA',
    fullName: 'Earnings Before Interest, Taxes, Depreciation and Amortization',
    description: '息税折旧摊销前利润，反映公司核心经营盈利能力',
    category: '财务指标',
    example: 'EBITDA = 净利润 + 利息 + 税费 + 折旧 + 摊销'
  },
  '护城河': {
    term: '护城河',
    fullName: 'Economic Moat',
    description: '企业长期竞争优势，能够抵御竞争对手侵蚀的能力',
    category: '投资分析',
    example: '品牌价值、专利技术、网络效应、规模经济等'
  },
  '高倍股': {
    term: '高倍股',
    fullName: 'Multibagger',
    description: '能够带来数倍回报的股票，通常指3-10倍以上收益',
    category: '投资概念',
    example: '如NVIDIA、特斯拉等在特定时期的表现'
  },
  '自由现金流': {
    term: '自由现金流',
    fullName: 'Free Cash Flow',
    description: '企业经营活动产生的现金减去资本支出后的净现金流',
    category: '财务指标',
    example: 'FCF = 经营现金流 - 资本支出'
  },
  '估值': {
    term: '估值',
    fullName: 'Valuation',
    description: '对企业或资产价值的评估，常用PE、PB、PS等指标',
    category: '投资分析',
    example: 'PE估值、DCF估值、相对估值等'
  },
  '技术分析': {
    term: '技术分析',
    fullName: 'Technical Analysis',
    description: '通过价格图表和交易量分析预测股价走势的方法',
    category: '分析方法',
    example: '移动平均线、RSI、MACD等技术指标'
  },
  // 新增金融术语
  'PE': {
    term: 'PE',
    fullName: 'Price-to-Earnings Ratio',
    description: '市盈率，股价与每股收益的比率，衡量股票估值水平',
    category: '估值指标',
    example: 'PE = 股价 / 每股收益，通常15-25倍为合理区间'
  },
  'PB': {
    term: 'PB',
    fullName: 'Price-to-Book Ratio',
    description: '市净率，股价与每股净资产的比率',
    category: '估值指标',
    example: 'PB = 股价 / 每股净资产，<1可能被低估'
  },
  'PS': {
    term: 'PS',
    fullName: 'Price-to-Sales Ratio',
    description: '市销率，股价与每股销售额的比率',
    category: '估值指标',
    example: 'PS = 股价 / 每股销售额，成长股通常>10'
  },
  'ROA': {
    term: 'ROA',
    fullName: 'Return on Assets',
    description: '总资产收益率，衡量公司利用总资产创造利润的效率',
    category: '财务指标',
    example: 'ROA = 净利润 / 总资产，>5%为良好'
  },
  'ROIC': {
    term: 'ROIC',
    fullName: 'Return on Invested Capital',
    description: '投资资本回报率，衡量投入资本的盈利能力',
    category: '财务指标',
    example: 'ROIC = 税后营业利润 / 投资资本，>15%为优秀'
  },
  '毛利率': {
    term: '毛利率',
    fullName: 'Gross Margin',
    description: '毛利润与营业收入的比率，反映产品盈利能力',
    category: '财务指标',
    example: '毛利率 = (营业收入 - 营业成本) / 营业收入'
  },
  '净利率': {
    term: '净利率',
    fullName: 'Net Margin',
    description: '净利润与营业收入的比率，反映整体盈利能力',
    category: '财务指标',
    example: '净利率 = 净利润 / 营业收入'
  },
  '负债率': {
    term: '负债率',
    fullName: 'Debt-to-Equity Ratio',
    description: '总负债与股东权益的比率，衡量财务杠杆水平',
    category: '财务指标',
    example: '负债率 = 总负债 / 股东权益，<1为安全'
  },
  '流动比率': {
    term: '流动比率',
    fullName: 'Current Ratio',
    description: '流动资产与流动负债的比率，衡量短期偿债能力',
    category: '财务指标',
    example: '流动比率 = 流动资产 / 流动负债，>1为安全'
  },
  '速动比率': {
    term: '速动比率',
    fullName: 'Quick Ratio',
    description: '速动资产与流动负债的比率，更严格的短期偿债能力指标',
    category: '财务指标',
    example: '速动比率 = (流动资产 - 存货) / 流动负债'
  },
  'DCF': {
    term: 'DCF',
    fullName: 'Discounted Cash Flow',
    description: '现金流折现法，通过未来现金流折现计算企业价值',
    category: '估值方法',
    example: 'DCF = Σ(未来现金流 / (1+折现率)^n)'
  },
  'Beta': {
    term: 'Beta',
    fullName: 'Beta Coefficient',
    description: '贝塔系数，衡量股票相对于市场的波动性',
    category: '风险指标',
    example: 'Beta>1表示波动性大于市场，<1表示波动性小于市场'
  },
  'Alpha': {
    term: 'Alpha',
    fullName: 'Alpha',
    description: '阿尔法系数，衡量投资组合相对于市场的超额收益',
    category: '绩效指标',
    example: 'Alpha>0表示超额收益，<0表示跑输市场'
  },
  '夏普比率': {
    term: '夏普比率',
    fullName: 'Sharpe Ratio',
    description: '风险调整后收益率，衡量单位风险下的超额收益',
    category: '绩效指标',
    example: '夏普比率 = (收益率 - 无风险利率) / 标准差'
  },
  '最大回撤': {
    term: '最大回撤',
    fullName: 'Maximum Drawdown',
    description: '投资期间的最大损失幅度，衡量下行风险',
    category: '风险指标',
    example: '从峰值到谷值的最大百分比损失'
  },
  '波动率': {
    term: '波动率',
    fullName: 'Volatility',
    description: '价格变动的标准差，衡量价格波动程度',
    category: '风险指标',
    example: '年化波动率通常用日收益率标准差×√252计算'
  },
  '相关性': {
    term: '相关性',
    fullName: 'Correlation',
    description: '两个资产价格变动的关联程度，-1到1之间',
    category: '投资分析',
    example: '相关性=1表示完全正相关，=-1表示完全负相关'
  },
  '分散化': {
    term: '分散化',
    fullName: 'Diversification',
    description: '通过投资不同资产降低整体投资组合风险',
    category: '投资策略',
    example: '投资不同行业、地区、资产类别来分散风险'
  },
  '资产配置': {
    term: '资产配置',
    fullName: 'Asset Allocation',
    description: '在不同资产类别间的资金分配策略',
    category: '投资策略',
    example: '股票60%、债券30%、现金10%的配置'
  },
  '再平衡': {
    term: '再平衡',
    fullName: 'Rebalancing',
    description: '定期调整投资组合权重回到目标配置',
    category: '投资策略',
    example: '每季度调整股票债券比例回到60:40'
  },
  '定投': {
    term: '定投',
    fullName: 'Dollar-Cost Averaging',
    description: '定期定额投资，平滑价格波动影响',
    category: '投资策略',
    example: '每月固定投资1000元购买指数基金'
  },
  '价值投资': {
    term: '价值投资',
    fullName: 'Value Investing',
    description: '寻找被低估的股票，关注内在价值',
    category: '投资理念',
    example: '购买PE<15、PB<1的优质公司'
  },
  '成长投资': {
    term: '成长投资',
    fullName: 'Growth Investing',
    description: '投资高增长潜力的公司，关注未来收益',
    category: '投资理念',
    example: '投资收入增长率>20%的科技公司'
  },
  '动量投资': {
    term: '动量投资',
    fullName: 'Momentum Investing',
    description: '基于价格趋势的投资策略，追涨杀跌',
    category: '投资策略',
    example: '买入近期表现强势的股票'
  },
  '逆向投资': {
    term: '逆向投资',
    fullName: 'Contrarian Investing',
    description: '与市场主流观点相反的投资策略',
    category: '投资策略',
    example: '在市场恐慌时买入优质资产'
  },
  '基本面分析': {
    term: '基本面分析',
    fullName: 'Fundamental Analysis',
    description: '通过分析公司财务、行业、经济等基本面因素评估价值',
    category: '分析方法',
    example: '分析财务报表、行业地位、竞争优势等'
  },
  '量化分析': {
    term: '量化分析',
    fullName: 'Quantitative Analysis',
    description: '使用数学模型和统计方法进行投资分析',
    category: '分析方法',
    example: '使用因子模型、机器学习算法等'
  },
  '风险管理': {
    term: '风险管理',
    fullName: 'Risk Management',
    description: '识别、评估和控制投资风险的过程',
    category: '投资管理',
    example: '设置止损、分散投资、对冲风险等'
  },
  '止损': {
    term: '止损',
    fullName: 'Stop Loss',
    description: '预设的卖出价格，用于限制损失',
    category: '风险控制',
    example: '股价下跌10%时自动卖出'
  },
  '止盈': {
    term: '止盈',
    fullName: 'Take Profit',
    description: '预设的卖出价格，用于锁定利润',
    category: '风险控制',
    example: '股价上涨50%时卖出部分仓位'
  },
  '仓位管理': {
    term: '仓位管理',
    fullName: 'Position Sizing',
    description: '控制单个投资在总资产中的比例',
    category: '风险控制',
    example: '单个股票不超过总资产的5%'
  },
  '对冲': {
    term: '对冲',
    fullName: 'Hedging',
    description: '通过反向投资来抵消风险敞口',
    category: '风险控制',
    example: '买入看跌期权对冲股票下跌风险'
  },
  '期权': {
    term: '期权',
    fullName: 'Options',
    description: '在特定时间以特定价格买卖资产的权利',
    category: '衍生品',
    example: '看涨期权、看跌期权、期权策略等'
  },
  '期货': {
    term: '期货',
    fullName: 'Futures',
    description: '标准化合约，约定未来以特定价格交易',
    category: '衍生品',
    example: '商品期货、股指期货、利率期货等'
  },
  'ETF': {
    term: 'ETF',
    fullName: 'Exchange-Traded Fund',
    description: '交易所交易基金，跟踪特定指数或资产',
    category: '投资产品',
    example: 'SPY跟踪标普500指数，QQQ跟踪纳斯达克100'
  },
  '共同基金': {
    term: '共同基金',
    fullName: 'Mutual Fund',
    description: '集合投资者资金进行专业管理的投资产品',
    category: '投资产品',
    example: '股票基金、债券基金、混合基金等'
  },
  '指数基金': {
    term: '指数基金',
    fullName: 'Index Fund',
    description: '跟踪特定市场指数的被动投资基金',
    category: '投资产品',
    example: '跟踪标普500、纳斯达克、道琼斯等指数'
  },
  '主动管理': {
    term: '主动管理',
    fullName: 'Active Management',
    description: '基金经理主动选择投资标的的管理方式',
    category: '投资管理',
    example: '通过选股和择时追求超额收益'
  },
  '被动管理': {
    term: '被动管理',
    fullName: 'Passive Management',
    description: '跟踪特定指数的管理方式，不主动选股',
    category: '投资管理',
    example: '指数基金、ETF等被动投资产品'
  },
  '复利': {
    term: '复利',
    fullName: 'Compound Interest',
    description: '利息再投资产生的收益，时间越长效果越显著',
    category: '投资概念',
    example: '年化10%收益，10年后本金翻倍'
  },
  '通货膨胀': {
    term: '通货膨胀',
    fullName: 'Inflation',
    description: '物价水平持续上涨，货币购买力下降',
    category: '经济指标',
    example: 'CPI年增长率2%表示温和通胀'
  },
  '利率': {
    term: '利率',
    fullName: 'Interest Rate',
    description: '资金使用成本，影响投资和消费决策',
    category: '经济指标',
    example: '美联储联邦基金利率影响全球金融市场'
  },
  'GDP': {
    term: 'GDP',
    fullName: 'Gross Domestic Product',
    description: '国内生产总值，衡量一国经济总量',
    category: '经济指标',
    example: '美国GDP年增长率反映经济健康状况'
  },
  '失业率': {
    term: '失业率',
    fullName: 'Unemployment Rate',
    description: '失业人口占劳动力人口的比例',
    category: '经济指标',
    example: '失业率下降通常利好股市'
  },
  'PMI': {
    term: 'PMI',
    fullName: 'Purchasing Managers Index',
    description: '采购经理指数，反映制造业和服务业景气度',
    category: '经济指标',
    example: 'PMI>50表示扩张，<50表示收缩'
  },
  'CPI': {
    term: 'CPI',
    fullName: 'Consumer Price Index',
    description: '消费者物价指数，衡量通货膨胀水平',
    category: '经济指标',
    example: 'CPI年增长率是央行制定货币政策的重要参考'
  },
  'PPI': {
    term: 'PPI',
    fullName: 'Producer Price Index',
    description: '生产者物价指数，衡量生产环节价格变化',
    category: '经济指标',
    example: 'PPI变化通常领先CPI变化'
  },
  '货币政策': {
    term: '货币政策',
    fullName: 'Monetary Policy',
    description: '央行通过调节货币供应影响经济的政策',
    category: '经济政策',
    example: '降息刺激经济，加息抑制通胀'
  },
  '财政政策': {
    term: '财政政策',
    fullName: 'Fiscal Policy',
    description: '政府通过税收和支出影响经济的政策',
    category: '经济政策',
    example: '减税刺激消费，增加基建投资'
  },
  '量化宽松': {
    term: '量化宽松',
    fullName: 'Quantitative Easing',
    description: '央行购买长期债券增加货币供应的政策',
    category: '货币政策',
    example: '美联储QE政策推高资产价格'
  },
  '缩表': {
    term: '缩表',
    fullName: 'Balance Sheet Reduction',
    description: '央行减少资产负债表规模的政策',
    category: '货币政策',
    example: '美联储缩表减少市场流动性'
  },
  '收益率曲线': {
    term: '收益率曲线',
    fullName: 'Yield Curve',
    description: '不同期限债券收益率的关系曲线',
    category: '债券分析',
    example: '收益率曲线倒挂通常预示经济衰退'
  },
  '信用利差': {
    term: '信用利差',
    fullName: 'Credit Spread',
    description: '高风险债券与无风险债券的收益率差',
    category: '债券分析',
    example: '信用利差扩大表示市场风险偏好下降'
  },
  '久期': {
    term: '久期',
    fullName: 'Duration',
    description: '债券价格对利率变化的敏感度',
    category: '债券分析',
    example: '久期越长，利率上升时债券价格下跌越多'
  },
  '凸性': {
    term: '凸性',
    fullName: 'Convexity',
    description: '债券价格与收益率关系的曲率',
    category: '债券分析',
    example: '凸性越大，利率变化时债券价格变化越有利'
  },
  '可转债': {
    term: '可转债',
    fullName: 'Convertible Bond',
    description: '可在特定条件下转换为股票的债券',
    category: '投资产品',
    example: '兼具债券安全性和股票上涨潜力的产品'
  },
  '优先股': {
    term: '优先股',
    fullName: 'Preferred Stock',
    description: '享有优先分红权的股票，介于股票和债券之间',
    category: '投资产品',
    example: '固定股息率，优先于普通股分红'
  },
  'REITs': {
    term: 'REITs',
    fullName: 'Real Estate Investment Trusts',
    description: '房地产投资信托基金，投资房地产资产',
    category: '投资产品',
    example: '通过股票形式投资商业地产、住宅等'
  },
  '商品': {
    term: '商品',
    fullName: 'Commodities',
    description: '大宗商品，如原油、黄金、农产品等',
    category: '投资产品',
    example: '通过期货、ETF等方式投资商品'
  },
  '外汇': {
    term: '外汇',
    fullName: 'Foreign Exchange',
    description: '不同国家货币之间的交易',
    category: '投资产品',
    example: '美元、欧元、日元等货币对交易'
  },
  '加密货币': {
    term: '加密货币',
    fullName: 'Cryptocurrency',
    description: '基于区块链技术的数字货币',
    category: '投资产品',
    example: '比特币、以太坊等数字货币'
  },
  '区块链': {
    term: '区块链',
    fullName: 'Blockchain',
    description: '分布式账本技术，支持加密货币等应用',
    category: '技术概念',
    example: '比特币、智能合约、DeFi等应用'
  },
  'DeFi': {
    term: 'DeFi',
    fullName: 'Decentralized Finance',
    description: '去中心化金融，基于区块链的金融服务',
    category: '金融创新',
    example: '去中心化交易所、借贷平台、稳定币等'
  },
  'NFT': {
    term: 'NFT',
    fullName: 'Non-Fungible Token',
    description: '非同质化代币，代表独特的数字资产',
    category: '数字资产',
    example: '数字艺术品、游戏道具、虚拟土地等'
  },
  '元宇宙': {
    term: '元宇宙',
    fullName: 'Metaverse',
    description: '虚拟现实和增强现实构建的数字化世界',
    category: '技术概念',
    example: 'VR/AR技术、虚拟社交、数字资产等'
  },
  '人工智能': {
    term: '人工智能',
    fullName: 'Artificial Intelligence',
    description: '模拟人类智能的计算机系统',
    category: '技术概念',
    example: '机器学习、深度学习、自然语言处理等'
  },
  '机器学习': {
    term: '机器学习',
    fullName: 'Machine Learning',
    description: '通过算法让计算机从数据中学习的技术',
    category: '技术概念',
    example: '预测模型、推荐系统、图像识别等'
  },
  '深度学习': {
    term: '深度学习',
    fullName: 'Deep Learning',
    description: '基于神经网络的机器学习方法',
    category: '技术概念',
    example: 'ChatGPT、图像生成、自动驾驶等'
  },
  '云计算': {
    term: '云计算',
    fullName: 'Cloud Computing',
    description: '通过网络提供计算资源的服务模式',
    category: '技术概念',
    example: 'AWS、Azure、Google Cloud等云服务'
  },
  '大数据': {
    term: '大数据',
    fullName: 'Big Data',
    description: '海量、高增长、多样化的数据集合',
    category: '技术概念',
    example: '用户行为数据、传感器数据、社交媒体数据等'
  },
  '物联网': {
    term: '物联网',
    fullName: 'Internet of Things',
    description: '通过互联网连接的智能设备网络',
    category: '技术概念',
    example: '智能家居、工业物联网、车联网等'
  },
  '5G': {
    term: '5G',
    fullName: 'Fifth Generation',
    description: '第五代移动通信技术，高速低延迟',
    category: '技术概念',
    example: '移动通信、工业互联网、自动驾驶等应用'
  },
  '芯片': {
    term: '芯片',
    fullName: 'Semiconductor Chip',
    description: '集成电路，现代电子设备的核心',
    category: '技术产品',
    example: 'CPU、GPU、存储芯片、传感器等'
  },
  '晶圆': {
    term: '晶圆',
    fullName: 'Silicon Wafer',
    description: '制造芯片的圆形硅片',
    category: '技术产品',
    example: '12英寸晶圆是目前主流制造尺寸'
  },
  '光刻机': {
    term: '光刻机',
    fullName: 'Lithography Machine',
    description: '芯片制造中的关键设备，用于图案转移',
    category: '技术设备',
    example: 'ASML的EUV光刻机是7nm以下制程的关键'
  },
  '制程': {
    term: '制程',
    fullName: 'Process Node',
    description: '芯片制造工艺的尺寸，越小越先进',
    category: '技术概念',
    example: '7nm、5nm、3nm等制程节点'
  },
  '摩尔定律': {
    term: '摩尔定律',
    fullName: "Moore's Law",
    description: '集成电路晶体管数量每18-24个月翻倍',
    category: '技术规律',
    example: '推动芯片性能持续提升的重要规律'
  },
  '新能源': {
    term: '新能源',
    fullName: 'Renewable Energy',
    description: '太阳能、风能、水能等清洁能源',
    category: '能源概念',
    example: '光伏发电、风力发电、水力发电等'
  },
  '碳中和': {
    term: '碳中和',
    fullName: 'Carbon Neutrality',
    description: '碳排放量与碳吸收量平衡的状态',
    category: '环保概念',
    example: '通过减排和碳汇实现净零排放'
  },
  'ESG': {
    term: 'ESG',
    fullName: 'Environmental, Social, and Governance',
    description: '环境、社会和公司治理的投资标准',
    category: '投资理念',
    example: '关注环保、社会责任、公司治理的投资策略'
  },
  '可持续发展': {
    term: '可持续发展',
    fullName: 'Sustainable Development',
    description: '满足当前需求而不损害未来世代需求的发展模式',
    category: '发展理念',
    example: '经济、社会、环境三方面平衡发展'
  },
  '循环经济': {
    term: '循环经济',
    fullName: 'Circular Economy',
    description: '资源循环利用的经济模式，减少浪费',
    category: '经济模式',
    example: '废物回收、产品再利用、资源再生等'
  },
  '绿色金融': {
    term: '绿色金融',
    fullName: 'Green Finance',
    description: '支持环保和可持续发展的金融活动',
    category: '金融概念',
    example: '绿色债券、绿色信贷、碳金融等'
  },
  '碳交易': {
    term: '碳交易',
    fullName: 'Carbon Trading',
    description: '碳排放权的买卖交易',
    category: '金融产品',
    example: '通过碳市场交易碳排放配额'
  },
  '碳税': {
    term: '碳税',
    fullName: 'Carbon Tax',
    description: '对碳排放征收的税费',
    category: '政策工具',
    example: '通过价格机制减少碳排放'
  },
  '碳足迹': {
    term: '碳足迹',
    fullName: 'Carbon Footprint',
    description: '个人或组织活动产生的碳排放总量',
    category: '环保概念',
    example: '计算产品全生命周期的碳排放'
  },
  '生物多样性': {
    term: '生物多样性',
    fullName: 'Biodiversity',
    description: '地球上生物种类的多样性',
    category: '环保概念',
    example: '保护生态系统和物种多样性'
  },
  '气候变化': {
    term: '气候变化',
    fullName: 'Climate Change',
    description: '地球气候系统的长期变化',
    category: '环保概念',
    example: '全球变暖、极端天气事件增加等'
  },
  '清洁能源': {
    term: '清洁能源',
    fullName: 'Clean Energy',
    description: '生产和使用过程中污染较少的能源',
    category: '能源概念',
    example: '太阳能、风能、核能、氢能等'
  },
  '储能': {
    term: '储能',
    fullName: 'Energy Storage',
    description: '将能量储存起来供后续使用的技术',
    category: '能源技术',
    example: '锂电池、抽水蓄能、压缩空气储能等'
  },
  '智能电网': {
    term: '智能电网',
    fullName: 'Smart Grid',
    description: '集成先进技术的现代化电力系统',
    category: '能源技术',
    example: '双向通信、自动调节、分布式发电等'
  },
  '微电网': {
    term: '微电网',
    fullName: 'Microgrid',
    description: '小规模的独立电力系统',
    category: '能源技术',
    example: '社区、校园、工业园区的独立供电系统'
  },
  '氢能': {
    term: '氢能',
    fullName: 'Hydrogen Energy',
    description: '以氢为载体的清洁能源',
    category: '能源技术',
    example: '氢燃料电池、氢能汽车、氢能发电等'
  },
  '核聚变': {
    term: '核聚变',
    fullName: 'Nuclear Fusion',
    description: '轻原子核结合成重原子核的核反应',
    category: '能源技术',
    example: '太阳能的来源，人造太阳技术'
  },
  '核裂变': {
    term: '核裂变',
    fullName: 'Nuclear Fission',
    description: '重原子核分裂成轻原子核的核反应',
    category: '能源技术',
    example: '核电站发电、核武器等应用'
  },
  '地热能': {
    term: '地热能',
    fullName: 'Geothermal Energy',
    description: '地球内部热能的可利用部分',
    category: '能源技术',
    example: '地热发电、地热供暖等应用'
  },
  '潮汐能': {
    term: '潮汐能',
    fullName: 'Tidal Energy',
    description: '利用潮汐运动产生的能量',
    category: '能源技术',
    example: '潮汐发电站、潮汐涡轮机等'
  },
  '波浪能': {
    term: '波浪能',
    fullName: 'Wave Energy',
    description: '利用海洋波浪运动产生的能量',
    category: '能源技术',
    example: '波浪发电装置、浮标式发电等'
  },
  '生物质能': {
    term: '生物质能',
    fullName: 'Biomass Energy',
    description: '利用有机物质产生的能量',
    category: '能源技术',
    example: '生物质发电、生物燃料、沼气等'
  }
};

/**
 * 从本地术语库获取术语信息
 * @param {string} term - 术语名称
 * @returns {object|null} 术语信息对象或null
 */
export function getGlossaryTerm(term) {
  if (!term) return null;
  
  // 尝试直接匹配
  if (LOCAL_GLOSSARY[term]) {
    return LOCAL_GLOSSARY[term];
  }
  
  // 尝试大小写不敏感匹配
  const lowerTerm = term.toLowerCase();
  for (const [key, value] of Object.entries(LOCAL_GLOSSARY)) {
    if (key.toLowerCase() === lowerTerm) {
      return value;
    }
  }
  
  // 尝试部分匹配
  for (const [key, value] of Object.entries(LOCAL_GLOSSARY)) {
    if (key.toLowerCase().includes(lowerTerm) || lowerTerm.includes(key.toLowerCase())) {
      return value;
    }
  }
  
  return null;
}

/**
 * 获取本地术语库中的所有术语
 * @returns {object} 所有术语的键值对
 */
export function getAllGlossaryTerms() {
  return LOCAL_GLOSSARY;
}

/**
 * 搜索术语
 * @param {string} query - 搜索查询
 * @returns {array} 匹配的术语列表
 */
export function searchGlossaryTerms(query) {
  if (!query) return [];
  
  const results = [];
  const lowerQuery = query.toLowerCase();
  
  for (const [key, value] of Object.entries(LOCAL_GLOSSARY)) {
    if (
      key.toLowerCase().includes(lowerQuery) ||
      value.fullName.toLowerCase().includes(lowerQuery) ||
      value.description.toLowerCase().includes(lowerQuery) ||
      value.category.toLowerCase().includes(lowerQuery)
    ) {
      results.push({
        key,
        ...value,
        relevance: calculateRelevance(key, value, lowerQuery)
      });
    }
  }
  
  // 按相关性排序
  return results.sort((a, b) => b.relevance - a.relevance);
}

/**
 * 计算搜索相关性分数
 * @param {string} key - 术语键
 * @param {object} value - 术语值
 * @param {string} query - 搜索查询
 * @returns {number} 相关性分数
 */
function calculateRelevance(key, value, query) {
  let score = 0;
  
  // 精确匹配术语键
  if (key.toLowerCase() === query) score += 100;
  // 术语键包含查询
  else if (key.toLowerCase().includes(query)) score += 50;
  
  // 全称匹配
  if (value.fullName.toLowerCase().includes(query)) score += 30;
  
  // 描述匹配
  if (value.description.toLowerCase().includes(query)) score += 20;
  
  // 分类匹配
  if (value.category.toLowerCase().includes(query)) score += 10;
  
  return score;
}

// API配置
const API_CONFIG = {
  wikipedia: {
    baseUrl: 'https://en.wikipedia.org/api/rest_v1/page/summary/',
    timeout: 5000
  },
  investopedia: {
    baseUrl: 'https://www.investopedia.com/terms/',
    timeout: 5000
  },
  alphaVantage: {
    baseUrl: 'https://www.alphavantage.co/query',
    timeout: 5000
  }
};

// 从本地词典获取术语
export function getLocalTerm(term) {
  const key = term.toUpperCase();
  return LOCAL_GLOSSARY[key] || LOCAL_GLOSSARY[term];
}

// 检查缓存是否有效
function isCacheValid(cacheKey) {
  const cached = GLOSSARY_CACHE.get(cacheKey);
  if (!cached) return false;
  
  const now = Date.now();
  return (now - cached.timestamp) < API_CACHE_DURATION;
}

// 设置缓存
function setCache(cacheKey, data) {
  GLOSSARY_CACHE.set(cacheKey, {
    data,
    timestamp: Date.now()
  });
}

// 获取缓存
function getCache(cacheKey) {
  const cached = GLOSSARY_CACHE.get(cacheKey);
  return cached ? cached.data : null;
}

// 从Wikipedia API获取术语
export async function getWikipediaTerm(term) {
  const cacheKey = `wikipedia_${term.toLowerCase()}`;
  
  // 检查缓存
  if (isCacheValid(cacheKey)) {
    return getCache(cacheKey);
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.wikipedia.timeout);
    
    const response = await fetch(
      `${API_CONFIG.wikipedia.baseUrl}${encodeURIComponent(term)}`,
      {
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'Investment-Handbook/1.0'
        }
      }
    );
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`Wikipedia API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.extract && data.extract.length > 50) {
      const result = {
        term: term,
        fullName: data.title,
        description: data.extract.substring(0, 300) + (data.extract.length > 300 ? '...' : ''),
        category: 'Wikipedia',
        source: 'wikipedia',
        url: data.content_urls?.desktop?.page || null
      };
      
      setCache(cacheKey, result);
      return result;
    }
  } catch (error) {
    console.warn(`Failed to fetch term "${term}" from Wikipedia:`, error.message);
  }
  
  return null;
}

// 从Investopedia获取术语（通过网页解析）
export async function getInvestopediaTerm(term) {
  const cacheKey = `investopedia_${term.toLowerCase()}`;
  
  // 检查缓存
  if (isCacheValid(cacheKey)) {
    return getCache(cacheKey);
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.investopedia.timeout);
    
    const response = await fetch(
      `${API_CONFIG.investopedia.baseUrl}${term.toLowerCase()}`,
      {
        signal: controller.signal,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      }
    );
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`Investopedia error: ${response.status}`);
    }
    
    const html = await response.text();
    
    // 简单的HTML解析（实际项目中可能需要更复杂的解析）
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const descriptionMatch = html.match(/<meta[^>]*name="description"[^>]*content="([^"]+)"/i);
    
    if (titleMatch && descriptionMatch) {
      const result = {
        term: term,
        fullName: titleMatch[1].replace(' - Investopedia', ''),
        description: descriptionMatch[1].substring(0, 300) + '...',
        category: 'Investopedia',
        source: 'investopedia',
        url: `${API_CONFIG.investopedia.baseUrl}${term.toLowerCase()}`
      };
      
      setCache(cacheKey, result);
      return result;
    }
  } catch (error) {
    console.warn(`Failed to fetch term "${term}" from Investopedia:`, error.message);
  }
  
  return null;
}

// 从Alpha Vantage获取金融术语（需要API key）
export async function getAlphaVantageTerm(term, apiKey) {
  if (!apiKey) {
    console.warn('Alpha Vantage API key is required');
    return null;
  }
  
  const cacheKey = `alphavantage_${term.toLowerCase()}`;
  
  // 检查缓存
  if (isCacheValid(cacheKey)) {
    return getCache(cacheKey);
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.alphaVantage.timeout);
    
    const response = await fetch(
      `${API_CONFIG.alphaVantage.baseUrl}?function=SYMBOL_SEARCH&keywords=${encodeURIComponent(term)}&apikey=${apiKey}`,
      {
        signal: controller.signal
      }
    );
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`Alpha Vantage API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.bestMatches && data.bestMatches.length > 0) {
      const match = data.bestMatches[0];
      const result = {
        term: term,
        fullName: match['2. name'],
        description: `Symbol: ${match['1. symbol']}, Type: ${match['3. type']}, Region: ${match['4. region']}`,
        category: 'Alpha Vantage',
        source: 'alphavantage',
        symbol: match['1. symbol']
      };
      
      setCache(cacheKey, result);
      return result;
    }
  } catch (error) {
    console.warn(`Failed to fetch term "${term}" from Alpha Vantage:`, error.message);
  }
  
  return null;
}

// 获取术语解释（多源优先级）
export async function getTermDefinition(term, options = {}) {
  const { 
    preferLocal = true, 
    includeWikipedia = true, 
    includeInvestopedia = true,
    alphaVantageKey = null 
  } = options;
  
  // 1. 先查本地词典（如果优先本地）
  if (preferLocal) {
    const localTerm = getLocalTerm(term);
    if (localTerm) {
      return localTerm;
    }
  }
  
  // 2. 查缓存
  const cacheKey = `term_${term.toLowerCase()}`;
  if (isCacheValid(cacheKey)) {
    return getCache(cacheKey);
  }
  
  // 3. 并行查询外部API
  const promises = [];
  
  if (includeWikipedia) {
    promises.push(getWikipediaTerm(term));
  }
  
  if (includeInvestopedia) {
    promises.push(getInvestopediaTerm(term));
  }
  
  if (alphaVantageKey) {
    promises.push(getAlphaVantageTerm(term, alphaVantageKey));
  }
  
  if (promises.length > 0) {
    try {
      const results = await Promise.allSettled(promises);
      const validResults = results
        .filter(result => result.status === 'fulfilled' && result.value)
        .map(result => result.value);
      
      if (validResults.length > 0) {
        // 选择最佳结果（优先Wikipedia，其次Investopedia）
        const bestResult = validResults.find(r => r.source === 'wikipedia') ||
                          validResults.find(r => r.source === 'investopedia') ||
                          validResults[0];
        
        setCache(cacheKey, bestResult);
        return bestResult;
      }
    } catch (error) {
      console.warn(`Failed to fetch term "${term}" from external APIs:`, error);
    }
  }
  
  // 4. 如果外部API失败，回退到本地词典
  if (!preferLocal) {
    const localTerm = getLocalTerm(term);
    if (localTerm) {
      return localTerm;
    }
  }
  
  // 5. 返回null，表示未找到
  return null;
}

// 批量获取术语
export async function getMultipleTerms(terms, options = {}) {
  const results = {};
  const promises = terms.map(async (term) => {
    const definition = await getTermDefinition(term, options);
    if (definition) {
      results[term] = definition;
    }
  });
  
  await Promise.all(promises);
  return results;
}

// 搜索相关术语
export async function searchTerms(query, options = {}) {
  const { maxResults = 10 } = options;
  const results = [];
  
  // 本地搜索
  const localMatches = Object.entries(LOCAL_GLOSSARY)
    .filter(([term, data]) => 
      term.toLowerCase().includes(query.toLowerCase()) ||
      data.fullName.toLowerCase().includes(query.toLowerCase()) ||
      data.description.toLowerCase().includes(query.toLowerCase())
    )
    .map(([term, data]) => ({ ...data, source: 'local' }));
  
  results.push(...localMatches);
  
  // 外部API搜索（如果需要）
  if (options.includeExternal) {
    try {
      const wikiResult = await getWikipediaTerm(query);
      if (wikiResult) {
        results.push(wikiResult);
      }
    } catch (error) {
      console.warn('External search failed:', error);
    }
  }
  
  return results.slice(0, maxResults);
}

// 获取缓存统计
export function getCacheStats() {
  const now = Date.now();
  const stats = {
    total: GLOSSARY_CACHE.size,
    valid: 0,
    expired: 0,
    sources: {}
  };
  
  for (const [key, value] of GLOSSARY_CACHE.entries()) {
    if (isCacheValid(key)) {
      stats.valid++;
      const source = value.data.source || 'unknown';
      stats.sources[source] = (stats.sources[source] || 0) + 1;
    } else {
      stats.expired++;
    }
  }
  
  return stats;
}

// 清理过期缓存
export function clearExpiredCache() {
  const now = Date.now();
  let cleared = 0;
  
  for (const [key, value] of GLOSSARY_CACHE.entries()) {
    if ((now - value.timestamp) >= API_CACHE_DURATION) {
      GLOSSARY_CACHE.delete(key);
      cleared++;
    }
  }
  
  return cleared;
}

// 导出API配置供其他模块使用
export { API_CONFIG }; 
 