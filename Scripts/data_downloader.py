#!/usr/bin/env python3
"""
QuantConnect 数据下载器

用法:
    python data_downloader.py <symbol> [--resolution daily|hour|minute|second|tick] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]

功能:
    - 下载股票、期货、期权、加密货币等数据
    - 支持多种时间分辨率
    - 自动处理数据格式和存储
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import json


class DataDownloader:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def get_asset_type(self, symbol):
        """判断资产类型"""
        symbol = symbol.upper()
        
        # 股票
        if len(symbol) <= 5 and symbol.isalpha():
            return "equity"
        
        # ETF
        if symbol in ["SPY", "QQQ", "IWM", "VTI", "VEA", "VWO", "BND", "GLD", "SLV"]:
            return "equity"
        
        # 期货
        if any(symbol.startswith(prefix) for prefix in ["ES", "NQ", "YM", "RTY", "CL", "GC", "SI", "ZB", "ZN"]):
            return "future"
        
        # 加密货币
        if any(symbol.endswith(suffix) for suffix in ["USD", "USDT", "BTC", "ETH"]):
            return "crypto"
        
        # 外汇
        if len(symbol) == 6 and symbol[:3].isalpha() and symbol[3:].isalpha():
            return "forex"
        
        # 默认返回股票
        return "equity"
    
    def get_market(self, asset_type, symbol):
        """获取市场信息"""
        if asset_type == "equity":
            # 简单判断：如果长度<=3，可能是印度市场
            if len(symbol) <= 3:
                return "india"
            else:
                return "usa"
        elif asset_type == "future":
            return "cme"  # 默认CME
        elif asset_type == "crypto":
            return "binance"  # 默认Binance
        elif asset_type == "forex":
            return "oanda"  # 默认OANDA
        
        return "usa"
    
    def download_data(self, symbol, resolution="daily", start_date=None, end_date=None, market=None):
        """下载数据"""
        symbol = symbol.upper()
        asset_type = self.get_asset_type(symbol)
        
        if market is None:
            market = self.get_market(asset_type, symbol)
        
        print(f"📊 开始下载数据:")
        print(f"   符号: {symbol}")
        print(f"   资产类型: {asset_type}")
        print(f"   市场: {market}")
        print(f"   分辨率: {resolution}")
        
        # 构建lean data命令
        cmd = ["lean", "data", "download", "--ticker", symbol]
        
        # 添加分辨率
        if resolution != "daily":
            cmd.extend(["--resolution", resolution])
        
        # 添加日期范围
        if start_date:
            cmd.extend(["--start-date", start_date])
        if end_date:
            cmd.extend(["--end-date", end_date])
        
        # 添加市场
        if market != "usa":
            cmd.extend(["--market", market])
        
        print(f"🔄 执行命令: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ 数据下载成功")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 数据下载失败: {e}")
            print(f"错误输出: {e.stderr}")
            return False
    
    def download_multiple_symbols(self, symbols, resolution="daily", start_date=None, end_date=None):
        """批量下载多个符号的数据"""
        results = []
        
        for symbol in symbols:
            print(f"\n{'='*50}")
            print(f"正在处理: {symbol}")
            print(f"{'='*50}")
            
            success = self.download_data(symbol, resolution, start_date, end_date)
            results.append((symbol, success))
            
            # 添加延迟避免请求过快
            import time
            time.sleep(1)
        
        # 输出结果摘要
        print(f"\n{'='*50}")
        print("下载结果摘要:")
        print(f"{'='*50}")
        
        successful = [s for s, success in results if success]
        failed = [s for s, success in results if not success]
        
        print(f"✅ 成功下载: {len(successful)} 个")
        for symbol in successful:
            print(f"   - {symbol}")
        
        if failed:
            print(f"❌ 下载失败: {len(failed)} 个")
            for symbol in failed:
                print(f"   - {symbol}")
        
        return results
    
    def download_index_data(self):
        """下载主要指数数据"""
        indices = ["SPY", "QQQ", "IWM", "VTI", "VEA", "VWO", "BND", "GLD", "SLV"]
        print("📈 下载主要指数数据...")
        return self.download_multiple_symbols(indices)
    
    def download_sector_etfs(self):
        """下载行业ETF数据"""
        sector_etfs = [
            "XLK", "XLF", "XLE", "XLV", "XLI", "XLP", "XLU", "XLB", "XLRE"
        ]
        print("🏭 下载行业ETF数据...")
        return self.download_multiple_symbols(sector_etfs)
    
    def download_commodities(self):
        """下载商品数据"""
        commodities = ["GLD", "SLV", "USO", "UNG", "DBA"]
        print("🪙 下载商品数据...")
        return self.download_multiple_symbols(commodities)
    
    def download_crypto(self):
        """下载加密货币数据"""
        crypto = ["BTCUSD", "ETHUSD", "LTCUSD", "ADAUSD", "DOTUSD"]
        print("₿ 下载加密货币数据...")
        return self.download_multiple_symbols(crypto, market="binance")
    
    def check_data_availability(self, symbol, resolution="daily"):
        """检查数据可用性"""
        symbol = symbol.upper()
        asset_type = self.get_asset_type(symbol)
        market = self.get_market(asset_type, symbol)
        
        # 构建数据文件路径
        if asset_type == "equity":
            if market == "usa":
                data_path = self.data_dir / "equity" / "usa" / resolution / f"{symbol.lower()}.zip"
            else:
                data_path = self.data_dir / "equity" / market / resolution / f"{symbol.lower()}.zip"
        elif asset_type == "future":
            data_path = self.data_dir / "future" / market / resolution / f"{symbol.lower()}.zip"
        elif asset_type == "crypto":
            data_path = self.data_dir / "crypto" / market / resolution / f"{symbol.lower()}.zip"
        elif asset_type == "forex":
            data_path = self.data_dir / "forex" / market / resolution / f"{symbol.lower()}.zip"
        else:
            data_path = self.data_dir / "equity" / "usa" / resolution / f"{symbol.lower()}.zip"
        
        if data_path.exists():
            size = data_path.stat().st_size
            print(f"✅ {symbol} 数据已存在 ({size:,} bytes)")
            return True
        else:
            print(f"❌ {symbol} 数据不存在")
            return False
    
    def list_available_data(self, asset_type=None, market=None):
        """列出可用的数据"""
        print("📋 可用数据列表:")
        
        if asset_type:
            asset_dirs = [self.data_dir / asset_type]
        else:
            asset_dirs = [d for d in self.data_dir.iterdir() if d.is_dir()]
        
        for asset_dir in asset_dirs:
            if not asset_dir.exists():
                continue
                
            print(f"\n{asset_dir.name.upper()}:")
            
            for market_dir in asset_dir.iterdir():
                if not market_dir.is_dir():
                    continue
                    
                if market and market_dir.name != market:
                    continue
                    
                print(f"  {market_dir.name}:")
                
                for resolution_dir in market_dir.iterdir():
                    if not resolution_dir.is_dir():
                        continue
                        
                    files = list(resolution_dir.glob("*.zip"))
                    if files:
                        print(f"    {resolution_dir.name}: {len(files)} 个文件")
                        for file in files[:5]:  # 只显示前5个
                            size = file.stat().st_size
                            print(f"      - {file.stem} ({size:,} bytes)")
                        if len(files) > 5:
                            print(f"      ... 还有 {len(files) - 5} 个文件")


def main():
    parser = argparse.ArgumentParser(description='QuantConnect 数据下载器')
    parser.add_argument('symbols', nargs='*', help='要下载的符号列表')
    parser.add_argument('--resolution', default='daily', 
                       choices=['daily', 'hour', 'minute', 'second', 'tick'],
                       help='数据分辨率')
    parser.add_argument('--start-date', help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--market', help='市场 (usa, india, cme, binance, oanda等)')
    parser.add_argument('--check', action='store_true', help='检查数据可用性')
    parser.add_argument('--list', action='store_true', help='列出可用数据')
    parser.add_argument('--indices', action='store_true', help='下载主要指数')
    parser.add_argument('--sectors', action='store_true', help='下载行业ETF')
    parser.add_argument('--commodities', action='store_true', help='下载商品')
    parser.add_argument('--crypto', action='store_true', help='下载加密货币')
    
    args = parser.parse_args()
    
    downloader = DataDownloader()
    
    # 列出可用数据
    if args.list:
        downloader.list_available_data()
        return
    
    # 检查数据可用性
    if args.check:
        if not args.symbols:
            print("❌ 请指定要检查的符号")
            return
        
        for symbol in args.symbols:
            downloader.check_data_availability(symbol, args.resolution)
        return
    
    # 下载预设数据
    if args.indices:
        downloader.download_index_data()
        return
    
    if args.sectors:
        downloader.download_sector_etfs()
        return
    
    if args.commodities:
        downloader.download_commodities()
        return
    
    if args.crypto:
        downloader.download_crypto()
        return
    
    # 下载指定符号
    if not args.symbols:
        print("❌ 请指定要下载的符号或使用预设选项")
        print("示例:")
        print("  python data_downloader.py SPY AAPL")
        print("  python data_downloader.py --indices")
        print("  python data_downloader.py --check SPY")
        return
    
    if len(args.symbols) == 1:
        # 单个符号
        success = downloader.download_data(
            args.symbols[0], 
            args.resolution, 
            args.start_date, 
            args.end_date, 
            args.market
        )
        if success:
            print("✅ 下载完成")
        else:
            print("❌ 下载失败")
    else:
        # 多个符号
        downloader.download_multiple_symbols(
            args.symbols, 
            args.resolution, 
            args.start_date, 
            args.end_date
        )


if __name__ == "__main__":
    main() 