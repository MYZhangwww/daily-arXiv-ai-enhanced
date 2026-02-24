# 从 Git Data 分支读取数据并发送飞书通知 / Read from Git Data Branch and Send Feishu Notification

## 📖 功能介绍

现在支持直接从 Git 的 `data` 分支读取最新数据文件，并自动发送飞书通知，**无需手动切换分支**。

## 🎯 核心优势

- ✅ **无需手动操作** - 自动从 data 分支获取最新数据
- ✅ **不切换分支** - 在 main 分支就能读取 data 分支的数据
- ✅ **自动检测最新** - 自动识别并使用最新的数据文件
- ✅ **向后兼容** - 仍支持读取本地文件
- ✅ **安全可靠** - 完整的错误处理和日志

## 🔧 新增工具

### 文件：`utils/feishu_git_helper.py`

提供 Git 数据读取功能：

```python
from utils.feishu_git_helper import GitDataManager, get_data_from_branch, get_latest_date

# 方式 1：使用高级管理器
manager = GitDataManager(repo_path=".", branch_name="data")
data = manager.get_data_for_notification()  # 获取最新数据

# 方式 2：快速函数
data = get_data_from_branch("data")  # 获取最新数据
date = get_latest_date("data")  # 获取最新日期
```

## 💻 使用方法

### 方式 1：从 Git Data 分支读取（推荐）⭐

```bash
# 自动获取最新数据并发送通知
python utils/feishu.py --from-git --branch data --mode featured

# 指定日期读取
python utils/feishu.py --from-git --branch data --date 2024-02-24 --mode featured
```

### 方式 2：从本地文件读取（传统方式）

```bash
# 使用本地文件
python utils/feishu.py --data data/2024-02-24.jsonl --date 2024-02-24 --mode featured
```

### 方式 3：Python 代码调用

```python
from utils.feishu import send_daily_crawl_notification

# 从 Git 分支读取
success = send_daily_crawl_notification(
    data_file="data",  # 分支名称（当 from_git=True 时）
    date_str="2024-02-24",
    mode="featured",
    from_git=True,  # 启用 Git 读取
    git_branch="data"  # Git 分支名称
)

# 从本地文件读取
success = send_daily_crawl_notification(
    data_file="data/2024-02-24.jsonl",  # 本地文件路径
    date_str="2024-02-24",
    mode="featured",
    from_git=False  # 禁用 Git 读取
)
```

## 🚀 工作流程

```
命令执行
    ↓
检查参数
    ├─ from_git=True? → Git 分支读取
    │   ├─ 检查分支存在
    │   ├─ Fetch 最新数据
    │   ├─ 读取数据文件
    │   └─ 解析 JSONL
    │
    └─ from_git=False → 本地文件读取
        ├─ 检查文件存在
        └─ 读取文件内容
    ↓
精选/统计处理
    ├─ featured 模式 → 精选 5 篇
    └─ statistics 模式 → 统计信息
    ↓
发送飞书通知
```

## 📋 命令行参数详解

### 本地文件模式

```
python utils/feishu.py --data <file_path> --date <date_str> [--mode featured|statistics]

参数说明：
  --data <file_path>        本地数据文件路径（必需）
  --date <date_str>         日期字符串 YYYY-MM-DD（必需）
  --mode <mode>             通知模式：featured 或 statistics（默认：featured）

示例：
  python utils/feishu.py --data data/2024-02-24.jsonl --date 2024-02-24
  python utils/feishu.py --data data/2024-02-24.jsonl --date 2024-02-24 --mode statistics
```

### Git 分支模式

```
python utils/feishu.py --from-git [--branch <branch_name>] [--date <date_str>] [--mode featured|statistics]

参数说明：
  --from-git                启用 Git 分支读取模式
  --branch <branch_name>    Git 分支名称（默认：data）
  --date <date_str>         日期字符串 YYYY-MM-DD（可选，自动检测最新）
  --mode <mode>             通知模式：featured 或 statistics（默认：featured）

示例：
  python utils/feishu.py --from-git
  python utils/feishu.py --from-git --branch data --mode featured
  python utils/feishu.py --from-git --branch data --date 2024-02-24
  python utils/feishu.py --from-git --branch my-data-branch
```

## 🔍 Git 数据读取原理

### 工作原理

1. **无需切换分支** - 使用 `git show` 命令直接读取指定分支的文件
2. **自动获取最新** - 扫描目录找到最新的 JSONL 文件
3. **分支同步** - 自动 `git fetch` 获取远程最新数据
4. **错误恢复** - 如果 Git 读取失败，自动降级到本地文件

### 核心函数

#### `GitDataHelper` 类

```python
helper = GitDataHelper(repo_path=".")

# 检查分支是否存在
if helper.branch_exists("data"):
    print("✅ data 分支存在")

# 从分支读取文件
content = helper.read_file_from_branch("data", "data/2024-02-24.jsonl")

# 获取目录中最新的文件
latest = helper.get_latest_file_in_branch("data", directory="data")

# 获取最新数据的日期
date = helper.get_file_date_from_branch("data")
```

