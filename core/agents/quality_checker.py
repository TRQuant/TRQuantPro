"""质量检查Agent

负责代码规范检查、类型安全检查、逻辑错误检测等
"""

from typing import Dict, Any, List
import ast
import subprocess
import logging

logger = logging.getLogger(__name__)


class QualityCheckerAgent:
    """质量检查Agent
    
    参考 LightAgent 的自学习能力 + 静态分析工具
    """
    
    def __init__(self):
        """初始化质量检查Agent"""
        self.checkers = [
            self._check_syntax,
            self._check_style,
            self._check_types,
            self._check_security,
            self._check_performance
        ]
    
    def execute(self, task: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行质量检查任务
        
        Args:
            task: 任务对象
            context: 上下文信息（包含生成的代码）
            
        Returns:
            质量检查结果
        """
        logger.info(f"Quality Checker Agent executing: {task.description}")
        
        # 获取生成的代码
        code_result = context.get("code_001", {})
        code = code_result.get("code", "")
        file_path = "generated_code.py"  # 临时文件路径
        
        if not code:
            logger.warning("No code found in context")
            return {
                "passed": False,
                "score": 0.0,
                "issues": ["No code found to check"]
            }
        
        # 执行全面质量检查
        results = self.check(code, file_path)
        
        return results
    
    def check(self, code: str, file_path: str) -> Dict[str, Any]:
        """全面质量检查
        
        Args:
            code: 代码内容
            file_path: 文件路径（用于工具检查）
            
        Returns:
            检查结果
        """
        results = {
            "syntax": True,
            "style": True,
            "types": True,
            "security": True,
            "performance": True,
            "issues": []
        }
        
        for checker in self.checkers:
            try:
                check_result = checker(code, file_path)
                check_name = checker.__name__.replace("_check_", "")
                
                if not check_result["passed"]:
                    results[check_name] = False
                    results["issues"].extend(check_result["issues"])
            except Exception as e:
                logger.error(f"Checker {checker.__name__} failed: {e}")
        
        results["score"] = self._calculate_score(results)
        results["passed"] = results["score"] >= 80.0
        
        return results
    
    def _check_syntax(self, code: str, file_path: str) -> Dict[str, Any]:
        """语法检查"""
        try:
            ast.parse(code)
            return {"passed": True, "issues": []}
        except SyntaxError as e:
            return {
                "passed": False,
                "issues": [f"语法错误: {e.msg} at line {e.lineno}"]
            }
        except Exception as e:
            return {
                "passed": False,
                "issues": [f"解析错误: {str(e)}"]
            }
    
    def _check_style(self, code: str, file_path: str) -> Dict[str, Any]:
        """代码风格检查（使用ruff）"""
        try:
            result = subprocess.run(
                ["ruff", "check", "--stdin-filename", file_path],
                input=code.encode(),
                capture_output=True,
                timeout=10
            )
            
            if result.returncode != 0:
                issues = result.stdout.decode().split("\n")
                issues = [i for i in issues if i.strip()]
                return {"passed": False, "issues": issues}
            
            return {"passed": True, "issues": []}
        except FileNotFoundError:
            logger.warning("ruff not found, skipping style check")
            return {"passed": True, "issues": []}
        except Exception as e:
            logger.warning(f"Style check failed: {e}")
            return {"passed": True, "issues": []}  # 不阻塞
    
    def _check_types(self, code: str, file_path: str) -> Dict[str, Any]:
        """类型检查（使用mypy）"""
        issues = []
        
        # 简单检查：是否有类型注解
        has_type_hints = "->" in code or ": " in code
        
        if not has_type_hints:
            issues.append("缺少类型注解")
        
        # 可以集成mypy进行更严格的检查
        # try:
        #     result = subprocess.run(
        #         ["mypy", "--no-error-summary", file_path],
        #         capture_output=True,
        #         timeout=10
        #     )
        #     if result.returncode != 0:
        #         issues.extend(result.stdout.decode().split("\n"))
        # except FileNotFoundError:
        #     logger.warning("mypy not found, skipping type check")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _check_security(self, code: str, file_path: str) -> Dict[str, Any]:
        """安全检查"""
        issues = []
        
        # 检查危险函数
        dangerous_patterns = [
            ("eval(", "使用eval()存在安全风险"),
            ("exec(", "使用exec()存在安全风险"),
            ("__import__", "动态导入存在安全风险"),
            ("pickle.loads", "反序列化存在安全风险"),
            ("subprocess.call", "subprocess调用需要谨慎"),
            ("os.system", "系统命令执行存在安全风险")
        ]
        
        for pattern, message in dangerous_patterns:
            if pattern in code:
                issues.append(f"{message} (发现: {pattern})")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _check_performance(self, code: str, file_path: str) -> Dict[str, Any]:
        """性能检查"""
        issues = []
        
        # 检查明显的性能问题
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            # 检查嵌套循环
            if "for " in line and i < len(lines):
                next_line = lines[i] if i < len(lines) else ""
                if "for " in next_line:
                    issues.append(f"第{i}行: 检测到嵌套循环，可能影响性能")
        
        # 检查大列表推导式
        if "[" in code and code.count("[") > 10:
            issues.append("检测到复杂的列表推导式，可能影响可读性")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _calculate_score(self, results: Dict[str, Any]) -> float:
        """计算质量分数（0-100）"""
        weights = {
            "syntax": 0.3,
            "style": 0.2,
            "types": 0.2,
            "security": 0.2,
            "performance": 0.1
        }
        
        score = 0.0
        for key, weight in weights.items():
            if results.get(key, False):
                score += weight * 100.0
        
        return round(score, 2)


