# Phase 3 快速参考指南 / Quick Reference Guide

## 🎯 核心概念 / Core Concepts

### 什么改变了？ / What Changed?

| 方面 | 旧方式 (❌) | 新方式 (✅) |
|------|-----------|-----------|
| 存储位置 | 本地 `data/` 目录 | Git `data` 分支 |
| 文件管理 | 单一 JSONL 文件 | 每日独立文件 |
| 历史保留 | ❌ 无法保留 | ✅ 完整 Git 历史 |
| 远程同步 | ❌ 手动 | ✅ 自动 push |
| GitHub Pages | ❌ 无法访问 | ✅ 直接访问 |

---

## 📋 文件位置 / File Locations

### Python 代码 / Python Code

```
utils/
├── recommended_papers.py       ← Git-Based 管理器
├── feishu.py                  ← 集成了推荐论文保存
└── feishu_git_helper.py       ← Git 操作帮助函数
```

### HTML/JS/CSS / Web Files

```
├── today-recommended.html      ← 推荐论文展示页面
├── js/today-recommended.js    ← GitHub URL 加载逻辑
├── css/today-recommended.css  ← 样式表
└── js/data-config.js          ← GitHub 仓库信息注入
```

### Git 数据 / Git Data

```
data/ (on 'data' branch)
├── recommended_2024-02-24.jsonl
├── recommended_2024-02-25.jsonl
└── recommended_2024-02-26.jsonl
```

---

## 🚀 快速开始 / Quick Start

### 1. 验证安装

```bash
cd /path/to/daily-arXiv-ai-enhanced
python test_phase3_simple.py
```

**预期输出：** `🎉 所有测试通过！/ All tests passed!`

### 2. 手动测试推荐保存

```bash
# 创建示例 JSON 文件
cat > test_papers.jsonl << 'EOF'
{"id":"2402.12345","title":"Test Paper","authors":"Author","category":"cs.CV","summary":"Test","url":"https://arxiv.org/abs/2402.12345","is_priority":true}
{"id":"2402.12346","title":"Test Paper 2","authors":"Author 2","category":"cs.AI","summary":"Test 2","url":"https://arxiv.org/abs/2402.12346","is_priority":false}
EOF

# 保存到 Git data 分支
python -c "
from utils.recommended_papers import RecommendedPapersManager
import json
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d')
with open('test_papers.jsonl', 'r') as f:
    papers = [json.loads(line) for line in f if line.strip()]

manager = RecommendedPapersManager()
success = manager.save_recommended_papers(papers, date)
print('✅ 成功保存' if success else '❌ 保存失败')
"
```

### 3. 在 GitHub Pages 上查看

访问：`https://YOUR_GITHUB_USERNAME.github.io/daily-arXiv-ai-enhanced/today-recommended.html`

---

## 💻 常用命令 / Common Commands

### Python 操作

```python
# 导入管理器
from utils.recommended_papers import RecommendedPapersManager

# 创建实例
manager = RecommendedPapersManager(repo_path=".", branch_name="data")

# 保存推荐论文到 Git
success = manager.save_recommended_papers(papers_list, "2024-02-24")

# 检查是否成功
if success:
    print("✅ 推荐论文已保存并推送到 Git")
else:
    print("❌ 保存失败")
```

### Git 命令

```bash
# 查看 data 分支中的推荐文件
git checkout data
ls -la data/recommended_*.jsonl

# 查看特定日期的推荐文件
git show data:data/recommended_2024-02-24.jsonl

# 查看推荐论文的提交历史
git log --oneline -- data/recommended_*.jsonl

# 回到 main 分支
git checkout main
```

### GitHub Actions

```bash
# 查看最新运行
gh run list

# 查看特定运行的日志
gh run view <run-id> --log

# 触发手动运行
gh workflow run run.yml
```

---

## 🔧 配置检查清单 / Configuration Checklist

### GitHub Secrets (Actions)

- [ ] `TOKEN_GITHUB` - 用于 Git 操作
- [ ] `OPENAI_API_KEY` - 用于 AI 增强
- [ ] `FEISHU_WEBHOOK_URL` - 用于飞书通知

### Git 配置

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### JavaScript 配置

`js/data-config.js` 中的占位符：
- `PLACEHOLDER_REPO_OWNER` - 在 GitHub Actions 中自动替换
- `PLACEHOLDER_REPO_NAME` - 在 GitHub Actions 中自动替换

---

## 📊 数据格式 / Data Format

### JSONL 结构 (每行一个 JSON 对象)

```json
{
  "id": "2402.12345",
  "title": "Paper Title Here",
  "authors": "Author 1, Author 2",
  "category": "cs.CV",
  "summary": "Full abstract...",
  "tldr": "AI生成的简短总结",
  "url": "https://arxiv.org/abs/2402.12345",
  "is_priority": true,
  "recommended_date": "2024-02-24",
  "recommended_at": "2024-02-24T10:30:45.123456",
  "priority_status": "priority"
}
```

### 必需字段 / Required Fields

- `id` - arXiv ID
- `title` - 论文标题
- `authors` - 作者列表
- `category` - 论文分类
- `url` - arXiv 链接
- `is_priority` - 是否优先级论文

### 可选字段 / Optional Fields

- `summary` - 论文摘要
- `tldr` - AI 总结
- `recommended_date` - 推荐日期 (自动添加)
- `recommended_at` - 推荐时间 (自动添加)
- `priority_status` - 优先级状态 (自动添加)

---

## 🐛 故障排除 / Troubleshooting

### 问题：推荐论文未出现在 GitHub Pages

**检查步骤：**

