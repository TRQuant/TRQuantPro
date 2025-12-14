"""
文件名: code_1_9_upload_backtest_report.py
保存路径: code_library/001_Chapter1_System_Overview/1.9/code_1_9_upload_backtest_report.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.9_Database_Architecture_CN.md
提取时间: 2025-12-13 20:18:07
函数/类名: upload_backtest_report

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from minio import Minio
from minio.error import S3Error

# 初始化MinIO客户端
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# 上传回测报告
def upload_backtest_report(backtest_id: int, report_path: str):
    bucket_name = "backtest-reports"
    object_name = f"{backtest_id}/report.html"
    
    client.fput_object(
        bucket_name,
        object_name,
        report_path
    )
    
    # 保存元数据到PostgreSQL
    # ...

# 下载回测报告
def download_backtest_report(backtest_id: int, save_path: str):
    bucket_name = "backtest-reports"
    object_name = f"{backtest_id}/report.html"
    
    client.fget_object(
        bucket_name,
        object_name,
        save_path
    )