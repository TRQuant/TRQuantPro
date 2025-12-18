#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Experiment - 实验追踪管理
========================

M1里程碑核心组件：实验可追踪、可对比

功能：
1. 实验配置与结果记录
2. 实验版本管理
3. A/B实验对比
4. 实验产物链接
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class ExperimentConfig:
    """实验配置"""
    strategy_pack: str = ""       # 策略包名称
    strategy_version: str = ""    # 策略版本
    factor_config: Dict = field(default_factory=dict)   # 因子配置
    backtest_config: Dict = field(default_factory=dict) # 回测配置
    optimization_config: Dict = field(default_factory=dict) # 优化配置
    custom_params: Dict = field(default_factory=dict)   # 自定义参数
    
    def get_config_hash(self) -> str:
        """获取配置哈希"""
        content = json.dumps(asdict(self), sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:8]


@dataclass
class ExperimentMetrics:
    """实验指标"""
    # 回测指标
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    
    # 十倍股专属指标（M4预留）
    recall_at_k: Dict[str, float] = field(default_factory=dict)  # Recall@5, @10, @20
    time_to_detection: float = 0.0  # 平均识别时间（天）
    false_positive_rate: float = 0.0  # 误杀率
    
    # 自定义指标
    custom_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class ExperimentArtifact:
    """实验产物"""
    artifact_id: str
    artifact_type: str  # report, model, code, data
    name: str
    path: str
    size_bytes: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Experiment:
    """
    实验记录
    
    完整记录一次实验的配置、数据、指标和产物
    """
    experiment_id: str
    name: str
    description: str = ""
    
    # 实验状态
    status: str = "created"  # created, running, completed, failed
    
    # 配置
    config: ExperimentConfig = field(default_factory=ExperimentConfig)
    
    # 数据快照引用
    data_snapshot_ids: List[str] = field(default_factory=list)
    workflow_id: str = ""
    
    # 指标
    metrics: ExperimentMetrics = field(default_factory=ExperimentMetrics)
    
    # 产物
    artifacts: List[ExperimentArtifact] = field(default_factory=list)
    
    # 时间戳
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: str = ""
    completed_at: str = ""
    
    # 标签
    tags: List[str] = field(default_factory=list)
    
    # 备注
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "config": asdict(self.config),
            "data_snapshot_ids": self.data_snapshot_ids,
            "workflow_id": self.workflow_id,
            "metrics": asdict(self.metrics),
            "artifacts": [asdict(a) for a in self.artifacts],
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "tags": self.tags,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experiment":
        exp = cls(
            experiment_id=data["experiment_id"],
            name=data["name"],
            description=data.get("description", ""),
            status=data.get("status", "created"),
            workflow_id=data.get("workflow_id", ""),
            data_snapshot_ids=data.get("data_snapshot_ids", []),
            created_at=data.get("created_at", ""),
            started_at=data.get("started_at", ""),
            completed_at=data.get("completed_at", ""),
            tags=data.get("tags", []),
            notes=data.get("notes", "")
        )
        
        if "config" in data:
            exp.config = ExperimentConfig(**data["config"])
        if "metrics" in data:
            exp.metrics = ExperimentMetrics(**data["metrics"])
        if "artifacts" in data:
            exp.artifacts = [ExperimentArtifact(**a) for a in data["artifacts"]]
        
        return exp


