# Social Auto Upload 内容分发平台 — 改进实施方案

> **目标**：基于 `dreammis/social-auto-upload` 开源仓库，构建一款类似"蚁小二"的内容分发桌面应用。
> **核心策略**：复用上游已有 Flask + Vue 3 前后端架构，在其基础上增强和扩展，而非从零重建。
> **适用人群**：全栈开发者、独立开发者。

---

## 一、上游仓库现状分析

在开始设计之前，必须理解上游仓库**已经提供了什么**，避免重复造轮子。

### 1.1 上游已有能力

| 模块 | 文件 | 完成度 | 说明 |
|------|------|--------|------|
| **Flask 后端** | `sau_backend.py` | ✅ 完整 | REST API，端口 5409，SQLite 数据库 |
| **Vue 3 前端** | `sau_frontend/` | ✅ 完整 | Element Plus UI，Vite 构建，5 个页面 |
| **CLI 工具** | `sau_cli.py` | ✅ 完整 | `sau` 命令行接口，支持 login/upload/check |
| **平台上传器** | `uploader/` | ✅ 完整 | 抖音、快手、视频号、小红书、B站、TikTok 等 |
| **Cookie 管理** | `cookies/` | ✅ 完整 | QR码登录 + Cookie 存储/验证 |
| **浏览器自动化** | Patchright | ✅ 完整 | Playwright 反检测分支，防封号核心 |

### 1.2 上游前端已有页面

| 页面 | 路由 | 功能 |
|------|------|------|
| Dashboard | `/` | 账号统计、素材统计、最近上传记录 |
| 账号管理 | `/account-management` | 多平台账号绑定、QR码登录(SSE)、状态验证 |
| 素材管理 | `/material-management` | 拖拽上传、文件预览、素材库 |
| 发布中心 | `/publish-center` | 多平台选择、批量发布、定时发布、标签管理 |
| 关于 | `/about` | 系统信息 |

### 1.3 上游已有 API 端点

```
文件操作:  POST /uploadSave, GET /getFiles, GET /deleteFile, GET /getFile, GET /download/{path}
账号管理:  GET /getAccounts, GET /getValidAccounts, POST /account, POST /updateUserinfo, GET /deleteAccount
Cookie:    POST /uploadCookie, GET /downloadCookie
发布:      POST /postVideo, POST /postVideoBatch
登录:      GET /login?type={platform}&id={name}  (SSE 流式返回 QR码)
```

---

## 二、总体架构设计（改进版）

### 2.1 架构原则

1. **依赖引入，而非代码拷贝** — 通过 `pip install -e .` 或 git submodule 引入上游
2. **复用现有 Flask + Vue 架构** — 在其基础上扩展，不重建
3. **桌面壳作为可选层** — 核心是本地 Web 服务，Tauri/Electron 仅提供桌面化体验
4. **渐进增强** — 先让上游代码跑起来，再逐步增加功能

### 2.2 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    桌面壳层 (Tauri / Electron)               │
│    窗口管理、系统托盘、自动更新、文件系统访问                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Vue 3 Frontend (from upstream)          │    │
│  │  Element Plus + Composition API + Pinia + Axios      │    │
│  │                                                      │    │
│  │  [已有] Dashboard / 账号管理 / 素材管理 / 发布中心     │    │
│  │  [新增] 任务中心 / 发布历史 / 系统设置 / 数据分析      │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │ REST + SSE (localhost:5409)        │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │           Flask Backend (sau_backend.py)             │    │
│  │           + 扩展 API 层 (ext_api/)                   │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │   social-auto-upload (Python Package)        │    │    │
│  │  │   - uploader/ (平台上传器)                    │    │    │
│  │  │   - Patchright (反检测浏览器)                 │    │    │
│  │  │   - Cookie Manager                           │    │    │
│  │  │   - sau CLI                                  │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                                                      │    │
│  │  [新增] 任务队列 / 发布日志 / 定时调度 / 心跳检测       │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                 本地环境 (用户机器)                    │    │
│  │  - 用户真实 IP (防封号核心优势)                       │    │
│  │  - Patchright 浏览器 (Chromium，反检测)               │    │
│  │  - SQLite 数据库 (账号 + 任务 + 日志)                 │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 为什么选择"增强现有架构"而非"从零重建"

