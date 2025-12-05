#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试候选池构建模块

使用JQData免费版构建候选池
"""

import sys
import logging
from pathlib import Path

# 设置项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def test_candidate_pool():
    """测试候选池构建"""
    try:
        from jqdata.client import JQDataClient
        from core.candidate_pool_builder import CandidatePoolBuilder
        from config.config_manager import get_config_manager
        
        # 1. 初始化JQData客户端
        logger.info("="*60)
        logger.info("步骤1: 初始化JQData客户端")
        logger.info("="*60)
        
        config_manager = get_config_manager()
        config = config_manager.get_jqdata_config()
        
        if not config.get('username') or not config.get('password'):
            logger.error("❌ 未找到JQData配置，请先配置 config/jqdata_config.json")
            logger.info("\n配置示例:")
            logger.info('{"username": "your_username", "password": "your_password"}')
            return
        
        jq_client = JQDataClient()
        if not jq_client.authenticate(config['username'], config['password']):
            logger.error("❌ JQData认证失败")
            return
        
        logger.info("✅ JQData认证成功")
        
        # 2. 创建候选池构建器
        logger.info("\n" + "="*60)
        logger.info("步骤2: 创建候选池构建器")
        logger.info("="*60)
        
        builder = CandidatePoolBuilder(jq_client=jq_client)
        logger.info("✅ 候选池构建器创建成功")
        
        # 3. 测试获取概念列表（可选）
        logger.info("\n" + "="*60)
        logger.info("步骤3: 获取概念列表（示例）")
        logger.info("="*60)
        
        try:
            concepts = jq_client.get_all_concepts()
            if not concepts.empty:
                logger.info(f"✅ 获取到 {len(concepts)} 个概念")
                logger.info("前5个概念:")
                for idx, (code, row) in enumerate(concepts.head().iterrows()):
                    logger.info(f"  {idx+1}. {row.get('name', code)} ({code})")
        except Exception as e:
            logger.warning(f"⚠️ 获取概念列表失败: {e}")
            logger.info("   继续使用已知概念名称测试...")
        
        # 4. 构建候选池（使用示例概念）
        logger.info("\n" + "="*60)
        logger.info("步骤4: 构建候选池")
        logger.info("="*60)
        
        # 示例：使用"石墨烯"概念（JQData中存在的概念）
        test_concept = "石墨烯"  # 可以改为实际存在的概念名称
        logger.info(f"测试概念: {test_concept}")
        
        try:
            pool = builder.build_from_mainline(
                mainline_name=test_concept,
                mainline_type='concept',
                date=None,  # 使用默认日期（免费版权限范围内的日期）
                use_cache=True
            )
            
            logger.info(f"\n✅ 候选池构建成功!")
            logger.info(f"   池ID: {pool.pool_id}")
            logger.info(f"   主线: {pool.mainline_name}")
            logger.info(f"   总成分股数: {pool.total_count}")
            logger.info(f"   筛选后数量: {pool.filtered_count}")
            
            # 显示前10只候选股票
            if pool.stocks:
                logger.info(f"\n前10只候选股票:")
                logger.info("-" * 80)
                for i, stock in enumerate(pool.stocks[:10], 1):
                    logger.info(
                        f"{i:2d}. {stock.name} ({stock.code})\n"
                        f"     技术得分: {stock.technical_score:.1f} | "
                        f"基本面得分: {stock.fundamental_score:.1f} | "
                        f"综合得分: {stock.composite_score:.1f}\n"
                        f"     标签: {', '.join(stock.tags) if stock.tags else '无'}\n"
                        f"     涨跌幅: {stock.change_pct:.2f}% | "
                        f"连续上涨: {stock.consecutive_up_days}天"
                    )
            else:
                logger.warning("⚠️ 候选池为空，可能原因:")
                logger.warning("   1. 概念名称不存在")
                logger.warning("   2. 成分股数据为空")
                logger.warning("   3. 筛选条件过严")
                logger.warning("   4. 免费版数据权限限制")
        
        except Exception as e:
            logger.error(f"❌ 构建候选池失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 5. 总结
        logger.info("\n" + "="*60)
        logger.info("测试总结")
        logger.info("="*60)
        logger.info("✅ 候选池构建模块测试完成")
        logger.info("\n使用建议:")
        logger.info("1. 确保JQData账号已认证")
        logger.info("2. 使用实际存在的概念/行业名称")
        logger.info("3. 注意免费版的数据权限限制（日期范围）")
        logger.info("4. 合理使用缓存，避免频繁API调用")
        
    except ImportError as e:
        logger.error(f"❌ 导入失败: {e}")
        logger.info("\n请确保已安装依赖:")
        logger.info("  pip install jqdatasdk pymongo pandas")
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_candidate_pool()


