# 快速开始 - 自动提交

## 一键自动提交和推送

```bash
python3 scripts/auto_commit_push.py
```

这个脚本会：
1. ✅ 读取当前版本号（从 `VERSION` 文件）
2. ✅ 检查是否有变更
3. ✅ 自动添加所有变更
4. ✅ 提交并包含版本号
5. ✅ 推送到GitHub

## 版本号管理

版本号在 `VERSION` 文件中，当前版本：**v2.0.0**

应用启动时会自动读取版本号并显示在GUI中。

## 更多信息

详细文档请查看：`docs/AUTO_COMMIT_GUIDE.md`