| 维度 | 原方案 (Electron+重建) | 改进方案 (增强现有) | 胜出 |
|------|----------------------|-------------------|------|
| 开发周期 | 4-5 周从零开发 | 2-3 周增量开发 | ✅ 改进 |
| 上游同步 | 拷贝代码，无法同步 | 依赖引入，git pull 即可 | ✅ 改进 |
| 核心功能 | 需要重写所有上传逻辑 | 直接复用已验证的上传器 | ✅ 改进 |
| 维护成本 | 双份代码，bug 修两次 | 单一代码源，统一维护 | ✅ 改进 |
| IP 优势 | 本机 IP，安全 | 本机 IP，安全 | 持平 |

---

## 三、技术栈选型

### 3.1 前端 UI（复用上游）

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5.x | Composition API |
| Element Plus | 2.9.x | UI 组件库（暗黑模式支持） |
| Pinia | 3.0.x | 状态管理 |
| Vue Router | 4.5.x | 路由（Hash 模式） |
| Axios | 1.9.x | HTTP 请求 |
| Vite | 6.x | 构建工具 |
| SCSS | - | 样式预处理 |

> **注意**：上游使用 Element Plus 而非 Ant Design Vue，保持一致以降低迁移成本。

### 3.2 后端服务（复用上游 + 扩展）

| 技术 | 用途 |
|------|------|
| Flask 3.x | Web 服务框架（上游已有） |
| Patchright 1.58+ | 浏览器自动化（非 Playwright，是反检测分支） |
| SQLite | 数据存储（上游已有） |
| asyncio | 任务队列和并发控制 |
| SSE (Server-Sent Events) | QR 码登录实时推送（上游已有） |

### 3.3 桌面壳（二选一）

| 方案 | 包体积 | 内存占用 | 开发语言 | 推荐度 |
|------|--------|---------|---------|--------|
| **Tauri** | ~10-20MB | ~50MB | Rust + JS | ⭐⭐⭐ |
| Electron | ~150-300MB | ~300MB | JS | ⭐⭐ |
| 无壳（纯浏览器） | 0 | 0 | - | ⭐（最简方案） |

> **推荐路径**：先以纯 Web 模式开发和调试（`python sau_backend.py` 启动后浏览器打开 `localhost:5409`），功能稳定后再加 Tauri 壳做桌面化。

### 3.4 浏览器环境（关键依赖）

```
Patchright（非 Playwright）
├── 基于 Playwright 的反检测分支
├── 自动绕过 WebDriver 检测
├── 需要独立安装浏览器二进制文件
└── 命令: patchright install chromium
```

> **打包注意事项**：Patchright 需要约 200MB 的 Chromium 二进制文件。桌面壳打包时必须内嵌或首次启动时自动下载。

---

## 四、项目目录结构（改进版）

```
social-auto-upload/                    # 上游仓库（作为基础）
├── sau_backend.py                     # ✅ 上游 Flask 后端（保留，扩展）
├── sau_cli.py                         # ✅ 上游 CLI 入口（保留）
├── sau_frontend/                      # ✅ 上游 Vue 前端（保留，扩展）
│   └── src/
│       ├── views/
│       │   ├── Dashboard.vue          # ✅ 已有
│       │   ├── AccountManagement.vue  # ✅ 已有
│       │   ├── MaterialManagement.vue # ✅ 已有
│       │   ├── PublishCenter.vue      # ✅ 已有
│       │   ├── TaskCenter.vue         # 🆕 新增：任务中心
│       │   ├── PublishHistory.vue     # 🆕 新增：发布历史
│       │   └── Settings.vue           # 🆕 新增：系统设置
│       ├── api/
│       │   ├── account.js             # ✅ 已有
│       │   ├── material.js            # ✅ 已有
│       │   ├── task.js                # 🆕 新增：任务 API
│       │   └── history.js             # 🆕 新增：历史 API
│       ├── stores/
│       │   ├── account.js             # ✅ 已有
│       │   ├── app.js                 # ✅ 已有
│       │   ├── task.js                # 🆕 新增：任务状态
│       │   └── settings.js            # 🆕 新增：设置状态
│       └── router/
│           └── index.js               # 扩展路由
├── uploader/                          # ✅ 上游平台上传器（保留，不拷贝）
│   ├── douyin_uploader/
│   ├── bilibili_uploader/
│   ├── xiaohongshu_uploader/
│   └── ks_uploader/
├── ext_api/                           # 🆕 新增：扩展 API 模块
│   ├── __init__.py
│   ├── task_queue.py                  # 任务队列管理
│   ├── publish_scheduler.py           # 定时发布调度
│   ├── heartbeat.py                   # Cookie 心跳检测
│   └── log_manager.py                 # 发布日志记录
├── cookies/                           # ✅ 上游 Cookie 存储（保留）
├── database/                          # ✅ 上游数据库（保留，扩展表结构）
│   └── social_auto_upload.db
├── tauri/                             # 🆕 新增：Tauri 桌面壳（可选）
│   ├── src/
│   └── Cargo.toml
└── docs/
    └── requirement.md                 # 本文档
```

