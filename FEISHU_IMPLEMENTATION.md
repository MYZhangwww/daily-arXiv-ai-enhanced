# 飞书通知功能实现说明 / Feishu Notification Feature Implementation

## 📋 概述 / Overview

本次更新为 daily-arXiv-ai-enhanced 项目添加了 **飞书机器人通知功能**。每当项目完成数据爬取后，会自动通过飞书机器人向指定群组发送爬取统计信息。

This update adds **Feishu robot notification feature** to the daily-arXiv-ai-enhanced project. After crawling papers, the project automatically sends crawl statistics to Feishu groups via robot.

## 🎯 核心特性 / Key Features

✅ **安全的签名校验** - HMAC-SHA256 签名验证，确保消息来自可信源
✅ **Signature Verification** - HMAC-SHA256 signature validation for message authenticity

✅ **富文本卡片消息** - 支持 Markdown 格式的精美消息展示
✅ **Rich Card Messages** - Beautiful message display with Markdown support

✅ **详细统计信息** - 自动收集：总论文数、分类统计、论文标题等
✅ **Detailed Statistics** - Auto-collect: total papers, category stats, paper titles, etc.

✅ **灵活的集成** - 可选功能，不依赖其他模块
✅ **Flexible Integration** - Optional feature, no dependency on other modules

✅ **完整文档** - 详细的部署和使用指南
✅ **Complete Documentation** - Comprehensive deployment and usage guides

## 📦 新增文件 / New Files

### 核心模块 / Core Module
- **`utils/feishu.py`** - 飞书机器人模块（包含签名校验、消息发送等）
  - `FeishuRobot` 类：封装飞书 API 操作
  - `get_crawl_statistics()` 函数：从数据文件提取统计信息
  - `send_daily_crawl_notification()` 函数：发送每日爬取通知
  - 命令行入口支持独立执行

### 文档和示例 / Documentation & Examples
- **`FEISHU_SETUP.md`** - 详细的飞书配置指南
  - 创建飞书机器人步骤
  - 环境变量配置方法
  - 故障排查指南
  - 技术实现细节

- **`GITHUB_ACTIONS_FEISHU.md`** - GitHub Actions 集成指南
  - 在 CI/CD 中配置飞书通知
  - 完整的 workflow 示例
  - 常见问题解决

- **`.env.feishu.example`** - 环境变量配置示例文件
  - Webhook URL 示例
  - Secret 密钥示例

### 测试工具 / Testing Tools
- **`test_feishu.py`** - 全面的测试套件
  - 签名生成测试
  - 消息构建测试
  - 环境变量检查
  - 完整工作流测试

## 🔄 工作流程 / Workflow

```
┌─────────────────┐
│  爬取 arXiv 论文  │
│  Crawl arXiv    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   去重检查      │
│  Dedup check    │
└────────┬────────┘
         │
         ↓
  [NEW] ┌──────────────────────┐
    ──→ │ 发送飞书通知        │ ← FEISHU_WEBHOOK_URL
        │ Send Feishu notif.   │   FEISHU_SECRET
        └──────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
         ↓                   ↓
    [继续工作流]      [忽略错误,继续]
    [Continue]       [Ignore error]
         │                   │
         └─────────┬─────────┘
                   ↓
        ┌──────────────────┐
        │  AI 增强处理     │
        │  AI enhancement  │
        └──────────┬───────┘
                   ↓
        ┌──────────────────┐
        │  Markdown 转换   │
        │  Markdown conv.  │
        └──────────────────┘
```

## 🚀 快速开始 / Quick Start

### 本地测试 / Local Testing

1. **设置环境变量** / Set environment variables

   ```bash
   export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/..."
   export FEISHU_SECRET="your-secret-here"
   ```

2. **运行测试脚本** / Run test script

   ```bash
   python test_feishu.py
   ```

3. **运行主流程** / Run main workflow

   ```bash
   bash run.sh
   ```

### GitHub Actions 部署 / GitHub Actions Deployment

1. 进入 Settings → Secrets and variables → Actions
2. 创建 `FEISHU_WEBHOOK_URL` 和 `FEISHU_SECRET` secrets
3. 修改 `.github/workflows/run.yml`，添加环境变量
4. 提交更改，工作流自动运行

详见：[GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md)

## 📝 核心代码结构 / Core Code Structure

### `utils/feishu.py`

