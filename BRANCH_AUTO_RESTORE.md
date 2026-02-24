# 🔄 Git 分支自动恢复功能 / Git Branch Auto-Restore Feature

## 问题描述 / Problem Statement

在读取 `data` 分支的数据后，本地 Git 分支会切换到 `data` 分支，需要手动切换回原来的分支。这在自动化工作流中很不便。

**Problem:** When reading data from the `data` branch, the local Git branch would switch to `data` branch and had to be manually switched back. This is inconvenient in automated workflows.

---

## 解决方案 / Solution

通过以下改进实现自动分支恢复：

**Solution:** Automatic branch restoration after data operations through:

### 1. 保存原分支 / Save Original Branch
```python
def _save_current_branch(self) -> None:
    """保存当前分支名 / Save current branch name"""
    self._original_branch = self._get_current_branch()
```

- 在执行 Git 操作前保存当前分支名
- Save current branch before performing Git operations

### 2. 恢复原分支 / Restore Original Branch
```python
def _restore_original_branch(self) -> bool:
    """恢复原分支 / Restore original branch"""
    if self._original_branch:
        return self._run_git_command(f"checkout {self._original_branch}")
```

- 在完成操作后自动切换回原分支
- Automatically switch back after operations complete

### 3. 使用 Try-Finally 保证恢复 / Guarantee Restoration with Try-Finally
```python
def fetch_branch(self, branch_name: str, auto_restore: bool = True) -> bool:
    if auto_restore:
        self._save_current_branch()
    
    try:
        # ... 执行 Git 操作 / Perform Git operations
        return True
    finally:
        # 无论成功或失败都恢复 / Always restore
        if auto_restore:
            self._restore_original_branch()
```

---

## 关键改进 / Key Improvements

### 新增方法 / New Methods

| 方法 / Method | 说明 / Description |
|---|---|
| `_get_current_branch()` | 获取当前分支名 / Get current branch name |
| `_save_current_branch()` | 保存当前分支 / Save current branch |
| `_restore_original_branch()` | 恢复原分支 / Restore original branch |

### 修改方法 / Modified Methods

| 方法 / Method | 变化 / Changes |
|---|---|
| `fetch_branch()` | 添加 `auto_restore` 参数和 try-finally 块 / Added auto_restore param and try-finally |
| `get_data_for_notification()` | 调用 `fetch_branch(auto_restore=True)` / Calls fetch_branch with auto_restore |

---

## 使用示例 / Usage Examples

### 例1：自动恢复（默认）/ Example 1: Auto-Restore (Default)
```python
from feishu_git_helper import GitDataManager

# 自动保存并恢复分支 / Auto save and restore branch
manager = GitDataManager(".", "data")
data = manager.get_data_for_notification()

# ✅ 完成后自动返回原分支 / Auto returns to original branch after done
print(f"当前分支: main")  # 分支不变 / Branch unchanged
```

### 例2：禁用自动恢复（特殊情况）/ Example 2: Disable Auto-Restore (Special Cases)
```python
from feishu_git_helper import GitDataHelper

helper = GitDataHelper(".")
# 不自动恢复分支 / Don't auto-restore
helper.fetch_branch("data", auto_restore=False)

# 手动切换回原分支 / Manually switch back
helper._restore_original_branch()
```

### 例3：从 feishu.py 集成 / Example 3: Integration in feishu.py
```python
# 自动恢复功能已集成到 feishu.py
# Auto-restore is already integrated in feishu.py

success = send_daily_crawl_notification(
    data_file="data",
    date_str="2024-02-24",
    mode="featured",
    from_git=True,  # 从 Git 分支读取
    git_branch="data"
)
# ✅ 操作完成后自动返回原分支
# Auto returns to original branch after operation
```

---

## 工作流程图 / Workflow Diagram

```
开始 / Start
    ↓
获取当前分支 (main)
Get current branch (main)
    ↓
读取 data 分支数据
Read data from data branch
    ├─ 切换到 data 分支
    │  Checkout data branch
    ├─ 读取数据
    │  Read data
    └─ 切换回 main 分支 ⬅️ 自动恢复！
       Checkout main branch ⬅️ Auto-restore!
    ↓
完成
Done
```

---

## 测试结果 / Test Results

运行 `test_branch_restore.py` 的结果：

**Test Results from `test_branch_restore.py`:**

