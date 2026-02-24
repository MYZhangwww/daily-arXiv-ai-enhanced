# 📚 飞书通知功能 - 文档索引 / Documentation Index

## 🎯 根据你的需求快速找到答案

### "我想快速开始" / "I want to get started quickly"
👉 **[FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md)** (5 分钟)
- 5 分钟快速开始
- 常用命令
- 快速故障排查

### "我不知道怎样创建飞书机器人" / "I don't know how to create Feishu robot"
👉 **[FEISHU_SETUP.md](./FEISHU_SETUP.md)** (20 分钟)
- 创建飞书机器人详细步骤
- 配置环境变量
- 工作流程说明
- 完整故障排查指南

### "我需要在 GitHub Actions 中使用此功能" / "I need to use this in GitHub Actions"
👉 **[GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md)** (15 分钟)
- GitHub Actions 配置步骤
- 完整 workflow 示例
- Secrets 管理
- CI/CD 最佳实践

### "我想了解技术实现细节" / "I want to understand technical details"
👉 **[FEISHU_IMPLEMENTATION.md](./FEISHU_IMPLEMENTATION.md)** (30 分钟)
- 项目概述
- 工作流程图
- 核心代码结构
- 安全性说明
- FAQ 常见问题

### "我想看项目实现的总结" / "I want to see implementation summary"
👉 **[FEISHU_IMPLEMENTATION_SUMMARY.md](./FEISHU_IMPLEMENTATION_SUMMARY.md)** (10 分钟)
- 功能实现完成情况
- 新增文件清单
- 代码统计
- 实现清单

### "我想查看源代码" / "I want to see source code"
👉 **[utils/feishu.py](./utils/feishu.py)** (详细注释)
- 完整的飞书 API 封装
- HMAC-SHA256 签名实现
- 消息发送逻辑
- 详细的代码注释

### "我想测试配置是否正确" / "I want to test if configuration is correct"
👉 **[test_feishu.py](./test_feishu.py)** (运行脚本)
```bash
python test_feishu.py
```

### "我想手动发送一条通知" / "I want to send a notification manually"
👉 **[send_feishu_notification.sh](./send_feishu_notification.sh)** (运行脚本)
```bash
bash send_feishu_notification.sh data/2024-12-15.jsonl
```

### "我想看环境变量配置示例" / "I want to see environment variable example"
👉 **[.env.feishu.example](./.env.feishu.example)**
```bash
export FEISHU_WEBHOOK_URL="..."
export FEISHU_SECRET="..."
```

---

## 📖 文档导览地图 / Documentation Navigation Map

```
入门 (Get Started)
├── 5分钟快速开始 → FEISHU_QUICK_REFERENCE.md ✨ START HERE
├── 创建飞书机器人 → FEISHU_SETUP.md
├── GitHub Actions → GITHUB_ACTIONS_FEISHU.md
└── 环境变量示例 → .env.feishu.example

理解 (Understanding)
├── 技术细节 → FEISHU_IMPLEMENTATION.md
├── 项目总结 → FEISHU_IMPLEMENTATION_SUMMARY.md
├── 源代码 → utils/feishu.py
└── 快速参考 → FEISHU_QUICK_REFERENCE.md

实践 (Practice)
├── 测试配置 → test_feishu.py
├── 发送通知 → send_feishu_notification.sh
├── 查看日志 → run.sh (查看输出)
└── 修改 workflow → .github/workflows/run.yml
```

---

## 🚀 场景导引 / Scenario Guide

### 场景 1: "我是第一次使用，需要完整指导"
**我的步骤** / My Steps:
1. 阅读 [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md) - 5 分钟快速开始部分
2. 按照步骤创建飞书机器人
3. 配置环境变量
4. 运行 `python test_feishu.py` 测试
5. 运行 `bash run.sh` 完整测试
6. 遇到问题？参考 [FEISHU_SETUP.md](./FEISHU_SETUP.md)

**预计时间** / Est. Time: 30-45 分钟

### 场景 2: "我只想快速配置然后就用，不关心细节"
**我的步骤** / My Steps:
1. 快速阅读 [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md)
2. 按步骤 1-4 执行
3. 完成！

**预计时间** / Est. Time: 15 分钟

### 场景 3: "我需要在 GitHub Actions 中使用"
**我的步骤** / My Steps:
1. 阅读 [GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md)
2. 在 GitHub 中配置 Secrets
3. 修改 `.github/workflows/run.yml`
4. 提交更改测试

**预计时间** / Est. Time: 20 分钟

### 场景 4: "配置完了但不工作，我需要排查问题"
**我的步骤** / My Steps:
1. 运行 `python test_feishu.py` 看具体错误
2. 查阅 [FEISHU_SETUP.md](./FEISHU_SETUP.md) 的故障排查部分
3. 如果还没解决，查看 [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md) 的故障排查表

**预计时间** / Est. Time: 10-20 分钟

### 场景 5: "我想自定义消息内容"
**我的步骤** / My Steps:
1. 查看 [utils/feishu.py](./utils/feishu.py)
2. 找到 `send_daily_crawl_notification()` 函数
3. 修改 `message_content` 字典
4. 查看 [FEISHU_IMPLEMENTATION.md](./FEISHU_IMPLEMENTATION.md) 的卡片格式说明

**预计时间** / Est. Time: 15 分钟