---

## 五、核心功能模块设计

### 5.1 任务队列系统（新增）

**痛点**：上游的 `postVideoBatch` 是简单的循环调用，没有并发控制、失败重试、进度追踪。

**设计**：

```python
# ext_api/task_queue.py

import asyncio
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class PublishTask:
    id: str
    platform: str          # douyin, bilibili, xiaohongshu, ...
    account_name: str
    video_path: str
    title: str
    description: str = ""
    tags: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str = ""
    publish_url: str = ""  # 发布成功后的作品链接

class TaskQueue:
    def __init__(self, max_concurrent: int = 2):
        self.queue: asyncio.Queue[PublishTask] = asyncio.Queue()
        self.running: dict[str, PublishTask] = {}
        self.completed: list[PublishTask] = []
        self.max_concurrent = max_concurrent
        self._workers: list[asyncio.Task] = []

    async def start(self):
        """启动工作线程"""
        for i in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)

    async def _worker(self, name: str):
        while True:
            task = await self.queue.get()
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            self.running[task.id] = task

            try:
                result = await self._execute(task)
                task.status = TaskStatus.SUCCESS
                task.publish_url = result.get("url", "")
            except Exception as e:
                task.retry_count += 1
                if task.retry_count <= task.max_retries:
                    task.status = TaskStatus.RETRYING
                    await asyncio.sleep(2 ** task.retry_count)  # 指数退避
                    await self.queue.put(task)
                else:
                    task.status = TaskStatus.FAILED
                    task.error_message = str(e)
            finally:
                task.finished_at = datetime.now()
                if task.id in self.running:
                    del self.running[task.id]
                if task.status != TaskStatus.RETRYING:
                    self.completed.append(task)
                self.queue.task_done()

    async def _execute(self, task: PublishTask) -> dict:
        """调用上游 uploader 执行上传"""
        from uploader.douyin_uploader.main import DouYinVideo
        from uploader.xiaohongshu_uploader.main import XiaoHongShuVideo
        # ... 根据平台选择对应 uploader
        # 复用上游已有的上传逻辑
        pass

    async def add_task(self, task: PublishTask):
        await self.queue.put(task)

    def get_status(self) -> dict:
        return {
            "pending": self.queue.qsize(),
            "running": len(self.running),
            "completed": len(self.completed),
            "tasks_running": [
                {"id": t.id, "platform": t.platform, "account": t.account_name}
                for t in self.running.values()
            ],
        }
```

**数据库扩展**：

```sql
-- 新增任务表
CREATE TABLE IF NOT EXISTS publish_tasks (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    account_name TEXT NOT NULL,
    video_path TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    tags TEXT DEFAULT '[]',          -- JSON 数组
    status TEXT DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    error_message TEXT DEFAULT '',
    publish_url TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    finished_at TIMESTAMP
);

-- 新增发布日志表
CREATE TABLE IF NOT EXISTS publish_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    level TEXT DEFAULT 'info',       -- info, warn, error
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES publish_tasks(id)
);
```

### 5.2 Cookie 心跳检测（新增）

**设计**：应用启动时和定期（每小时）检测所有账号 Cookie 有效性。

