"""
文件名: code_6_4_run_pipeline.py
保存路径: code_library/006_Chapter6_Factor_Library/6.4/code_6_4_run_pipeline.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.4_Factor_Pipeline_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: run_pipeline

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def run_pipeline(
    self,
    date: Optional[Union[str, datetime]] = None,
    factor_categories: Optional[List[str]] = None,
    max_retries: int = 3,
) -> Dict[str, Any]:
        """
    run_pipeline函数
    
    **设计原理**：
    - **核心功能**：实现run_pipeline的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    if date is None:
        date = datetime.now()
    
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    
    self.run_stats["start_time"] = datetime.now()
    
    try:
        # 1. 获取股票池
        logger.info(f"步骤1: 获取股票池 ({self.stock_pool})...")
        stocks = self.get_stock_pool(date)
        stocks = self.filter_stocks(stocks, date)
        self.run_stats["total_stocks"] = len(stocks)
        
        if not stocks:
            logger.warning("股票池为空，跳过计算")
            return self.run_stats
        
        # 2. 获取因子列表
        logger.info("步骤2: 获取因子列表...")
        if factor_categories:
            factor_names = []
            for category in factor_categories:
                factor_names.extend(self.factor_manager.list_factors(category))
        else:
            factor_names = self.factor_manager.list_factors()
        
        # 3. 批量计算因子
        logger.info(f"步骤3: 批量计算因子 ({len(factor_names)}个)...")
        success_count = 0
        failed_count = 0
        
        for factor_name in factor_names:
            try:
                # 计算因子
                result = self.factor_manager.calculate_factor(
                    factor_name, stocks, date
                )
                
                if result is None or result.values.empty:
                    logger.warning(f"因子计算返回空结果: {factor_name}")
                    failed_count += 1
                    continue
                
                # 中性化处理（可选）
                if self.neutralize:
                    neutralized_values = self.neutralizer.neutralize(
                        result.values,
                        stocks,
                        date,
                        neutralize_industry=True,
                        neutralize_size=True
                    )
                    result.values = neutralized_values
                
                # 存储因子值
                self.factor_storage.save_factor_values(
                    factor_name,
                    date,
                    result.values,
                    overwrite=True
                )
                
                success_count += 1
                logger.info(f"因子计算成功: {factor_name} ({result.values.notna().sum()}/{len(stocks)})")
            
            except Exception as e:
                logger.error(f"因子计算失败: {factor_name}, 错误: {e}")
                failed_count += 1
                self.run_stats["errors"].append({
                    "factor": factor_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        self.run_stats["success_factors"] = success_count
        self.run_stats["failed_factors"] = failed_count
        
        logger.info(f"流水线完成: 成功 {success_count}, 失败 {failed_count}")
    
    except Exception as e:
        logger.error(f"流水线运行失败: {e}")
        self.run_stats["errors"].append({
            "stage": "pipeline",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
    
    finally:
        self.run_stats["end_time"] = datetime.now()
        self._save_run_log()
    
    return self.run_stats