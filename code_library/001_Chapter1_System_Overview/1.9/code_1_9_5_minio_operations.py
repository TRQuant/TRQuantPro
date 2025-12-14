"""
MinIO/S3对象存储操作函数

设计原理：
1. 使用MinIO客户端进行对象存储操作
2. 支持上传、下载、删除等基本操作
3. 元数据存储在PostgreSQL，文件存储在MinIO/S3
4. 实现版本管理和访问控制

为什么这样设计：
1. 分离存储：大文件存储在对象存储，降低数据库压力
2. 成本优化：对象存储成本低于数据库存储
3. 可扩展性：对象存储支持水平扩展
4. 版本管理：支持对象版本控制，便于追溯

使用场景：
- 回测报告存储（HTML/PDF格式）
- 研究文档存储（Markdown/PDF格式）
- 图表文件存储（PNG/JPEG格式）
- 策略代码快照存储

注意事项：
- 需要配置MinIO/S3访问凭证
- 注意文件大小限制
- 定期清理过期文件
"""

from minio import Minio
from minio.error import S3Error
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def init_minio_client(
    endpoint: str,
    access_key: str,
    secret_key: str,
    secure: bool = False
) -> Minio:
    """
    初始化MinIO客户端
    
    设计原理：
    - 使用MinIO Python客户端库
    - 支持HTTP和HTTPS连接
    - 配置访问凭证和端点
    
    Args:
        endpoint: MinIO服务器地址（格式：host:port）
        access_key: 访问密钥
        secret_key: 秘密密钥
        secure: 是否使用HTTPS（默认False）
    
    Returns:
        MinIO客户端实例
    """
    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )
    return client


def upload_backtest_report(
    client: Minio,
    backtest_id: int,
    report_path: str,
    bucket_name: str = "backtest-reports"
) -> str:
    """
    上传回测报告到MinIO/S3
    
    设计原理：
    - 使用fput_object方法上传文件
    - 对象路径：{backtest_id}/report.html
    - 上传后需要保存元数据到PostgreSQL
    
    Args:
        client: MinIO客户端实例
        backtest_id: 回测任务ID
        report_path: 本地报告文件路径
        bucket_name: 存储桶名称（默认：backtest-reports）
    
    Returns:
        对象名称（object_name）
    """
    object_name = f"{backtest_id}/report.html"
    
    try:
        # 确保存储桶存在
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
        
        # 上传文件
        client.fput_object(
            bucket_name,
            object_name,
            report_path
        )
        
        logger.info(f"回测报告已上传: {object_name}")
        return object_name
        
    except S3Error as e:
        logger.error(f"上传回测报告失败: {e}")
        raise


def download_backtest_report(
    client: Minio,
    backtest_id: int,
    save_path: str,
    bucket_name: str = "backtest-reports"
) -> bool:
    """
    从MinIO/S3下载回测报告
    
    设计原理：
    - 使用fget_object方法下载文件
    - 保存到指定路径
    
    Args:
        client: MinIO客户端实例
        backtest_id: 回测任务ID
        save_path: 保存路径
        bucket_name: 存储桶名称（默认：backtest-reports）
    
    Returns:
        是否下载成功
    """
    object_name = f"{backtest_id}/report.html"
    
    try:
        client.fget_object(
            bucket_name,
            object_name,
            save_path
        )
        
        logger.info(f"回测报告已下载: {save_path}")
        return True
        
    except S3Error as e:
        logger.error(f"下载回测报告失败: {e}")
        return False


def delete_backtest_report(
    client: Minio,
    backtest_id: int,
    bucket_name: str = "backtest-reports"
) -> bool:
    """
    删除MinIO/S3中的回测报告
    
    Args:
        client: MinIO客户端实例
        backtest_id: 回测任务ID
        bucket_name: 存储桶名称（默认：backtest-reports）
    
    Returns:
        是否删除成功
    """
    object_name = f"{backtest_id}/report.html"
    
    try:
        client.remove_object(bucket_name, object_name)
        logger.info(f"回测报告已删除: {object_name}")
        return True
        
    except S3Error as e:
        logger.error(f"删除回测报告失败: {e}")
        return False

