#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Notebook结果管理器
==================

功能：
1. 自动保存notebook运行结果到带时间戳的文件夹
2. 保存结果到MongoDB统一管理
3. 保存notebook输出（包括图表、数据、文本）
4. 提供查询和引用机制
5. 支持版本管理和历史追踪

使用方式：
    from core.notebook_result_manager import NotebookResultManager
    
    manager = NotebookResultManager("chen_xiaoqun_strategy", "01_market_environment_judgment")
    manager.save_result(result_dict, outputs=outputs, charts=charts)
    
    # 查询历史结果
    history = manager.list_results(limit=10)
    latest = manager.get_latest_result()
"""

import logging
import json
import pickle
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict, field
import hashlib
import zipfile
import io

logger = logging.getLogger(__name__)

# MongoDB可用性检测
try:
    from pymongo import MongoClient, DESCENDING, ASCENDING
    from pymongo.errors import ConnectionFailure
    from bson import ObjectId
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("pymongo未安装，MongoDB存储功能不可用")

# 尝试导入可选依赖
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


@dataclass
class NotebookResultMetadata:
    """Notebook结果元数据"""
    notebook_name: str              # notebook名称（如：01_market_environment_judgment）
    strategy_name: str              # 策略名称（如：chen_xiaoqun_strategy）
    run_id: str                     # 运行ID（时间戳）
    run_date: str                   # 运行日期（YYYY-MM-DD）
    run_time: str                   # 运行时间（HH:MM:SS）
    result_summary: Dict[str, Any]  # 结果摘要
    parameters: Dict[str, Any] = field(default_factory=dict)  # 运行参数
    tags: List[str] = field(default_factory=list)  # 标签
    description: str = ""           # 描述
    version: str = "1.0.0"          # 版本
    file_path: str = ""             # 文件路径（相对路径）
    file_size: int = 0               # 文件大小（字节）
    output_count: int = 0            # 输出数量
    chart_count: int = 0             # 图表数量
    created_at: str = ""             # 创建时间（ISO格式）
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NotebookResultManager:
    """
    Notebook结果管理器
    
    支持：
    - 自动保存到带时间戳的文件夹
    - MongoDB统一管理
    - 保存输出、图表、数据
    - 查询和引用机制
    """
    
    # MongoDB配置
    MONGO_URI = "mongodb://localhost:27017"
    DB_NAME = "jqquant"
    COLLECTION_NAME = "notebook_results"
    
    def __init__(
        self,
        strategy_name: str,
        notebook_name: str,
        base_output_dir: Optional[Path] = None,
        mongo_uri: Optional[str] = None,
        db_name: Optional[str] = None
    ):
        """
        初始化Notebook结果管理器
        
        Args:
            strategy_name: 策略名称（如：chen_xiaoqun_strategy）
            notebook_name: notebook名称（如：01_market_environment_judgment）
            base_output_dir: 基础输出目录（默认为 notebooks/research/results）
            mongo_uri: MongoDB连接URI
            db_name: 数据库名称
        """
        self.strategy_name = strategy_name
        self.notebook_name = notebook_name
        
        # 设置输出目录
        if base_output_dir:
            self.base_output_dir = Path(base_output_dir)
        else:
            # 自动检测项目根目录
            current_dir = Path.cwd()
            project_root = None
            for parent in [current_dir] + list(current_dir.parents):
                if (parent / 'core').exists() and (parent / 'config').exists():
                    project_root = parent
                    break
            
            if project_root is None:
                project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')
            
            self.base_output_dir = project_root / 'notebooks' / 'research' / 'results'
        
        # 创建策略和notebook子目录
        self.strategy_dir = self.base_output_dir / strategy_name
        self.notebook_dir = self.strategy_dir / notebook_name
        self.notebook_dir.mkdir(parents=True, exist_ok=True)
        
        # MongoDB配置
        self.mongo_uri = mongo_uri or self.MONGO_URI
        self.db_name = db_name or self.DB_NAME
        
        # MongoDB连接
        self.client = None
        self.db = None
        self._connected = False
        
        self._connect_mongodb()
        
        logger.info(f"NotebookResultManager 初始化: {strategy_name}/{notebook_name}")
        logger.info(f"输出目录: {self.notebook_dir}")
    
    def _connect_mongodb(self):
        """连接MongoDB"""
        if not MONGODB_AVAILABLE:
            logger.warning("pymongo不可用，MongoDB功能将不可用")
            return
        
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self._connected = True
            
            # 创建索引
            self._create_indexes()
            
            logger.info(f"MongoDB连接成功: {self.db_name}")
        except Exception as e:
            logger.warning(f"MongoDB连接失败: {e}，将仅使用文件系统保存")
            self._connected = False
    
    def _create_indexes(self):
        """创建MongoDB索引"""
        if not self._connected:
            return
        
        try:
            collection = self.db[self.COLLECTION_NAME]
            # 创建索引
            collection.create_index([("strategy_name", ASCENDING), ("notebook_name", ASCENDING)])
            collection.create_index([("run_date", DESCENDING)])
            collection.create_index([("run_id", ASCENDING)], unique=True)
            collection.create_index([("created_at", DESCENDING)])
            logger.info("MongoDB索引创建成功")
        except Exception as e:
            logger.warning(f"创建索引失败: {e}")
    
    def _generate_run_id(self) -> str:
        """生成运行ID（时间戳格式：YYYYMMDD_HHMMSS）"""
        cn_now = datetime.now(timezone.utc) + timedelta(hours=8)
        return cn_now.strftime('%Y%m%d_%H%M%S')
    
    def _generate_run_dir(self, run_id: str) -> Path:
        """生成运行目录（带日期标签）"""
        # 格式：YYYYMMDD_HHMMSS
        run_dir = self.notebook_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir
    
    def _extract_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """提取结果摘要"""
        summary = {}
        
        # 提取关键字段
        key_fields = [
            'cycle', 'emotion_cycle', 'position', 'strategy',
            'limit_up_count', 'max_height', 'zhaban_rate',
            'sentiment_score', 'fund_attitude_score', 'risk_signal_score',
            'composite_score', 'signal_level'
        ]
        
        for field in key_fields:
            if field in result:
                summary[field] = result[field]
        
        # 如果有DataFrame，提取基本信息
        for key, value in result.items():
            if HAS_PANDAS and isinstance(value, pd.DataFrame):
                summary[f"{key}_shape"] = value.shape
                summary[f"{key}_columns"] = list(value.columns)[:10]  # 只保存前10列
        
        return summary
    
    def save_result(
        self,
        result: Dict[str, Any],
        outputs: Optional[List[Any]] = None,
        charts: Optional[List[Any]] = None,
        parameters: Optional[Dict[str, Any]] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        save_notebook_copy: bool = True
    ) -> Dict[str, Any]:
        """
        保存notebook结果
        
        Args:
            result: 结果字典
            outputs: 输出列表（文本、数据等）
            charts: 图表列表（matplotlib/plotly图表对象）
            parameters: 运行参数
            description: 描述
            tags: 标签列表
            save_notebook_copy: 是否保存notebook副本
        
        Returns:
            保存信息字典（包含run_id、文件路径等）
        """
        # 生成运行ID和目录
        run_id = self._generate_run_id()
        run_dir = self._generate_run_dir(run_id)
        
        cn_now = datetime.now(timezone.utc) + timedelta(hours=8)
        run_date = cn_now.strftime('%Y-%m-%d')
        run_time = cn_now.strftime('%H:%M:%S')
        
        logger.info(f"开始保存结果: {run_id}")
        
        # 提取摘要
        result_summary = self._extract_summary(result)
        
        # 保存结果数据
        result_file = run_dir / "result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        
        result_size = result_file.stat().st_size
        
        # 保存输出
        output_count = 0
        if outputs:
            output_dir = run_dir / "outputs"
            output_dir.mkdir(exist_ok=True)
            
            for idx, output in enumerate(outputs):
                output_file = output_dir / f"output_{idx+1}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(str(output))
                output_count += 1
        
        # 保存图表
        chart_count = 0
        if charts:
            chart_dir = run_dir / "charts"
            chart_dir.mkdir(exist_ok=True)
            
            for idx, chart in enumerate(charts):
                chart_file = chart_dir / f"chart_{idx+1}.png"
                
                # 检测图表类型并保存
                if hasattr(chart, 'write_image'):
                    # Plotly图表
                    chart.write_image(str(chart_file))
                elif hasattr(chart, 'savefig'):
                    # Matplotlib图表
                    chart.savefig(chart_file, dpi=150, bbox_inches='tight')
                else:
                    # 尝试保存为图片
                    try:
                        if hasattr(chart, 'figure'):
                            chart.figure.savefig(chart_file, dpi=150, bbox_inches='tight')
                        else:
                            logger.warning(f"无法保存图表 {idx+1}，类型: {type(chart)}")
                            continue
                    except Exception as e:
                        logger.warning(f"保存图表 {idx+1} 失败: {e}")
                        continue
                
                chart_count += 1
        
        # 保存DataFrame为CSV（如果有）
        if HAS_PANDAS:
            data_dir = run_dir / "data"
            data_dir.mkdir(exist_ok=True)
            
            for key, value in result.items():
                if isinstance(value, pd.DataFrame):
                    csv_file = data_dir / f"{key}.csv"
                    value.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 创建元数据
        metadata = NotebookResultMetadata(
            notebook_name=self.notebook_name,
            strategy_name=self.strategy_name,
            run_id=run_id,
            run_date=run_date,
            run_time=run_time,
            result_summary=result_summary,
            parameters=parameters or {},
            tags=tags or [],
            description=description,
            file_path=str(run_dir.relative_to(self.base_output_dir)),
            file_size=result_size,
            output_count=output_count,
            chart_count=chart_count
        )
        
        # 保存元数据
        metadata_file = run_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f, ensure_ascii=False, indent=2)
        
        # 保存到MongoDB
        mongodb_id = None
        if self._connected:
            try:
                doc = metadata.to_dict()
                doc['result_summary'] = result_summary
                
                # 如果结果太大，只保存摘要
                if result_size > 10 * 1024 * 1024:  # 10MB
                    doc['result_data'] = None
                    doc['note'] = "结果数据过大，请从文件系统读取"
                else:
                    doc['result_data'] = result
                
                # 插入MongoDB
                collection = self.db[self.COLLECTION_NAME]
                result_obj = collection.insert_one(doc)
                mongodb_id = str(result_obj.inserted_id)
                logger.info(f"MongoDB保存成功: {mongodb_id}")
            except Exception as e:
                logger.warning(f"MongoDB保存失败: {e}")
        
        # 保存notebook副本（如果指定）
        if save_notebook_copy:
            try:
                notebook_source = self.base_output_dir.parent / self.strategy_name / f"{self.notebook_name}.ipynb"
                if notebook_source.exists():
                    notebook_copy = run_dir / f"{self.notebook_name}.ipynb"
                    shutil.copy2(notebook_source, notebook_copy)
                    logger.info(f"Notebook副本已保存: {notebook_copy}")
            except Exception as e:
                logger.warning(f"保存notebook副本失败: {e}")
        
        save_info = {
            'run_id': run_id,
            'run_date': run_date,
            'run_time': run_time,
            'file_path': str(run_dir),
            'relative_path': str(run_dir.relative_to(self.base_output_dir)),
            'mongodb_id': mongodb_id,
            'result_size': result_size,
            'output_count': output_count,
            'chart_count': chart_count
        }
        
        logger.info(f"✅ 结果保存完成: {run_id}")
        logger.info(f"   文件路径: {run_dir}")
        if mongodb_id:
            logger.info(f"   MongoDB ID: {mongodb_id}")
        
        return save_info
    
    def list_results(
        self,
        limit: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        列出历史结果
        
        Args:
            limit: 返回数量限制
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
        
        Returns:
            结果列表
        """
        results = []
        
        # 从文件系统读取
        if self.notebook_dir.exists():
            run_dirs = sorted(
                [d for d in self.notebook_dir.iterdir() if d.is_dir()],
                key=lambda x: x.name,
                reverse=True
            )
            
            for run_dir in run_dirs[:limit]:
                metadata_file = run_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        # 日期过滤
                        if start_date and metadata.get('run_date', '') < start_date:
                            continue
                        if end_date and metadata.get('run_date', '') > end_date:
                            continue
                        
                        results.append(metadata)
                    except Exception as e:
                        logger.warning(f"读取元数据失败 {run_dir}: {e}")
        
        # 从MongoDB读取（如果可用）
        if self._connected:
            try:
                collection = self.db[self.COLLECTION_NAME]
                query = {
                    'strategy_name': self.strategy_name,
                    'notebook_name': self.notebook_name
                }
                
                if start_date:
                    query['run_date'] = {'$gte': start_date}
                if end_date:
                    if 'run_date' in query:
                        query['run_date']['$lte'] = end_date
                    else:
                        query['run_date'] = {'$lte': end_date}
                
                db_results = list(collection.find(query).sort('created_at', DESCENDING).limit(limit))
                
                # 合并结果（去重）
                existing_ids = {r['run_id'] for r in results}
                for db_result in db_results:
                    if db_result.get('run_id') not in existing_ids:
                        # 移除MongoDB的_id
                        db_result.pop('_id', None)
                        results.append(db_result)
            except Exception as e:
                logger.warning(f"MongoDB查询失败: {e}")
        
        # 按时间排序
        results.sort(key=lambda x: x.get('run_id', ''), reverse=True)
        
        return results[:limit]
    
    def get_latest_result(self) -> Optional[Dict[str, Any]]:
        """获取最新结果"""
        results = self.list_results(limit=1)
        return results[0] if results else None
    
    def load_result(self, run_id: str) -> Optional[Dict[str, Any]]:
        """
        加载指定运行ID的结果
        
        Args:
            run_id: 运行ID
        
        Returns:
            结果字典
        """
        run_dir = self.notebook_dir / run_id
        
        if not run_dir.exists():
            logger.warning(f"运行目录不存在: {run_dir}")
            return None
        
        result_file = run_dir / "result.json"
        if not result_file.exists():
            logger.warning(f"结果文件不存在: {result_file}")
            return None
        
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
            return result
        except Exception as e:
            logger.error(f"加载结果失败: {e}")
            return None
    
    def get_result_path(self, run_id: str) -> Optional[Path]:
        """获取结果路径"""
        run_dir = self.notebook_dir / run_id
        return run_dir if run_dir.exists() else None


def save_notebook_result(
    strategy_name: str,
    notebook_name: str,
    result: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    """
    便捷函数：保存notebook结果
    
    Args:
        strategy_name: 策略名称
        notebook_name: notebook名称
        result: 结果字典
        **kwargs: 其他参数（outputs, charts, parameters等）
    
    Returns:
        保存信息字典
    """
    manager = NotebookResultManager(strategy_name, notebook_name)
    return manager.save_result(result, **kwargs)


if __name__ == '__main__':
    # 测试
    manager = NotebookResultManager(
        "chen_xiaoqun_strategy",
        "01_market_environment_judgment"
    )
    
    # 测试保存
    test_result = {
        'cycle': '启动期',
        'position': '10%',
        'strategy': '首板卡位术',
        'limit_up_count': 50,
        'max_height': 5,
        'zhaban_rate': 15.5
    }
    
    save_info = manager.save_result(
        test_result,
        description="测试结果",
        tags=["test"]
    )
    
    print(f"保存信息: {save_info}")
    
    # 测试查询
    results = manager.list_results(limit=5)
    print(f"\n历史结果（共{len(results)}条）:")
    for r in results:
        print(f"  {r['run_id']}: {r['run_date']} {r['run_time']}")
