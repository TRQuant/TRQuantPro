import logging
import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()






import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()




import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from qmt_bridge.api import app, service
from qmt_bridge.service import QMTBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QMT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QMT_BRIDGE_PORT", "8100"))


def main():
    global service
    service = QMTBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____  __  __ _______\n", style="cyan")
    banner.append(" / __ \\|  \\/  |__   __|\n", style="cyan")
    banner.append("| |  | | \\  / |  | |   \n", style="cyan")
    banner.append("| |  | | |\\/| |  | |   \n", style="cyan")
    banner.append("| |__| | |  | |  | |   \n", style="cyan")
    banner.append(" \\____/|_|  |_|  |_|   \n", style="cyan")
    banner.append("\n QMT Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="cyan", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()














