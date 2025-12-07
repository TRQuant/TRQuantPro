"""BulletTrade 配置管理

基于 BulletTrade 官方文档：https://bullettrade.cn/
管理配置文件和环境设置
"""

from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class BulletTradeConfig:
    """BulletTrade 配置
    
    配置文件位置：
    - 设置文件：~/.bullet-trade/setting.json
    - 环境变量：~/.bullet-trade/.env 或项目根目录 .env
    
    Attributes:
        data_provider: 数据提供者 ('jqdata', 'miniqmt', 'tushare', 'simulator')
        broker: 券商接口 ('qmt', 'qmt-remote', 'simulator')
        research_root: 研究根目录
        server_host: 远程服务器地址
        server_port: 远程服务器端口
        server_token: 远程服务器令牌
    """
    data_provider: str = "jqdata"
    broker: str = "simulator"
    research_root: Optional[str] = None
    server_host: str = "0.0.0.0"
    server_port: int = 58620
    server_token: Optional[str] = None
    
    # JQData 配置
    jqdata_username: Optional[str] = None
    jqdata_password: Optional[str] = None
    
    # QMT 配置
    qmt_path: Optional[str] = None
    qmt_account: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.research_root:
            # 默认研究根目录
            # Windows: ~/bullet-trade
            # Linux/Mac: ~/bullet-trade
            self.research_root = str(Path.home() / "bullet-trade")
    
    @classmethod
    def get_config_dir(cls) -> Path:
        """获取配置目录"""
        return Path.home() / ".bullet-trade"
    
    @classmethod
    def get_setting_path(cls) -> Path:
        """获取设置文件路径"""
        return cls.get_config_dir() / "setting.json"
    
    @classmethod
    def load(cls) -> "BulletTradeConfig":
        """从配置文件加载配置
        
        Returns:
            BulletTradeConfig 实例
        """
        config = cls()
        
        # 1. 从 setting.json 加载
        setting_path = cls.get_setting_path()
        if setting_path.exists():
            try:
                with open(setting_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    for key, value in settings.items():
                        if hasattr(config, key):
                            setattr(config, key, value)
                logger.info(f"Loaded settings from: {setting_path}")
            except Exception as e:
                logger.warning(f"Failed to load settings: {e}")
        
        # 2. 从环境变量覆盖
        env_mappings = {
            'DEFAULT_DATA_PROVIDER': 'data_provider',
            'DEFAULT_BROKER': 'broker',
            'JQDATA_USERNAME': 'jqdata_username',
            'JQDATA_PASSWORD': 'jqdata_password',
            'QMT_PATH': 'qmt_path',
            'QMT_ACCOUNT': 'qmt_account',
            'BT_SERVER_HOST': 'server_host',
            'BT_SERVER_PORT': 'server_port',
            'BT_SERVER_TOKEN': 'server_token',
        }
        
        for env_key, config_key in env_mappings.items():
            env_value = os.environ.get(env_key)
            if env_value:
                if config_key == 'server_port':
                    setattr(config, config_key, int(env_value))
                else:
                    setattr(config, config_key, env_value)
        
        return config
    
    def save(self) -> None:
        """保存配置到文件"""
        config_dir = self.get_config_dir()
        config_dir.mkdir(parents=True, exist_ok=True)
        
        settings = {
            'data_provider': self.data_provider,
            'broker': self.broker,
            'research_root': self.research_root,
            'server_host': self.server_host,
            'server_port': self.server_port,
        }
        
        # 不保存敏感信息
        setting_path = self.get_setting_path()
        with open(setting_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Settings saved to: {setting_path}")
    
    def to_env_content(self) -> str:
        """生成 .env 文件内容"""
        lines = [
            "# BulletTrade 环境配置",
            f"DEFAULT_DATA_PROVIDER={self.data_provider}",
            f"DEFAULT_BROKER={self.broker}",
        ]
        
        if self.jqdata_username:
            lines.append(f"JQDATA_USERNAME={self.jqdata_username}")
        if self.jqdata_password:
            lines.append(f"JQDATA_PASSWORD={self.jqdata_password}")
        if self.qmt_path:
            lines.append(f"QMT_PATH={self.qmt_path}")
        if self.qmt_account:
            lines.append(f"QMT_ACCOUNT={self.qmt_account}")
        
        return "\n".join(lines)
    
    def save_env(self, path: Optional[str] = None) -> str:
        """保存 .env 文件
        
        Args:
            path: 保存路径，默认研究根目录
            
        Returns:
            保存的文件路径
        """
        if not path:
            path = str(Path(self.research_root) / ".env")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_env_content())
        
        logger.info(f"Env file saved to: {path}")
        return path


def setup_bullet_trade_env(
    data_provider: str = "jqdata",
    broker: str = "simulator",
    jqdata_username: Optional[str] = None,
    jqdata_password: Optional[str] = None
) -> BulletTradeConfig:
    """快速设置 BulletTrade 环境
    
    Args:
        data_provider: 数据提供者
        broker: 券商接口
        jqdata_username: JQData 用户名
        jqdata_password: JQData 密码
        
    Returns:
        配置实例
        
    Example:
        >>> config = setup_bullet_trade_env(
        ...     data_provider="jqdata",
        ...     broker="qmt",
        ...     jqdata_username="your_username",
        ...     jqdata_password="your_password"
        ... )
    """
    config = BulletTradeConfig(
        data_provider=data_provider,
        broker=broker,
        jqdata_username=jqdata_username,
        jqdata_password=jqdata_password
    )
    
    # 保存配置
    config.save()
    config.save_env()
    
    return config


def get_bullet_trade_cli_path() -> Optional[str]:
    """获取 bullet-trade CLI 路径"""
    import shutil
    return shutil.which("bullet-trade")


def check_bullet_trade_installation() -> Dict[str, Any]:
    """检查 BulletTrade 安装状态
    
    Returns:
        安装状态信息
    """
    import subprocess
    
    result = {
        "installed": False,
        "version": None,
        "cli_path": None,
        "qmt_support": False,
        "config_exists": False,
        "message": ""
    }
    
    # 检查 CLI
    cli_path = get_bullet_trade_cli_path()
    if cli_path:
        result["cli_path"] = cli_path
        
        try:
            proc = subprocess.run(
                ["bullet-trade", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if proc.returncode == 0:
                result["installed"] = True
                result["version"] = proc.stdout.strip()
                result["message"] = f"BulletTrade {result['version']} 已安装"
            else:
                result["message"] = f"bullet-trade 命令执行失败: {proc.stderr}"
        except Exception as e:
            result["message"] = f"检查失败: {e}"
    else:
        result["message"] = "BulletTrade 未安装。请运行: pip install bullet-trade"
    
    # 检查配置文件
    config_path = BulletTradeConfig.get_setting_path()
    result["config_exists"] = config_path.exists()
    
    # 检查 QMT 支持
    try:
        import xtquant
        result["qmt_support"] = True
    except ImportError:
        result["qmt_support"] = False
    
    return result



