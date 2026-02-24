# 飞书精选文章通知快速开始指南 / Quick Start Guide

## 📖 功能概述 / Overview

新的**精选文章模式**将每日飞书通知从统计数据转换为**精选的 5 篇高质量文章及其 AI 总结**。

The new **Featured Papers Mode** transforms daily Feishu notifications from statistics to **5 curated high-quality papers with their AI summaries**.

## 🚀 快速开始 / Quick Start

### 方式 1: 使用演示脚本 / Method 1: Use Demo Script

```powershell
# Windows PowerShell
python demo_featured_papers.py
```

这会演示如何提取和发送精选文章。

### 方式 2: 命令行直接调用 / Method 2: Direct CLI

```bash
# 使用精选文章模式（默认）/ Use featured papers mode (default)
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"

# 或显式指定 / Or explicitly specify
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode featured

# 切换回统计模式 / Switch back to statistics mode
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics
```

### 方式 3: 在 Python 代码中使用 / Method 3: Use in Python Code

```python
from utils.feishu import send_daily_crawl_notification

# 发送精选文章通知 / Send featured papers notification
success = send_daily_crawl_notification(
    data_file="data/2024-02-24.jsonl",
    date_str="2024-02-24",
    mode="featured"  # 默认值，可省略
)

# 或发送统计通知 / Or send statistics notification
success = send_daily_crawl_notification(
    data_file="data/2024-02-24.jsonl",
    date_str="2024-02-24",
    mode="statistics"
)
```

### 方式 4: 集成到主工作流 / Method 4: Integrated in Main Workflow

```bash
# Linux/Mac
bash run.sh

# Windows PowerShell
.\run.ps1
```

已自动配置为使用精选文章模式。

## 📊 通知内容示例 / Notification Example

### 精选文章模式的飞书卡片 / Featured Papers Card

```
标题：📚 Daily arXiv AI 精选 (2024-02-24)
━━━━━━━━━━━━━━━━━━━━━━━

[1] Vision Transformers for Dense Prediction Tasks
    cs.CV | Alice Smith, Bob Johnson, Charlie Brown
    🤖 Introduces Vision Transformers for dense tasks with improved efficiency

[2] Language Models as Zero-Shot Planners for Robotics
    cs.CL | Diana Prince, Eve Wilson
    🤖 Demonstrates LLMs can perform robot planning tasks zero-shot

[3] Efficient Attention Mechanisms for Large-Scale Transformers
    cs.AI | Frank Miller, Grace Lee, Henry Zhang
    🤖 Proposes efficient attention reducing complexity from O(n²) to O(n log n)

[4] 3D Object Detection with Point Clouds Using Graph Neural Networks
    cs.CV | Isabella Martinez, Jack Wilson
    🤖 Graph neural networks improve 3D detection accuracy by 15%

[5] Multimodal Learning for Cross-Domain Understanding
    cs.CL | Kevin Brown
    🤖 Multimodal approach achieves 25% improvement over single modality

━━━━━━━━━━━━━━━━━━━━━━━
📅 更新时间: 2024-02-24 10:30:45
📖 数据源: arXiv + AI 增强分析
```

## 🔧 配置要求 / Configuration Requirements

### 环境变量 / Environment Variables

```bash
# 必需 / Required
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID"

# 可选（推荐用于签名验证）/ Optional (recommended for signature verification)
export FEISHU_SECRET="YOUR_SECRET_KEY"
```

### 数据文件格式 / Data File Format

JSONL 格式文件，每行一个 JSON 对象：

```json
{
  "id": "2401.00001",
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "categories": ["cs.CV"],
  "abs": "https://arxiv.org/abs/2401.00001",
  "summary": "摘要内容",
  "AI": {
    "tldr": "AI生成的一句话总结",
    "motivation": "研究动机",
    "method": "研究方法",
    "result": "研究结果",
    "conclusion": "研究结论"
  }
}
```

## ✨ 核心特性 / Key Features

- ✅ **AI感知**：优先选择包含 AI 总结的论文
- ✅ **自动截断**：标题限制 60 字，摘要限制 150 字
- ✅ **双模式**：支持精选文章和统计两种通知模式
- ✅ **向后兼容**：旧的统计模式仍可用
- ✅ **安全**：HMAC-SHA256 签名验证
- ✅ **跨平台**：支持 Windows PowerShell 和 Linux/Mac Bash