class ExperimentTracker:
    """
    实验追踪器
    
    管理实验的全生命周期
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "experiments"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._mongo_db = None
        self._init_mongo()
    
    def _init_mongo(self):
        """初始化MongoDB连接"""
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            self._mongo_db = client.get_database("trquant")
        except:
            pass
    
    def create_experiment(
        self,
        name: str,
        config: ExperimentConfig = None,
        description: str = "",
        tags: List[str] = None
    ) -> Experiment:
        """创建实验"""
        import uuid
        
        experiment_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        experiment = Experiment(
            experiment_id=experiment_id,
            name=name,
            description=description,
            config=config or ExperimentConfig(),
            tags=tags or []
        )
        
        self._save(experiment)
        logger.info(f"[Experiment] 创建实验: {experiment_id} ({name})")
        
        return experiment
    
    def start_experiment(self, experiment_id: str) -> bool:
        """开始实验"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return False
        
        exp.status = "running"
        exp.started_at = datetime.now().isoformat()
        self._save(exp)
        
        logger.info(f"[Experiment] 开始实验: {experiment_id}")
        return True
    
    def complete_experiment(
        self,
        experiment_id: str,
        metrics: ExperimentMetrics = None,
        notes: str = ""
    ) -> bool:
        """完成实验"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return False
        
        exp.status = "completed"
        exp.completed_at = datetime.now().isoformat()
        if metrics:
            exp.metrics = metrics
        if notes:
            exp.notes = notes
        
        self._save(exp)
        logger.info(f"[Experiment] 完成实验: {experiment_id}")
        return True
    
    def fail_experiment(self, experiment_id: str, error: str = "") -> bool:
        """标记实验失败"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return False
        
        exp.status = "failed"
        exp.completed_at = datetime.now().isoformat()
        exp.notes = f"失败原因: {error}" if error else exp.notes
        
        self._save(exp)
        logger.warning(f"[Experiment] 实验失败: {experiment_id}")
        return True
    
    def update_metrics(self, experiment_id: str, metrics: Dict[str, float]) -> bool:
        """更新实验指标"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return False
        
        for key, value in metrics.items():
            if hasattr(exp.metrics, key):
                setattr(exp.metrics, key, value)
            else:
                exp.metrics.custom_metrics[key] = value
        
        self._save(exp)
        return True
    
    def add_artifact(
        self,
        experiment_id: str,
        artifact_type: str,
        name: str,
        path: str
    ) -> Optional[str]:
        """添加实验产物"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return None
        
        import uuid
        artifact_id = f"art_{uuid.uuid4().hex[:8]}"
        
        artifact = ExperimentArtifact(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            name=name,
            path=path
        )
        
        # 获取文件大小
        artifact_path = Path(path)
        if artifact_path.exists():
            artifact.size_bytes = artifact_path.stat().st_size
        
        exp.artifacts.append(artifact)
        self._save(exp)
        
        logger.info(f"[Experiment] 添加产物: {experiment_id}/{artifact_id}")
        return artifact_id
    
    def link_snapshot(self, experiment_id: str, snapshot_id: str) -> bool:
        """关联数据快照"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return False
        
        if snapshot_id not in exp.data_snapshot_ids:
            exp.data_snapshot_ids.append(snapshot_id)
            self._save(exp)
        
        return True
    
    def link_workflow(self, experiment_id: str, workflow_id: str) -> bool:
        """关联工作流"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return False
        
        exp.workflow_id = workflow_id
        self._save(exp)
        return True
    
    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """获取实验"""
        file_path = self.storage_path / f"{experiment_id}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, 'r') as f:
            return Experiment.from_dict(json.load(f))
    
    def list_experiments(
        self,
        status: str = None,
        strategy_pack: str = None,
        tags: List[str] = None,
        limit: int = 100
    ) -> List[Experiment]:
        """列出实验"""
        experiments = []
        
        for file_path in sorted(self.storage_path.glob("exp_*.json"), reverse=True):
            try:
                with open(file_path, 'r') as f:
                    exp = Experiment.from_dict(json.load(f))
                
                # 过滤
                if status and exp.status != status:
                    continue
                if strategy_pack and exp.config.strategy_pack != strategy_pack:
                    continue
                if tags and not set(tags).issubset(set(exp.tags)):
                    continue
                
                experiments.append(exp)
                
                if len(experiments) >= limit:
                    break
            except:
                continue
        
        return experiments
    
    def compare_experiments(self, exp_id_1: str, exp_id_2: str) -> Dict[str, Any]:
        """对比两个实验"""
        exp1 = self.get_experiment(exp_id_1)
        exp2 = self.get_experiment(exp_id_2)
        
        if not exp1 or not exp2:
            return {"error": "实验不存在"}
        
        comparison = {
            "experiment_1": {"id": exp_id_1, "name": exp1.name},
            "experiment_2": {"id": exp_id_2, "name": exp2.name},
            "config_diff": {
                "same_config": exp1.config.get_config_hash() == exp2.config.get_config_hash()
            },
            "metrics_comparison": {},
            "winner": None
        }
        
        # 对比指标
        metrics1 = asdict(exp1.metrics)
        metrics2 = asdict(exp2.metrics)
        
        for key in metrics1:
            if key == "custom_metrics":
                continue
            v1, v2 = metrics1[key], metrics2[key]
            if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                diff = v2 - v1
                comparison["metrics_comparison"][key] = {
                    "exp1": v1,
                    "exp2": v2,
                    "diff": diff,
                    "diff_pct": (diff / v1 * 100) if v1 != 0 else 0
                }
        
        # 判断胜者（基于夏普比率）
        if exp1.metrics.sharpe_ratio > exp2.metrics.sharpe_ratio:
            comparison["winner"] = exp_id_1
        elif exp2.metrics.sharpe_ratio > exp1.metrics.sharpe_ratio:
            comparison["winner"] = exp_id_2
        
        return comparison
    
    def export_experiment(self, experiment_id: str, export_path: Path = None) -> str:
        """导出实验报告"""
        exp = self.get_experiment(experiment_id)
        if not exp:
            return ""
        
        export_path = export_path or self.storage_path / f"{experiment_id}_export.json"
        
        export_data = {
            "experiment": exp.to_dict(),
            "exported_at": datetime.now().isoformat()
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(export_path)
    
    def _save(self, experiment: Experiment):
        """保存实验"""
        file_path = self.storage_path / f"{experiment.experiment_id}.json"
        with open(file_path, 'w') as f:
            json.dump(experiment.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 同步到MongoDB
        if self._mongo_db is not None:
            try:
                self._mongo_db.experiments.update_one(
                    {"experiment_id": experiment.experiment_id},
                    {"$set": experiment.to_dict()},
                    upsert=True
                )
            except:
                pass


# 全局追踪器
_tracker: Optional[ExperimentTracker] = None

def get_experiment_tracker() -> ExperimentTracker:
    """获取实验追踪器"""
    global _tracker
    if _tracker is None:
        _tracker = ExperimentTracker()
    return _tracker
