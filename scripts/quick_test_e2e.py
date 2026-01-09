#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证端到端测试关键功能
只测试环境检查和数据验证，不运行完整训练
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.test_advisor_v4_e2e import check_environment, run_data_validation
from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config

def main():
    print("="*70)
    print("快速验证测试")
    print("="*70)
    
    # 1. 环境检查
    print("\n[1/2] 环境检查...")
    env_ok, env_details = check_environment(full_mode=False)
    if env_ok:
        print("✅ 环境检查通过")
    else:
        print("❌ 环境检查失败")
        return 1
    
    # 2. 数据验证
    print("\n[2/2] 数据验证...")
    try:
        config = AdvisorV4Config()
        workflow = AdvisorV4Workflow(config=config, verbose=False)
        validation_ok, validation_details = run_data_validation(workflow, full_mode=False)
        if validation_ok:
            print("✅ 数据验证通过")
        else:
            print("❌ 数据验证失败")
            return 1
    except Exception as e:
        print(f"❌ 数据验证异常: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*70)
    print("✅ 快速验证通过！")
    print("="*70)
    return 0

if __name__ == '__main__':
    sys.exit(main())