---

- ✅ **AI-Aware**: Prioritizes papers with AI summaries
- ✅ **Auto-Truncation**: Title max 60 chars, summary max 150 chars
- ✅ **Dual Modes**: Supports both featured papers and statistics
- ✅ **Backward Compatible**: Legacy statistics mode still available
- ✅ **Secure**: HMAC-SHA256 signature verification
- ✅ **Cross-Platform**: Supports Windows PowerShell and Linux/Mac Bash

## 🎯 常见场景 / Common Scenarios

### 场景 1: 只需精选文章，不需要统计
### Scenario 1: Only featured papers, no statistics

```powershell
# 在 run.ps1 中已默认配置
# Already configured by default in run.ps1
.\run.ps1
```

### 场景 2: 根据需要切换模式
### Scenario 2: Switch modes as needed

```powershell
# 先发送精选文章
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode featured

# 然后发送统计（可选）
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics
```

### 场景 3: 自定义精选数量
### Scenario 3: Customize number of featured papers

在 `utils/feishu.py` 中修改 `send_daily_crawl_notification` 的调用：

```python
# 改为获取 10 篇论文而不是默认的 5 篇
featured = get_featured_papers(data_file, top_n=10)
```

## 🐛 故障排除 / Troubleshooting

### 问题 1: 没有 AI 总结的论文怎么办？
### Issue 1: What if papers don't have AI summaries?

自动降级到使用原始摘要的前 150 字符。论文仍会显示，但不会有 🤖 标记。

Papers still display but without the 🤖 marker. The first 150 chars of abstract will be used.

### 问题 2: 如何禁用签名验证？
### Issue 2: How to disable signature verification?

不设置 `FEISHU_SECRET` 环境变量。如果没有设置，签名验证会自动跳过。

Don't set the `FEISHU_SECRET` environment variable. If not set, signature verification is automatically skipped.

### 问题 3: 消息太长被截断了
### Issue 3: Message truncated as too long

这是 Feishu 的限制。本功能已自动处理截断：
- 标题：最多 60 字符
- TLDR：最多 150 字符
- 作者：最多显示前 3 位

This is Feishu's limit. The feature handles truncation automatically:
- Title: max 60 chars
- TLDR: max 150 chars
- Authors: max 3 displayed

## 📚 相关文档 / Related Docs

- [完整实现指南 / Full Implementation Guide](FEISHU_IMPLEMENTATION.md)
- [精选文章模式详解 / Featured Papers Mode Details](FEISHU_FEATURED_PAPERS_MODE.md)
- [安装和配置 / Setup and Configuration](FEISHU_SETUP.md)
- [Windows 测试指南 / Windows Testing Guide](WINDOWS_TESTING_GUIDE.md)

## 💡 下一步 / Next Steps

1. 配置 `FEISHU_WEBHOOK_URL` 环境变量
2. 运行演示脚本测试功能
3. 在实际工作流中使用
4. 根据需要调整参数

---

1. Set up `FEISHU_WEBHOOK_URL` environment variable
2. Run demo script to test the feature
3. Use in actual workflow
4. Adjust parameters as needed

## ❓ 常见问题 / FAQ

**Q: 精选文章是如何选择的？**
**Q: How are featured papers selected?**

A: 优先选择有 AI 总结的论文，然后按在数据文件中的顺序排列，最多取前 5 篇。

A: Papers with AI summaries are prioritized, then ordered by appearance in data file, max 5 papers.

**Q: 可以改成 10 篇吗？**
**Q: Can I change it to 10 papers?**

A: 可以。在调用 `get_featured_papers()` 时设置 `top_n=10`。但注意 Feishu 卡片有长度限制。

A: Yes, set `top_n=10` when calling `get_featured_papers()`. Note Feishu cards have length limits.

**Q: 怎样同时发送精选文章和统计？**
**Q: How to send both featured papers and statistics?**

A: 调用两次 `send_daily_crawl_notification()` 函数，分别使用不同的 `mode` 参数。

A: Call `send_daily_crawl_notification()` twice with different `mode` parameters.

---

需要帮助？查看完整文档或运行演示脚本！

Need help? Check the full docs or run the demo script!
