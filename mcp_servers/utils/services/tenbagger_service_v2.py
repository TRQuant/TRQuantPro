"""
十倍股服务实现 V2

实现ITenbaggerService接口，封装V2评估系统的功能。

Author: TRQuant Team
Date: 2025-12-21
"""

from typing import Dict, Any, List, Optional
import logging

from core.mcp.interfaces.tenbagger_interface import (
    ITenbaggerService,
    TenbaggerRequest,
    TenbaggerResponse,
    TenbaggerBatchRequest,
    TenbaggerRankingRequest
)

logger = logging.getLogger(__name__)


class TenbaggerServiceV2(ITenbaggerService):
    """
    十倍股服务实现 V2
    
    封装V2评估系统的功能，实现ITenbaggerService接口。
    这样GUI层不直接依赖V2的具体实现，可以独立升级。
    """
    
    def __init__(self):
        self._evaluator = None
        self._data_fetcher = None
        self._report_generator = None
    
    def _get_evaluator(self):
        """延迟加载评估器"""
        if self._evaluator is None:
            from mcp_servers.utils.tenbagger_v2 import get_evaluator_v2
            self._evaluator = get_evaluator_v2()
        return self._evaluator
    
    def _get_data_fetcher(self):
        """延迟加载数据获取器"""
        if self._data_fetcher is None:
            from mcp_servers.utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher
            from jqdata.client import JQDataClient
            from config.config_manager import get_config_manager
            
            jq_client = JQDataClient()
            cm = get_config_manager()
            jq_config = cm.get_jqdata_config()
            jq_client.authenticate(jq_config['username'], jq_config['password'])
            
            self._data_fetcher = TenbaggerDataFetcher(jq_client)
        return self._data_fetcher
    
    def _get_report_generator(self):
        """延迟加载报告生成器"""
        if self._report_generator is None:
            from mcp_servers.utils.tenbagger_v2.report_generator import ReportGenerator
            self._report_generator = ReportGenerator(self._get_evaluator())
        return self._report_generator
    
    def get_version(self) -> str:
        """获取服务版本"""
        return "v2"
    
    def evaluate(self, request: TenbaggerRequest) -> TenbaggerResponse:
        """评估单个股票"""
        try:
            evaluator = self._get_evaluator()
            
            # 如果有数据，直接使用；否则获取数据
            if request.data:
                data = request.data
            else:
                data_fetcher = self._get_data_fetcher()
                data = data_fetcher.fetch_stock_data(request.symbol)
                if not data:
                    return TenbaggerResponse(
                        success=False,
                        error=f"无法获取 {request.symbol} 的数据",
                        version="v2"
                    )
            
            # 评估
            report = evaluator.evaluate(request.symbol, request.name or request.symbol, data)
            
            return TenbaggerResponse(
                success=True,
                report=report.to_dict(),
                version="v2"
            )
        except Exception as e:
            logger.error(f"评估 {request.symbol} 失败: {e}", exc_info=True)
            return TenbaggerResponse(
                success=False,
                error=str(e),
                version="v2"
            )
    
    def batch_evaluate(self, request: TenbaggerBatchRequest) -> List[TenbaggerResponse]:
        """批量评估"""
        responses = []
        evaluator = self._get_evaluator()
        data_fetcher = self._get_data_fetcher()
        
        for symbol in request.symbols[:request.max_count]:
            try:
                # 获取数据
                data = data_fetcher.fetch_stock_data(symbol)
                if not data:
                    continue
                
                # 评估
                report = evaluator.evaluate(symbol, data.get("name", symbol), data)
                responses.append(TenbaggerResponse(
                    success=True,
                    report=report.to_dict(),
                    version="v2"
                ))
            except Exception as e:
                logger.warning(f"批量评估 {symbol} 失败: {e}")
                responses.append(TenbaggerResponse(
                    success=False,
                    error=str(e),
                    version="v2"
                ))
        
        return responses
    
    def get_report(self, symbol: str) -> TenbaggerResponse:
        """获取报告"""
        try:
            evaluator = self._get_evaluator()
            report = evaluator.get_report(symbol)
            
            if report:
                return TenbaggerResponse(
                    success=True,
                    report=report.to_dict(),
                    version="v2"
                )
            else:
                return TenbaggerResponse(
                    success=False,
                    error=f"未找到 {symbol} 的评估报告",
                    version="v2"
                )
        except Exception as e:
            logger.error(f"获取 {symbol} 报告失败: {e}", exc_info=True)
            return TenbaggerResponse(
                success=False,
                error=str(e),
                version="v2"
            )
    
    def get_rankings(self, request: TenbaggerRankingRequest) -> List[TenbaggerResponse]:
        """获取排名"""
        try:
            evaluator = self._get_evaluator()
            recommendations = evaluator.get_recommendations(min_level=request.min_level)
            
            # 排序并取Top N
            sorted_reports = sorted(
                recommendations,
                key=lambda r: r.final_score,
                reverse=True
            )[:request.top_n]
            
            return [
                TenbaggerResponse(
                    success=True,
                    report=r.to_dict(),
                    version="v2"
                )
                for r in sorted_reports
            ]
        except Exception as e:
            logger.error(f"获取排名失败: {e}", exc_info=True)
            return []
    
    def generate_report(
        self,
        format: str = "markdown",
        min_level: str = "A",
        output_path: Optional[str] = None
    ) -> TenbaggerResponse:
        """生成报告"""
        try:
            generator = self._get_report_generator()
            
            if output_path:
                saved_path = generator.save_report(
                    output_path,
                    format=format,
                    min_level=min_level
                )
                return TenbaggerResponse(
                    success=True,
                    report={"output_path": saved_path, "format": format},
                    version="v2"
                )
            else:
                if format == "html":
                    content = generator.generate_html(min_level=min_level)
                elif format == "json":
                    content = generator.generate_json(min_level=min_level)
                else:
                    content = generator.generate_markdown(min_level=min_level)
                
                return TenbaggerResponse(
                    success=True,
                    report={"content": content, "format": format},
                    version="v2"
                )
        except Exception as e:
            logger.error(f"生成报告失败: {e}", exc_info=True)
            return TenbaggerResponse(
                success=False,
                error=str(e),
                version="v2"
            )
