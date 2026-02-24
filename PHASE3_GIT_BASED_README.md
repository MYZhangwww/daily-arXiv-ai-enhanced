# 第3阶段：今日推荐专栏 (Git-Based 架构)
# Phase 3: Today's Recommendations Column (Git-Based Architecture)

## 概述 / Overview

推荐论文系统已完全迁移到 **Git data 分支**，与日常爬虫结果同步管理。所有推荐数据存储在远程 GitHub 仓库的 `data` 分支，支持 GitHub Pages 直接访问。

The recommended papers system has been completely migrated to the **Git data branch**, synchronized with daily crawler results. All recommendation data is stored in the `data` branch of the remote GitHub repository, with support for direct GitHub Pages access.

## 架构设计 / Architecture Design

### 数据流 / Data Flow

```
Feishu 通知 (优先级论文)
↓
feishu.py (获取精选论文)
↓
recommended_papers.py (Git-based 保存)
↓
Git data 分支 (远程存储)
    └── data/recommended_YYYY-MM-DD.jsonl
↓
GitHub Pages (Web 访问)
    └── today-recommended.html (动态加载 JSONL)
```

### 关键特性 / Key Features

1. **Git-Based 存储**
   - 推荐论文存储在 `data` 分支 (Git data branch)
   - 每日生成一个文件：`recommended_YYYY-MM-DD.jsonl`
   - 自动 Git commit + push

2. **本地-远程同步**
   - 自动拉取最新 data 分支
   - 完成后自动恢复原分支
   - 遵循 GitHub Actions 工作流模式

3. **GitHub Pages 支持**
   - 前端从 GitHub 原始内容 URL 获取数据
   - 支持本地开发和生产部署
   - 无需本地文件系统

4. **每日历史保存**
   - 每天的推荐论文独立保存
   - 永久保留历史数据
   - 支持多日期查询

## 文件结构 / File Structure

### 后端 / Backend

**`utils/recommended_papers.py`** - Git-Based 推荐论文管理器

```python
from utils.recommended_papers import RecommendedPapersManager

# 使用方法 / Usage
manager = RecommendedPapersManager(repo_path=".", branch_name="data")
success = manager.save_recommended_papers(papers, date_str="2024-02-24")
```

**主要方法 / Main Methods:**
- `save_recommended_papers(papers, date_str)` - 保存到 Git data 分支并推送

### 前端 / Frontend

**`today-recommended.html`** - 推荐论文展示页面
- 展示来自 Git data 分支的推荐论文
- 支持日期过滤、优先级过滤
- 网格视图和列表视图

**`js/today-recommended.js`** - 核心逻辑
- 从 GitHub 原始内容 URL 动态加载 JSONL 文件
- 支持本地开发和 GitHub Pages 部署
- 自动扫描 90 天内的推荐文件

**`css/today-recommended.css`** - 样式表

### 数据格式 / Data Format

**Git data 分支中的推荐文件：**

```
data/
├── recommended_2024-02-24.jsonl
├── recommended_2024-02-25.jsonl
└── recommended_2024-02-26.jsonl
```

**JSONL 格式 (每行一个 JSON 对象):**

```jsonl
{
  "id": "2402.12345",
  "title": "Paper Title",
  "authors": "Author1, Author2",
  "category": "cs.CV",
  "summary": "Paper summary...",
  "tldr": "AI 总结...",
  "url": "https://arxiv.org/abs/2402.12345",
  "is_priority": true,
  "recommended_date": "2024-02-24",
  "recommended_at": "2024-02-24T10:30:45.123456",
  "priority_status": "priority"
}
```

## 使用流程 / Usage Flow

### 1. Feishu 通知时自动保存

在 `utils/feishu.py` 的 `_send_featured_papers_notification()` 中：

```python
from recommended_papers import RecommendedPapersManager

# 获取精选论文 / Get featured papers
featured_papers = get_featured_papers(...)

# 保存到 Git data 分支 / Save to Git data branch
manager = RecommendedPapersManager(repo_path=".", branch_name="data")
success = manager.save_recommended_papers(featured_papers, date_str)

if success:
    print("✅ 推荐论文已保存到 Git data 分支")
```

### 2. 前端从 GitHub 动态加载

JavaScript 自动：
1. 检测本地开发或 GitHub Pages 部署
2. 扫描最近 90 天的推荐文件
3. 从 GitHub 原始内容 URL 加载 JSONL
4. 按日期分组展示

```javascript
// 自动获取所有可用日期的推荐数据
// Automatically fetch recommendation data for all available dates
loadAvailableDates();
```

## GitHub URLs 配置 / GitHub URLs Configuration

### 原始内容 URL 格式 / Raw Content URL Format

```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/data/{filename}
```

**示例 / Example:**
```
https://raw.githubusercontent.com/dw-dengwei/daily-arXiv-ai-enhanced/data/data/recommended_2024-02-24.jsonl
```

### data-config.js 中的占位符 / Placeholders in data-config.js

```javascript
// 这些占位符在 GitHub Actions 中自动注入
// These placeholders are auto-injected in GitHub Actions
const dataSource = {
    owner: 'PLACEHOLDER_REPO_OWNER',  // 由 Actions 替换为实际所有者
    repo: 'PLACEHOLDER_REPO_NAME'      // 由 Actions 替换为实际仓库名
};
```

## 工作流集成 / Workflow Integration

### GitHub Actions (`.github/workflows/run.yml`)

在爬虫完成后自动调用：

