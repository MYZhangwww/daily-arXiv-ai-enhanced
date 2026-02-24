# 🪟 Windows 上的飞书功能测试指南

## 📋 Windows 系统测试方案

由于 Windows 原生不支持 bash，我为你提供了多种解决方案。

---

## ✨ 推荐方案：PowerShell 脚本

我已经为你创建了 **`run.ps1`** - Windows PowerShell 版本的运行脚本。

### 如何使用

#### 步骤 1: 打开 PowerShell

在 Windows 上打开 PowerShell（按 `Win + X`，选择 "PowerShell"）

#### 步骤 2: 设置环境变量

```powershell
# 设置飞书配置
$env:FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/your-hook-id"
$env:FEISHU_SECRET = "your-secret-here"

# 可选：设置 OpenAI 配置
$env:OPENAI_API_KEY = "your-api-key"
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
$env:LANGUAGE = "Chinese"
$env:CATEGORIES = "cs.CV, cs.CL"
$env:MODEL_NAME = "gpt-4o-mini"
```

#### 步骤 3: 运行脚本

```powershell
# 进入项目目录
cd e:\VibeCoding\daily-arXiv-ai-enhanced

# 运行 PowerShell 脚本
.\run.ps1
```

**完成！** 脚本会自动执行爬取、去重、飞书通知等所有步骤。

---

## 🚀 快速测试飞书功能（最简单）

如果你只想测试飞书通知功能，**不需要运行完整脚本**：

### 方式 1: 直接运行 Python 测试

```powershell
# 进入项目目录
cd e:\VibeCoding\daily-arXiv-ai-enhanced

# 运行测试套件
python test_feishu.py
```

这会检查：
- ✓ HMAC-SHA256 签名生成
- ✓ 消息构建
- ✓ 环境变量配置
- ✓ 实际通知发送（如已配置）

### 方式 2: 手动发送通知

```powershell
# 设置环境变量
$env:FEISHU_WEBHOOK_URL = "your-webhook-url"
$env:FEISHU_SECRET = "your-secret"

# 发送通知（使用现有的数据文件）
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"
```

---

## 📊 其他 Windows 方案

### 方案 A: 使用 WSL2（如已安装）

```powershell
# 在 PowerShell 中运行 bash 脚本
wsl bash run.sh
```

**优点**: 完全 bash 兼容  
**要求**: 需要安装 WSL2

### 方案 B: 使用 Git Bash

如果安装了 Git for Windows：

```powershell
# 方式 1: 在 PowerShell 中
& "C:\Program Files\Git\bin\bash.exe" run.sh

# 方式 2: 直接打开 Git Bash 并运行
bash run.sh
```

**优点**: 轻量级  
**要求**: 需要安装 Git for Windows

---

## ⚠️ 注意事项

### PowerShell 执行策略

如果遇到以下错误：

```
run.ps1 : 无法加载文件 ... 因为在此系统上禁止运行脚本
```

需要修改执行策略：

```powershell
# 仅对当前用户临时允许
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 然后运行脚本
.\run.ps1
```

### 特殊字符编码

如果遇到 PowerShell 显示中文乱码，运行这个命令：

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::UTF8
```

---

## 🧪 各种场景的测试命令

### 场景 1: 仅测试飞书功能（推荐新手）

```powershell
# 最简单！直接测试
python test_feishu.py
```

### 场景 2: 测试飞书 + 配置检查

```powershell
# 设置环境变量
$env:FEISHU_WEBHOOK_URL = "your-webhook-url"
$env:FEISHU_SECRET = "your-secret"

# 运行测试
python test_feishu.py
```

### 场景 3: 手动发送通知

```powershell
# 如果有现成的数据文件
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"
```

### 场景 4: 完整工作流测试

```powershell
# 设置所有环境变量
$env:FEISHU_WEBHOOK_URL = "your-webhook-url"
$env:FEISHU_SECRET = "your-secret"
$env:OPENAI_API_KEY = "your-api-key"

