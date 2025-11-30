import logging
import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段






import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段




import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段

import os
from pathlib import Path
from typing import Optional

from bridge_common.base_service import BaseBridgeService

logger = logging.getLogger(__name__)


class QMTBridgeService(BaseBridgeService):
    """
    QMT Bridge Service

    目前使用基础文件扫描模式：
    - 策略目录：strategies/qmt
    - 数据目录：data/qmt/{backtest_results,trades}

    后续可扩展：
    - 解析 xtquant Strategy 的 meta 信息
    - 调用 xtquant SDK 直接拉取回测/实盘结果
    """

    def __init__(
        self,
        strategy_dir: Optional[str] = None,
        data_dir: Optional[str] = None,
        enable_watchdog: bool = True,
    ):
        root = Path(os.getenv("QMT_BRIDGE_ROOT", Path(__file__).parent.parent))
        strategy_dir = Path(strategy_dir or root / "strategies" / "qmt")
        data_dir = Path(data_dir or root / "data" / "qmt")
        super().__init__(
            platform="QMT",
            strategy_dir=strategy_dir,
            data_dir=data_dir,
            enable_watchdog=enable_watchdog,
        )

    # 可在此处覆盖 _extract_description / _parse_backtest 等方法，解析特定字段














