"""
研究结果保存模块
================

提供统一的研究结果保存功能，支持：
- 多种格式：JSON, CSV, HTML, Parquet
- 自动版本管理和时间戳
- 结果对比和历史追踪
- 元数据记录

使用方式:
    from notebooks.lib.result_saver import ResultSaver, save_result, load_result
    
    saver = ResultSaver("market_analysis")
    saver.save(results, format="json")
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

# 尝试导入可选依赖
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class ResultMetadata:
    """结果元数据"""
    name: str
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0.0"
    notebook: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    checksum: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ResultSaver:
    """
    研究结果保存器
    
    支持保存研究结果到多种格式，自动管理版本和元数据。
    """
    
    def __init__(
        self,
        name: str,
        output_dir: Optional[Path] = None,
        auto_timestamp: bool = True,
        include_metadata: bool = True
    ):
        """
        初始化结果保存器
        
        Args:
            name: 结果名称（用于文件命名）
            output_dir: 输出目录（默认为 notebooks/research/output）
            auto_timestamp: 是否自动添加时间戳
            include_metadata: 是否包含元数据
        """
        self.name = name
        self.auto_timestamp = auto_timestamp
        self.include_metadata = include_metadata
        
        # 设置输出目录
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # 自动检测项目目录
            from .research_init import get_project_root
            self.output_dir = get_project_root() / 'notebooks' / 'research' / 'output'
        
        # 确保目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        self._create_subdirs()
        
        # 元数据
        self.metadata = ResultMetadata(name=name)
        
        logger.info(f"ResultSaver 初始化: {name}, 输出目录: {self.output_dir}")
    
    def _create_subdirs(self):
        """创建子目录结构"""
        subdirs = ['reports', 'charts', 'data', 'logs']
        for subdir in subdirs:
            (self.output_dir / subdir).mkdir(exist_ok=True)
    
    def _generate_filename(self, extension: str, subdir: str = "") -> Path:
        """生成文件名"""
        if self.auto_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.name}_{timestamp}.{extension}"
        else:
            filename = f"{self.name}.{extension}"
        
        if subdir:
            return self.output_dir / subdir / filename
        return self.output_dir / filename
    
    def _calculate_checksum(self, data: Any) -> str:
        """计算数据校验和"""
        if isinstance(data, str):
            content = data
        elif isinstance(data, (dict, list)):
            content = json.dumps(data, sort_keys=True, default=str)
        elif HAS_PANDAS and isinstance(data, pd.DataFrame):
            content = data.to_json()
        else:
            content = str(data)
        
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def set_metadata(
        self,
        description: str = None,
        version: str = None,
        notebook: str = None,
        parameters: Dict = None,
        tags: List[str] = None
    ):
        """设置元数据"""
        if description:
            self.metadata.description = description
        if version:
            self.metadata.version = version
        if notebook:
            self.metadata.notebook = notebook
        if parameters:
            self.metadata.parameters = parameters
        if tags:
            self.metadata.tags = tags
    
    def save_json(
        self,
        data: Union[Dict, List],
        filename: str = None,
        pretty: bool = True
    ) -> Path:
        """
        保存为 JSON 格式
        
        Args:
            data: 要保存的数据
            filename: 文件名（可选）
            pretty: 是否格式化输出
            
        Returns:
            保存的文件路径
        """
        if filename:
            filepath = self.output_dir / 'data' / filename
        else:
            filepath = self._generate_filename('json', 'data')
        
        # 添加元数据
        if self.include_metadata:
            self.metadata.checksum = self._calculate_checksum(data)
            output = {
                "_metadata": self.metadata.to_dict(),
                "data": data
            }
        else:
            output = data
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2 if pretty else None, default=str)
        
        logger.info(f"✅ JSON 保存成功: {filepath}")
        return filepath
    
    def save_csv(
        self,
        data: Union['pd.DataFrame', Dict, List],
        filename: str = None,
        index: bool = True
    ) -> Path:
        """
        保存为 CSV 格式
        
        Args:
            data: 要保存的数据（DataFrame、字典或列表）
            filename: 文件名（可选）
            index: 是否包含索引
            
        Returns:
            保存的文件路径
        """
        if not HAS_PANDAS:
            raise ImportError("需要安装 pandas 才能保存 CSV")
        
        if filename:
            filepath = self.output_dir / 'data' / filename
        else:
            filepath = self._generate_filename('csv', 'data')
        
        # 转换为 DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        df.to_csv(filepath, index=index, encoding='utf-8-sig')
        
        logger.info(f"✅ CSV 保存成功: {filepath}")
        return filepath
    
    def save_parquet(
        self,
        data: 'pd.DataFrame',
        filename: str = None
    ) -> Path:
        """
        保存为 Parquet 格式（高效压缩）
        
        Args:
            data: DataFrame 数据
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if not HAS_PANDAS:
            raise ImportError("需要安装 pandas 才能保存 Parquet")
        
        if filename:
            filepath = self.output_dir / 'data' / filename
        else:
            filepath = self._generate_filename('parquet', 'data')
        
        data.to_parquet(filepath)
        
        logger.info(f"✅ Parquet 保存成功: {filepath}")
        return filepath
    
    def save_html_report(
        self,
        content: str,
        title: str = None,
        filename: str = None
    ) -> Path:
        """
        保存为 HTML 报告
        
        Args:
            content: HTML 内容
            title: 报告标题
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if filename:
            filepath = self.output_dir / 'reports' / filename
        else:
            filepath = self._generate_filename('html', 'reports')
        
        # 包装为完整 HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or self.name}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .report-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .report-header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .report-header .meta {{
            margin-top: 10px;
            font-size: 14px;
            opacity: 0.9;
        }}
        .content {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .positive {{ color: #26a69a; font-weight: bold; }}
        .negative {{ color: #ef5350; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="report-header">
        <h1>{title or self.name}</h1>
        <div class="meta">
            生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            版本: {self.metadata.version}
        </div>
    </div>
    <div class="content">
        {content}
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ HTML 报告保存成功: {filepath}")
        return filepath
    
    def save_chart(
        self,
        figure: Any,
        filename: str = None,
        format: str = "png"
    ) -> Path:
        """
        保存图表
        
        Args:
            figure: matplotlib 或 plotly 图表对象
            filename: 文件名（可选）
            format: 格式（png, svg, html）
            
        Returns:
            保存的文件路径
        """
        if filename:
            filepath = self.output_dir / 'charts' / filename
        else:
            filepath = self._generate_filename(format, 'charts')
        
        # 检测图表类型并保存
        figure_type = type(figure).__name__
        
        if hasattr(figure, 'write_image'):
            # Plotly 图表
            if format == 'html':
                figure.write_html(str(filepath))
            else:
                figure.write_image(str(filepath))
        elif hasattr(figure, 'savefig'):
            # Matplotlib 图表
            figure.savefig(filepath, dpi=150, bbox_inches='tight')
        else:
            raise TypeError(f"不支持的图表类型: {figure_type}")
        
        logger.info(f"✅ 图表保存成功: {filepath}")
        return filepath
    
    def save(
        self,
        data: Any,
        format: str = "json",
        filename: str = None,
        **kwargs
    ) -> Path:
        """
        通用保存方法
        
        Args:
            data: 要保存的数据
            format: 格式（json, csv, parquet, html）
            filename: 文件名（可选）
            **kwargs: 额外参数
            
        Returns:
            保存的文件路径
        """
        format = format.lower()
        
        if format == 'json':
            return self.save_json(data, filename, **kwargs)
        elif format == 'csv':
            return self.save_csv(data, filename, **kwargs)
        elif format == 'parquet':
            return self.save_parquet(data, filename)
        elif format == 'html':
            return self.save_html_report(data, filename=filename, **kwargs)
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def list_results(self, pattern: str = "*") -> List[Path]:
        """列出已保存的结果"""
        results = []
        for subdir in ['data', 'reports', 'charts']:
            dir_path = self.output_dir / subdir
            if dir_path.exists():
                results.extend(dir_path.glob(f"{self.name}*{pattern}"))
        return sorted(results, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def get_latest_result(self, format: str = "json") -> Optional[Path]:
        """获取最新的结果文件"""
        results = self.list_results(f"*.{format}")
        return results[0] if results else None


def load_result(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    加载保存的结果
    
    Args:
        filepath: 文件路径
        
    Returns:
        加载的数据
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    suffix = filepath.suffix.lower()
    
    if suffix == '.json':
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif suffix == '.csv':
        if not HAS_PANDAS:
            raise ImportError("需要安装 pandas 才能加载 CSV")
        return pd.read_csv(filepath)
    elif suffix == '.parquet':
        if not HAS_PANDAS:
            raise ImportError("需要安装 pandas 才能加载 Parquet")
        return pd.read_parquet(filepath)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


def save_result(
    name: str,
    data: Any,
    format: str = "json",
    **kwargs
) -> Path:
    """
    便捷函数：保存研究结果
    
    Args:
        name: 结果名称
        data: 数据
        format: 格式
        **kwargs: 额外参数
        
    Returns:
        保存的文件路径
    """
    saver = ResultSaver(name)
    return saver.save(data, format=format, **kwargs)


def compare_results(
    result1: Union[str, Path, Dict],
    result2: Union[str, Path, Dict],
    keys: List[str] = None
) -> Dict[str, Any]:
    """
    比较两个结果
    
    Args:
        result1: 第一个结果（路径或数据）
        result2: 第二个结果（路径或数据）
        keys: 要比较的键（可选）
        
    Returns:
        比较结果字典
    """
    # 加载数据
    if isinstance(result1, (str, Path)):
        data1 = load_result(result1)
    else:
        data1 = result1
    
    if isinstance(result2, (str, Path)):
        data2 = load_result(result2)
    else:
        data2 = result2
    
    # 提取实际数据（如果有元数据包装）
    if isinstance(data1, dict) and 'data' in data1:
        data1 = data1['data']
    if isinstance(data2, dict) and 'data' in data2:
        data2 = data2['data']
    
    comparison = {
        "identical": data1 == data2,
        "differences": []
    }
    
    if isinstance(data1, dict) and isinstance(data2, dict):
        all_keys = set(data1.keys()) | set(data2.keys())
        if keys:
            all_keys = all_keys & set(keys)
        
        for key in all_keys:
            val1 = data1.get(key)
            val2 = data2.get(key)
            
            if val1 != val2:
                comparison["differences"].append({
                    "key": key,
                    "value1": val1,
                    "value2": val2
                })
    
    return comparison


if __name__ == '__main__':
    # 测试
    saver = ResultSaver("test_results")
    
    # 测试 JSON 保存
    test_data = {
        "trend_score": 0.75,
        "market_regime": "bull",
        "signals": [1, 2, 3]
    }
    
    saver.set_metadata(
        description="测试结果",
        notebook="test_notebook",
        tags=["test", "example"]
    )
    
    json_path = saver.save_json(test_data)
    print(f"JSON 保存到: {json_path}")
    
    # 加载并验证
    loaded = load_result(json_path)
    print(f"加载的数据: {loaded}")

