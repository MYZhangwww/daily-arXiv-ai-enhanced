#!/usr/bin/env python3
"""
测试分支自动恢复功能 / Test automatic branch restoration

这个脚本演示了如何在读取 data 分支的数据后自动切换回原分支
This script demonstrates automatic branch switching after reading data
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加 utils 目录到 Python 路径 / Add utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

from feishu_git_helper import GitDataHelper, GitDataManager, get_data_from_branch


def print_section(title):
    """打印分隔符 / Print separator"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def get_current_branch():
    """获取当前分支 / Get current branch"""
    result = subprocess.run(
        "git rev-parse --abbrev-ref HEAD",
        shell=True,
        capture_output=True,
        text=True,
        cwd="."
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def main():
    """主函数 / Main function"""
    
    print_section("🧪 Git 分支自动恢复测试 / Git Branch Auto-Restore Test")
    
    # 1. 显示当前分支 / Show current branch
    print("1️⃣  检查初始分支状态 / Check initial branch status")
    current = get_current_branch()
    print(f"   当前分支 / Current branch: {current}")
    
    # 2. 尝试读取 data 分支数据 / Try to read from data branch
    print("\n2️⃣  读取 data 分支数据 / Reading from data branch...")
    try:
        helper = GitDataHelper(".")
        
        # 检查 data 分支是否存在 / Check if data branch exists
        if helper.branch_exists("data"):
            print("   ✅ data 分支存在 / data branch exists")
            
            # 尝试获取最新数据（带自动恢复）/ Try to get latest data
            print("   📂 使用 GitDataManager（自动恢复分支）/ Using GitDataManager (auto-restore)...")
            manager = GitDataManager(".", "data")
            data = manager.get_data_for_notification()
            
            if data:
                lines = data.split('\n')
                print(f"   ✅ 成功读取 {len(lines)} 行数据 / Read {len(lines)} lines")
            else:
                print("   ⚠️  没有获取到数据 / No data retrieved")
        else:
            print("   ⚠️  data 分支不存在 / data branch does not exist")
            print("   💡 提示 / Tip: 如果要测试此功能，请先推送 data 分支 / Please push data branch first")
    
    except Exception as e:
        print(f"   ❌ 错误 / Error: {e}")
    
    # 3. 检查最终分支 / Check final branch
    print("\n3️⃣  检查最终分支状态 / Check final branch status")
    final = get_current_branch()
    print(f"   最终分支 / Final branch: {final}")
    
    # 4. 验证恢复 / Verify restoration
    print("\n4️⃣  验证结果 / Verify result")
    if current == final:
        print(f"   ✅ 分支恢复成功！/ Branch successfully restored!")
        print(f"   📌 当前分支保持在 / Current branch remained at: {final}")
        return 0
    else:
        print(f"   ❌ 分支未能恢复！/ Branch was not restored!")
        print(f"   原始分支 / Original: {current} → 当前分支 / Current: {final}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