---

## 📋 快速检查表 / Quick Checklist

### 首次配置 / First Time Setup

- [ ] 阅读了 [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md)
- [ ] 在飞书创建了自定义机器人
- [ ] 复制了 Webhook URL
- [ ] 复制了 Secret 密钥
- [ ] 设置了环境变量 `FEISHU_WEBHOOK_URL`
- [ ] 设置了环境变量 `FEISHU_SECRET`
- [ ] 运行了 `python test_feishu.py`
- [ ] 所有测试都通过了
- [ ] 运行了 `bash run.sh` 进行完整测试
- [ ] 收到了飞书群的通知消息

### GitHub Actions 配置 / GitHub Actions Setup

- [ ] 创建了 `FEISHU_WEBHOOK_URL` secret
- [ ] 创建了 `FEISHU_SECRET` secret
- [ ] 修改了 `.github/workflows/run.yml`
- [ ] 添加了环境变量到 `env` 部分
- [ ] 提交并推送了更改
- [ ] 手动触发了 workflow 进行测试
- [ ] 在飞书群中收到了通知

---

## 🔗 外部资源 / External Resources

### 官方文档 / Official Documentation
- [飞书开放平台](https://open.feishu.cn/document/client-docs/bot-v3)
- [飞书机器人 API](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)
- [飞书卡片消息](https://open.feishu.cn/document/common-capabilities/message-card)
- [HMAC-SHA256 签名](https://open.feishu.cn/document/common-capabilities/message-card/security-instructions)

### 相关技术
- [Python requests 库](https://docs.python-requests.org/)
- [HMAC-SHA256 概念](https://en.wikipedia.org/wiki/HMAC)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

## 🎓 学习路径 / Learning Path

### 初级 (Beginner)
1. [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md) - 快速开始
2. [.env.feishu.example](./.env.feishu.example) - 看看配置
3. [send_feishu_notification.sh](./send_feishu_notification.sh) - 了解使用方式

### 中级 (Intermediate)
4. [FEISHU_SETUP.md](./FEISHU_SETUP.md) - 深入配置
5. [GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md) - CI/CD 集成
6. [test_feishu.py](./test_feishu.py) - 了解测试

### 高级 (Advanced)
7. [FEISHU_IMPLEMENTATION.md](./FEISHU_IMPLEMENTATION.md) - 技术细节
8. [utils/feishu.py](./utils/feishu.py) - 源代码分析
9. [FEISHU_IMPLEMENTATION_SUMMARY.md](./FEISHU_IMPLEMENTATION_SUMMARY.md) - 项目总结

---

## ❓ 常见问题快速链接 / Common Questions Quick Links

| 问题 | 答案位置 |
|------|---------|
| 如何创建飞书机器人？ | [FEISHU_SETUP.md](./FEISHU_SETUP.md#1-创建飞书自定义机器人) |
| 如何配置环境变量？ | [FEISHU_SETUP.md](./FEISHU_SETUP.md#2-配置环境变量) |
| GitHub Actions 怎样配置？ | [GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md) |
| 签名校验怎样工作？ | [FEISHU_IMPLEMENTATION.md](./FEISHU_IMPLEMENTATION.md#签名校验算法) |
| 为什么收不到消息？ | [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md#故障排查快速指南) |
| 可以自定义消息吗？ | [FEISHU_IMPLEMENTATION.md](./FEISHU_IMPLEMENTATION.md#可选功能仅发送文本消息) |
| 如何测试配置？ | [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md#常用命令) |

---

## 📞 获取帮助 / Get Help

### 如果....... / If...

| 情况 | 查看文档 | 运行命令 |
|------|---------|---------|
| 遇到错误 | [FEISHU_SETUP.md](./FEISHU_SETUP.md#故障排查) | `python test_feishu.py` |
| 不知道从何开始 | [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md) | - |
| 想了解细节 | [FEISHU_IMPLEMENTATION.md](./FEISHU_IMPLEMENTATION.md) | - |
| 需要配置帮助 | [FEISHU_SETUP.md](./FEISHU_SETUP.md) | - |
| GitHub Actions 问题 | [GITHUB_ACTIONS_FEISHU.md](./GITHUB_ACTIONS_FEISHU.md) | - |

---

## 🎯 推荐阅读顺序 / Recommended Reading Order

**对于新用户 / For New Users:**
```
FEISHU_QUICK_REFERENCE.md (5 min)
    ↓
FEISHU_SETUP.md (20 min)
    ↓
运行测试 / Run test_feishu.py
    ↓
运行主流程 / Run run.sh
    ↓
完成！ / Done!
```

**对于开发者 / For Developers:**
```
FEISHU_QUICK_REFERENCE.md (5 min)
    ↓
FEISHU_IMPLEMENTATION.md (30 min)
    ↓
utils/feishu.py (源代码分析)
    ↓
自定义和扩展
```

**对于 DevOps / For DevOps:**
```
FEISHU_QUICK_REFERENCE.md (5 min)
    ↓
GITHUB_ACTIONS_FEISHU.md (15 min)
    ↓
修改 .github/workflows/run.yml
    ↓
测试和部署
```

---

**💡 贴士**: 将此索引文件加入书签，以便快速导航到你需要的文档！

**Tip**: Bookmark this index file for quick navigation to the documentation you need!
