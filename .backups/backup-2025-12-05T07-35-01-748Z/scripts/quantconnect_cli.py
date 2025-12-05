import json
from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()






from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()




from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()

from typing import Optional

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="QuantConnect + IBKR Bridge CLI")
console = Console()

QC_BRIDGE_URL = "http://127.0.0.1:8200"


def _get(endpoint: str, params: Optional[dict] = None):
    resp = requests.get(f"{QC_BRIDGE_URL}{endpoint}", params=params)
    resp.raise_for_status()
    return resp.json()


@app.command()
def strategies():
    data = _get("/strategies")
    table = Table(title="QuantConnect 策略")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("更新时间", style="dim")
    for item in data:
        table.add_row(item["id"], item["name"], item["updated_at"])
    console.print(table)


@app.command()
def backtests(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/backtests", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 回测")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("策略")
    table.add_column("区间")
    table.add_column("收益", style="green")
    table.add_column("回撤", style="red")
    for item in data:
        table.add_row(
            item["id"],
            item["strategy_name"],
            f"{item['start_date']} ~ {item['end_date']}",
            f"{item['metrics']['total_return']:.2%}",
            f"{item['metrics']['max_drawdown']:.2%}",
        )
    console.print(table)


@app.command()
def trades(strategy_id: Optional[str] = typer.Option(None, "--strategy")):
    data = _get("/trades", params={"strategy_id": strategy_id} if strategy_id else None)
    table = Table(title="QuantConnect 交易记录")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("策略")
    table.add_column("代码")
    table.add_column("方向")
    table.add_column("价格")
    table.add_column("数量")
    for trade in data[:50]:
        table.add_row(
            trade["trade_id"],
            trade["strategy_id"],
            trade["symbol"],
            trade["side"],
            f"{trade['price']:.2f}",
            str(trade["volume"]),
        )
    console.print(table)


@app.command()
def refresh():
    resp = requests.post(f"{QC_BRIDGE_URL}/refresh")
    resp.raise_for_status()
    console.print("[green]已触发刷新[/green]")


if __name__ == "__main__":
    app()














