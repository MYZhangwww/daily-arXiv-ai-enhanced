# 🚀 飞书通知功能 - 快速参考 / Quick Reference

## 5 分钟快速开始 / 5-Minute Quick Start

### 步骤 1: 在飞书创建机器人 (2 分钟) / Step 1: Create Robot in Feishu

```
飞书群 → 群设置 → 群机器人 → 创建机器人 → 自定义机器人
↓
✓ 勾选"加签" (Enable Signature)
✓ 复制 Webhook URL 和 Secret
```

### 步骤 2: 配置环境变量 (1 分钟) / Step 2: Set Environment Variables

**本地开发 / Local Development:**

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/..."
export FEISHU_SECRET="your-secret-here"
```

**GitHub Actions:**

```
Settings → Secrets and variables → Actions
→ New repository secret
  - Name: FEISHU_WEBHOOK_URL
  - Value: (paste webhook URL)
→ New repository secret
  - Name: FEISHU_SECRET
  - Value: (paste secret)
```

### 步骤 3: 修改 workflow (1 分钟) / Step 3: Update Workflow

编辑 `.github/workflows/run.yml`，在 `jobs` → `env` 添加：

```yaml
env:
  FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
  FEISHU_SECRET: ${{ secrets.FEISHU_SECRET }}
```

### 步骤 4: 测试 (1 分钟) / Step 4: Test

```bash
# 本地测试 / Local test
python test_feishu.py

# 完整流程 / Full workflow
bash run.sh
```

## 常用命令 / Common Commands

### 发送通知 / Send Notification

```bash
# 自动使用今日数据文件 / Auto use today's data file
bash send_feishu_notification.sh

# 指定数据文件 / Specify data file
bash send_feishu_notification.sh data/2024-12-15.jsonl

# 直接调用 Python 模块 / Call Python module directly
python utils/feishu.py --data data/2024-12-15.jsonl --date "2024-12-15"
```

### 测试配置 / Test Configuration

```bash
# 完整测试 / Full test
python test_feishu.py

# 仅测试签名 / Test signature only
python -c "from utils.feishu import FeishuRobot; r = FeishuRobot('url', 'secret'); print(r._generate_signature())"
```

## 消息格式 / Message Format

```
🤖 arXiv 每日爬取统计 - 2024-12-15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
爬取日期: 2024-12-15
总论文数: 127
分类统计 (TOP 5): cs.CV: 45, cs.CL: 32, cs.AI: 28, cs.RO: 15, cs.GR: 7
首篇论文: Vision Transformers for Dense Prediction Tasks
最后论文: Language Models as Zero-Shot Planners
爬取完成时间: 2024-12-15 10:23:45
```

## 故障排查快速指南 / Troubleshooting Cheat Sheet

| 问题 | 解决方案 |
|------|--------|
| 收不到消息 | 1. 检查 Webhook URL 是否正确<br>2. 确认机器人被添加到群<br>3. 运行 `python test_feishu.py` |
| 签名错误 | 检查 Secret 是否完全正确（包括空格和特殊字符） |
| 导入错误 | 安装依赖: `pip install requests>=2.31.0` |
| 找不到数据文件 | 检查文件路径是否正确，文件是否存在 |

## 文件速查表 / File Quick Reference

| 文件 | 用途 | 何时查看 |
|------|------|--------|
| `utils/feishu.py` | 核心模块 | 需要修改消息内容时 |
| `FEISHU_SETUP.md` | 详细配置指南 | 首次配置时 |
| `FEISHU_IMPLEMENTATION.md` | 技术文档 | 理解实现细节时 |
| `GITHUB_ACTIONS_FEISHU.md` | GitHub Actions | 部署到 GitHub Actions 时 |
| `test_feishu.py` | 测试脚本 | 诊断配置问题时 |
| `send_feishu_notification.sh` | 便捷脚本 | 手动发送通知时 |

## 环境变量汇总 / Environment Variables Summary

```bash
# 必需 / Required
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/...

