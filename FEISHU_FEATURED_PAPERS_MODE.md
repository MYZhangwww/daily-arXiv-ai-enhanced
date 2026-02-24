# 🎯 飞书通知 - 精选文章模式使用指南

## 📋 新增功能说明

飞书通知功能现已支持**两种模式**：

### 1️⃣ 精选文章模式（推荐）✨ 

**模式名**: `featured` (默认)

**功能**: 发送精选的 5 篇文章，包含每篇文章的：
- 文章标题
- 作者信息
- 文章分类
- AI 生成的 TL;DR 总结

**特点**:
- 优先使用有 AI 总结的论文
- 展示 AI 分析标记 🤖
- 信息更加丰富和有用

### 2️⃣ 统计信息模式

**模式名**: `statistics`

**功能**: 发送统计信息（原始模式），包含：
- 爬取论文总数
- 分类统计
- 首尾论文标题

---

## 🚀 使用方式

### 方式 1: 使用默认模式（精选文章）

```powershell
# Windows PowerShell
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"

# Linux/Mac
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"
```

### 方式 2: 指定统计信息模式

```powershell
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics
```

### 方式 3: 显式指定精选文章模式

```powershell
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode featured
```

---

## 📊 消息示例

### 精选文章模式 (featured)

```
📚 arXiv 精选论文 - 2024-02-24
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

更新日期: 2024-02-24
精选论文数: 5

论文 1:
[1] Vision Transformers for Dense Prediction Tasks in Computer Vision
分类: cs.CV | 作者: Alice Smith, Bob Johnson, Charlie Brown
摘要: 🤖 This paper proposes an efficient transformer-based approach for dense prediction tasks...

论文 2:
[2] Language Models as Zero-Shot Planners for Robotics
分类: cs.CL | 作者: Diana Prince, Eve Wilson
摘要: 🤖 Large language models can be effectively used for robotics planning without task-specific...

...以此类推...

通知时间: 2024-02-24 10:23:45
数据来源: arXiv + AI 增强分析
```

### 统计信息模式 (statistics)

```
🤖 arXiv 每日爬取统计 - 2024-02-24
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

爬取日期: 2024-02-24
总论文数: 127
分类统计 (TOP 5): cs.CV: 45, cs.CL: 32, cs.AI: 28, cs.RO: 15, cs.GR: 7
首篇论文: Vision Transformers for Dense Prediction...
最后论文: Language Models as Zero-Shot Planners...
爬取完成时间: 2024-02-24 10:23:45
```

---

## 🔧 与 run.sh/run.ps1 的集成

在 `run.sh` 或 `run.ps1` 中，飞书通知会自动使用**精选文章模式**：

```bash
# run.sh 中的调用
python utils/feishu.py --data "data/${today}.jsonl" --date "$today"
# 相当于
python utils/feishu.py --data "data/${today}.jsonl" --date "$today" --mode featured
```

---

## 📝 如何修改默认模式

如果想修改 `run.sh`/`run.ps1` 使用统计模式，编辑相应文件：

**run.sh 中**:
```bash
# 改为这样
python utils/feishu.py --data "data/${today}.jsonl" --date "$today" --mode statistics
```

**run.ps1 中**:
```powershell
# 改为这样
python utils/feishu.py --data $dataFile --date $today --mode statistics
```

---

## 🎯 什么时候用哪个模式？

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 日常使用 | featured | 展示精选内容，更有价值 |
| 监控爬取数量 | statistics | 快速了解爬取规模 |
| 质量检查 | featured | 看到具体论文质量 |
| 自动化上报 | statistics | 简洁高效 |

---

## 💡 高级用法

### 仅测试功能

```powershell
# 测试精选文章模式
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode featured

# 测试统计模式
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics
```

### Python 中直接调用

```python
from utils.feishu import send_daily_crawl_notification

# 发送精选文章
send_daily_crawl_notification("data/2024-02-24.jsonl", "2024-02-24", mode="featured")

# 发送统计信息
send_daily_crawl_notification("data/2024-02-24.jsonl", "2024-02-24", mode="statistics")
```

---

## 🔍 数据要求

### 精选文章模式 (featured)

**数据文件**: 任何包含论文信息的 JSONL 文件

**字段要求**:
```json
{
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "categories": ["cs.CV"],
  "abs": "https://arxiv.org/abs/...",
  "summary": "论文摘要",
  "AI": {
    "tldr": "AI 生成的 TL;DR"  // 可选，如有则优先使用
  }
}
```

**优先级**:
1. 优先选择有 `AI.tldr` 的论文
2. 如果没有 AI 总结，使用 `summary` 字段
3. 最多显示 5 篇论文

### 统计信息模式 (statistics)

**数据文件**: 任何包含论文信息的 JSONL 文件

**字段要求**:
```json
{
  "title": "论文标题",
  "categories": ["cs.CV"],
  "authors": ["作者1"]
}
```

---

## ✅ 检查清单

- [ ] 飞书 Webhook URL 已配置
- [ ] 飞书 Secret 已配置（可选）
- [ ] 数据文件路径正确
- [ ] Python 环境已就绪
- [ ] 依赖已安装：`pip install requests`

---

## 🆘 常见问题

### Q: 为什么没有看到 AI 总结？

A: AI 总结需要先运行 `ai/enhance.py` 来处理数据。检查数据文件中是否有 `AI` 字段。

### Q: 如何只显示 3 篇论文而不是 5 篇？

A: 修改 `utils/feishu.py` 中的 `get_featured_papers(data_file, top_n=3)` 参数。

### Q: 可以自定义论文的选择标准吗？

A: 可以，修改 `get_featured_papers()` 函数中的筛选逻辑。

### Q: 消息字数太多会怎样？

A: 飞书卡片消息有字数限制。代码已自动截断标题（60字）和摘要（150字）。

---

## 📚 相关文档

- **完整飞书指南**: [FEISHU_SETUP.md](../FEISHU_SETUP.md)
- **快速参考**: [FEISHU_QUICK_REFERENCE.md](../FEISHU_QUICK_REFERENCE.md)
- **源代码**: [utils/feishu.py](./feishu.py)

---

## 🎉 新增功能亮点

✨ **双模式支持** - 灵活选择通知内容  
✨ **AI 感知** - 自动检测和展示 AI 总结  
✨ **智能截断** - 自动处理长文本  
✨ **信息丰富** - 展示题目、作者、分类、总结  
✨ **向后兼容** - 原有功能保持不变  

---

**祝你使用愉快！** 🚀
