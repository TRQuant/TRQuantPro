# GUI架构设计

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: TRQuant桌面GUI系统（PyQt6）

---

## 📋 概述

本文档定义了TRQuant桌面GUI系统的架构设计，采用MVC/MVVM模式组织代码，实现界面与业务逻辑的解耦。

## 🎯 设计目标

1. **解耦**: 界面与业务逻辑分离
2. **可维护性**: 代码结构清晰，易于维护
3. **可测试性**: 业务逻辑可独立测试
4. **可扩展性**: 易于添加新功能

---

## 🏗️ 架构模式

### 选择：MVC模式

采用MVC（Model-View-Controller）模式：

- **Model**: 数据模型和业务逻辑
- **View**: UI界面（PyQt6组件）
- **Controller**: 控制器，处理用户交互

### 架构图

```
┌─────────────┐
│    View     │  PyQt6 Widgets
│  (界面层)    │
└──────┬──────┘
       │ 信号/槽
┌──────▼──────┐
│ Controller  │  业务逻辑控制
│  (控制层)    │
└──────┬──────┘
       │
┌──────▼──────┐
│    Model    │  数据模型
│  (数据层)    │
└─────────────┘
```

---

## 📁 目录结构

```
gui/
├── framework/           # 基础框架
│   ├── base_model.py    # 基础Model类
│   ├── base_view.py     # 基础View类
│   ├── base_controller.py # 基础Controller类
│   └── signal_manager.py # 信号管理器
├── models/              # 数据模型
│   ├── data_model.py
│   ├── strategy_model.py
│   └── backtest_model.py
├── views/               # 视图组件
│   ├── main_window.py
│   └── widgets/
├── controllers/         # 控制器
│   ├── main_controller.py
│   └── panel_controllers/
└── styles/              # 样式
    └── theme.py
```

---

## 🔧 实现方案

### 1. 基础Model类

```python
class BaseModel(QObject):
    """基础Model类"""
    
    data_changed = pyqtSignal(str, object)  # 数据变更信号
    
    def __init__(self):
        super().__init__()
        self._data = {}
    
    def get_data(self, key: str):
        """获取数据"""
        return self._data.get(key)
    
    def set_data(self, key: str, value: Any):
        """设置数据"""
        self._data[key] = value
        self.data_changed.emit(key, value)
```

### 2. 基础View类

```python
class BaseView(QWidget):
    """基础View类"""
    
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI（子类实现）"""
        pass
    
    def update_view(self, data: Dict[str, Any]):
        """更新视图（子类实现）"""
        pass
```

### 3. 基础Controller类

```python
class BaseController(QObject):
    """基础Controller类"""
    
    def __init__(self, model: BaseModel, view: BaseView):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()
    
    def connect_signals(self):
        """连接信号和槽"""
        self.model.data_changed.connect(self.view.update_view)
```

---

## 📖 使用示例

### 示例：策略管理面板

```python
# models/strategy_model.py
class StrategyModel(BaseModel):
    def load_strategies(self):
        # 加载策略数据
        strategies = load_from_database()
        self.set_data('strategies', strategies)

# views/strategy_view.py
class StrategyView(BaseView):
    def init_ui(self):
        self.table = QTableWidget()
        # ... UI初始化
    
    def update_view(self, key: str, value: Any):
        if key == 'strategies':
            self.update_table(value)

# controllers/strategy_controller.py
class StrategyController(BaseController):
    def __init__(self):
        model = StrategyModel()
        view = StrategyView()
        super().__init__(model, view)
    
    def on_add_strategy(self):
        # 处理添加策略
        self.model.add_strategy(...)
```

---

## 📖 相关文档

- [GUI任务触发器设计](./GUI_TASK_TRIGGER_DESIGN.md)
- [GUI图表库选择](./GUI_CHART_LIBRARY_SELECTION.md)

---

**最后更新**: 2025-12-14