```python
class FeishuRobot:
    """飞书机器人类"""
    
    def __init__(self, webhook_url: str, secret: Optional[str] = None):
        """初始化机器人，支持可选的签名校验"""
    
    def _generate_signature(self) -> tuple:
        """生成 HMAC-SHA256 签名和时间戳"""
    
    def send_text_message(self, content: str) -> bool:
        """发送文本消息"""
    
    def send_card_message(self, title: str, content_dict: Dict) -> bool:
        """发送卡片消息（默认使用此方法）"""

def send_daily_crawl_notification(data_file: str, date_str: str) -> bool:
    """主入口：发送每日爬取统计通知"""
```

### `run.sh` 集成

```bash
# 在去重检查后添加
if [ -n "$FEISHU_WEBHOOK_URL" ]; then
    python utils/feishu.py --data "data/${today}.jsonl" --date "$today"
fi
```

## 🔐 安全性 / Security

### 签名校验流程 / Signature Verification Process

```
1. 获取当前时间戳 / Get current timestamp
2. 构造签名串: "{timestamp}\n{secret}"
3. 计算 HMAC-SHA256: hmac_code = HMAC_SHA256(签名串, secret)
4. Base64 编码: sign = base64_encode(hmac_code)
5. 添加到 URL: {webhook_url}&timestamp={timestamp}&sign={sign}
6. 飞书服务器验证签名的正确性
```

### 敏感信息处理 / Sensitive Information Handling

- ✅ 密钥从环境变量读取，不写入代码
- ✅ 不记录密钥到日志
- ✅ 使用 GitHub Secrets 存储敏感信息
- ✅ 支持本地和 CI/CD 环境

## 📊 消息示例 / Message Example

飞书群会收到类似以下的消息：

```
🤖 arXiv 每日爬取统计 - 2024-12-15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

爬取日期: 2024-12-15
总论文数: 127
分类统计 (TOP 5): cs.CV: 45, cs.CL: 32, cs.AI: 28, cs.RO: 15, cs.GR: 7
首篇论文: Vision Transformers for Dense Prediction Tasks...
最后论文: Language Models as Zero-Shot Planners...
爬取完成时间: 2024-12-15 10:23:45
```

## 🧪 测试覆盖 / Test Coverage

运行 `python test_feishu.py` 进行以下测试：

| 测试 | 说明 |
|------|------|
| 签名生成 | 验证 HMAC-SHA256 签名生成 |
| 消息构建 | 验证统计信息提取和消息格式 |
| 环境变量 | 检查 Webhook URL 和 Secret 配置 |
| 完整工作流 | 如已配置，发送真实通知（可选） |

## 🔧 依赖项 / Dependencies

### 新增依赖 / New Dependency
- `requests>=2.31.0` - HTTP 库（用于发送 Webhook 请求）

已添加到 `pyproject.toml`。

### 标准库 / Standard Library
- `json` - JSON 处理
- `hmac`, `hashlib` - 签名生成
- `time`, `datetime` - 时间处理
- `os`, `sys`, `pathlib` - 文件和系统操作

## 📚 相关文档 / Related Documentation

1. **详细配置指南**: [FEISHU_SETUP.md](./FEISHU_SETUP.md)
   - 飞书机器人创建步骤
   - 本地和云端配置方法
   - 故障排查指南
   - 技术细节说明

2. **GitHub Actions 集成**: [GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md)
   - CI/CD 配置示例
   - 完整的 workflow 文件
   - 常见问题解答

3. **环境变量示例**: [.env.feishu.example](./.env.feishu.example)
   - 配置模板

4. **飞书 API 文档**: [https://open.feishu.cn/document/client-docs/bot-v3](https://open.feishu.cn/document/client-docs/bot-v3)

## ❓ 常见问题 / FAQ

**Q: 如果飞书通知失败，会影响主流程吗？**  
A: 不会。通知失败只会打印警告，不影响数据爬取和处理流程。

**Q: Secret 密钥是可选的吗？**  
A: 可选，但建议配置。未配置 Secret 时，消息将不进行签名校验。

**Q: 支持其他消息格式吗？**  
A: 支持。`feishu.py` 提供了 `send_text_message()` 和 `send_card_message()` 两种方法。

**Q: 可以自定义消息内容吗？**  
A: 可以。修改 `send_daily_crawl_notification()` 函数中的 `message_content` 字典。

## 🤝 贡献 / Contributing

欢迎提交 issue 或 pull request 来改进此功能！

Feel free to submit issues or pull requests to improve this feature!

## 📄 许可证 / License

本功能模块遵循原项目的 Apache-2.0 许可证。

This feature module follows the Apache-2.0 license of the original project.