```bash
# 发送 Feishu 通知（包括保存推荐论文到 Git）
python utils/feishu.py --data "data/${today}.jsonl" --date "$today" --mode featured
```

这个命令自动：
1. 获取精选论文
2. 发送 Feishu 通知
3. 调用 `RecommendedPapersManager` 保存到 Git data 分支
4. 推送到远程

### 本地运行 / Local Execution

```bash
# 保存推荐论文到本地 Git（需要已初始化 Git 仓库）
python -c "
from utils.recommended_papers import save_recommended_papers
import json

# 读取推荐论文
with open('data/2024-02-24.jsonl', 'r') as f:
    papers = [json.loads(line) for line in f if line.strip()]

# 保存到 Git data 分支
save_recommended_papers(papers, '2024-02-24')
"
```

## Git 操作流程 / Git Operation Flow

### RecommendedPapersManager 内部流程

```
1. 保存原分支名
   Save original branch name
   ↓
2. 拉取 data 分支（自动恢复）
   Fetch data branch (auto-restore)
   ↓
3. 切换到 data 分支
   Checkout data branch
   ↓
4. 创建推荐 JSONL 文件 (recommended_YYYY-MM-DD.jsonl)
   Create recommended JSONL file
   ↓
5. git add + git commit
   ↓
6. git push origin data
   ↓
7. 恢复原分支
   Restore original branch
```

## 故障排除 / Troubleshooting

### 问题 1: 推荐文件未出现在 data 分支

**检查点：**
1. Git 凭证是否正确配置
2. GitHub Actions 是否有写权限
3. 检查 GitHub Actions 日志中的错误信息

```bash
# 手动检查 data 分支
git fetch origin data:data
git checkout data
ls data/recommended_*.jsonl
```

### 问题 2: 前端无法加载数据

**检查点：**
1. 确认 data 分支中文件确实存在
2. 检查 JavaScript 控制台错误
3. 验证 CORS 是否允许跨域访问

```javascript
// 浏览器控制台
console.log('GitHub Raw URL:', getGitHubRawUrl('2024-02-24'));
```

### 问题 3: 本地开发时找不到推荐文件

**解决方案：**
```bash
# 在本地创建 data 分支
git fetch origin data:data
git checkout data
git pull origin data

# 回到 main 分支
git checkout main
```

## 环境变量配置 / Environment Variables

在 GitHub Secrets 中配置（GitHub Actions 自动使用）：

```
TOKEN_GITHUB          # GitHub Token（用于 Git 操作）
OPENAI_API_KEY        # OpenAI API Key
OPENAI_BASE_URL       # OpenAI Base URL
FEISHU_WEBHOOK_URL    # Feishu Webhook URL
FEISHU_SECRET         # Feishu Secret (可选)
```

## 测试推荐论文保存 / Test Recommended Papers Saving

### 快速测试脚本 / Quick Test Script

```python
#!/usr/bin/env python3

import json
from datetime import datetime
from utils.recommended_papers import RecommendedPapersManager

# 创建测试数据 / Create test data
test_papers = [
    {
        "id": "2402.12345",
        "title": "Test Paper 1",
        "authors": "Test Author 1",
        "category": "cs.CV",
        "summary": "Test summary 1",
        "tldr": "Test TLDR 1",
        "url": "https://arxiv.org/abs/2402.12345",
        "is_priority": True
    },
    {
        "id": "2402.12346",
        "title": "Test Paper 2",
        "authors": "Test Author 2",
        "category": "cs.AI",
        "summary": "Test summary 2",
        "tldr": "Test TLDR 2",
        "url": "https://arxiv.org/abs/2402.12346",
        "is_priority": False
    }
]

# 保存到 Git data 分支 / Save to Git data branch
manager = RecommendedPapersManager(repo_path=".", branch_name="data")
today = datetime.now().strftime("%Y-%m-%d")
success = manager.save_recommended_papers(test_papers, today)

if success:
    print(f"✅ 成功保存 {len(test_papers)} 篇测试论文 / Successfully saved {len(test_papers)} test papers")
    print(f"📝 文件位置 / File location: data/recommended_{today}.jsonl")
    print(f"🌐 GitHub URL: https://raw.githubusercontent.com/YOUR_OWNER/YOUR_REPO/data/data/recommended_{today}.jsonl")
else:
    print("❌ 保存失败 / Failed to save")
```

## 数据持久化 / Data Persistence

### 推荐历史保留 / Keeping Recommendation History

- ✅ 每天的推荐数据永久保存在 Git 历史中
- ✅ 支持查询任意日期的推荐论文
- ✅ 本地-远程自动同步

### 版本控制 / Version Control

```bash
# 查看推荐论文的提交历史 / View commit history
git log --oneline -- data/recommended_*.jsonl

# 查看特定日期的推荐论文 / View recommendations for a specific date
git show data:data/recommended_2024-02-24.jsonl
```

## 后续改进 / Future Improvements

1. **增量更新** - 支持只更新新增推荐
2. **数据导出** - 支持导出为 CSV、Excel 格式
3. **统计分析** - 推荐论文趋势分析
4. **智能推荐** - 基于用户偏好的个性化推荐

## 相关文档 / Related Documentation

- [Phase 1: Git 分支自动恢复](./docs/phase1_git_auto_restore.md)
- [Phase 2: 优先级论文与完整信息](./docs/phase2_priority_papers.md)
- [GitHub Actions 工作流](./github/workflows/run.yml)
