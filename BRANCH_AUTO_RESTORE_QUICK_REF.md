# 📌 分支自动恢复 - 快速参考 / Branch Auto-Restore - Quick Reference

## 🎯 一句话总结 / TL;DR

**问题 / Problem:** 读取 data 分支后无法自动返回原分支  
**解决方案 / Solution:** ✅ 现已自动恢复！No manual switching needed!

---

## ⚡ 快速开始 / Quick Start

### 之前（手动）/ Before (Manual)
```bash
# 1. 发送通知（切换到 data 分支）
python utils/feishu.py --from-git --branch data
# 现在你在 data 分支 / Now on data branch

# 2. 手动切换回原分支
git checkout main
# ❌ 需要手动操作
```

### 现在（自动）/ Now (Automatic)
```bash
# 1. 发送通知（自动恢复分支）
python utils/feishu.py --from-git --branch data
# ✅ 自动返回原分支！

# 2. 验证分支
git rev-parse --abbrev-ref HEAD  # main ✅
```

---

## 🚀 常用命令 / Common Commands

| 场景 / Scenario | 命令 / Command |
|---|---|
| **发送精选论文通知** | `python utils/feishu.py --from-git --mode featured` |
| **发送统计信息通知** | `python utils/feishu.py --from-git --mode statistics` |
| **测试自动恢复** | `python test_branch_restore.py` |
| **检查当前分支** | `git rev-parse --abbrev-ref HEAD` |
| **查看所有分支** | `git branch -a` |

---

## 🔧 工作原理 / How It Works

```
1️⃣  启动
    ↓
2️⃣  保存当前分支 (main)
    ↓
3️⃣  切换到 data 分支
    ↓
4️⃣  读取数据
    ↓
5️⃣  自动切换回 main
    ↓
6️⃣  完成 ✅
```

---

## 📊 核心代码 / Core Code

### 保存分支 / Save Branch
```python
self._original_branch = self._get_current_branch()
# 结果：_original_branch = "main"
```

### 恢复分支 / Restore Branch
```python
git checkout {self._original_branch}
# 执行：git checkout main
```

### 异常安全 / Exception-Safe
```python
try:
    # Git 操作
finally:
    # 总是恢复，即使出错
    self._restore_original_branch()
```

---

## ✨ 特性对比 / Feature Comparison

| 功能 / Feature | 之前 / Before | 现在 / Now |
|---|---|---|
| 自动恢复分支 | ❌ | ✅ |
| 需要手动操作 | ✅ | ❌ |
| 异常安全 | ❌ | ✅ |
| 支持自定义 | ❌ | ✅ |
| CI/CD 友好 | ⚠️ | ✅ |

---

## 🧪 测试验证 / Test Verification

```bash
# 运行测试脚本
python test_branch_restore.py

# 预期输出
✅ 分支恢复成功！/ Branch successfully restored!
📌 当前分支保持在 / Current branch remained at: main
```

---

## ⚙️ 配置选项 / Configuration Options

### 启用自动恢复（默认）/ Enable Auto-Restore (Default)
```python
manager.get_data_for_notification()
# ✅ 自动保存和恢复分支
```

### 禁用自动恢复（特殊情况）/ Disable Auto-Restore (Special Cases)
```python
helper.fetch_branch("data", auto_restore=False)
# 需要手动恢复分支 / Manual restore needed
helper._restore_original_branch()
```

---

## 📝 日志输出 / Log Output

```
📌 保存原分支 / Saved original branch: main
[... 读取数据 ...]
🔄 切换回原分支 / Switching back to original branch: main
✅ 成功切换回原分支 / Successfully switched back to: main
```

---

## ❓ 常见问题 / FAQ

### Q1: 如果恢复失败怎么办？
```
⚠️  警告 / Warning: 无法切换回原分支 / Failed to switch back
# 系统会输出警告，但不中断流程
# 你可以手动切换: git checkout main
```

### Q2: 支持 detached HEAD 吗？
```
✅ 是的！系统会恢复到原始 HEAD 状态
# 自动识别 detached HEAD 并恢复
```

### Q3: 在 CI/CD 中能用吗？
```
✅ 完全支持！自动恢复确保 CI/CD 分支状态正确
```

### Q4: 如何查看完整文档？
```
📖 查看：BRANCH_AUTO_RESTORE.md
```

---

## 🔗 相关资源 / Related Resources

| 资源 / Resource | 位置 / Location |
|---|---|
| 完整文档 | `BRANCH_AUTO_RESTORE.md` |
| 测试脚本 | `test_branch_restore.py` |
| 源代码 | `utils/feishu_git_helper.py` |
| Feishu 集成 | `utils/feishu.py` |

---

## 💡 使用建议 / Tips

1. **自动化工作流**  
   在 CI/CD 中使用此功能，无需担心分支状态

2. **本地开发**  
   正常开发流程中，分支会自动保持正确

3. **脚本集成**  
   在任何需要读取 data 分支的脚本中使用，自动恢复

4. **错误调试**  
   如果恢复失败，检查 stderr 输出获取详细信息

---

## 🎉 总结 / Summary

✅ **问题已解决！** / Problem Solved!

| 问题 / Problem | 解决方案 / Solution |
|---|---|
| 分支自动切换 | ✅ 自动恢复 |
| 需要手动操作 | ✅ 完全自动化 |
| 异常处理 | ✅ try-finally 保证 |
| CI/CD 友好 | ✅ 无需特殊配置 |

**现在只需一行命令，分支自动管理！** 🚀

```bash
python utils/feishu.py --from-git --mode featured
# 自动完成：保存 → 读取 → 恢复！
```

---

**需要帮助？/ Need help?**  
查看 `BRANCH_AUTO_RESTORE.md` 获取详细文档。  
Check `BRANCH_AUTO_RESTORE.md` for detailed documentation.