```python
# ext_api/heartbeat.py

import asyncio
from datetime import datetime

class CookieHeartbeat:
    def __init__(self, interval_seconds: int = 3600):
        self.interval = interval_seconds
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            await self._check_all()
            await asyncio.sleep(self.interval)

    async def _check_all(self):
        """检测所有账号的 Cookie 有效性"""
        accounts = self._get_all_accounts()
        for account in accounts:
            is_valid = await self._validate(account)
            if not is_valid:
                await self._mark_expired(account)

    async def _validate(self, account) -> bool:
        """调用上游 uploader 的 Cookie 验证逻辑"""
        # 复用上游已有的 check 功能
        pass

    async def _mark_expired(self, account):
        """标记账号为失效，通知前端"""
        # 更新数据库状态
        # 通过 SSE 推送通知
        pass
```

### 5.3 扩展 API 端点（新增）

在 `sau_backend.py` 的基础上增加以下端点：

```python
# ext_api/__init__.py — 在 sau_backend.py 中 import 并注册 Blueprint

from flask import Blueprint

ext_api = Blueprint('ext_api', __name__, url_prefix='/api/v2')

# 任务管理
@ext_api.route('/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表（支持分页、状态过滤）"""
    pass

@ext_api.route('/tasks', methods=['POST'])
def create_task():
    """创建发布任务"""
    pass

@ext_api.route('/tasks/<task_id>/cancel', methods=['POST'])
def cancel_task(task_id):
    """取消任务"""
    pass

@ext_api.route('/tasks/<task_id>/retry', methods=['POST'])
def retry_task(task_id):
    """重试失败任务"""
    pass

# 任务进度（SSE）
@ext_api.route('/tasks/stream', methods=['GET'])
def task_stream():
    """SSE 实时推送任务状态变更"""
    pass

# 发布历史
@ext_api.route('/history', methods=['GET'])
def get_history():
    """发布历史记录（支持日期范围、平台、状态过滤）"""
    pass

# Cookie 心跳
@ext_api.route('/accounts/heartbeat', methods=['POST'])
def trigger_heartbeat():
    """手动触发心跳检测"""
    pass

# 统计数据
@ext_api.route('/stats', methods=['GET'])
def get_stats():
    """获取统计数据（成功率、发布量趋势等）"""
    pass

# 系统设置
@ext_api.route('/settings', methods=['GET', 'PUT'])
def settings():
    """获取/更新系统设置"""
    pass
```

### 5.4 前端新增页面

#### TaskCenter.vue — 任务中心

- 实时展示任务队列状态（待执行/执行中/已完成/失败）
- SSE 接收任务进度推送
- 支持取消、重试失败任务
- 显示每个任务的详细日志

#### PublishHistory.vue — 发布历史

- 按日期、平台、账号、状态筛选
- 展示发布成功后的作品链接（可点击跳转）
- 支持导出 CSV 报表

#### Settings.vue — 系统设置

- 发布间隔设置（防风控，默认 30-60 秒随机间隔）
- 最大并发任务数
- Cookie 心跳检测间隔
- 浏览器模式（有头/无头）
- 代理设置（可选）
- 数据目录配置

---

## 六、开发排期（改进版）

### 阶段一：环境搭建与上游复用验证（Week 1）

**目标**：让上游代码完整跑起来，验证核心链路。

| 任务 | 说明 |
|------|------|
| 克隆上游仓库 | `git clone` + 安装依赖 |
| 启动 Flask 后端 | `python sau_backend.py` → localhost:5409 |
| 启动 Vue 前端 | `cd sau_frontend && npm run dev` |
| 安装 Patchright 浏览器 | `patchright install chromium` |
| 验证核心链路 | 抖音扫码登录 → 上传视频 → 确认发布成功 |
| 记录问题清单 | 记录上游代码的 bug、缺失功能、待改进项 |

### 阶段二：任务队列与后端扩展（Week 2）

**目标**：实现可靠的任务队列系统，解决并发和重试问题。

| 任务 | 说明 |
|------|------|
| 数据库扩展 | 新增 publish_tasks、publish_logs 表 |
| 实现任务队列 | asyncio Queue + Worker 模式 |
| 实现失败重试 | 指数退避，最多 3 次 |
| 实现 SSE 任务推送 | 实时通知前端任务状态变更 |
| 扩展 Flask API | 注册 ext_api Blueprint |
| Cookie 心跳检测 | 定期验证 + 失效通知 |

### 阶段三：前端新页面开发（Week 2-3）

**目标**：开发新增页面，完善用户体验。

