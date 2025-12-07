"""代码生成Agent

参考 ReCode 的递归代码生成机制，确保代码质量
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class CodeGeneratorAgent:
    """代码生成Agent
    
    参考 ReCode 的递归代码生成机制
    """
    
    def __init__(self, llm_client=None, max_iterations: int = 3):
        """初始化代码生成Agent
        
        Args:
            llm_client: LLM客户端（可选）
            max_iterations: 最大迭代次数（递归优化）
        """
        self.llm_client = llm_client
        self.max_iterations = max_iterations
    
    def execute(self, task: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行代码生成任务
        
        Args:
            task: 任务对象
            context: 上下文信息（包含架构设计等）
            
        Returns:
            生成的代码和元数据
        """
        logger.info(f"Code Generator Agent executing: {task.description}")
        
        # 获取架构设计
        architecture = context.get("arch_001", {}).get("architecture", {})
        
        # 递归生成代码
        result = self.generate_code(
            architecture=architecture,
            module_name=self._extract_module_name(task),
            iteration=0
        )
        
        return result
    
    def generate_code(
        self,
        architecture: Dict[str, Any],
        module_name: str,
        iteration: int = 0
    ) -> Dict[str, Any]:
        """递归生成代码
        
        Args:
            architecture: 架构设计
            module_name: 模块名称
            iteration: 当前迭代次数
            
        Returns:
            生成的代码和元数据
        """
        if iteration >= self.max_iterations:
            raise ValueError(f"Max iterations ({self.max_iterations}) reached")
        
        logger.info(f"Generating code for {module_name} (iteration {iteration + 1})")
        
        # 1. 生成代码
        code = self._generate_code(architecture, module_name)
        
        # 2. 自检
        issues = self._self_check(code, architecture)
        
        # 3. 如果有问题，递归修复
        if issues:
            logger.info(f"Iteration {iteration + 1}: Found {len(issues)} issues")
            fixed_code = self._fix_issues(code, issues)
            return self.generate_code(
                architecture,
                module_name,
                iteration + 1
            )
        
        # 4. 生成测试
        tests = self._generate_tests(code, module_name)
        
        return {
            "code": code,
            "tests": tests,
            "iteration": iteration + 1,
            "quality_score": self._calculate_quality_score(code),
            "issues": []
        }
    
    def _generate_code(self, architecture: Dict[str, Any], module_name: str) -> str:
        """生成代码"""
        if self.llm_client:
            prompt = self._build_prompt(architecture, module_name)
            return self.llm_client.generate(prompt)
        else:
            # 返回示例代码
            return self._generate_example_code(module_name)
    
    def _build_prompt(self, architecture: Dict[str, Any], module_name: str) -> str:
        """构建生成代码的Prompt"""
        return f"""
你是TRQuant系统的代码生成专家，负责实现BulletTrade模块。

## 架构设计
{architecture}

## 模块名称
{module_name}

## 实现要求
1. **代码规范**：
   - 严格遵循PEP 8
   - 所有函数必须有类型注解
   - 所有公共函数必须有docstring（Google风格）
   - 行长度不超过100字符

2. **质量要求**：
   - 单一职责原则
   - 函数长度不超过50行
   - 完整的错误处理
   - 避免使用any类型（TypeScript）

3. **测试要求**：
   - 为每个公共函数生成单元测试
   - 测试覆盖率目标>80%

请生成完整的Python代码。
"""
    
    def _self_check(self, code: str, architecture: Dict[str, Any]) -> List[str]:
        """自检代码质量"""
        issues = []
        
        # 检查类型注解
        if not self._has_type_hints(code):
            issues.append("缺少类型注解")
        
        # 检查文档字符串
        if not self._has_docstrings(code):
            issues.append("缺少文档字符串")
        
        # 检查规范
        if not self._check_style(code):
            issues.append("代码风格不符合规范")
        
        return issues
    
    def _has_type_hints(self, code: str) -> bool:
        """检查是否有类型注解"""
        # 简单检查：是否包含类型注解的关键字
        return "->" in code or ": " in code
    
    def _has_docstrings(self, code: str) -> bool:
        """检查是否有文档字符串"""
        return '"""' in code or "'''" in code
    
    def _check_style(self, code: str) -> bool:
        """检查代码风格"""
        # 简单检查：行长度
        lines = code.split("\n")
        long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 100]
        return len(long_lines) == 0
    
    def _fix_issues(self, code: str, issues: List[str]) -> str:
        """修复问题"""
        if self.llm_client:
            fix_prompt = f"""
修复以下代码问题：
{chr(10).join(issues)}

代码：
```python
{code}
```

修复要求：
1. 保持原有功能不变
2. 修复所有问题
3. 遵循代码规范
"""
            return self.llm_client.generate(fix_prompt)
        else:
            # 简单修复：添加类型注解和文档字符串
            return self._simple_fix(code, issues)
    
    def _simple_fix(self, code: str, issues: List[str]) -> str:
        """简单修复（用于测试）"""
        # 这里可以实现简单的自动修复逻辑
        return code
    
    def _generate_tests(self, code: str, module_name: str) -> str:
        """生成测试代码"""
        if self.llm_client:
            test_prompt = f"""
为以下代码生成单元测试：

```python
{code}
```

要求：
1. 使用pytest框架
2. 测试所有公共函数
3. 包含边界条件测试
4. 包含异常情况测试
"""
            return self.llm_client.generate(test_prompt)
        else:
            return f"# Tests for {module_name}\n# TODO: Implement tests"
    
    def _calculate_quality_score(self, code: str) -> float:
        """计算质量分数（0-100）"""
        score = 100.0
        
        # 检查类型注解
        if not self._has_type_hints(code):
            score -= 20
        
        # 检查文档字符串
        if not self._has_docstrings(code):
            score -= 20
        
        # 检查代码风格
        if not self._check_style(code):
            score -= 10
        
        return max(0.0, score)
    
    def _extract_module_name(self, task: Any) -> str:
        """从任务中提取模块名称"""
        description = task.description
        # 简单提取：查找"实现"或"生成"后面的模块名
        if "实现" in description:
            parts = description.split("实现")
            if len(parts) > 1:
                return parts[1].strip()
        return "unknown_module"
    
    def _generate_example_code(self, module_name: str) -> str:
        """生成示例代码（用于测试）"""
        return f'''"""{module_name}模块

示例代码生成
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class {module_name.title().replace("_", "")}:
    """{module_name}类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """初始化
        
        Args:
            config: 配置字典
        """
        self.config = config or {{}}
        logger.info(f"Initialized {{self.__class__.__name__}}")
    
    def process(self) -> Dict[str, Any]:
        """处理
        
        Returns:
            处理结果
        """
        return {{"status": "success"}}
'''

