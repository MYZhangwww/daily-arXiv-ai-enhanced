# 🪟 Windows 快速开始（3分钟）

## ⚡ 最快的方式：仅测试飞书功能

你无需 bash，直接在 Windows PowerShell 中运行 Python！

### 步骤 1: 打开 PowerShell

```
Win + X → 选择 Windows PowerShell 或 PowerShell
```

### 步骤 2: 进入项目目录

```powershell
cd e:\VibeCoding\daily-arXiv-ai-enhanced
```

### 步骤 3: 设置飞书配置

```powershell
$env:FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/..."
$env:FEISHU_SECRET = "your-secret-here"
```

### 步骤 4: 运行测试

```powershell
python test_feishu.py
```

✅ **完成！** 脚本会测试你的配置。

---

## 🚀 运行完整流程

### 步骤 1: 设置所有环境变量

```powershell
# 飞书配置
$env:FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/..."
$env:FEISHU_SECRET = "your-secret-here"

# 可选：AI 功能
$env:OPENAI_API_KEY = "your-api-key"
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
$env:LANGUAGE = "Chinese"
$env:CATEGORIES = "cs.CV, cs.CL"
$env:MODEL_NAME = "gpt-4o-mini"
```

### 步骤 2: 运行 PowerShell 脚本

```powershell
.\run.ps1
```

✅ **完成！** 脚本会自动执行所有步骤。

---

## 📋 常用命令速查

```powershell
# 测试飞书配置
python test_feishu.py

# 运行完整工作流
.\run.ps1

# 手动发送通知
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"

# 查看帮助
python test_feishu.py --help
```

---

## ⚠️ 如果脚本无法运行

### 错误：脚本执行被禁用

```powershell
# 允许脚本运行（当前会话）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 然后运行脚本
.\run.ps1
```

### 错误：找不到 Python

```powershell
# 检查 Python 是否已安装
python --version

# 如果没有，需要先安装 Python
```

---

## 📚 更详细的指南

- **详细 Windows 测试指南**: [WINDOWS_TESTING_GUIDE.md](./WINDOWS_TESTING_GUIDE.md)
- **飞书功能完全指南**: [START_HERE.md](./START_HERE.md)
- **快速参考**: [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md)

---

## 🎯 下一步

1. ✅ 按上面的步骤测试飞书功能
2. 📖 查看 [WINDOWS_TESTING_GUIDE.md](./WINDOWS_TESTING_GUIDE.md) 了解更多选项
3. 🚀 根据需要运行完整工作流

---

**就这么简单！** 🎉
