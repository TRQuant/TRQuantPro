"""
MCP工具参数验证器

提供统一的参数验证功能，确保所有MCP工具的参数符合JSON Schema定义。
"""

import jsonschema
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ParameterValidationError(Exception):
    """参数验证错误"""
    def __init__(self, message: str, errors: List[str]):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class ParameterValidator:
    """参数验证器"""
    
    @staticmethod
    def validate(schema: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证参数是否符合Schema定义
        
        Args:
            schema: JSON Schema定义
            params: 待验证的参数
        
        Returns:
            {"valid": True, "validated_params": {...}} 或抛出异常
        
        Raises:
            ParameterValidationError: 参数验证失败
        """
        try:
            # 应用默认值
            validated_params = ParameterValidator._apply_defaults(schema, params)
            
            # 验证参数
            jsonschema.validate(instance=validated_params, schema=schema)
            
            logger.debug(f"参数验证通过: {validated_params}")
            return {
                "valid": True,
                "validated_params": validated_params
            }
        except jsonschema.ValidationError as e:
            error_msg = f"参数验证失败: {e.message}"
            errors = [f"{e.path}: {e.message}"]
            
            # 收集所有验证错误
            for error in e.context:
                errors.append(f"{error.path}: {error.message}")
            
            logger.error(f"{error_msg}, 错误详情: {errors}")
            raise ParameterValidationError(error_msg, errors)
        except Exception as e:
            error_msg = f"参数验证异常: {str(e)}"
            logger.error(error_msg)
            raise ParameterValidationError(error_msg, [str(e)])
    
    @staticmethod
    def _apply_defaults(schema: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用Schema中定义的默认值
        
        Args:
            schema: JSON Schema定义
            params: 待验证的参数
        
        Returns:
            应用默认值后的参数
        """
        validated_params = params.copy()
        
        if "properties" not in schema:
            return validated_params
        
        for prop_name, prop_schema in schema["properties"].items():
            if prop_name not in validated_params and "default" in prop_schema:
                validated_params[prop_name] = prop_schema["default"]
                logger.debug(f"应用默认值: {prop_name} = {prop_schema['default']}")
        
        return validated_params
    
    @staticmethod
    def validate_required(schema: Dict[str, Any], params: Dict[str, Any]) -> bool:
        """
        检查必填参数是否提供
        
        Args:
            schema: JSON Schema定义
            params: 待验证的参数
        
        Returns:
            True if all required parameters are provided
        """
        if "required" not in schema:
            return True
        
        missing = [param for param in schema["required"] if param not in params]
        if missing:
            raise ParameterValidationError(
                f"缺少必填参数: {', '.join(missing)}",
                [f"参数 '{param}' 是必填的" for param in missing]
            )
        
        return True
    
    @staticmethod
    def get_schema_summary(schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取Schema摘要信息
        
        Args:
            schema: JSON Schema定义
        
        Returns:
            Schema摘要信息
        """
        summary = {
            "type": schema.get("type", "object"),
            "required": schema.get("required", []),
            "properties": {}
        }
        
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                summary["properties"][prop_name] = {
                    "type": prop_schema.get("type", "unknown"),
                    "description": prop_schema.get("description", ""),
                    "default": prop_schema.get("default"),
                    "required": prop_name in schema.get("required", [])
                }
        
        return summary


def validate_mcp_tool_params(tool_name: str, schema: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证MCP工具参数的便捷函数
    
    Args:
        tool_name: 工具名称
        schema: JSON Schema定义
        params: 待验证的参数
    
    Returns:
        验证后的参数
    
    Raises:
        ParameterValidationError: 参数验证失败
    """
    try:
        result = ParameterValidator.validate(schema, params)
        logger.info(f"工具 '{tool_name}' 参数验证通过")
        return result["validated_params"]
    except ParameterValidationError as e:
        logger.error(f"工具 '{tool_name}' 参数验证失败: {e.message}")
        raise
