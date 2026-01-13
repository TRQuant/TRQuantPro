# -*- coding: utf-8 -*-
"""
QMT Strategy Templates
======================

Provides standard templates for QMT strategy development.

Templates:
- backtest_basic.py: Basic backtest template
- backtest_factor.py: Multi-factor backtest template
- live_basic.py: Basic live trading template
"""

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent


def get_template(name: str) -> str:
    """Get template content by name"""
    template_path = TEMPLATES_DIR / f"{name}.py"
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    raise FileNotFoundError(f"Template not found: {name}")


def list_templates() -> list:
    """List available templates"""
    return [f.stem for f in TEMPLATES_DIR.glob("*.py") if f.stem != "__init__"]
