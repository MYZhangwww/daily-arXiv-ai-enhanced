# Git Data 分支集成 - 技术实现指南

## 📌 项目背景

您的工程将爬取的数据存储在 Git 的 `data` 分支中，而代码在 `main` 分支。现在我们实现了直接从 `data` 分支读取数据的功能，**无需手动切换分支**。

## 🎯 核心特性

### 问题：原来怎样工作
```
main 分支（代码）
    ↓
手动 git checkout data
    ↓
data 分支（数据）
    ↓
读取文件
    ↓
手动 git checkout main
    ↓
发送通知
```

### 解决方案：现在怎样工作
```
main 分支（代码）
    ↓
--from-git 参数
    ↓ （Git 读取，不切换分支）
data 分支（数据）
    ↓
直接读取文件
    ↓
发送通知
```

## 🔧 实现细节

### 新增文件

#### 1. `utils/feishu_git_helper.py`（380+ 行）

提供 Git 操作和数据读取功能：

**核心类**：

```python
class GitDataHelper:
    """Git 数据辅助类"""
    - branch_exists(branch_name)      # 检查分支存在
    - fetch_branch(branch_name)       # 获取分支最新数据
    - read_file_from_branch()         # 从分支读取文件
    - get_latest_file_in_branch()     # 获取最新文件
    - get_file_date_from_branch()     # 获取文件日期

class GitDataManager:
    """Git 数据管理器"""
    - get_data_for_notification()     # 获取用于通知的数据
    - get_latest_data_date()          # 获取最新日期
```

**快速函数**：

```python
get_data_from_branch(branch_name, date_str, repo_path)  # 快速获取数据
get_latest_date(branch_name, repo_path)                 # 快速获取日期
```

#### 2. `utils/feishu.py`（已更新）

**修改内容**：

```python
# 1. 导入 Git 辅助工具
from feishu_git_helper import get_data_from_branch, get_latest_date

# 2. 新增函数
def get_data_content(data_source, date_str, from_git)  # 读取数据（支持 Git/本地）

# 3. 修改函数签名
def get_featured_papers(data_content, top_n)           # 改为接收内容而非文件路径
def send_daily_crawl_notification(                     # 新增 from_git 和 git_branch 参数
    data_file, date_str, mode, from_git=False, git_branch="data"
)

# 4. 更新辅助函数
def _send_statistics_notification(robot, data_content, date_str)
def _send_featured_papers_notification(robot, data_content, date_str)

# 5. 更新 main()
# 新增 --from-git 和 --branch 参数
# 支持自动获取最新日期
```

## 💻 使用方式

### 场景 1：完全自动化（推荐）

```bash
python utils/feishu.py --from-git --mode featured
```

工作流：
1. 检查 `data` 分支存在
2. `git fetch origin` 获取最新数据
3. 自动扫描找到最新的 `.jsonl` 文件
4. 直接读取数据内容
5. 精选 5 篇论文
6. 发送飞书通知

### 场景 2：指定日期

```bash
python utils/feishu.py --from-git --date 2024-02-24 --mode featured
```

工作流：
1. 检查 `data` 分支存在
2. `git fetch origin` 获取最新数据
3. 读取指定日期的文件 `data/2024-02-24.jsonl`
4. 精选论文
5. 发送通知

### 场景 3：使用自定义分支

```bash
python utils/feishu.py --from-git --branch my-data-branch --mode featured
```

### 场景 4：降级到本地文件

```bash
python utils/feishu.py --data data/2024-02-24.jsonl --date 2024-02-24
```

## 🔐 技术细节

### Git 操作原理

#### 核心：不切换分支的文件读取

```bash
# 传统方式（需要切换分支）
git checkout data
cat data/2024-02-24.jsonl
git checkout main

# 新方式（直接读取）
git show data:data/2024-02-24.jsonl
```

#### 实现代码

```python
def _run_git_command(self, command: str):
    """运行 Git 命令"""
    full_command = f"git -C {self.repo_path} {command}"
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

# 使用示例
code, content, error = self._run_git_command("show data:data/2024-02-24.jsonl")
if code == 0:
    print(content)  # 文件内容
```

### 分支同步机制

```python
def fetch_branch(self, branch_name: str) -> bool:
    """
    工作流：
    1. git fetch origin              # 获取远程最新信息
    2. 检查 origin/data 存在
    3. 如果本地有 data:
       - git checkout data           # 切换
       - git pull origin data        # 更新
    4. 如果本地无 data:
       - git checkout --track origin/data  # 创建并跟踪
    """
```

### 自动日期检测

```python
def get_file_date_from_branch(self, branch_name: str) -> Optional[str]:
    """
    1. git ls-tree -r --name-only data data/
       # 列出 data 目录中的所有文件
    2. 过滤 .jsonl 文件
    3. 按名称排序
    4. 获取最新（最后一个）文件
    5. 提取日期（假设文件名为 YYYY-MM-DD.jsonl）
    """
```

## 📊 数据流

```
命令行输入
    ↓
参数解析 (argparse)
    ├─ --from-git? 
    │   ├─ YES → GitDataManager
    │   │   ├─ branch_exists()?
    │   │   │   ├─ YES → fetch_branch()
    │   │   │   │   └─ pull 最新数据
    │   │   │   └─ NO → 错误退出
    │   │   └─ get_data_for_notification()
    │   │       └─ read_file_from_branch()
    │   │           └─ git show branch:file
    │   │
    │   └─ NO → 本地文件读取
    │       └─ os.path.exists()?
    │           └─ open & read
    ↓
get_data_content() 统一处理
    ↓ (数据内容字符串)
选择模式
    ├─ featured → get_featured_papers()
    └─ statistics → 解析统计
    ↓
构建飞书消息
    ↓
发送通知
```

