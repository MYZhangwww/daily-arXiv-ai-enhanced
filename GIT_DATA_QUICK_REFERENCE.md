# Git Data 分支集成 - 快速参考卡

## 🎯 核心问题解决

**您的问题**：
> 原工程是把数据存入 data 分支下，在发送飞书消息时，如何能读取 data 分支并发送？

**我们的解决方案**：
✅ 直接从 Git data 分支读取数据，无需手动切换分支

---

## 📋 三行代码快速开始

```bash
# 1. 查看演示
python demo_git_data_branch.py

# 2. 自动获取最新数据并发送
python utils/feishu.py --from-git --mode featured

# 3. 指定日期读取
python utils/feishu.py --from-git --date 2024-02-24
```

---

## 🔧 新增功能

| 功能 | 文件 | 说明 |
|------|------|------|
| Git 数据读取 | `utils/feishu_git_helper.py` | 380+ 行工具类 |
| 集成支持 | `utils/feishu.py` | 新增 150+ 行 |
| 用户指南 | `GIT_DATA_BRANCH_GUIDE.md` | 详细使用说明 |
| 技术指南 | `GIT_DATA_TECHNICAL_GUIDE.md` | 实现原理 |
| 演示脚本 | `demo_git_data_branch.py` | 立即体验 |

---

## 💻 核心命令参考

### 自动模式（推荐）⭐
```bash
# 自动获取最新数据，发送精选文章通知
python utils/feishu.py --from-git

# 自动获取最新数据，发送统计通知
python utils/feishu.py --from-git --mode statistics
```

### 指定日期
```bash
# 发送特定日期的数据
python utils/feishu.py --from-git --date 2024-02-24

# 精选模式（默认）
python utils/feishu.py --from-git --date 2024-02-24 --mode featured

# 统计模式
python utils/feishu.py --from-git --date 2024-02-24 --mode statistics
```

### 本地文件（备选）
```bash
# 如果 data 分支不存在，使用本地文件
python utils/feishu.py --data data/2024-02-24.jsonl --date 2024-02-24
```

### 自定义分支
```bash
# 从其他分支读取
python utils/feishu.py --from-git --branch my-data-branch
```

---

## 🔑 关键参数

```
--from-git              启用 Git 分支读取模式
--branch <name>         指定分支名称（默认：data）
--date <YYYY-MM-DD>     指定日期（可选，自动检测最新）
--mode <featured|stat>  通知模式（默认：featured）
--data <path>           本地文件路径（当不使用 --from-git）
```

---

## 🚀 工作流程

```
主分支（main）
    ↓
python utils/feishu.py --from-git
    ↓
Git 自动读取 data 分支数据
    ↓
无需手动切换分支
    ↓
直接发送飞书通知
```

---

## 📊 API 参考

### Python 代码调用

```python
from utils.feishu import send_daily_crawl_notification

# 方式 1：从 Git 分支读取
success = send_daily_crawl_notification(
    data_file="data",
    date_str="2024-02-24",
    mode="featured",
    from_git=True,
    git_branch="data"
)

# 方式 2：从本地文件读取
success = send_daily_crawl_notification(
    data_file="data/2024-02-24.jsonl",
    date_str="2024-02-24",
    mode="featured",
    from_git=False
)
```

### 高级用法

```python
from utils.feishu_git_helper import GitDataManager, get_latest_date

# 获取最新数据日期
date = get_latest_date("data")  # 返回 "2024-02-24"

# 使用管理器
manager = GitDataManager()
data = manager.get_data_for_notification()  # 获取最新数据
data = manager.get_data_for_notification("2024-02-24")  # 获取指定日期
```

---

## 🎯 典型场景

### 场景 1：日常自动化
```bash
#!/bin/bash
# 每天 9:00 AM 运行
0 9 * * * python utils/feishu.py --from-git --mode featured
```

### 场景 2：GitHub Actions
```yaml
- run: python utils/feishu.py --from-git --mode featured
```

