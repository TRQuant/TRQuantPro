# 流程图测试文档

## 测试1: 简单流程图

```mermaid
flowchart TD
    A[开始] --> B{判断条件}
    B -->|是| C[操作1]
    B -->|否| D[操作2]
    C --> E[结束]
    D --> E
    
    style A fill:#e1f5ff
    style C fill:#e1ffe1
    style D fill:#ffe1e1
    style E fill:#f5f5f5
```

## 测试2: 陈小群战法简化流程图

```mermaid
flowchart TD
    A[开盘前准备] --> B{市场情绪周期}
    
    B -->|启动期| C[首板卡位 10%]
    B -->|加速期| D[二板定龙 50%]
    B -->|高位震荡| E[逐步减仓]
    B -->|退潮期| F[空仓观望]
    
    C --> G{二板确认?}
    G -->|是| D
    G -->|否| H[止损退出]
    
    D --> I{三板确认?}
    I -->|是| J[继续加仓 40%]
    I -->|否| K[持有观察]
    
    J --> L[持有至见顶]
    L --> M[退出]
    K --> M
    H --> M
    E --> M
    F --> M
    
    style A fill:#e1f5ff
    style C fill:#ffe1f5
    style D fill:#e1ffe1
    style E fill:#ffe1e1
    style F fill:#f5f5f5
    style J fill:#ffe1f5
    style L fill:#e1ffe1
    style M fill:#ffe1e1
```

## 测试3: 完整操作流程

```mermaid
flowchart TD
    Start[每日开盘前准备] --> CheckMarket{判断市场情绪周期}
    
    CheckMarket -->|启动期| FirstBoard[首板卡位术<br/>10%仓位]
    CheckMarket -->|加速期| SecondBoard[二板定龙术<br/>50%仓位]
    CheckMarket -->|高位震荡| Reduce[逐步减仓]
    CheckMarket -->|退潮期| Wait[空仓观望]
    
    FirstBoard --> Check1{早盘9:35前涨停?}
    Check1 -->|是| Check2{流通市值<30亿?}
    Check1 -->|否| Wait
    Check2 -->|是| Check3{封单量>2%?}
    Check2 -->|否| Wait
    Check3 -->|是| Enter1[扫板介入 10%]
    Check3 -->|否| Wait
    
    Enter1 --> Check4{次日二板确认?}
    Check4 -->|是| Check5{换手率>25%?}
    Check4 -->|否| StopLoss[止损退出]
    Check5 -->|是| Check6{板块内3只以上跟风?}
    Check5 -->|否| StopLoss
    Check6 -->|是| Enter2[重仓介入 50%]
    Check6 -->|否| StopLoss
    
    SecondBoard --> Enter2
    Enter2 --> Check7{第三板确认?}
    Check7 -->|是| Check8{缩量涨停或量能放大?}
    Check7 -->|否| Hold[持有观察]
    Check8 -->|是| Enter3[继续加仓 40%]
    Check8 -->|否| Hold
    
    Enter3 --> Check9{板块效应持续增强?}
    Check9 -->|是| HoldToTop[持有至见顶]
    Check9 -->|否| Reduce
    
    HoldToTop --> Exit{明显见顶或停牌风险?}
    Hold --> Exit
    Reduce --> Exit
    StopLoss --> Exit
    
    Exit -->|是| FinalExit[果断退出]
    Exit -->|否| HoldToTop
    
    FinalExit --> Wait
    
    style Start fill:#e1f5ff
    style FirstBoard fill:#ffe1f5
    style SecondBoard fill:#e1ffe1
    style Enter1 fill:#e1f5ff
    style Enter2 fill:#e1ffe1
    style Enter3 fill:#ffe1f5
    style HoldToTop fill:#e1ffe1
    style Reduce fill:#ffe1e1
    style Wait fill:#f5f5f5
    style FinalExit fill:#ffe1e1
    style StopLoss fill:#ffe1e1
```

## 测试说明

这三个测试流程图分别测试：
1. **测试1**: 最简单的流程图，验证基本语法
2. **测试2**: 简化的陈小群战法流程，验证中文节点和样式
3. **测试3**: 完整的操作流程，验证复杂逻辑和换行文本

如果这些流程图都能正确显示，说明Mermaid格式是正确的。
