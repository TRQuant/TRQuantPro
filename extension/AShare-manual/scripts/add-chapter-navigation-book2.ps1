# 第二册章节导航批量添加脚本
# 为第二册所有章节添加章节导航功能

$book2Path = "src/pages/book2"

# 定义章节结构
$chapters = @{
    "201_Chapter1" = @{
        "1.1" = @("1.1.1 宏观趋势影响投资收益的理论基础", "1.1.2 实证数据：宏观趋势的决定性影响", "1.1.3 宏观因素的影响权重分析")
        "1.2" = @("1.2.1 市场环境的分类与特征", "1.2.2 不同市场环境下的投资策略", "1.2.3 市场环境转换的识别与应对", "1.2.4 实战案例：市场环境识别与投资策略")
        "1.3" = @("1.3.1 沃伦·巴菲特：价值投资的趋势大师", "1.3.2 乔治·索罗斯：反身性理论的趋势大师", "1.3.3 瑞·达里奥：债务周期的宏观趋势大师")
        "1.4" = @("1.4.1 趋势分析框架构建", "1.4.2 多维度趋势判断方法", "1.4.3 趋势跟踪与调整机制")
        "1.5" = @("1.5.1 实时趋势追踪工具", "1.5.2 趋势变化预警系统", "1.5.3 投资策略动态调整")
    }
    "202_Chapter2" = @{
        "2.1" = @("2.1.1 经济周期基本理论", "2.1.2 周期识别指标体系", "2.1.3 周期阶段识别方法")
        "2.2" = @("2.2.1 扩张期市场特征", "2.2.2 顶峰期市场特征", "2.2.3 收缩期市场特征", "2.2.4 谷底期市场特征")
        "2.3" = @("2.3.1 周期驱动投资策略", "2.3.2 行业轮动策略", "2.3.3 资产配置调整", "2.3.4 风险管理机制")
        "2.4" = @("2.4.1 周期跟踪工具", "2.4.2 实时数据监控", "2.4.3 策略调整决策")
    }
    "203_Chapter3" = @{
        "3.1" = @("3.1.1 货币政策理论基础", "3.1.2 货币政策传导机制", "3.1.3 政策效果评估方法")
        "3.2" = @("3.2.1 美联储政策框架", "3.2.2 欧洲央行政策框架", "3.2.3 其他主要央行政策框架")
        "3.3" = @("3.3.1 利率传导路径", "3.3.2 信贷传导路径", "3.3.3 资产价格传导路径", "3.3.4 汇率传导路径")
        "3.4" = @("3.4.1 政策变化市场反应", "3.4.2 投资策略调整", "3.4.3 风险管理措施")
        "3.5" = @("3.5.1 政策跟踪工具", "3.5.2 决策支持系统", "3.5.3 实时监控机制")
    }
    "204_Chapter4" = @{
        "4.1" = @("4.1.1 财政政策理论基础", "4.1.2 财政政策类型分析", "4.1.3 政策效果评估框架")
        "4.2" = @("4.2.1 政府支出市场影响", "4.2.2 税收政策市场反应", "4.2.3 财政赤字影响分析")
        "4.3" = @("4.3.1 税收政策投资影响", "4.3.2 企业税负分析", "4.3.3 个人税收政策影响")
        "4.4" = @("4.4.1 财政政策跟踪", "4.4.2 投资策略调整", "4.4.3 风险控制措施")
    }
    "205_Chapter5" = @{
        "5.1" = @("5.1.1 美国经济分析", "5.1.2 欧洲经济分析", "5.1.3 中国经济分析", "5.1.4 其他主要经济体分析")
        "5.2" = @("5.2.1 汇率影响因素", "5.2.2 汇率投资影响", "5.2.3 汇率风险管理")
        "5.3" = @("5.3.1 国际资本流动", "5.3.2 全球资产配置", "5.3.3 跨境投资策略")
        "5.4" = @("5.4.1 全球宏观跟踪", "5.4.2 投资策略调整", "5.4.3 风险控制机制")
    }
    "206_Chapter6" = @{
        "6.1" = @("6.1.1 核心经济指标", "6.1.2 就业市场指标", "6.1.3 通胀指标分析", "6.1.4 消费指标解读")
        "6.2" = @("6.2.1 领先指标构建", "6.2.2 预测模型开发", "6.2.3 预警系统设计")
        "6.3" = @("6.3.1 数据发布影响", "6.3.2 市场反应分析", "6.3.3 投资策略调整")
        "6.4" = @("6.4.1 指标监控系统", "6.4.2 实时分析工具", "6.4.3 决策支持平台")
    }
    "207_Chapter7" = @{
        "7.1" = @("7.1.1 系统性风险识别", "7.1.2 风险传导机制", "7.1.3 风险预警指标")
        "7.2" = @("7.2.1 宏观风险指标", "7.2.2 市场风险指标", "7.2.3 流动性风险指标")
        "7.3" = @("7.3.1 风险监控系统", "7.3.2 预警机制设计", "7.3.3 应对策略制定")
        "7.4" = @("7.4.1 风险跟踪工具", "7.4.2 实时监控平台", "7.4.3 决策支持系统")
    }
    "208_Chapter8" = @{
        "8.1" = @("8.1.1 风险指标设计", "8.1.2 指标体系构建", "8.1.3 权重分配方法")
        "8.2" = @("8.2.1 实时监控技术", "8.2.2 数据采集处理", "8.2.3 预警信号生成")
        "8.3" = @("8.3.1 预警系统构建", "8.3.2 响应机制设计", "8.3.3 应急预案制定")
        "8.4" = @("8.4.1 系统集成部署", "8.4.2 性能优化", "8.4.3 维护更新")
    }
    "209_Chapter9" = @{
        "9.1" = @("9.1.1 战略资产配置", "9.1.2 配置框架设计", "9.1.3 优化方法选择")
        "9.2" = @("9.2.1 宏观环境分析", "9.2.2 配置策略制定", "9.2.3 执行监控机制")
        "9.3" = @("9.3.1 战术调整方法", "9.3.2 调整时机判断", "9.3.3 风险管理措施")
        "9.4" = @("9.4.1 配置跟踪工具", "9.4.2 调整决策支持", "9.4.3 绩效评估系统")
    }
    "210_Chapter10" = @{
        "10.1" = @("10.1.1 择时理论基础", "10.1.2 市场效率分析", "10.1.3 择时可行性评估")
        "10.2" = @("10.2.1 宏观择时信号", "10.2.2 技术择时信号", "10.2.3 综合信号判断")
        "10.3" = @("10.3.1 择时策略设计", "10.3.2 执行优化方法", "10.3.3 风险控制机制")
        "10.4" = @("10.4.1 择时跟踪工具", "10.4.2 策略评估系统", "10.4.3 持续优化机制")
    }
    "211_Chapter11" = @{
        "11.1" = @("11.1.1 数据获取管理", "11.1.2 数据质量保证", "11.1.3 数据存储系统")
        "11.2" = @("11.2.1 分析框架设计", "11.2.2 方法论选择", "11.2.3 工具链构建")
        "11.3" = @("11.3.1 模型构建方法", "11.3.2 验证测试流程", "11.3.3 部署维护机制")
        "11.4" = @("11.4.1 系统集成部署", "11.4.2 性能监控", "11.4.3 持续改进")
    }
}

