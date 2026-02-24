# GitHub Actions 飞书通知配置示例 / GitHub Actions Feishu Notification Configuration Example

## 如何在 .github/workflows/run.yml 中配置飞书通知

### 步骤 1：添加环境变量到 Secrets

1. 进入仓库 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 创建以下两个 Secrets：

| Secret 名称 | 值 | 说明 |
|-----------|---|----|
| FEISHU_WEBHOOK_URL | https://open.feishu.cn/open-apis/bot/v2/hook/... | 飞书机器人 Webhook URL |
| FEISHU_SECRET | your-secret-here | 飞书机器人密钥（来自"加签"设置） |

### 步骤 2：修改 .github/workflows/run.yml

在 `jobs` 部分添加 `env` 环境变量声明：

```yaml
name: arXiv-daily-ai-enhanced

on:
  schedule:
    - cron: "0 8 * * *"  # Every day at 8 UTC
  workflow_dispatch:

jobs:
  crawl-and-enhance:
    runs-on: ubuntu-latest
    env:
      # 现有环境变量...
      # Existing environment variables...
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      OPENAI_BASE_URL: ${{ secrets.OPENAI_BASE_URL }}
      
      # 新增：飞书通知配置 / New: Feishu notification configuration
      FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
      FEISHU_SECRET: ${{ secrets.FEISHU_SECRET }}
      
    steps:
      # ... 其他步骤 / Other steps ...
      
      - name: Run local test script
        run: bash run.sh
        # 现在 run.sh 会自动检测 FEISHU_WEBHOOK_URL 并发送通知
        # Now run.sh will automatically detect FEISHU_WEBHOOK_URL and send notifications
```

### 步骤 3：获取飞书 Webhook URL 和密钥

1. **打开飞书群组**
   - Open Feishu group

2. **群设置 → 群机器人**
   - Group Settings → Group Robots

3. **创建机器人**
   - Create Robot
   - 选择 "自定义机器人" / Select "Custom Robot"

4. **配置机器人**
   - 输入机器人名称 / Enter robot name
   - **重要**：勾选 "加签" (Enable Signature Verification)
   
5. **复制凭证**
   - Webhook URL: `https://open.feishu.cn/open-apis/bot/v2/hook/{HOOK_ID}`
   - Secret: 在"加签"后显示的密钥值

### 步骤 4：测试配置

提交更改后，你可以：

1. 手动触发工作流：
   ```
   Actions → arXiv-daily-ai-enhanced → Run workflow
   ```

2. 查看工作流日志：
   ```
   Actions → 选择最新的 run → 查看 "Run local test script" 步骤的输出
   ```

3. 检查飞书群消息：
   - 如果配置正确，你应该在群里看到爬取统计消息

### 完整的 run.yml 示例

```yaml
name: arXiv-daily-ai-enhanced

on:
  schedule:
    - cron: "0 8 * * *"
  workflow_dispatch:

jobs:
  crawl-and-enhance:
    runs-on: ubuntu-latest
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      OPENAI_BASE_URL: ${{ secrets.OPENAI_BASE_URL }}
      FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
      FEISHU_SECRET: ${{ secrets.FEISHU_SECRET }}

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Run local test script
        run: bash run.sh
        
      - name: Commit and push if changed
        run: |
          git config user.email "your-email@example.com"
          git config user.name "Your Name"
          git add -A
          git commit -m "Update arXiv papers" || exit 0
          git push
```

## 故障排查 / Troubleshooting

### 问题 1: 飞书没有收到消息

检查清单 / Checklist:
- [ ] FEISHU_WEBHOOK_URL 是否正确配置到 Secrets
- [ ] FEISHU_SECRET 是否正确配置到 Secrets
- [ ] 机器人是否被添加到了群组
- [ ] 查看 Actions 日志中的错误信息

### 问题 2: "signature verification failed"

这表示密钥不匹配。检查：
- [ ] Secret 是否完全复制（包括所有字符）
- [ ] 飞书群组是否有 Webhook URL 更新

### 问题 3: 工作流执行成功但没有消息

检查：
- [ ] 爬取是否真的成功了（查看日志 "Step 2: Performing deduplication"）
- [ ] 数据文件是否存在
- [ ] 网络连接是否正常

## 消息示例 / Message Example

飞书群会收到如下格式的消息：

```
🤖 arXiv 每日爬取统计 - 2024-12-15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
爬取日期: 2024-12-15
总论文数: 127
分类统计 (TOP 5): cs.CV: 45, cs.CL: 32, cs.AI: 28, cs.RO: 15, cs.GR: 7
首篇论文: Vision Transformers for Dense...
最后论文: Language Models as Zero-Shot...
爬取完成时间: 2024-12-15 10:23:45 UTC
```

## 可选：仅在爬取新内容时发送通知

如果你只想在有新论文时才发送通知，可以修改 `run.sh`：

```bash
# 在 Step 2 成功后发送通知
case $dedup_exit_code in
    0)
        # 有新内容 - 发送通知 / Has new content - send notification
        if [ -n "$FEISHU_WEBHOOK_URL" ]; then
            python utils/feishu.py --data "data/${today}.jsonl" --date "$today"
        fi
        ;;
    1)
        # 无新内容 - 不发送通知 / No new content - don't send notification
        exit 1
        ;;
esac
```

## 需要帮助？

参考以下资源：
- [FEISHU_SETUP.md](../FEISHU_SETUP.md) - 详细的飞书配置指南
- [utils/feishu.py](../utils/feishu.py) - 飞书模块源代码
- [Feishu 开放平台文档](https://open.feishu.cn/document/client-docs/bot-v3)
