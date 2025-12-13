# JQQuant_V2 备份指南

## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`







## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`





## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`


## 概述

本项目已配置双远程仓库备份：
- **origin**: 主仓库 `https://github.com/ZhuTechLLC/JQQuant.git`
- **backup**: 备份仓库 `https://github.com/ZhuTechLLC/JQQuant_V2.git`

## 快速备份

### 方法1: 使用Python脚本（推荐）

```bash
python3 backup_to_v2.py
```

脚本会：
1. 检查git状态
2. 询问是否提交更改
3. 推送到origin仓库
4. 推送到backup仓库（JQQuant_V2）

### 方法2: 使用Shell脚本

```bash
./backup_to_v2.sh
```

### 方法3: 手动备份

```bash
# 1. 检查状态
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "你的提交信息"

# 4. 推送到origin
git push origin master

# 5. 推送到backup
git push backup master
```

## 查看远程仓库

```bash
git remote -v
```

输出示例：
```
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (fetch)
backup   https://github.com/ZhuTechLLC/JQQuant_V2.git (push)
origin   https://github.com/ZhuTechLLC/JQQuant.git (fetch)
origin   https://github.com/ZhuTechLLC/JQQuant.git (push)
```

## 配置Git凭据

如果推送时遇到认证问题，可以：

### 方法1: 使用SSH（推荐）

```bash
# 修改远程仓库URL为SSH格式
git remote set-url origin git@github.com:ZhuTechLLC/JQQuant.git
git remote set-url backup git@github.com:ZhuTechLLC/JQQuant_V2.git
```

### 方法2: 使用Personal Access Token

```bash
# 使用token推送
git push https://<token>@github.com/ZhuTechLLC/JQQuant.git master
git push https://<token>@github.com/ZhuTechLLC/JQQuant_V2.git master
```

### 方法3: 配置Git凭据存储

```bash
# 配置凭据存储
git config --global credential.helper store

# 首次推送时输入用户名和token，之后会自动保存
```

## 自动化备份

可以设置定时任务自动备份：

### Linux/Mac (cron)

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * cd /home/taotao/dev/QuantTest/TRQuant && /usr/bin/python3 backup_to_v2.py >> /tmp/jqquant_backup.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周）
4. 操作：启动程序 `python.exe backup_to_v2.py`
5. 起始于：项目目录路径

## 注意事项

1. **敏感信息**：确保 `config/jqdata_config.json` 已添加到 `.gitignore`，不会被提交
2. **大文件**：`results/*.json` 文件已被忽略，只保留HTML报告
3. **分支管理**：当前使用 `master` 分支，如需使用其他分支，请修改脚本中的分支名

## 故障排除

### 问题1: 推送失败 - 认证错误

**解决方案**：
- 检查Git凭据配置
- 使用SSH或Personal Access Token
- 确认仓库权限

### 问题2: 推送失败 - 远程仓库不存在

**解决方案**：
- 确认JQQuant_V2仓库已在GitHub创建
- 检查仓库名称和路径是否正确

### 问题3: 冲突错误

**解决方案**：
```bash
# 拉取最新代码
git pull origin master
git pull backup master

# 解决冲突后重新推送
git push origin master
git push backup master
```

## 联系支持

如有问题，请查看：
- 项目文档：`docs/ARCHITECTURE.md`
- 测试总结：`docs/TEST_SUMMARY.md`
- 项目README：`README.md`