#### `GitDataManager` 类

```python
manager = GitDataManager(repo_path=".", branch_name="data")

# 获取用于通知的数据
data = manager.get_data_for_notification()  # 最新数据
data = manager.get_data_for_notification("2024-02-24")  # 指定日期

# 获取最新数据的日期
date = manager.get_latest_data_date()
```

## 📊 实际场景示例

### 场景 1：完全自动化发送

```bash
# 自动获取最新数据并发送通知到飞书
python utils/feishu.py --from-git --mode featured
```

**输出**：
```
📂 从 Git 分支读取数据 / Reading data from Git branch: data
📄 从 data 分支读取文件 / Reading file from data branch: data/2024-02-24.jsonl
✅ 成功读取 542 行数据 / Successfully read 542 lines
✅ 飞书通知发送成功 / Feishu notification sent successfully
```

### 场景 2：指定日期读取

```bash
# 发送特定日期的数据
python utils/feishu.py --from-git --date 2024-02-20 --mode featured
```

### 场景 3：手动和自动混合

```bash
# 日常自动运行：从 Git 分支获取
python utils/feishu.py --from-git

# 补发历史数据：从本地文件读取
python utils/feishu.py --data archive/2024-02-15.jsonl --date 2024-02-15
```

### 场景 4：集成到 CI/CD

```bash
#!/bin/bash
# 每日定时任务

# 发送精选文章通知
python utils/feishu.py --from-git --branch data --mode featured

# 同时发送统计通知
python utils/feishu.py --from-git --branch data --mode statistics
```

## 🐛 故障排除

### 问题 1：无法找到 data 分支

```
❌ 错误 / Error: 分支不存在 / Branch does not exist: data
```

**解决方案**：
```bash
# 检查分支是否存在
git branch -r | grep data

# 如果没有，从远程创建
git fetch origin data:data

# 如果仍然没有，检查分支名称是否正确
python utils/feishu.py --from-git --branch <actual-branch-name>
```

### 问题 2：无法读取文件

```
❌ 错误 / Error: 无法读取文件 / Failed to read file
```

**解决方案**：
```bash
# 检查文件是否真的在分支中
git ls-tree -r --name-only data | grep jsonl

# 尝试手动 fetch 更新
git fetch origin data

# 重新尝试
python utils/feishu.py --from-git
```

### 问题 3：Git 命令超时

```
⚠️ Git 读取出错 / Git read error: 命令超时 / Command timeout
```

**解决方案**：
- 检查网络连接
- 尝试使用 `--date` 指定日期，避免扫描全部文件
- 使用本地文件作为备选

### 问题 4：日期自动检测失败

```bash
# 需要手动指定日期
python utils/feishu.py --from-git --date 2024-02-24
```

## 🎓 进阶用法

### 1. 自定义数据处理

```python
from utils.feishu_git_helper import GitDataManager
from utils.feishu import get_featured_papers

manager = GitDataManager()
data_content = manager.get_data_for_notification()

# 获取前 10 篇论文而不是 5 篇
papers = get_featured_papers(data_content, top_n=10)

for paper in papers:
    print(f"📄 {paper['title']}")
    print(f"   {paper['tldr']}\n")
```

### 2. 批量处理多个日期

```bash
#!/bin/bash
# 补发最近 7 天的通知

for i in {0..6}; do
    date=$(date -d "-$i days" +%Y-%m-%d)
    python utils/feishu.py --from-git --date $date --mode featured
done
```

### 3. 条件发送

```python
from utils.feishu_git_helper import get_latest_date
from utils.feishu import send_daily_crawl_notification

# 只有新数据时才发送
date = get_latest_date("data")
if date and date > "2024-02-23":  # 仅在 2024-02-24 之后发送
    send_daily_crawl_notification(
        data_file="data",
        date_str=date,
        from_git=True
    )
```

## ✨ 环境变量

```bash
# 飞书配置
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
export FEISHU_SECRET="xxx"  # 可选
```

## 📚 相关文件

| 文件 | 说明 |
|------|------|
| `utils/feishu.py` | 核心飞书模块（已更新） |
| `utils/feishu_git_helper.py` | ⭐ Git 辅助工具（新增） |
| `QUICK_START_FEATURED_MODE.md` | 精选文章模式快速开始 |

## 🔗 快速链接

- [Git 操作参考](https://git-scm.com/docs/git-show)
- [Feishu API 文档](https://open.feishu.cn/document/server-docs/bot-framework/bot/overview)
- [JSONL 格式说明](https://jsonlines.org/)

---

## 总结

**从 Git data 分支读取数据的三种方式**：

| 方式 | 命令 | 特点 |
|------|------|------|
| **自动获取最新** | `--from-git` | ⭐ 推荐，完全自动 |
| **指定日期** | `--from-git --date 2024-02-24` | 灵活，控制力强 |
| **本地文件** | `--data data/2024-02-24.jsonl` | 可靠，无网络需求 |

**推荐工作流**：
```bash
# 每日定时任务
python utils/feishu.py --from-git --mode featured
```

就这么简单！🎉