### 场景 3：手动补发
```bash
# 补发历史数据
python utils/feishu.py --from-git --date 2024-02-20
python utils/feishu.py --from-git --date 2024-02-19
python utils/feishu.py --from-git --date 2024-02-18
```

### 场景 4：双通知
```bash
#!/bin/bash
# 同时发送精选和统计
python utils/feishu.py --from-git --mode featured
python utils/feishu.py --from-git --mode statistics
```

---

## ⚙️ 环境变量

```bash
# 必需
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 可选（推荐）
export FEISHU_SECRET="xxx"
```

---

## 🐛 快速故障排除

| 问题 | 解决方案 |
|------|--------|
| `分支不存在` | `git branch -r` 检查是否有 `origin/data`，或使用 `--data` 参数 |
| `无法读取文件` | 检查 data 分支中是否有 `.jsonl` 文件 |
| `Git 超时` | 指定 `--date` 参数，或检查网络连接 |
| `日期自动检测失败` | 手动指定 `--date 2024-02-24` |
| `权限错误` | 检查 Git 凭据配置，或使用本地文件模式 |

---

## 📚 文档链接

- **快速指南**：[GIT_DATA_BRANCH_GUIDE.md](GIT_DATA_BRANCH_GUIDE.md) ⭐
- **技术指南**：[GIT_DATA_TECHNICAL_GUIDE.md](GIT_DATA_TECHNICAL_GUIDE.md)
- **演示脚本**：[demo_git_data_branch.py](demo_git_data_branch.py)
- **核心代码**：[utils/feishu_git_helper.py](utils/feishu_git_helper.py)
- **集成代码**：[utils/feishu.py](utils/feishu.py)

---

## ✨ 关键特点一览

| 特点 | 说明 |
|------|------|
| **无需切换分支** | ✅ 直接在 main 分支读取 data 分支数据 |
| **自动同步** | ✅ 自动 `git fetch` 获取最新数据 |
| **自动检测** | ✅ 自动识别最新的 `.jsonl` 文件 |
| **容错能力** | ✅ data 分支不存在时自动降级到本地文件 |
| **完全兼容** | ✅ 100% 兼容现有的本地文件方式 |
| **跨平台** | ✅ Windows, Linux, Mac 全支持 |
| **生产就绪** | ✅ 完整的错误处理和日志 |

---

## 🎓 进阶技巧

### 1. 列出 data 分支中的所有文件
```bash
git ls-tree -r --name-only data data/
```

### 2. 检查特定日期是否有数据
```bash
git show data:data/2024-02-24.jsonl 2>/dev/null && echo "存在" || echo "不存在"
```

### 3. 自动更新分支
```bash
git fetch origin data:data
```

### 4. 在 Python 中获取所有可用日期
```python
from utils.feishu_git_helper import GitDataHelper
helper = GitDataHelper()
code, files, _ = helper._run_git_command("ls-tree -r --name-only data data/")
dates = [f.split('/')[-1].replace('.jsonl', '') for f in files.split('\n') if f]
```

---

## 📞 需要帮助？

1. 查看演示脚本
   ```bash
   python demo_git_data_branch.py
   ```

2. 查看帮助信息
   ```bash
   python utils/feishu.py -h
   ```

3. 查看完整文档
   - [GIT_DATA_BRANCH_GUIDE.md](GIT_DATA_BRANCH_GUIDE.md)
   - [GIT_DATA_TECHNICAL_GUIDE.md](GIT_DATA_TECHNICAL_GUIDE.md)

4. 检查日志
   ```bash
   # 命令会输出详细的日志信息
   python utils/feishu.py --from-git --mode featured 2>&1
   ```

---

## 🎉 总结

**一句话**：现在可以直接从 Git data 分支读取数据，自动发送飞书通知，无需任何手动操作！

**推荐用法**：
```bash
python utils/feishu.py --from-git --mode featured
```

**就这么简单！** ✨

---

*最后更新: 2026-02-24*  
*版本: 1.0*
