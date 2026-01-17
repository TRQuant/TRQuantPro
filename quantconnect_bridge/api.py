import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}






from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}




from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}

from typing import List, Optional

from fastapi import FastAPI, HTTPException

from ptrade_bridge.models import Strategy, BacktestResult, Trade
from quantconnect_bridge.service import QuantConnectBridgeService

logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantConnect Bridge API",
    description="量化投资平台（QuantConnect + IBKR）桥接服务",
    version="0.1.0",
)

service: Optional[QuantConnectBridgeService] = None


@app.on_event("startup")
async def startup_event():
    logger.info("QuantConnect Bridge API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    if service:
        service.stop()
    logger.info("QuantConnect Bridge API 已关闭")


@app.get("/", summary="服务状态")
async def index():
    return {"service": "QuantConnect Bridge", "status": "running", "version": app.version}


@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return service.get_strategies()


@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def strategy_detail(strategy_id: str):
    strategy = service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@app.get("/backtests", response_model=List[BacktestResult])
async def list_backtests(strategy_id: Optional[str] = None):
    return service.get_backtests(strategy_id)


@app.get("/backtests/{backtest_id}", response_model=BacktestResult)
async def backtest_detail(backtest_id: str):
    backtest = service.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@app.get("/trades", response_model=List[Trade])
async def list_trades(strategy_id: Optional[str] = None):
    return service.get_trades(strategy_id)


@app.post("/refresh")
async def refresh():
    service.refresh()
    return {"message": "Reload triggered"}














