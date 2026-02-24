# 飞书通知功能使用指南 / Feishu Notification User Guide

## 功能概述 / Overview

本功能允许项目在每日爬取 arXiv 论文后，通过飞书(Feishu)机器人将爬取统计信息发送到指定的飞书群组。

This feature allows the project to send daily arXiv crawl statistics to a specified Feishu group via Feishu robot after crawling papers.

## 功能特点 / Features

✅ **签名校验** - 支持飞书机器人的签名校验，提高消息安全性  
✅ **Signature Verification** - Support Feishu robot signature verification for enhanced security

✅ **卡片消息** - 支持富文本卡片消息格式，展现更丰富的信息  
✅ **Card Messages** - Support rich text card message format with more information

✅ **统计信息** - 自动统计并展示：总论文数、分类统计(TOP 5)、首尾论文标题等  
✅ **Statistics** - Automatically collect and display: total papers, category statistics (TOP 5), first/last paper titles, etc.

✅ **错误处理** - 友好的错误提示，不影响主流程  
✅ **Error Handling** - Friendly error messages without affecting main workflow

## 配置步骤 / Setup Steps

### 1. 创建飞书自定义机器人 / Create Feishu Custom Robot

1. 打开飞书群组，点击右上角"群设置" → "群机器人"  
   Open Feishu group, click "Group Settings" → "Group Robots" in top-right corner

2. 点击"创建机器人" → "自定义机器人"  
   Click "Create Robot" → "Custom Robot"

3. 输入机器人名称，选择一个头像（可选）  
   Enter robot name and select avatar (optional)

4. **重要**：勾选 "加签" (Signature Verification)  
   **Important**: Check "Signature Verification" option

5. 复制生成的 Webhook URL 和 Secret Key

### 2. 配置环境变量 / Configure Environment Variables

#### 方式一：本地测试（修改 run.sh） / Method 1: Local Testing (Modify run.sh)

编辑 `run.sh`，在环境变量定义部分添加：

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxx"
export FEISHU_SECRET="your-secret-here"
```

#### 方式二：GitHub Actions（推荐） / Method 2: GitHub Actions (Recommended)

1. 进入仓库 Settings → Secrets and variables → Actions
2. 创建两个 Secret：
   - `FEISHU_WEBHOOK_URL`: 飞书 Webhook URL
   - `FEISHU_SECRET`: 飞书机器人密钥

3. 修改 `.github/workflows/run.yml`，在 jobs 中添加环境变量：

```yaml
jobs:
  crawl-and-enhance:
    runs-on: ubuntu-latest
    env:
      FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
      FEISHU_SECRET: ${{ secrets.FEISHU_SECRET }}
```

## 工作流程 / Workflow

在 `run.sh` 中，飞书通知会在以下时机触发：

```
1. 爬取数据 (Crawl data)
   ↓
2. 去重检查 (Duplicate check)
   ↓
3. [新增] 发送飞书通知 ← 告知爬取结果
   ↓
4. AI 增强处理 (AI enhancement) [可选]
   ↓
5. Markdown 转换 (Markdown conversion)
   ↓
6. 更新文件列表 (Update file list)
```

## 消息示例 / Message Example

发送的飞书消息包含以下信息：

```
🤖 arXiv 每日爬取统计 - 2024-12-15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
爬取日期: 2024-12-15
总论文数: 127
分类统计 (TOP 5): cs.CV: 45, cs.CL: 32, cs.AI: 28, cs.RO: 15, cs.GR: 7
首篇论文: Vision Transformers for Dense Prediction...
最后论文: Language Models as Zero-Shot Planners...
爬取完成时间: 2024-12-15 10:23:45
```

## 技术细节 / Technical Details

### 签名校验算法 / Signature Verification Algorithm

飞书使用以下算法校验签名：

```python
timestamp = int(time.time())
string_to_sign = f"{timestamp}\n{secret}"
hmac_code = hmac.new(
    string_to_sign.encode(),
    digestmod=hashlib.sha256
).digest()
sign = base64.b64encode(hmac_code).decode()
```

签名和时间戳作为 URL 参数添加：

```
{webhook_url}&timestamp={timestamp}&sign={sign}
```

### 支持的消息格式 / Supported Message Formats

- **文本消息** (text): 简单文本内容
- **卡片消息** (interactive): 富文本格式，支持 Markdown 语法

本项目使用卡片消息格式来展现更丰富的信息。

## 故障排查 / Troubleshooting

### 问题1：收不到消息
**Problem 1: Not receiving messages**

检查以下项目：
- [ ] Webhook URL 是否正确复制
- [ ] 机器人是否被添加到群组
- [ ] Secret Key 是否正确配置
- [ ] 网络连接是否正常

Check:
- [ ] Is Webhook URL copied correctly?
- [ ] Is robot added to the group?
- [ ] Is Secret Key configured correctly?
- [ ] Is network connection normal?

### 问题2：消息格式错误
**Problem 2: Message format error**

这通常是由于飞书 API 返回错误。查看日志中的错误信息，确认：
- [ ] 飞书 API Key 是否过期
- [ ] 卡片格式是否符合飞书要求

This is usually due to Feishu API error. Check:
- [ ] Is API Key expired?
- [ ] Does card format comply with Feishu requirements?

### 问题3：签名校验失败
**Problem 3: Signature verification failed**

确保：
- [ ] Secret Key 完全正确（包括空格）
- [ ] 系统时间精确（差异应在 60s 以内）

Make sure:
- [ ] Secret Key is exactly correct (including spaces)
- [ ] System time is accurate (within 60s difference)

## 可选功能：仅发送文本消息 / Optional: Send Text Message Only

如果只想发送简单的文本消息，可以在 `utils/feishu.py` 中使用 `send_text_message()` 方法。

编辑 `utils/feishu.py`，修改 `send_daily_crawl_notification()` 函数：

```python
# 使用文本消息而非卡片消息
text_content = f"🤖 arXiv 每日爬取统计\n日期: {date_str}\n论文总数: {stats['总论文数']}"
success = robot.send_text_message(text_content)
```

## 相关资源 / Resources

- [飞书开放平台 - 机器人文档](https://open.feishu.cn/document/client-docs/bot-v3)
- [飞书卡片消息格式](https://open.feishu.cn/document/common-capabilities/message-card)
- [HMAC-SHA256 签名说明](https://open.feishu.cn/document/common-capabilities/message-card/security-instructions)

## 常见用途 / Common Use Cases

1. **团队协作**: 通知团队每天爬取的最新论文数量和分类
2. **监控统计**: 跟踪爬取的论文数量变化趋势
3. **自动告警**: 当论文数量异常时发送警告
4. **知识分享**: 在飞书群组内分享最新的学术动态

## 许可证 / License

本功能模块遵循原项目的 Apache-2.0 许可证。
This feature module follows the Apache-2.0 license of the original project.
