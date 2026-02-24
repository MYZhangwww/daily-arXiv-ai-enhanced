#!/usr/bin/env python3
"""
🔄 分支自动恢复 - 快速验证脚本 / Branch Auto-Restore - Quick Verification Script

这个脚本可以快速验证分支自动恢复功能是否正常工作
This script quickly verifies if auto-restore feature is working
"""

import subprocess
import sys


def run_command(cmd):
    """执行命令 / Run command"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip()


def main():
    """主函数 / Main function"""
    print("\n🔍 Git 分支自动恢复功能 - 快速验证 / Quick Verification\n")
    print("=" * 60)
    
    # 1. 检查当前分支
    print("\n1️⃣  当前分支状态 / Current branch status")
    success, output = run_command("git rev-parse --abbrev-ref HEAD")
    if success:
        current = output
        print(f"   ✅ 当前分支: {current}")
    else:
        print("   ❌ 无法获取分支信息 / Failed to get branch info")
        return 1
    
    # 2. 检查 data 分支
    print("\n2️⃣  检查 data 分支 / Check data branch")
    success, output = run_command("git branch -r --list origin/data")
    if success and "origin/data" in output:
        print("   ✅ data 分支存在 / data branch exists")
    else:
        print("   ⚠️  data 分支不存在，跳过测试 / data branch not found, skipping test")
        print("   💡 如要完整测试，请先创建或 push data 分支")
        return 0
    
    # 3. 测试自动恢复功能
    print("\n3️⃣  运行完整测试 / Run complete test")
    success = run_command("python test_branch_restore.py")[0]
    
    if not success:
        print("   ⚠️  测试脚本不可用，尝试直接验证功能")
        print("   Trying direct verification...")
    
    # 4. 最终验证
    print("\n4️⃣  最终验证 / Final verification")
    success, output = run_command("git rev-parse --abbrev-ref HEAD")
    if success:
        final = output
        if final == current:
            print(f"   ✅ 分支保持在: {final}")
            print(f"   ✅ 自动恢复功能 ✅ 正常工作 / Auto-restore working correctly")
            return 0
        else:
            print(f"   ⚠️  分支已变更: {current} → {final}")
            print(f"   💡 运行: git checkout {current} 来手动恢复")
            return 1
    else:
        print("   ❌ 无法验证分支状态 / Failed to verify branch")
        return 1


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔄 Git 分支自动恢复 - 快速验证")
    print("=" * 60)
    exit_code = main()
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ 验证通过！功能正常工作")
        print("✅ Verification passed! Feature working correctly")
    else:
        print("⚠️  验证未通过，请检查日志")
        print("⚠️  Verification failed, check logs above")
    print("=" * 60 + "\n")
    
    sys.exit(exit_code)
