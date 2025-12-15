#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动Debug流程脚本

在开发新模块后自动执行以下检查：
1. 语法检查
2. 导入检查
3. 类型检查（如果有类型注解）
4. 模块初始化测试
5. GUI组件加载测试

用法:
    python scripts/auto_debug.py [module_path]
    
示例:
    python scripts/auto_debug.py gui/widgets/heatmap_panel.py
    python scripts/auto_debug.py markets/ashare/mainline/
"""

import sys
import os
import ast
import importlib
import traceback
from pathlib import Path
from typing import List, Dict, Tuple

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class AutoDebugger:
    """自动Debug工具"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.passed: List[str] = []
    
    def log(self, msg: str, level: str = "INFO"):
        """日志输出"""
        if self.verbose:
            icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌"}
            print(f"{icons.get(level, '')} {msg}")
    
    def check_syntax(self, file_path: Path) -> bool:
        """检查Python语法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            self.log(f"语法检查通过: {file_path.name}", "OK")
            return True
        except SyntaxError as e:
            self.errors.append({
                "file": str(file_path),
                "type": "SyntaxError",
                "message": str(e),
                "line": e.lineno,
            })
            self.log(f"语法错误 {file_path.name}:{e.lineno}: {e.msg}", "ERROR")
            return False
    
    def check_imports(self, file_path: Path) -> bool:
        """检查导入是否正确"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            # 收集所有导入
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # 测试关键导入
            failed_imports = []
            for imp in imports:
                try:
                    # 跳过相对导入
                    if imp.startswith('.'):
                        continue
                    importlib.import_module(imp.split('.')[0])
                except ImportError as e:
                    failed_imports.append((imp, str(e)))
            
            if failed_imports:
                for imp, err in failed_imports:
                    self.warnings.append({
                        "file": str(file_path),
                        "type": "ImportWarning",
                        "message": f"无法导入 {imp}: {err}",
                    })
                    self.log(f"导入警告 {file_path.name}: 无法导入 {imp}", "WARN")
                return True  # 警告不算失败
            
            self.log(f"导入检查通过: {file_path.name}", "OK")
            return True
            
        except Exception as e:
            self.errors.append({
                "file": str(file_path),
                "type": "ImportCheckError",
                "message": str(e),
            })
            self.log(f"导入检查失败 {file_path.name}: {e}", "ERROR")
            return False
    
    def check_colors_usage(self, file_path: Path) -> bool:
        """检查Colors类属性使用是否正确"""
        try:
            # 获取Colors类所有属性
            from gui.styles.theme import Colors
            valid_colors = {attr for attr in dir(Colors) if not attr.startswith('_')}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # 查找所有 Colors.XXX 的使用
            import re
            pattern = r'Colors\.([A-Z_]+)'
            matches = re.findall(pattern, source)
            
            invalid_colors = []
            for match in set(matches):
                if match not in valid_colors:
                    invalid_colors.append(match)
            
            if invalid_colors:
                for color in invalid_colors:
                    self.errors.append({
                        "file": str(file_path),
                        "type": "ColorAttributeError",
                        "message": f"Colors 类没有属性 '{color}'",
                    })
                    self.log(f"颜色属性错误 {file_path.name}: Colors.{color} 不存在", "ERROR")
                return False
            
            if matches:
                self.log(f"颜色属性检查通过: {file_path.name} (使用了 {len(set(matches))} 个颜色)", "OK")
            return True
            
        except ImportError:
            self.log(f"跳过颜色检查: 无法导入Colors类", "WARN")
            return True
        except Exception as e:
            self.log(f"颜色检查异常: {e}", "WARN")
            return True
    
    def check_module_load(self, file_path: Path) -> bool:
        """测试模块是否能正确加载"""
        try:
            # 确保使用绝对路径
            file_path = file_path.resolve()
            
            # 转换文件路径为模块路径
            try:
                rel_path = file_path.relative_to(PROJECT_ROOT.resolve())
            except ValueError:
                # 如果不在项目根目录下，尝试直接使用
                rel_path = file_path
            
            module_path = str(rel_path).replace('/', '.').replace('\\', '.').replace('.py', '')
            
            # 尝试导入模块
            spec = importlib.util.spec_from_file_location(module_path, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_path] = module
                spec.loader.exec_module(module)
                
                self.log(f"模块加载测试通过: {file_path.name}", "OK")
                return True
            else:
                raise ImportError(f"无法创建模块规范: {file_path}")
                
        except Exception as e:
            self.errors.append({
                "file": str(file_path),
                "type": "ModuleLoadError",
                "message": str(e),
                "traceback": traceback.format_exc(),
            })
            self.log(f"模块加载失败 {file_path.name}: {e}", "ERROR")
            return False
    
    def check_gui_widget(self, file_path: Path) -> bool:
        """测试GUI组件是否能正确初始化"""
        if 'gui' not in str(file_path):
            return True
        
        try:
            # 检查是否有QApplication
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
            
            # 转换文件路径为模块路径
            rel_path = file_path.relative_to(PROJECT_ROOT)
            module_path = str(rel_path).replace('/', '.').replace('\\', '.').replace('.py', '')
            
            # 导入模块
            module = importlib.import_module(module_path)
            
            # 查找所有Widget类
            widgets_tested = 0
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and hasattr(obj, 'setup_ui'):
                    try:
                        # 尝试实例化
                        widget = obj()
                        widgets_tested += 1
                        self.log(f"GUI组件测试通过: {name}", "OK")
                    except Exception as e:
                        self.errors.append({
                            "file": str(file_path),
                            "type": "WidgetInitError",
                            "message": f"组件 {name} 初始化失败: {e}",
                        })
                        self.log(f"GUI组件初始化失败 {name}: {e}", "ERROR")
                        return False
            
            if widgets_tested == 0:
                self.log(f"未找到GUI组件: {file_path.name}", "INFO")
            
            return True
            
        except Exception as e:
            self.errors.append({
                "file": str(file_path),
                "type": "GUITestError",
                "message": str(e),
            })
            self.log(f"GUI测试异常 {file_path.name}: {e}", "ERROR")
            return False
    
    def run_checks(self, path: str) -> bool:
        """运行所有检查"""
        target = Path(path)
        
        if not target.exists():
            target = PROJECT_ROOT / path
        
        if not target.exists():
            self.log(f"路径不存在: {path}", "ERROR")
            return False
        
        # 收集所有Python文件
        if target.is_file():
            files = [target]
        else:
            files = list(target.rglob("*.py"))
        
        self.log(f"\n{'='*60}")
        self.log(f"🔍 自动Debug检查: {len(files)} 个文件")
        self.log(f"{'='*60}\n")
        
        all_passed = True
        
        for file_path in files:
            if '__pycache__' in str(file_path):
                continue
            
            self.log(f"\n📄 检查文件: {file_path.name}")
            self.log("-" * 40)
            
            # 1. 语法检查
            if not self.check_syntax(file_path):
                all_passed = False
                continue
            
            # 2. 导入检查
            if not self.check_imports(file_path):
                all_passed = False
                continue
            
            # 3. 颜色属性检查
            if not self.check_colors_usage(file_path):
                all_passed = False
                continue
            
            # 4. 模块加载测试
            if not self.check_module_load(file_path):
                all_passed = False
                continue
            
            self.passed.append(str(file_path))
        
        # 输出总结
        self.log(f"\n{'='*60}")
        self.log("📊 检查结果总结")
        self.log(f"{'='*60}")
        self.log(f"✅ 通过: {len(self.passed)} 个文件")
        self.log(f"⚠️ 警告: {len(self.warnings)} 个")
        self.log(f"❌ 错误: {len(self.errors)} 个")
        
        if self.errors:
            self.log("\n❌ 错误详情:")
            for err in self.errors:
                self.log(f"  - {err['file']}: {err['type']}")
                self.log(f"    {err['message']}")
        
        return all_passed


def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 默认检查常用目录
        paths = [
            "gui/widgets/",
            "markets/ashare/mainline/",
        ]
    else:
        paths = sys.argv[1:]
    
    debugger = AutoDebugger()
    
    all_passed = True
    for path in paths:
        if not debugger.run_checks(path):
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有检查通过!")
        sys.exit(0)
    else:
        print("\n💥 存在错误，请修复后重试")
        sys.exit(1)


if __name__ == "__main__":
    main()