# 导航脚本模板
$navigationScript = @"
<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const targetPosition = element.offsetTop + 88;
    
    window.scrollTo({
      top: Math.max(0, targetPosition),
      behavior: 'smooth'
    });
  }
}
</script>

<style>
.chapter-overview .overview-item {
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  cursor: pointer;
}

.chapter-overview .overview-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.chapter-overview .overview-item h4 {
  margin: 0 0 8px 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.chapter-overview .overview-item p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .chapter-overview {
    grid-template-columns: 1fr;
  }
  
  .chapter-overview .overview-item {
    padding: 12px;
  }
  
  .chapter-overview .overview-item h4 {
    font-size: 1rem;
  }
}
</style>
"@

# 处理每个章节
foreach ($chapterDir in $chapters.Keys) {
    $chapterPath = Join-Path $book2Path $chapterDir
    
    if (Test-Path $chapterPath) {
        Write-Host "处理章节: $chapterDir"
        
        foreach ($section in $chapters[$chapterDir].Keys) {
            $sectionFiles = Get-ChildItem -Path $chapterPath -Filter "*$section*" -File
            
            foreach ($file in $sectionFiles) {
                if ($file.Name -match "\.md$" -and -not $file.Name.Contains("backup")) {
                    Write-Host "  处理文件: $($file.Name)"
                    
                    $content = Get-Content $file.FullName -Raw -Encoding UTF8
                    
                    # 检查是否已有导航脚本
                    if ($content -notmatch "function scrollToSection") {
                        # 查找章节概览部分
                        if ($content -match "## 📋 章节概览") {
                            # 添加导航脚本和样式
                            $content = $content -replace "## 📋 章节概览", "## 📋 章节概览`n`n$navigationScript"
                            
                            # 为章节概览项添加点击事件
                            $sectionNumber = $section -replace "\.", "-"
                            $content = $content -replace '<div class="overview-item">', "<div class=`"overview-item`" onclick=`"scrollToSection('section-$sectionNumber-1')`" style=`"cursor: pointer;`">"
                            
                            # 为章节标题添加ID
                            foreach ($subsection in $chapters[$chapterDir][$section]) {
                                $subsectionNumber = $subsection -replace "\.", "-"
                                $subsectionId = "section-$subsectionNumber"
                                $content = $content -replace "## $subsection", "<h2 id=`"$subsectionId`">$subsection</h2>"
                            }
                            
                            # 保存文件
                            Set-Content -Path $file.FullName -Value $content -Encoding UTF8
                            Write-Host "    ✓ 已添加导航功能"
                        }
                    } else {
                        Write-Host "    - 已有导航功能，跳过"
                    }
                }
            }
        }
    }
}

Write-Host "第二册章节导航功能添加完成！" 