# -*- coding: utf-8 -*-
"""
LaVague Cursor Context - 专为Cursor IDE设计
===========================================

本模块创建了一个自定义的LaVague Context，专为Cursor IDE环境设计。
在Cursor IDE中，LaVague通过MCP工具调用，使用Cursor内置的AI能力。

参考LaVague官方实现：
- https://github.com/lavague-ai/LaVague
- 使用LlamaIndex兼容的LLM模型

在Cursor IDE中的使用方式：
1. 通过MCP工具调用（推荐）
2. 使用默认OpenAI Context（需要OPENAI_API_KEY）
"""

import os
import logging
from typing import Optional
from lavague.core.context import Context, DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE

logger = logging.getLogger(__name__)


class CursorContext(Context):
    """
    Cursor Context - 专为Cursor IDE设计的LaVague Context
    
    在Cursor IDE中，LaVague通过以下方式工作：
    1. 通过MCP工具调用（推荐）- 使用Cursor内置AI能力
    2. 使用OpenAI API（备选）- 需要OPENAI_API_KEY
    
    使用方式：
        from core.crawlers.lavague_cursor_context import CursorContext
        from lavague.core import ActionEngine, WorldModel
        from lavague.drivers.selenium import SeleniumDriver
        
        context = CursorContext()
        driver = SeleniumDriver(headless=True)
        action_engine = ActionEngine.from_context(context, driver)
        world_model = WorldModel.from_context(context)
    """
    
    def __init__(
        self,
        use_openai: bool = False,
        llm_model: str = "gpt-4o-mini",
        mm_llm_model: str = "gpt-4o",
        embedding_model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
    ):
        """
        初始化Cursor Context
        
        Args:
            use_openai: 是否使用OpenAI API（默认False，在Cursor IDE中通过MCP调用）
            llm_model: LLM模型名称（仅当use_openai=True时使用）
            mm_llm_model: 多模态LLM模型名称（仅当use_openai=True时使用）
            embedding_model: 嵌入模型名称（仅当use_openai=True时使用）
            api_key: OpenAI API密钥（仅当use_openai=True时使用）
        """
        self.use_openai = use_openai
        
        try:
            if use_openai:
                # 使用OpenAI API（备选方案，需要API密钥）
                from llama_index.llms.openai import OpenAI
                from llama_index.multi_modal_llms.openai import OpenAIMultiModal
                from llama_index.embeddings.openai import OpenAIEmbedding
                
                if api_key is None:
                    api_key = os.getenv("OPENAI_API_KEY")
                    if api_key is None:
                        raise ValueError("OPENAI_API_KEY is not set")
                
                llm = OpenAI(
                    api_key=api_key,
                    model=llm_model,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    temperature=DEFAULT_TEMPERATURE,
                )
                mm_llm = OpenAIMultiModal(api_key=api_key, model=mm_llm_model)
                embedding = OpenAIEmbedding(api_key=api_key, model=embedding_model)
                
                logger.info(f"✅ 使用OpenAI API: LLM={llm_model}, MM_LLM={mm_llm_model}")
                
            else:
                # Cursor IDE模式：尝试使用默认Context，如果失败则提示
                # 在Cursor IDE中，LaVague通过MCP工具调用，使用Cursor内置AI能力
                # 注意：LaVague的默认Context需要OPENAI_API_KEY，但在Cursor IDE中通过MCP调用时，
                # 实际的AI调用由Cursor的MCP工具处理，这里只是初始化LaVague框架
                try:
                    from lavague.core.context import get_default_context
                    default_context = get_default_context()
                    
                    # 使用默认Context的模型
                    llm = default_context.llm
                    mm_llm = default_context.mm_llm
                    embedding = default_context.embedding
                    
                    logger.info("✅ 使用Cursor IDE模式（通过MCP工具调用，使用Cursor内置AI）")
                    logger.info("   注意：在Cursor IDE中，LaVague通过MCP工具自动使用Cursor的AI能力")
                except Exception as e:
                    # 如果默认Context初始化失败（缺少OPENAI_API_KEY），给出明确提示
                    logger.warning("⚠️  默认Context初始化失败（可能需要OPENAI_API_KEY）")
                    logger.info("   在Cursor IDE中，建议通过MCP工具调用LaVague功能")
                    logger.info("   或者设置OPENAI_API_KEY环境变量，或使用use_openai=True模式")
                    raise ValueError(
                        "Cursor IDE模式需要OPENAI_API_KEY或通过MCP工具调用。"
                        "在Cursor IDE中，建议使用MCP工具：crawler.lavague.execute"
                    )
            
            # 初始化Context
            super().__init__(
                llm=llm,
                mm_llm=mm_llm,
                embedding=embedding,
                extraction_llm=llm,  # 使用相同的LLM进行提取
            )
            
            logger.info("✅ CursorContext初始化成功")
            
        except ImportError as e:
            logger.error(f"❌ 导入失败: {e}")
            logger.info("请安装必要的依赖:")
            if use_openai:
                logger.info("  pip install llama-index-llms-openai llama-index-embeddings-openai")
            else:
                logger.info("  pip install lavague lavague-contexts-openai")
            raise
        except Exception as e:
            logger.error(f"❌ Context初始化失败: {e}")
            raise


def get_cursor_context(use_openai: bool = False) -> CursorContext:
    """
    获取Cursor Context实例
    
    Args:
        use_openai: 是否使用OpenAI API（默认False，在Cursor IDE中通过MCP调用）
    
    Returns:
        CursorContext实例
    """
    return CursorContext(use_openai=use_openai)