```bash
# 1. 检查 data 分支是否有推荐文件
git checkout data
ls -la data/recommended_*.jsonl

# 2. 验证文件格式
head -1 data/recommended_2024-02-24.jsonl | python -m json.tool

# 3. 检查文件是否被推送
git log --oneline -5 -- data/recommended_*.jsonl

# 4. 验证 GitHub Pages 构建
# 访问 GitHub -> Actions -> 查看最新工作流状态
```

### 问题：前端无法加载数据

**调试方法：**

```javascript
// 在浏览器控制台运行
console.log('Current URL:', window.location.href);
console.log('Is Local Dev:', isLocalDev());
console.log('GitHub URL Sample:', getGitHubRawUrl('2024-02-24'));

// 检查 fetch
fetch(getGitHubRawUrl('2024-02-24'))
  .then(r => r.text())
  .then(console.log)
  .catch(console.error);
```

### 问题：Git 提交失败

**解决方案：**

```bash
# 检查 Git 用户配置
git config user.name
git config user.email

# 配置 Git 用户
git config --global user.name "GitHub Actions"
git config --global user.email "actions@github.com"

# 检查远程仓库
git remote -v

# 验证 SSH/HTTPS 凭证
git pull origin data
```

---

## 🔐 权限和凭证 / Permissions & Credentials

### GitHub Token 要求

推荐论文保存需要以下权限：

- `repo` - 完整仓库访问
- `workflows` - 工作流访问

### 本地运行时

```bash
# 生成 Personal Access Token
# 访问 GitHub -> Settings -> Developer settings -> Personal access tokens

# 配置本地 Git 凭证
git config credential.helper store
git pull origin main
# 输入 GitHub Token 作为密码

# 或使用 SSH
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
ssh-keygen -t ed25519
# 将公钥添加到 GitHub -> Settings -> SSH keys
```

---

## 📈 监控和日志 / Monitoring & Logs

### GitHub Actions 日志

```bash
# 查看工作流日志
gh run view <run-id> --log

# 实时监控
gh run watch <run-id>

# 查看推荐论文保存的日志
# 在 GitHub -> Actions -> arXiv-daily-ai-enhanced -> 查找包含 "推荐论文" 的日志
```

### 本地日志

```bash
# Python 脚本会输出到 stderr
# 重定向到文件查看
python utils/feishu.py ... 2> debug.log

# 查看 Git 操作日志
GIT_TRACE=1 python -c "from utils.recommended_papers import ..."
```

---

## 🌐 部署检查 / Deployment Checklist

### 首次部署

- [ ] Git 仓库已初始化
- [ ] GitHub 远程仓库已配置
- [ ] `data` 分支已创建
- [ ] GitHub Actions 已启用
- [ ] Secrets 已配置
- [ ] data-config.js 占位符已设置

### GitHub Pages 配置

```bash
# 在 GitHub 仓库设置中：
# Settings -> Pages -> Source -> Deploy from a branch
# Branch: main
# Folder: / (root)

# 验证部署
curl https://YOUR_USERNAME.github.io/daily-arXiv-ai-enhanced/today-recommended.html
```

### 数据分支配置

```bash
# 确保 data 分支的文件可以通过原始内容访问
# https://raw.githubusercontent.com/OWNER/REPO/data/data/recommended_2024-02-24.jsonl
```

---

## 📚 相关文档 / Related Documentation

- [PHASE3_GIT_BASED_README.md](./PHASE3_GIT_BASED_README.md) - 详细架构文档
- [PHASE3_COMPLETION_REPORT.md](./PHASE3_COMPLETION_REPORT.md) - 完成报告
- [.github/workflows/run.yml](./.github/workflows/run.yml) - GitHub Actions 工作流
- [utils/feishu_git_helper.py](./utils/feishu_git_helper.py) - Git 帮助函数

---

## ⚡ 性能和优化 / Performance & Optimization

### 前端优化

```javascript
// JavaScript 自动：
// 1. 缓存已加载的数据
// 2. 只加载可见数据（延迟加载）
// 3. 压缩 JSON 响应

// 当前限制：
// - 扫描最近 90 天
// - 可以优化为增量加载
```

### 数据库考虑

未来可以考虑：
- [ ] 迁移到数据库存储（保留 Git 历史）
- [ ] 实现缓存层
- [ ] 创建索引加快查询

---

## 🎓 学习资源 / Learning Resources

### Git 深入学习

- [Git Official Book](https://git-scm.com/book/en/v2)
- [GitHub Docs](https://docs.github.com)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

### JSON 和 JSONL

- [JSON Standard](https://www.json.org)
- [JSONL Format](https://jsonlines.org/)

### 浏览器开发

- [MDN Web Docs](https://developer.mozilla.org)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)

---

## 🤝 贡献指南 / Contributing

### 报告 Bug

1. 检查 [Issues](https://github.com/YOUR_USERNAME/daily-arXiv-ai-enhanced/issues)
2. 创建新 Issue，包括：
   - 问题描述
   - 重现步骤
   - 期望行为
   - 实际行为
   - 环境信息

### 提交改进

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改
4. 创建 Pull Request

---

## 📞 获取帮助 / Getting Help

### 快速问题

- 检查本快速参考指南
- 查看 PHASE3_GIT_BASED_README.md
- 查看 PHASE3_COMPLETION_REPORT.md

### 深层问题

- 在 GitHub Issues 提问
- 查看 GitHub Discussions
- 检查 GitHub Actions 日志

---

**最后更新：** 2026-02-24  
**版本：** 1.0 (Production Ready)  
**状态：** ✅ 完全可用 / Fully Operational
