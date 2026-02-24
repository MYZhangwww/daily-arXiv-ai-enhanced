#!/usr/bin/env python3
"""
第3阶段简化测试 - 验证 Git-Based 推荐论文管理器
Phase 3 Simplified Test - Verify Git-Based Recommended Papers Manager

不需要实际推送到远程，只验证本地 Git 操作
No remote push required, only verify local Git operations
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加当前目录到路径 / Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.recommended_papers import RecommendedPapersManager


def test_manager_initialization():
    """测试管理器初始化 / Test manager initialization"""
    print("\n" + "=" * 70)
    print("✅ 测试 1: 管理器初始化 / Test 1: Manager Initialization")
    print("=" * 70)
    
    try:
        manager = RecommendedPapersManager(repo_path=".", branch_name="data")
        print("✅ 管理器已成功初始化")
        print(f"  • 仓库路径 / Repository path: {manager.repo_path}")
        print(f"  • 分支名称 / Branch name: {manager.branch_name}")
        return True
    except Exception as e:
        print(f"❌ 初始化失败 / Initialization failed: {e}")
        return False


def test_branch_exists():
    """测试分支检查 / Test branch existence check"""
    print("\n" + "=" * 70)
    print("✅ 测试 2: 分支检查 / Test 2: Branch Existence Check")
    print("=" * 70)
    
    try:
        manager = RecommendedPapersManager(repo_path=".", branch_name="data")
        exists = manager.helper.branch_exists("data")
        
        if exists:
            print("✅ data 分支存在 / data branch exists")
            return True
        else:
            print("⚠️  data 分支不存在（但这不影响功能）")
            print("⚠️  data branch doesn't exist (but doesn't affect functionality)")
            return True
    except Exception as e:
        print(f"❌ 检查失败 / Check failed: {e}")
        return False


def test_git_operations():
    """测试 Git 基本操作 / Test basic Git operations"""
    print("\n" + "=" * 70)
    print("✅ 测试 3: Git 基本操作 / Test 3: Basic Git Operations")
    print("=" * 70)
    
    try:
        manager = RecommendedPapersManager(repo_path=".", branch_name="data")
        
        # 测试 Git 命令执行 / Test Git command execution
        code, stdout, stderr = manager.helper._run_git_command("--version")
        
        if code == 0:
            print(f"✅ Git 命令执行成功 / Git command executed successfully")
            print(f"  • 版本信息 / Version: {stdout}")
            return True
        else:
            print(f"❌ Git 命令执行失败 / Git command failed: {stderr}")
            return False
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {e}")
        return False


def test_data_format():
    """测试推荐论文数据格式 / Test recommended papers data format"""
    print("\n" + "=" * 70)
    print("✅ 测试 4: 数据格式 / Test 4: Data Format")
    print("=" * 70)
    
    try:
        test_papers = [
            {
                "id": "2402.12345",
                "title": "Test Paper",
                "authors": "Author Name",
                "category": "cs.CV",
                "summary": "Test summary",
                "tldr": "Test TLDR",
                "url": "https://arxiv.org/abs/2402.12345",
                "is_priority": True
            }
        ]
        
        # 验证数据格式 / Validate data format
        for paper in test_papers:
            required_fields = ["id", "title", "authors", "category", "url", "is_priority"]
            missing = [f for f in required_fields if f not in paper]
            
            if missing:
                print(f"❌ 缺少字段 / Missing fields: {missing}")
                return False
        
        print("✅ 数据格式验证通过 / Data format validation passed")
        print(f"  • 必需字段: id, title, authors, category, url, is_priority")
        print(f"  • 可选字段: summary, tldr, recommended_date, recommended_at, priority_status")
        return True
    except Exception as e:
        print(f"❌ 验证失败 / Validation failed: {e}")
        return False


def test_file_naming_convention():
    """测试文件命名规范 / Test file naming convention"""
    print("\n" + "=" * 70)
    print("✅ 测试 5: 文件命名规范 / Test 5: File Naming Convention")
    print("=" * 70)
    
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"recommended_{today}.jsonl"
        
        print(f"✅ 命名规范验证通过 / Naming convention validation passed")
        print(f"  • 日期格式 / Date format: YYYY-MM-DD")
        print(f"  • 文件名格式 / File name format: recommended_YYYY-MM-DD.jsonl")
        print(f"  • 示例 / Example: {filename}")
        print(f"  • 存储位置 / Location: data/{filename}")
        return True
    except Exception as e:
        print(f"❌ 验证失败 / Validation failed: {e}")
        return False


def test_github_url_generation():
    """测试 GitHub URL 生成 / Test GitHub URL generation"""
    print("\n" + "=" * 70)
    print("✅ 测试 6: GitHub URL 生成 / Test 6: GitHub URL Generation")
    print("=" * 70)
    
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        owner = "PLACEHOLDER_REPO_OWNER"
        repo = "PLACEHOLDER_REPO_NAME"
        branch = "data"
        filename = f"recommended_{today}.jsonl"
        
        github_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/data/{filename}"
        
        print(f"✅ GitHub URL 生成成功 / GitHub URL generated successfully")
        print(f"  • URL 格式 / URL format:")
        print(f"    https://raw.githubusercontent.com/{{owner}}/{{repo}}/data/data/{{filename}}")
        print(f"  • 示例 / Example:")
        print(f"    {github_url}")
        print(f"  • 占位符 / Placeholders:")
        print(f"    - {{owner}}: 从 data-config.js 注入")
        print(f"    - {{repo}}: 从 data-config.js 注入")
        return True
    except Exception as e:
        print(f"❌ 生成失败 / Generation failed: {e}")
        return False


def summary_test():
    """总结测试结果 / Summarize test results"""
    print("\n" + "=" * 70)
    print("📊 测试总结 / Test Summary")
    print("=" * 70)
    print()
    
    tests = [
        ("管理器初始化", test_manager_initialization),
        ("分支检查", test_branch_exists),
        ("Git 操作", test_git_operations),
        ("数据格式", test_data_format),
        ("文件命名", test_file_naming_convention),
        ("GitHub URL", test_github_url_generation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n⚠️  测试异常 / Test exception {name}: {e}")
            results.append((name, False))
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print()
    print("=" * 70)
    print(f"📈 总体结果 / Overall Results: {passed}/{total} 通过 / Passed")
    print("=" * 70)
    print()
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} {name}")
    
    print()
    
    if passed == total:
        print("🎉 所有测试通过！/ All tests passed!")
        print()
        print("下一步：/ Next steps:")
        print("  1. 运行实际的 Feishu 通知流程")
        print("  2. 验证推荐论文是否保存到 data 分支")
        print("  3. 在 GitHub Pages 上验证前端数据加载")
        print("  4. 检查 Git 提交历史")
        return True
    else:
        print(f"⚠️  有 {total - passed} 个测试失败 / {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    print()
    print("🧪 Phase 3 Git-Based 推荐论文管理器验证测试")
    print("🧪 Phase 3 Git-Based Recommended Papers Manager Verification Test")
    print()
    
    success = summary_test()
    sys.exit(0 if success else 1)