| 任务 | 说明 |
|------|------|
| TaskCenter.vue | 任务中心页面 |
| PublishHistory.vue | 发布历史页面 |
| Settings.vue | 系统设置页面 |
| 优化已有页面 | Dashboard 增加任务统计图表 |
| 暗黑模式 | Element Plus 暗黑主题适配 |
| 移动端适配 | 响应式布局（可选） |

### 阶段四：桌面壳与打包（Week 3-4）

**目标**：将 Web 应用桌面化，可分发安装。

| 任务 | 说明 |
|------|------|
| Tauri 壳开发 | 窗口管理、系统托盘 |
| Python 打包 | 内嵌 Python 环境 + Patchright 浏览器 |
| 自动更新 | Tauri updater 集成 |
| 安装包测试 | Windows/macOS 安装测试 |
| 首次启动引导 | Patchright 浏览器自动安装 |

### 阶段五：测试与优化（Week 4-5）

| 任务 | 说明 |
|------|------|
| 全平台发布测试 | 抖音、快手、小红书、视频号、B站 |
| 错误恢复测试 | 浏览器崩溃、网络断开、Cookie 过期场景 |
| 性能优化 | 大量任务下的队列表现 |
| UI 润色 | 交互细节、动画、空状态 |
| 文档编写 | 用户使用手册 |

---

## 七、风险控制与注意事项

### 7.1 平台风控

| 风险 | 应对策略 |
|------|---------|
| 发布频率过高被限流 | 任务队列强制间隔（默认 30-60 秒随机） |
| 同一 IP 多账号关联 | 设置页可配置发布间隔 |
| 浏览器指纹识别 | Patchright 内置反检测，不要降级到 Playwright |

### 7.2 Cookie 管理

| 风险 | 应对策略 |
|------|---------|
| Cookie 过期 | 心跳检测（每小时）+ 启动时全量验证 |
| Cookie 泄露 | Cookie 仅存本地，不上传任何服务器 |
| 多账号 Cookie 冲突 | 每个账号独立 Cookie 文件 |

### 7.3 浏览器自动化

| 风险 | 应对策略 |
|------|---------|
| 平台 UI 变更 | 定期同步上游更新，上游已维护选择器 |
| 浏览器崩溃 | 任务队列自动重试 + 错误日志记录 |
| Patchright 版本不兼容 | 锁定 Patchright 版本，谨慎升级 |

### 7.4 打包分发

| 风险 | 应对策略 |
|------|---------|
| Patchright 浏览器二进制 (~200MB) | 首次启动时自动下载，或内嵌到安装包 |
| 跨平台兼容性 | 路径使用 `pathlib.Path`，不硬编码 |
| macOS 沙盒限制 | 数据存 `~/Library/Application Support/` |
| Python 环境隔离 | 考虑使用 `uv` 或内嵌 Python 解释器 |

---

## 八、与原方案的关键差异总结

| 维度 | 原方案 | 改进方案 | 理由 |
|------|--------|---------|------|
| 核心策略 | 从零重建 | 复用上游 + 扩展 | 上游已有 80% 的功能 |
| 前端框架 | Ant Design Vue | Element Plus | 上游已用 Element Plus |
| 通信方式 | WebSocket | REST + SSE | 上游已用此模式 |
| Python 集成 | 拷贝代码到 core/ | pip 依赖引入 | 可同步上游更新 |
| 浏览器驱动 | Playwright/Patchright | 仅 Patchright | 反检测必需 |
| 任务管理 | 无 | asyncio Queue + 重试 | 浏览器自动化的必备 |
| 桌面壳 | Electron (必须) | Tauri (可选) | 体积和性能优势 |
| 账号绑定 | 自研扫码流程 | 复用上游 SSE 扫码 | 上游已实现且验证 |
| B站上传 | 统一浏览器方案 | biliup CLI 集成 | 上游 B 站走独立 CLI |
| 定时发布 | 未设计 | 复用上游 + 扩展 | 上游已支持 |

---

## 九、前端设计规范

前端设计系统（配色、排版、组件规格、布局等）详见：

- **设计主文档**：`design-system/social-auto-upload/MASTER.md`
- **各页面设计稿**：`design-system/social-auto-upload/pages/` 目录下对应页面文件