# 运行完整脚本
.\run.ps1
```

---

## 📝 PowerShell 脚本详解

`run.ps1` 脚本的功能：

| 步骤 | 功能 | 说明 |
|------|------|------|
| 步骤 1 | 爬取数据 | 使用 Scrapy 爬取 arXiv 论文 |
| 步骤 2 | 去重检查 | 检查数据是否有新内容 |
| **步骤 3** | **发送飞书通知** | **✨ 新增功能** |
| 步骤 4 | AI 增强 | 使用 OpenAI 进行摘要 |
| 步骤 5 | Markdown 转换 | 转换为 Markdown 格式 |
| 步骤 6 | 更新文件列表 | 更新资源文件 |

---

## 💡 最佳实践

### 推荐工作流程

```powershell
# 1. 首先测试飞书功能（无需数据爬取）
python test_feishu.py

# 2. 如果测试通过，运行完整脚本
.\run.ps1
```

### 环境变量管理

**临时设置**（仅当前 PowerShell 会话）：
```powershell
$env:FEISHU_WEBHOOK_URL = "..."
```

**永久设置**（推荐用于开发）：

在 PowerShell 配置文件中添加：
```powershell
# 编辑配置文件
notepad $PROFILE

# 添加以下内容
$env:FEISHU_WEBHOOK_URL = "your-webhook-url"
$env:FEISHU_SECRET = "your-secret"
```

---

## 🔍 故障排查

### 问题 1: 脚本无法执行

**错误信息**:
```
cannot be loaded because running scripts is disabled on this system
```

**解决方案**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\run.ps1
```

### 问题 2: 找不到 Python

**错误信息**:
```
python : 无法将"python"项识别为 cmdlet、函数或脚本文件
```

**解决方案**:
```powershell
# 检查 Python 是否安装
python --version

# 如果找不到，需要安装 Python 或添加到 PATH
```

### 问题 3: Scrapy 命令出错

**解决方案**:
```powershell
# 确保在项目目录中
cd e:\VibeCoding\daily-arXiv-ai-enhanced

# 检查依赖是否已安装
pip install scrapy requests
```

### 问题 4: 飞书通知失败

**检查清单**:
- [ ] FEISHU_WEBHOOK_URL 是否正确设置
- [ ] FEISHU_SECRET 是否正确设置
- [ ] 网络连接是否正常
- [ ] 运行 `python test_feishu.py` 进行诊断

---

## 📚 相关文档

- **飞书功能详细指南**: [FEISHU_SETUP.md](./FEISHU_SETUP.md)
- **飞书快速参考**: [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md)
- **测试脚本说明**: [test_feishu.py](./test_feishu.py)

---

## 🎯 快速参考

### 最常用的命令

```powershell
# 1. 测试飞书配置
python test_feishu.py

# 2. 运行完整工作流
.\run.ps1

# 3. 手动发送通知
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"
```

### 环境变量快速设置

```powershell
# 一行命令设置所有变量
$env:FEISHU_WEBHOOK_URL = "your-url"; $env:FEISHU_SECRET = "your-secret"

# 验证设置
Write-Host $env:FEISHU_WEBHOOK_URL
Write-Host $env:FEISHU_SECRET
```

---

## ✅ 检查清单

- [ ] Python 已安装
- [ ] 项目依赖已安装 (`pip install -r requirements.txt` 或使用 uv)
- [ ] 环境变量已设置
- [ ] 测试脚本通过 (`python test_feishu.py`)
- [ ] PowerShell 执行策略允许脚本运行
- [ ] 可以访问飞书群组

---

**祝你在 Windows 上使用愉快！** 🎉

如有问题，参考 [FEISHU_QUICK_REFERENCE.md](./FEISHU_QUICK_REFERENCE.md) 的故障排查部分。
