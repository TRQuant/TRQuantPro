# docs目录整理报告

## 当前状态分析

### 目录大小分布
- docs/ 总大小: 209M
- docs/docs/ (重复目录): 180M
- docs/ExtentionDev/: 需检查
- docs/Ptrade_coding/: 11M
- docs/09_legacy/: 14M (包含backups: 2.6M)

### 重复目录情况

1. **docs/docs/ (180M)**
   - 完全重复的嵌套结构
   - 包含与根目录相同的子目录结构
   - **建议: 直接删除**

2. **ExtentionDev目录**
   - docs/ExtentionDev/: 37个文件
   - 02_development_guides/ExtentionDev/: 41个文件
   - 有10个相同文件名，需要对比内容
   - **建议: 对比后合并，保留02_development_guides/中的版本（文件更多）**

3. **Ptrade_coding目录**
   - docs/Ptrade_coding/: 65个文件
   - 04_platform_integration/Ptrade_coding/: 65个文件
   - 文件数相同，可能是完全重复
   - **建议: 对比后删除根目录版本**

### 根目录散乱文件
- Markdown文件: 352个
- 文本文件: 10个
- **建议: 按DOCS_ORGANIZATION_PLAN.md中的分类规则整理**

## 整理步骤

### 步骤1: 删除docs/docs/目录 ✅ 安全
```bash
rm -rf docs/docs/
```
这将释放约180M空间

### 步骤2: 处理ExtentionDev（需要确认）
由于02_development_guides/ExtentionDev/文件更多，建议：
- 对比相同文件名的文件，保留较新或较完整的版本
- 如果根目录的ExtentionDev有独特文件，移动到02_development_guides/
- 删除根目录的ExtentionDev

### 步骤3: 处理Ptrade_coding（需要确认）
由于文件数相同，建议：
- 对比文件内容确认是否完全重复
- 如果重复，删除根目录版本
- 如果有差异，合并后删除根目录版本

### 步骤4: 整理根目录文件（手动）
参考DOCS_ORGANIZATION_PLAN.md中的分类规则，将文件移动到相应目录

### 步骤5: 清理09_legacy/backups（可选）
审查backups目录，删除过时的备份文件

## 执行建议

1. **立即执行**: 删除docs/docs/目录（完全安全）
2. **需要确认**: ExtentionDev和Ptrade_coding的合并
3. **手动整理**: 根目录文件分类（工作量大，需要仔细）