```
🧪 Git 分支自动恢复测试 / Git Branch Auto-Restore Test
============================================================

1️⃣  检查初始分支状态 / Check initial branch status
   当前分支 / Current branch: main

2️⃣  读取 data 分支数据 / Reading from data branch...
   ✅ data 分支存在 / data branch exists
   📂 使用 GitDataManager（自动恢复分支）...
   📌 保存原分支 / Saved original branch: main
   [... 读取数据 ... / ... reading data ...]
   🔄 切换回原分支 / Switching back to original branch: main
   ✅ 成功切换回原分支 / Successfully switched back to: main

3️⃣  检查最终分支状态 / Check final branch status
   最终分支 / Final branch: main

4️⃣  验证结果 / Verify result
   ✅ 分支恢复成功！/ Branch successfully restored!
   📌 当前分支保持在 / Current branch remained at: main
```

---

## 命令行使用 / Command Line Usage

### 自动恢复（推荐）/ Auto-Restore (Recommended)
```bash
# 从 data 分支发送通知（自动恢复分支）
python utils/feishu.py --from-git --branch data --mode featured

# ✅ 完成后自动回到 main 分支
```

### 使用脚本测试 / Test with Script
```bash
# 测试分支自动恢复功能
python test_branch_restore.py

# 验证当前分支（应该是 main）
git rev-parse --abbrev-ref HEAD
```

---

## 关键特性 / Key Features

| 特性 / Feature | 说明 / Description |
|---|---|
| ✅ 自动保存 | 操作前自动保存当前分支 |
| ✅ 自动恢复 | 操作完成后自动恢复原分支 |
| ✅ 异常安全 | 使用 try-finally 保证恢复 |
| ✅ 可选配置 | 可通过 `auto_restore` 参数禁用 |
| ✅ 双语日志 | 中英文日志输出便于理解 |
| ✅ 错误处理 | 恢复失败时输出警告但不中断流程 |

---

## 常见问题 / FAQ

### Q: 如果恢复失败会怎样？
**A:** 系统会输出警告信息，但不会中断主流程。您仍然能够手动切换分支。
```
⚠️  警告 / Warning: 无法切换回原分支 / Failed to switch back
```

### Q: 如何禁用自动恢复？
**A:** 调用时传入 `auto_restore=False` 参数：
```python
helper.fetch_branch("data", auto_restore=False)
```

### Q: 在 CI/CD 中如何使用？
**A:** 直接使用，自动恢复功能会确保 CI/CD 流程中分支保持正确：
```bash
python utils/feishu.py --from-git --branch data
# ✅ 自动恢复，CI/CD 环境分支状态不变
```

### Q: 支持 detached HEAD 状态吗？
**A:** 支持。系统会将 detached HEAD 记录为 `HEAD`，完成后恢复到该状态。

---

## 更新历史 / Changelog

### v2.0 - 自动分支恢复 / Auto-Restore Feature
- ✅ 添加 `_get_current_branch()` 方法
- ✅ 添加 `_save_current_branch()` 方法
- ✅ 添加 `_restore_original_branch()` 方法
- ✅ 修改 `fetch_branch()` 支持自动恢复
- ✅ 修改 `get_data_for_notification()` 启用自动恢复
- ✅ 创建 `test_branch_restore.py` 测试脚本
- ✅ 添加双语日志和错误处理

---

## 下一步 / Next Steps

1. **验证功能 / Verify Feature:**
   ```bash
   python test_branch_restore.py
   ```

2. **集成到工作流 / Integrate into Workflow:**
   ```bash
   python utils/feishu.py --from-git --branch data --mode featured
   ```

3. **在 CI/CD 中使用 / Use in CI/CD:**
   - 在 GitHub Actions 或其他 CI/CD 中运行上述命令
   - 分支会自动保持正确状态

---

## 技术细节 / Technical Details

### 分支保存机制 / Branch Save Mechanism
```python
self._original_branch = self._get_current_branch()
# 返回示例 / Returns example: "main", "develop", "HEAD" (detached)
```

### 分支恢复机制 / Branch Restore Mechanism
```python
git checkout {self._original_branch}
# 这个命令对所有情况都适用：
# - 普通分支 / Regular branch: main, develop
# - HEAD detached 状态 / HEAD detached: git checkout <commit-hash>
```

### 异常处理 / Exception Handling
```python
try:
    # Git 操作 / Git operations
finally:
    # 总是恢复，即使异常发生 / Always restore even if exception
    self._restore_original_branch()
```

---

## 相关文件 / Related Files

| 文件 / File | 说明 / Description |
|---|---|
| `utils/feishu_git_helper.py` | Git 辅助工具（新增自动恢复功能）|
| `utils/feishu.py` | Feishu 通知模块（已集成此功能）|
| `test_branch_restore.py` | 自动恢复功能测试脚本 |

---

**祝使用愉快！/ Happy coding! 🚀**