# 可选 / Optional（建议设置）
FEISHU_SECRET=your-secret-here

# 原有变量（不变） / Existing variables (unchanged)
OPENAI_API_KEY=...
OPENAI_BASE_URL=...
LANGUAGE=Chinese
CATEGORIES=cs.CV, cs.CL
MODEL_NAME=gpt-4o-mini
```

## 工作流程图 / Workflow Diagram

```
┌──────────────────────┐
│   爬取 arXiv 论文    │
│   Crawl arXiv        │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│    去重检查          │
│   Dedup Check        │
└──────────┬───────────┘
           │
           ├─ 无新内容 → 退出 (EXIT 1)
           │
           ↓
┌──────────────────────┐
│ [NEW] 发送飞书通知  │ ← 如果设置了 FEISHU_WEBHOOK_URL
│  Send Feishu notif.  │
└──────────┬───────────┘
           │
           ↓ (无论是否发送成功，继续)
┌──────────────────────┐
│  AI 增强处理         │
│ AI Enhancement       │ (可选，取决于 OPENAI_API_KEY)
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│  Markdown 转换       │
│ Markdown Conversion  │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│  更新文件列表        │
│ Update File List     │
└──────────────────────┘
```

## API 返回码 / API Response Codes

| 返回码 | 含义 |
|--------|------|
| 0 | 成功 / Success |
| 1 | 失败（应用级别）/ Failed (application level) |
| 2 | 错误（处理错误）/ Error (processing error) |

## 常见配置错误 / Common Configuration Mistakes

❌ **错误 1**: 复制 Webhook URL 时包含了多余的空格
```bash
# 错误 / Wrong
export FEISHU_WEBHOOK_URL="https://... " # 末尾有空格

# 正确 / Correct  
export FEISHU_WEBHOOK_URL="https://..."
```

❌ **错误 2**: Secret 使用了错误的值
```bash
# 错误 / Wrong - 使用了 Webhook URL
export FEISHU_SECRET="https://open.feishu.cn/..."

# 正确 / Correct - 使用了机器人密钥
export FEISHU_SECRET="ocqBxxxxxxxxxxxxxxxx"
```

❌ **错误 3**: 在 GitHub Actions 中没有添加环境变量
```yaml
# 错误 / Wrong - 没有 env 部分
jobs:
  crawl:
    runs-on: ubuntu-latest
    steps:
      - run: bash run.sh

# 正确 / Correct - 添加了 env
jobs:
  crawl:
    runs-on: ubuntu-latest
    env:
      FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
      FEISHU_SECRET: ${{ secrets.FEISHU_SECRET }}
    steps:
      - run: bash run.sh
```

## 需要更多帮助？ / Need More Help?

1. **快速问题** → 查看 FEISHU_IMPLEMENTATION.md 的 FAQ
2. **配置问题** → 参考 FEISHU_SETUP.md 的故障排查
3. **GitHub Actions** → 阅读 GITHUB_ACTIONS_FEISHU.md
4. **代码问题** → 查看 utils/feishu.py 的源代码注释

## 快速测试命令 / Quick Test Commands

```bash
# 1. 检查依赖 / Check dependencies
python -c "import requests; print('requests OK')"

# 2. 测试导入 / Test import
python -c "from utils.feishu import FeishuRobot; print('feishu module OK')"

# 3. 生成签名 / Generate signature
python -c "from utils.feishu import FeishuRobot; r = FeishuRobot('url', 'secret'); t, s = r._generate_signature(); print(f'timestamp: {t}, sign: {s[:20]}...')"

# 4. 完整测试 / Full test
python test_feishu.py

# 5. 发送通知 / Send notification
python utils/feishu.py --data data/2024-12-15.jsonl --date "2024-12-15"
```

---

💡 **提示**: 将此文件加入书签，方便快速查阅！  
**Tip**: Bookmark this file for quick reference!