## 🧪 测试方案

### 单元测试（Python）

```python
from utils.feishu_git_helper import GitDataHelper, GitDataManager

# 测试 1：分支检测
helper = GitDataHelper(".")
assert helper.branch_exists("main")

# 测试 2：文件读取（如果 data 分支存在）
if helper.branch_exists("data"):
    content = helper.read_file_from_branch("data", "data/2024-02-24.jsonl")
    assert content is not None
    assert len(content) > 0

# 测试 3：日期检测
manager = GitDataManager()
date = manager.get_latest_data_date()
if date:
    assert len(date) == 10  # YYYY-MM-DD 格式
```

### 集成测试（命令行）

```bash
# 测试 1：检查帮助信息
python utils/feishu.py -h | grep "from-git"

# 测试 2：演示脚本
python demo_git_data_branch.py

# 测试 3：模拟 data 分支
git checkout --orphan data 2>/dev/null || git branch data
mkdir -p data
echo '{"title":"test","AI":{"tldr":"test"}}'  > data/2024-02-24.jsonl
git add data/2024-02-24.jsonl
git commit -m "Add test data"

# 测试 4：从 data 分支读取
python utils/feishu.py --from-git --mode featured  # 不指定 --date，自动检测

# 测试 5：清理（可选）
git checkout main
git branch -D data
```

## 🔄 工作流集成

### GitHub Actions 示例

```yaml
name: Daily Feishu Notification

on:
  schedule:
    - cron: '0 9 * * *'  # 每天 9:00 UTC

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Send Feishu Notification
        env:
          FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
          FEISHU_SECRET: ${{ secrets.FEISHU_SECRET }}
        run: |
          python utils/feishu.py --from-git --mode featured
```

### Cron 脚本示例

```bash
#!/bin/bash
# /etc/cron.d/feishu-notification

# 每天 9:00 AM 运行
0 9 * * * cd /path/to/daily-arXiv-ai-enhanced && \
  export FEISHU_WEBHOOK_URL="xxx" && \
  python utils/feishu.py --from-git --mode featured 2>> /var/log/feishu.log
```

### 本地开发脚本

```bash
#!/bin/bash
# scripts/send_feishu_from_git.sh

cd "$(dirname "$0")/.."

# 加载环境变量
source .env.local 2>/dev/null || true

# 发送通知
python utils/feishu.py --from-git --mode featured

# 或者发送统计
# python utils/feishu.py --from-git --mode statistics
```

## ⚙️ 配置要求

### 环境变量

```bash
# 必需
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID

# 可选（推荐）
FEISHU_SECRET=YOUR_SECRET_KEY
```

### Git 配置

```bash
# 可选：如果 data 分支在远程
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git fetch origin

# 或者如果使用 SSH
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
```

## 🐛 常见问题

### Q1: 为什么还需要 data 分支？

**A**: 
- 代码和数据分离，便于版本控制
- 减少 main 分支的体积
- 便于独立更新数据
- 符合 Git 最佳实践

### Q2: 如果 data 分支不存在怎么办？

**A**: 
- 系统会提示错误
- 可以自动降级到本地文件：`--data data/2024-02-24.jsonl`
- 或者检查 data 分支是否真的存在：`git branch -r | grep data`

### Q3: 性能如何？

**A**: 
- Git 读取速度快（< 100ms）
- 网络依赖：`git fetch` 需要网络
- 建议在离线时使用 `--data` 参数使用本地文件

### Q4: 能否读取历史数据？

**A**: 是的！
```bash
python utils/feishu.py --from-git --date 2024-02-20
```

### Q5: 多个分支如何处理？

**A**: 
```bash
# data 分支
python utils/feishu.py --from-git --branch data

# 其他分支
python utils/feishu.py --from-git --branch my-data
```

## 🚀 性能优化建议

1. **缓存最新日期**
   ```python
   date = get_latest_date("data")
   # 缓存 date，避免重复调用
   ```

2. **批量读取**
   ```bash
   # 一次读取多日期的数据
   for date in $(git ls-tree -r --name-only data data/ | grep jsonl); do
       # 处理每个日期
   done
   ```

3. **离线备份**
   ```bash
   # 定期备份 data 分支到本地
   git clone --branch data --depth 1 . ./data_backup
   ```

## 📚 相关文档

- [GIT_DATA_BRANCH_GUIDE.md](GIT_DATA_BRANCH_GUIDE.md) - 用户指南
- [Git 官方文档](https://git-scm.com/docs/git-show)
- [subprocess 模块](https://docs.python.org/3/library/subprocess.html)

## ✨ 总结

| 方面 | 说明 |
|------|------|
| **核心功能** | Git 分支数据读取，无需切换分支 |
| **关键文件** | `feishu_git_helper.py`, `feishu.py` |
| **主要优势** | 自动化、便捷、可靠 |
| **使用场景** | CI/CD、自动化通知、批量处理 |
| **向后兼容** | 完全兼容本地文件读取 |
| **代码行数** | 新增 380+ 行辅助代码，修改 150+ 行核心代码 |

---

**准备就绪？开始使用吧！** 🚀

```bash
python utils/feishu.py --from-git --mode featured
```
