# 量化策略全流程工作台部署与使用指南

## 目标
- 在公司内网快速搭建“策略开发→回测→报告→协同”一体化平台；
- 让非技术同事可以通过浏览器完成策略回测、报告查看与流程协同；
- 保留研发同事在 Cursor/VS Code 中的灵活开发体验。

---

## 一、环境准备
- **服务器要求**：Linux (推荐 Ubuntu 20.04+)、8 核 CPU / 16 GB 内存 / 40 GB 磁盘；
- **已安装软件**：Docker 24+、Docker Compose Plugin；
- **账号配置**：获取聚宽等数据源 Token，并填入 `config/jqdata_config.json` 或相应环境变量。

### 目录结构
部署前确保以下目录在仓库根目录可用，用于持久化数据：
- `config/`：数据源账号、策略配置；
- `strategies/`：所有策略代码、回测结果、报告；
- `docs/`：流程文档与工作流自动更新内容；
- `logs/`：API 与工作流运行日志。

---

## 二、容器化部署流程
1. **克隆仓库并切换到项目根目录**：
   ```bash
   git clone <internal-repo-url> jqquant
   cd jqquant
   ```

2. **构建并启动容器**：
   ```bash
   docker compose up -d --build
   ```
   - `api`：FastAPI 工作流后端，监听 `9100/tcp`；
   - `frontend`：Nginx 反向代理 + React 仪表盘，映射到宿主 `8080/tcp`；
   - `worker`（可选）：同 API 镜像，默认休眠，可通过 `docker compose run worker <command>` 触发批处理任务。

3. **验证服务**：
   - 打开浏览器访问 `http://<服务器IP>:8080`；
   - 仪表盘侧边栏显示“概览 / 策略库 / 策略向导 / 投资流程 / 报告中心 / 自动化工作流 / 文档”；
   - 顶部右侧 `健康检查` 面板显示 API 状态为 `ok`。

4. **日志与排障**：
   ```bash
   docker compose logs api -f
   docker compose logs frontend -f
   ```
   如需进入容器排查：
   ```bash
   docker compose exec api /bin/bash
   ```

---

## 三、日常使用（面向非技术成员）

### 1. 策略向导：一键触发回测
1. 登录仪表盘后点击侧边栏的 `策略向导`；
2. 在“选择模板”页挑选策略（如 `月度动量轮动`、`自适应动量增强 V2`），阅读亮点；
3. 进入“配置参数”页：
   - 自动填入策略 ID、关键词、默认日期范围；
   - 可选择内置股票池或在“自定义标的”中输入代码；
   - 根据需要调整再平衡周期、动量窗口等参数；
   - 选择报告主题与需要保留的章节。
4. 在“确认执行”页检查摘要，点击 `提交工作流`；
5. 页面显示任务号后，可跳转到 `自动化工作流` 页面查看执行进度，或稍后在 `报告中心` 查看生成的 HTML 报告与指标。

### 2. 报告中心
- 列表展示所有回测记录，提供报告、指标 JSON、可视化校验告警；
- 支持按照策略、关键词筛选；
- 点击“打开报告”可直接预览 Jinja2 模板渲染的标准化报告。

### 3. 投资流程 & 文档中心
- “投资流程”页面梳理了从策略立项到实盘联动的阶段任务，并内嵌关键可视化、上线检查清单；
- “文档”页面将项目内 Markdown 文档转换为可阅读的页面，支持检索与跳转。

---

## 四、研发协作（面向技术成员）

### 1. 本地开发
- 在 Cursor/VS Code 中修改策略、回测脚本、前端页面；
- 使用 `npm run dev`、`python scripts/run_report_workflow.py ...` 完成本地验证；
- 通过 `pytest` 运行单元测试：
  ```bash
  pytest -q
  ```

### 2. 镜像与部署
- 合并代码后由 CI 构建 `api`、`frontend` 镜像并推送到内部仓库；
- 生产环境拉取最新镜像并执行 `docker compose up -d`；
- 建议配置 `staging` 环境供业务验收。

### 3. 批处理/定时任务
- 使用 `worker` 服务执行任意回测流程：
  ```bash
  docker compose run --rm worker \
    python scripts/run_report_workflow.py \
      --strategy momentum_rotation \
      --keyword qa_cycle \
      --start 2024-01-01 --end 2024-06-30 \
      --stock-pool-key high_growth_stocks
  ```
- 可结合企业级调度（Airflow / Jenkins）调用同一命令实现夜间批量回测。

#### API 触发示例
- **通用工作流接口**：
  ```bash
  curl -X POST http://<host>:9100/workflow/run \
    -H "Content-Type: application/json" \
    -d '{
      "strategy": "momentum_rotation",
      "keyword": "ops_check",
      "start": "2024-07-01",
      "end": "2024-09-30",
      "stock_pool_key": "high_growth_stocks",
      "theme": "default"
    }'
  ```
- **基于模板的快速触发**：
  ```bash
  curl -X POST http://<host>:9100/workflow/run-template \
    -H "Content-Type: application/json" \
    -d '{
      "template_id": "momentum_rotation",
      "start": "2024-07-01",
      "end": "2024-09-30",
      "keyword": "ops_template",
      "params": {"top_n": 6}
    }'
  ```
  接口会自动套用模板默认参数、推荐股票池与报告主题，支持按需覆盖关键字段。

---

## 五、权限与安全建议
- 将容器服务置于公司内网，并使用 Nginx/Ingress 与公司 SSO 集成；
- `config` 目录中的敏感凭证需通过 Vault 或 Kubernetes Secret 管理；
- 建议对“提交工作流”“上线执行”设置审批流程，风控与交易团队审核后执行。

---

## 六、问题排查速查表
| 现象 | 可能原因 | 排查步骤 |
| --- | --- | --- |
| 仪表盘访问404 | 前端未启动或构建失败 | `docker compose ps` 检查容器状态；`docker compose logs frontend` 查看日志 |
| `/api` 请求失败 | 后端未启动或端口被占用 | 检查 `api` 日志，确认 `9100` 端口监听；避免重复实例 |
| 工作流卡在 `queued` | 后端无法执行 CLI | 查看 `api` 日志中 `run_report_workflow` 输出；确认 `strategies/`、`config/` 可写 |
| 报告缺少指标 | 数据源缺失或策略无交易 | 查看生成的 `visual_validation.json`，补充数据或调整参数 |
| 回测参数缺失 | 旧版本未写入 strategy_params | 重新执行回测或手工在 metadata.json 中补充；新版已自动写入 |

---

## 七、测试与质量保障
- 安装测试依赖：`pip install -r requirements.txt`
- 运行全部单元测试：
  ```bash
  pytest
  ```
- 覆盖内容：
  - 核心统计函数 (`tests/test_trade_and_return_summary.py`)
  - 工作流模板与回测元数据接口 (`tests/test_workflow_api_templates.py`)
- 建议在合并或部署前执行 `pytest`，保证 API、模板与指标复用流程安全。
- 已配置 GitHub Actions (`.github/workflows/ci.yml`)，在 `main/master` 分支的 push / PR 上自动执行 `pytest` 与前端 `npm run build`，用于持续集成把关。

---

如需进一步支持，可在 `自动化工作流` 页面导出任务日志，或联系平台维护人员。
