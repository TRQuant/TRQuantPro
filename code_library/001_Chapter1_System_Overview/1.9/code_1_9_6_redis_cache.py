"""
Redis缓存操作函数

设计原理：
1. 使用Redis进行高速缓存和任务队列
2. 支持TTL自动过期
3. 支持发布/订阅机制
4. 支持多种数据结构（String、List、Hash、Set）

为什么这样设计：
1. 高性能：内存存储，访问速度快
2. 丰富数据结构：支持多种数据结构，适应不同场景
3. 自动过期：支持TTL，自动清理过期数据
4. 发布/订阅：支持实时消息推送

使用场景：
- 行情快照缓存（TTL: 60秒）
- 任务队列（回测任务、数据更新任务）
- 风控状态缓存（TTL: 1小时）
- 实时数据推送

注意事项：
- 注意内存占用，设置合理的TTL
- 任务队列需要处理失败重试
- 缓存数据需要与数据库同步
"""

import redis
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def init_redis_client(
    host: str = 'localhost',
    port: int = 6379,
    db: int = 0
) -> redis.Redis:
    """
    初始化Redis客户端
    
    Args:
        host: Redis服务器地址
        port: Redis服务器端口
        db: 数据库编号
    
    Returns:
        Redis客户端实例
    """
    r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    return r


def cache_market_snapshot(
    client: redis.Redis,
    symbol: str,
    data: Dict[str, Any],
    ttl: int = 60
) -> bool:
    """
    缓存行情快照（TTL: 60秒）
    
    设计原理：
    - 使用Redis的String类型存储
    - 设置TTL自动过期
    - JSON序列化存储
    
    Args:
        client: Redis客户端实例
        symbol: 股票代码
        data: 行情数据字典
        ttl: 过期时间（秒，默认60）
    
    Returns:
        是否缓存成功
    """
    key = f"market:snapshot:{symbol}"
    
    try:
        client.setex(key, ttl, json.dumps(data))
        logger.debug(f"行情快照已缓存: {symbol}")
        return True
    except Exception as e:
        logger.error(f"缓存行情快照失败: {e}")
        return False


def get_market_snapshot(
    client: redis.Redis,
    symbol: str
) -> Optional[Dict[str, Any]]:
    """
    获取行情快照
    
    Args:
        client: Redis客户端实例
        symbol: 股票代码
    
    Returns:
        行情数据字典，如果不存在返回None
    """
    key = f"market:snapshot:{symbol}"
    
    try:
        data = client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"获取行情快照失败: {e}")
        return None


def enqueue_backtest_task(
    client: redis.Redis,
    backtest_id: int,
    config: Dict[str, Any]
) -> bool:
    """
    将回测任务加入队列
    
    设计原理：
    - 使用Redis的List类型实现队列
    - 使用lpush从左侧推入（FIFO）
    - JSON序列化任务数据
    
    Args:
        client: Redis客户端实例
        backtest_id: 回测任务ID
        config: 回测配置字典
    
    Returns:
        是否加入队列成功
    """
    queue_name = "queue:backtest"
    task_data = {
        "backtest_id": backtest_id,
        "config": config,
        "created_at": datetime.now().isoformat()
    }
    
    try:
        client.lpush(queue_name, json.dumps(task_data))
        logger.info(f"回测任务已加入队列: {backtest_id}")
        return True
    except Exception as e:
        logger.error(f"加入回测任务队列失败: {e}")
        return False


def dequeue_backtest_task(
    client: redis.Redis,
    timeout: int = 1
) -> Optional[Dict[str, Any]]:
    """
    从队列中取出回测任务
    
    设计原理：
    - 使用brpop阻塞式弹出（从右侧弹出）
    - 支持超时设置，避免无限阻塞
    
    Args:
        client: Redis客户端实例
        timeout: 超时时间（秒，默认1）
    
    Returns:
        任务数据字典，如果队列为空返回None
    """
    queue_name = "queue:backtest"
    
    try:
        result = client.brpop(queue_name, timeout=timeout)
        if result:
            _, task_json = result
            return json.loads(task_json)
        return None
    except Exception as e:
        logger.error(f"从队列取出回测任务失败: {e}")
        return None


def cache_risk_state(
    client: redis.Redis,
    account_id: int,
    state: Dict[str, Any],
    ttl: int = 3600
) -> bool:
    """
    缓存风控状态（TTL: 1小时）
    
    设计原理：
    - 使用Redis的String类型存储
    - 设置TTL自动过期（默认1小时）
    - JSON序列化存储
    
    Args:
        client: Redis客户端实例
        account_id: 账户ID
        state: 风控状态字典
        ttl: 过期时间（秒，默认3600）
    
    Returns:
        是否缓存成功
    """
    key = f"risk:state:{account_id}"
    
    try:
        client.setex(key, ttl, json.dumps(state))
        logger.debug(f"风控状态已缓存: {account_id}")
        return True
    except Exception as e:
        logger.error(f"缓存风控状态失败: {e}")
        return False


def get_risk_state(
    client: redis.Redis,
    account_id: int
) -> Optional[Dict[str, Any]]:
    """
    获取风控状态
    
    Args:
        client: Redis客户端实例
        account_id: 账户ID
    
    Returns:
        风控状态字典，如果不存在返回None
    """
    key = f"risk:state:{account_id}"
    
    try:
        data = client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"获取风控状态失败: {e}")
        return None

