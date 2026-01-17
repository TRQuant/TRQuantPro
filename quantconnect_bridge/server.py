import logging
import os

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
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

from quantconnect_bridge.api import app, service
from quantconnect_bridge.service import QuantConnectBridgeService

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

HOST = os.getenv("QC_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("QC_BRIDGE_PORT", "8200"))


def main():
    global service
    service = QuantConnectBridgeService()
    app.service = service  # type: ignore[attr-defined]

    console = Console()
    banner = Text()
    banner.append("  ____                  _   _____                      _   _  ____  \n", style="magenta")
    banner.append(" / __ \\                | | |  __ \\                    | | (_)/ __ \\ \n", style="magenta")
    banner.append("| |  | |_   _ _ __ __ _| | | |  | |_   _  ___  _ __ __| |  _| |  | |\n", style="magenta")
    banner.append("| |  | | | | | '__/ _` | | | |  | | | | |/ _ \\| '__/ _` | | | |  | |\n", style="magenta")
    banner.append("| |__| | |_| | | | (_| | | | |__| | |_| | (_) | | | (_| | | | |__| |\n", style="magenta")
    banner.append(" \\___\\_\\\\__,_|_|  \\__,_|_| |_____/ \\__, |\\___/|_|  \\__,_| |_|\\____/ \n", style="magenta")
    banner.append("                                    __/ |                           \n", style="magenta")
    banner.append("                                   |___/                            \n", style="magenta")
    banner.append("\n QuantConnect Bridge Service v0.1.0", style="white")

    console.print(Panel(banner, box=MINIMAL, border_style="magenta", expand=False))
    console.print(f"[bold green]服务地址:[/bold green] http://{HOST}:{PORT}")
    console.print(f"[bold green]API 文档:[/bold green] http://{HOST}:{PORT}/docs")
    console.print(f"[bold yellow]策略目录:[/bold yellow] {service.strategy_dir}")
    console.print(f"[bold yellow]数据目录:[/bold yellow] {service.data_dir}")

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()














