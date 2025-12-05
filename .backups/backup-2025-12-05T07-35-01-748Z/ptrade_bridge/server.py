#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()






# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
PTrade Bridge Server
启动 FastAPI 服务

用法:
    python -m ptrade_bridge.server
    或
    python ptrade_bridge/server.py
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
import logging
from ptrade_bridge.api import create_app
from ptrade_bridge.service import PTradeBridgeConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """启动服务"""
    config = PTradeBridgeConfig()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ████████╗ █████╗  ██████╗ ██████╗ ██╗   ██╗██╗          ║
║     ╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║          ║
║        ██║   ███████║██║   ██║██████╔╝██║   ██║██║          ║
║        ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║██║          ║
║        ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║          ║
║        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ║
║                                                              ║
║              PTrade Bridge Service v1.0.0                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

服务地址: http://{config.host}:{config.port}
API 文档: http://{config.host}:{config.port}/docs

策略目录: {config.strategies_dir}
数据目录: {config.data_dir}
""")
    
    logger.info(f"启动 PTrade Bridge 服务...")
    
    app = create_app(config)
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()














