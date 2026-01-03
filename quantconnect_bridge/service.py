import logging
import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QuantConnectBridgeService(BaseBridgeService):
    """
    QuantConnect/IBKR Bridge Service

    读取 Lean 项目的策略文件以及导出的回测/交易数据。
    后续可扩展：
    - 调用 `lean backtest` 自动触发回测并刷新数据
    - 集成 IBKR 实盘订单/成交记录
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QC_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "quantconnect")
        data_dir = Path(data_dir or root / "data" / "quantconnect")
        super().__init__(
            platform="QuantConnect+IBKR",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    def _extract_description(self, file: Path) -> str:
        # 对 Lean 项目的 main.py / Notebook 增强识别
        desc = super()._extract_description(file)
        if desc == f"{self.platform} Strategy":
            try:
                if file.suffix == ".ipynb":
                    return "QuantConnect Notebook"
            except Exception:
                pass
        return desc














