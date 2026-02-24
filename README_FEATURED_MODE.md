# 飞书精选文章通知 - README 更新片段

> 将此内容添加到项目的主 README.md 中，以告知用户新增的功能

## 🚀 新功能：精选文章模式通知

### 功能介绍

将每日飞书通知从单纯的统计数据升级为**精选 5 篇高质量论文及其 AI 总结**，帮助您快速了解最有价值的研究成果。

#### 核心特性

- ✅ **AI 感知**: 优先展示包含 AI 总结的论文
- ✅ **智能精选**: 精选 5 篇最有价值的论文
- ✅ **自动处理**: 文本截断、格式化自动进行
- ✅ **双模式**: 支持精选文章和统计两种通知模式
- ✅ **跨平台**: Windows PowerShell 和 Linux/Mac Bash 完全支持
- ✅ **安全认证**: HMAC-SHA256 签名验证

### 快速开始

#### 第 1 步：查看演示（1 分钟）

```bash
python demo_featured_papers.py
```

这会展示如何从示例数据中提取精选论文。

#### 第 2 步：配置环境（2 分钟）

```bash
# 设置飞书 Webhook URL
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID"

# 可选：设置签名密钥
export FEISHU_SECRET="YOUR_SECRET_KEY"
```

#### 第 3 步：发送通知（1 分钟）

```bash
# 使用精选文章模式（默认）
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"

# 或集成到主工作流
bash run.sh          # Linux/Mac
.\run.ps1            # Windows PowerShell
```

### 使用示例

#### 命令行

```bash
# 精选文章模式（默认）- 展示 5 篇高质量论文
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode featured

# 统计模式 - 展示统计数据（向后兼容）
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics
```

#### Python 代码

```python
from utils.feishu import send_daily_crawl_notification

# 发送精选文章通知
success = send_daily_crawl_notification(
    data_file="data/2024-02-24.jsonl",
    date_str="2024-02-24",
    mode="featured"
)

if success:
    print("✅ 通知已发送到飞书")
```

### 飞书通知示例

#### 精选文章模式

```
📚 arXiv 精选论文 - 2024-02-24
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] Vision Transformers for Dense Prediction...
    cs.CV | Alice Smith, Bob Johnson, Charlie Brown
    🤖 Introduces Vision Transformers for dense tasks with improved efficiency

[2] Language Models as Zero-Shot Planners for Robotics
    cs.CL | Diana Prince, Eve Wilson
    🤖 Demonstrates LLMs can perform robot planning tasks zero-shot

[3] Efficient Attention Mechanisms for Large-Scale...
    cs.AI | Frank Miller, Grace Lee, Henry Zhang
    🤖 Proposes efficient attention reducing complexity from O(n²) to O(n log n)

... （还有 2 篇）

📅 更新时间: 2024-02-24 10:30:45
📖 数据源: arXiv + AI 增强分析
```

### 配置要求

#### 环境变量

```bash
# 必需
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID

# 可选（推荐用于签名验证）
FEISHU_SECRET=YOUR_SECRET_KEY
```

#### 数据文件格式

JSONL 格式，每行一个 JSON 对象：

```json
{
  "id": "2401.00001",
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "categories": ["cs.CV"],
  "abs": "https://arxiv.org/abs/2401.00001",
  "summary": "摘要内容",
  "AI": {
    "tldr": "AI 生成的一句话总结",
    "motivation": "研究动机",
    "method": "研究方法",
    "result": "研究结果",
    "conclusion": "研究结论"
  }
}
```

### 功能对比

| 功能 | 精选文章模式 | 统计模式 |
|-----|-----------|--------|
| 内容 | 5 篇论文 + AI 总结 | 统计数据 + 分类分布 |
| AI 感知 | ✅ 优先 AI 论文 | ❌ 不涉及 |
| 使用场景 | 日常通知、价值展示 | 数据分析、趋势观察 |
| 默认模式 | ✅ 是 | ❌ 否 |

### 常见问题

**Q: 没有 AI 总结的论文怎么办？**
A: 自动使用原始摘要的前 150 字符，仍会显示但不会有 🤖 标记。

**Q: 可以修改精选论文数量吗？**
A: 可以，在代码中修改 `get_featured_papers(data_file, top_n=10)` 即可。

**Q: 怎样在 Windows 上运行？**
A: 使用 PowerShell 运行 `.\run.ps1` 或 `python demo_featured_papers.py`。

**Q: 怎样同时发送两种模式？**
A: 调用两次 `send_daily_crawl_notification()` 函数，分别使用不同的 `mode` 参数。

### 完整文档

- 📖 [快速开始指南](QUICK_START_FEATURED_MODE.md) - 5 分钟上手
- 📖 [功能详解](FEISHU_FEATURED_PAPERS_MODE.md) - 深入了解
- 📖 [完成报告](IMPLEMENTATION_COMPLETE.md) - 项目总结
- 📖 [文档导航](DOCUMENTATION_INDEX.md) - 快速查询
- 📖 [完成清单](COMPLETION_CHECKLIST.md) - 验证清单

### 技术细节

- **语言**: Python 3.12+
- **认证**: HMAC-SHA256 签名验证
- **API**: Feishu Open API Webhook
- **格式**: Card Message with Markdown
- **兼容性**: Windows PowerShell + Linux/Mac Bash

---

**开始使用吧！** 🚀

```bash
python demo_featured_papers.py
```

---

## 相关文件变更

### 新增文件
- ✅ `demo_featured_papers.py` - 演示脚本
- ✅ `QUICK_START_FEATURED_MODE.md` - 快速开始
- ✅ `FEISHU_FEATURED_PAPERS_MODE.md` - 功能详解
- ✅ `FEATURED_PAPERS_SUMMARY.md` - 完整总结
- ✅ `IMPLEMENTATION_COMPLETE.md` - 完成报告
- ✅ `DOCUMENTATION_INDEX.md` - 文档导航
- ✅ `COMPLETION_CHECKLIST.md` - 完成清单

### 修改文件
- ✅ `utils/feishu.py` - 添加精选文章模式支持
- ✅ `run.sh` - 集成精选文章模式
- ✅ `run.ps1` - 集成精选文章模式

---

*最后更新: 2024 年 2 月*  
*版本: 1.0 稳定版*
