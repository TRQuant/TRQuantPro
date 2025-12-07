/**
 * 数据更新服务
 * ==============
 *
 * 提供数据源更新功能，包括聚宽认证和数据获取
 */

import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import { logger } from '../utils/logger';

const MODULE = 'DataUpdateService';

export interface DataUpdateResult {
  success: boolean;
  message: string;
  details?: string | Record<string, unknown>;
}

export class DataUpdateService {
  private static instance: DataUpdateService;
  private _pythonPath: string;

  private constructor() {
    // 尝试找到Python路径
    const config = vscode.workspace.getConfiguration('trquant');
    this._pythonPath = config.get<string>('pythonPath', 'python');
  }

  public static getInstance(): DataUpdateService {
    if (!DataUpdateService.instance) {
      DataUpdateService.instance = new DataUpdateService();
    }
    return DataUpdateService.instance;
  }

  /**
   * 更新行情数据
   */
  public async updateMarketData(): Promise<DataUpdateResult> {
    try {
      logger.info('开始更新行情数据...', MODULE);

      // 使用与桌面端一致的数据源管理器
      const result = await this.executePythonScript(`
import sys
import os
from datetime import date, datetime, timedelta

# 确保工作区路径在 sys.path 中
workspace_path = r'__WORKSPACE_PATH__'
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)

try:
    # 使用与桌面端相同的数据源管理器
    from core.data_source_manager import get_data_source_manager, DataSourceType
    
    # 获取数据源管理器（会自动初始化）
    manager = get_data_source_manager()
    print("✓ 数据源管理器已就绪")
    
    # 检查JQData权限范围
    jq_status = manager.get_source_status(DataSourceType.JQDATA)
    if jq_status and jq_status.is_available:
        print(f"✓ JQData可用: {jq_status.start_date} 至 {jq_status.end_date}")
        # 使用权限范围内的日期
        end_date = jq_status.end_date or date.today().strftime('%Y-%m-%d')
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=5)).strftime('%Y-%m-%d')
    else:
        # 默认使用最近5天
        end_date = date.today().strftime('%Y-%m-%d')
        start_date = (date.today() - timedelta(days=5)).strftime('%Y-%m-%d')
    
    print(f"✓ 查询日期范围: {start_date} 至 {end_date}")
    
    # 获取主要指数数据（与桌面端一致）
    indices = ['000001.XSHG', '399001.XSHE', '399006.XSHE', '000300.XSHG']
    updated_count = 0
    failed_count = 0
    
    for idx in indices:
        try:
            # 使用数据源管理器的统一接口
            result = manager.get_price(idx, start_date, end_date)
            if result.success and result.data is not None and not result.data.empty:
                # 保存到缓存
                manager.save_to_cache(idx, result.data)
                updated_count += 1
                print(f"✓ {idx} 已更新: {len(result.data)} 条数据 (来源: {result.source.value})")
            else:
                failed_count += 1
                print(f"✗ {idx} 更新失败: {result.error if result.error else '无数据'}")
        except Exception as e:
            failed_count += 1
            print(f"✗ 更新 {idx} 失败: {e}")
    
    print(f"\\n✓ 行情数据更新完成")
    print(f"  成功: {updated_count} 个指数")
    if failed_count > 0:
        print(f"  失败: {failed_count} 个指数")
        
except ImportError as e:
    print(f"✗ 导入模块失败: {e}")
    print("请确保已安装依赖: pip install jqdatasdk")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"✗ 更新失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
            `);

      if (result.success) {
        return {
          success: true,
          message: '行情数据更新成功',
          details: result.output,
        };
      } else {
        return {
          success: false,
          message: `行情数据更新失败: ${result.error}`,
          details: result.output,
        };
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      logger.error(`更新行情数据失败: ${errorMsg}`, MODULE);
      return {
        success: false,
        message: `更新失败: ${errorMsg}`,
      };
    }
  }

  /**
   * 更新财务数据
   */
  public async updateFinancialData(): Promise<DataUpdateResult> {
    try {
      logger.info('开始更新财务数据...', MODULE);

      const result = await this.executePythonScript(`
import sys
import os

# 确保工作区路径在 sys.path 中
workspace_path = r'__WORKSPACE_PATH__'
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)

try:
    # 使用与桌面端相同的数据源管理器
    from core.data_source_manager import get_data_source_manager
    
    # 初始化数据源管理器
    manager = get_data_source_manager()
    if not manager.initialize():
        print("✗ 数据源管理器初始化失败")
        sys.exit(1)
    
    print("✓ 数据源管理器初始化成功")
    
    # 获取JQData客户端（如果可用）
    jq_client = manager.get_jq_client()
    if not jq_client or not jq_client.is_authenticated():
        print("✗ JQData未认证，无法获取财务数据")
        print("请先测试聚宽认证")
        sys.exit(1)
    
    # 财务数据更新逻辑
    import jqdatasdk as jq
    from jqdatasdk import query, valuation, indicator
    
    # 获取所有股票代码
    stocks = jq.get_all_securities(types=['stock'], date=None)
    print(f"✓ 获取到 {len(stocks)} 只股票")
    
    # 批量获取财务数据（示例：前100只）
    stock_codes = stocks.index[:100].tolist()
    
    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
        indicator.roa
    ).filter(valuation.code.in_(stock_codes))
    
    df = jq.get_fundamentals(q, date=None)
    print(f"✓ 已更新 {len(df)} 只股票的财务数据")
    print("\\n✓ 财务数据更新完成")
        
except ImportError as e:
    print(f"✗ 导入模块失败: {e}")
    print("请确保已安装依赖: pip install jqdatasdk")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"✗ 更新失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
            `);

      if (result.success) {
        return {
          success: true,
          message: '财务数据更新成功',
          details: result.output,
        };
      } else {
        return {
          success: false,
          message: `财务数据更新失败: ${result.error}`,
          details: result.output,
        };
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      logger.error(`更新财务数据失败: ${errorMsg}`, MODULE);
      return {
        success: false,
        message: `更新失败: ${errorMsg}`,
      };
    }
  }

  /**
   * 测试聚宽认证
   */
  public async testJQAuth(): Promise<DataUpdateResult> {
    try {
      logger.info('测试聚宽认证...', MODULE);

      const result = await this.executePythonScript(`
import sys
import os

# 确保工作区路径在 sys.path 中
workspace_path = r'__WORKSPACE_PATH__'
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)

try:
    # 使用与桌面端相同的数据源管理器
    from core.data_source_manager import get_data_source_manager, DataSourceType
    
    print("=" * 50)
    print("正在初始化数据源管理器...")
    print("=" * 50)
    
    # 获取数据源管理器（会自动初始化）
    manager = get_data_source_manager()
    print("✓ 数据源管理器已就绪")
    
    # 检查各数据源状态
    print()
    print("=" * 50)
    print("数据源状态")
    print("=" * 50)
    
    all_status = manager.get_all_status()
    for source_type, status in all_status.items():
        icon = "✓" if status.is_available else "✗"
        print(f"{icon} {source_type.value}:")
        if status.is_available:
            print(f"    账户类型: {status.account_type.value}")
            if status.start_date and status.end_date:
                print(f"    数据范围: {status.start_date} 至 {status.end_date}")
            if status.is_realtime:
                print(f"    实时数据: 是")
        else:
            print(f"    错误: {status.error_message}")
    
    # 检查MongoDB
    print()
    print("=" * 50)
    print("MongoDB 连接测试")
    print("=" * 50)
    try:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
        client.server_info()
        db_names = client.list_database_names()
        print(f"✓ MongoDB 已连接")
        print(f"    数据库: {', '.join(db_names)}")
    except Exception as e:
        print(f"✗ MongoDB 连接失败: {e}")
    
    # 数据获取测试
    print()
    print("=" * 50)
    print("数据获取测试")
    print("=" * 50)
    
    jq_status = manager.get_source_status(DataSourceType.JQDATA)
    if jq_status and jq_status.is_available:
        # 使用权限范围内的日期
        from datetime import datetime, timedelta
        end_date = jq_status.end_date
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=5)).strftime('%Y-%m-%d')
        
        print(f"测试获取指数数据 ({start_date} 至 {end_date})...")
        result = manager.get_price('000001.XSHG', start_date, end_date)
        if result.success and result.data is not None and not result.data.empty:
            latest = result.data.iloc[-1]
            print(f"✓ 上证指数最新收盘价: {latest.get('close', 'N/A')}")
            print(f"    数据来源: {result.source.value}")
            print(f"    数据条数: {len(result.data)}")
        else:
            print(f"✗ 获取失败: {result.error}")
    else:
        print("⚠ JQData 不可用，跳过数据获取测试")
    
    print()
    print("=" * 50)
    print("✓ 所有测试完成")
    print("=" * 50)
        
except ImportError as e:
    print(f"✗ 导入模块失败: {e}")
    print("请确保已安装依赖: pip install jqdatasdk pymongo")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
            `);

      if (result.success) {
        return {
          success: true,
          message: '聚宽认证测试成功',
          details: result.output,
        };
      } else {
        return {
          success: false,
          message: `聚宽认证测试失败: ${result.error}`,
          details: result.output,
        };
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      logger.error(`测试聚宽认证失败: ${errorMsg}`, MODULE);
      return {
        success: false,
        message: `测试失败: ${errorMsg}`,
      };
    }
  }

  /**
   * 执行Python脚本
   */
  private async executePythonScript(
    script: string
  ): Promise<{ success: boolean; output: string; error?: string }> {
    return new Promise((resolve) => {
      const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
      const workspacePath = workspaceFolder?.uri.fsPath || '';

      if (!workspacePath) {
        resolve({
          success: false,
          output: '',
          error: '未找到工作区路径，请先打开项目文件夹',
        });
        return;
      }

      // 创建临时脚本文件
      const tempScriptPath = path.join(workspacePath, '.temp_data_update.py');

      // 替换脚本中的工作区路径占位符
      const fixedScript = script.replace(/__WORKSPACE_PATH__/g, workspacePath.replace(/\\/g, '/'));

      try {
        fs.writeFileSync(tempScriptPath, fixedScript, 'utf-8');
      } catch (e) {
        resolve({
          success: false,
          output: '',
          error: `无法创建临时脚本文件: ${e instanceof Error ? e.message : String(e)}`,
        });
        return;
      }

      // 使用 python3 或 python
      const pythonCmd = this._pythonPath || 'python3';

      const proc = cp.spawn(pythonCmd, [tempScriptPath], {
        cwd: workspacePath,
        env: {
          ...process.env,
          PYTHONUNBUFFERED: '1',
          PYTHONIOENCODING: 'utf-8',
        },
      });

      let output = '';
      let errorOutput = '';

      proc.stdout.on('data', (data: Buffer) => {
        output += data.toString('utf-8');
      });

      proc.stderr.on('data', (data: Buffer) => {
        errorOutput += data.toString('utf-8');
      });

      proc.on('close', (code: number) => {
        // 清理临时文件
        try {
          if (fs.existsSync(tempScriptPath)) {
            fs.unlinkSync(tempScriptPath);
          }
        } catch (e) {
          // 忽略清理错误
        }

        // 合并输出和错误输出
        const allOutput = output + (errorOutput ? '\n[STDERR]\n' + errorOutput : '');

        resolve({
          success: code === 0,
          output: allOutput || '无输出',
          error: code !== 0 ? errorOutput || `进程退出码: ${code}` : undefined,
        });
      });

      proc.on('error', (err: Error) => {
        // 清理临时文件
        try {
          if (fs.existsSync(tempScriptPath)) {
            fs.unlinkSync(tempScriptPath);
          }
        } catch (e) {
          // 忽略清理错误
        }

        let errorMsg = err.message;
        if (err.message.includes('ENOENT')) {
          errorMsg = `Python解释器未找到: ${pythonCmd}。请确保已安装Python并配置正确路径。`;
        }

        resolve({
          success: false,
          output: '',
          error: errorMsg,
        });
      });
    });
  }
}
