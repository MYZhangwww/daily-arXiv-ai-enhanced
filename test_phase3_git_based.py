#!/usr/bin/env python3
"""
第3阶段测试脚本 - Git-Based 推荐论文保存
Phase 3 Test Script - Git-Based Recommended Papers Saving

测试新的 Git data 分支存储方式
Test the new Git data branch storage approach
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加当前目录到路径 / Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.recommended_papers import RecommendedPapersManager


def create_test_papers():
    """创建测试论文数据 / Create test papers data"""
    return [
        {
            "id": "2402.12345",
            "title": "Test Paper 1: Advanced Autonomous Driving Systems",
            "authors": "John Doe, Jane Smith, Bob Johnson",
            "category": "cs.CV",
            "summary": "This paper presents a comprehensive study on autonomous driving systems using computer vision and machine learning techniques.",
            "tldr": "提出了一个新的自动驾驶视觉系统",
            "url": "https://arxiv.org/abs/2402.12345",
            "is_priority": True
        },
        {
            "id": "2402.12346",
            "title": "Test Paper 2: Deep Learning for Image Recognition",
            "authors": "Alice Brown, Charlie Davis",
            "category": "cs.AI",
            "summary": "A study on using deep learning models for image recognition tasks.",
            "tldr": "深度学习在图像识别中的应用",
            "url": "https://arxiv.org/abs/2402.12346",
            "is_priority": False
        },
        {
            "id": "2402.12347",
            "title": "Test Paper 3: Self-Driving Technology Integration",
            "authors": "Eve Foster, Frank Green",
            "category": "cs.RO",
            "summary": "Integration of self-driving technology with real-world traffic systems.",
            "tldr": "自动驾驶技术的实际应用整合",
            "url": "https://arxiv.org/abs/2402.12347",
            "is_priority": True
        }
    ]


def test_git_based_saving():
    """测试基于 Git 的论文保存 / Test Git-based paper saving"""
    
    print("=" * 70)
    print("🧪 第3阶段 Git-Based 推荐论文保存测试")
    print("🧪 Phase 3 Git-Based Recommended Papers Saving Test")
    print("=" * 70)
    print()
    
    # 获取今天的日期 / Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 测试日期 / Test Date: {today}")
    print()
    
    # 创建测试数据 / Create test data
    print("📝 创建测试数据 / Creating test data...")
    test_papers = create_test_papers()
    print(f"✅ 已创建 {len(test_papers)} 篇测试论文 / Created {len(test_papers)} test papers")
    for idx, paper in enumerate(test_papers, 1):
        priority_marker = "⭐" if paper.get("is_priority") else "  "
        print(f"   {idx}. {priority_marker} {paper['id']} - {paper['title'][:50]}...")
    print()
    
    # 初始化 Git-based 管理器 / Initialize Git-based manager
    print("🔧 初始化 Git-Based 管理器 / Initializing Git-Based Manager...")
    try:
        manager = RecommendedPapersManager(repo_path=".", branch_name="data")
        print("✅ 管理器已初始化 / Manager initialized")
    except Exception as e:
        print(f"❌ 初始化失败 / Initialization failed: {e}")
        return False
    print()
    
    # 保存到 Git data 分支 / Save to Git data branch
    print("🚀 保存论文到 Git data 分支 / Saving papers to Git data branch...")
    print()
    
    success = manager.save_recommended_papers(test_papers, today)
    
    if success:
        print()
        print("=" * 70)
        print("✅ 测试通过 / Test Passed!")
        print("=" * 70)
        print()
        print("📊 测试结果摘要 / Test Results Summary:")
        print(f"  • 已保存的论文数: {len(test_papers)} / Papers saved: {len(test_papers)}")
        print(f"  • 优先级论文: {sum(1 for p in test_papers if p.get('is_priority'))} / Priority papers: {sum(1 for p in test_papers if p.get('is_priority'))}")
        print(f"  • 推荐日期: {today} / Recommendation date: {today}")
        print()
        print("📁 Git data 分支信息 / Git data branch info:")
        print(f"  • 分支名称 / Branch name: data")
        print(f"  • 文件名 / File name: recommended_{today}.jsonl")
        print(f"  • 文件路径 / File path: data/recommended_{today}.jsonl")
        print()
        print("🌐 GitHub Pages 访问链接 / GitHub Pages Access URL:")
        print(f"  (需要替换 OWNER 和 REPO 为实际值)")
        print(f"  (Replace OWNER and REPO with actual values)")
        print(f"  https://raw.githubusercontent.com/OWNER/REPO/data/data/recommended_{today}.jsonl")
        print()
        print("📋 前端如何加载数据 / How frontend loads data:")
        print(f"  1. 扫描最近 90 天的推荐文件 / Scan recommendation files from recent 90 days")
        print(f"  2. 从 GitHub 原始内容 URL 加载 JSONL / Load JSONL from GitHub raw content URL")
        print(f"  3. 按日期分组展示 / Display grouped by date")
        print()
        return True
    else:
        print()
        print("=" * 70)
        print("❌ 测试失败 / Test Failed!")
        print("=" * 70)
        print()
        print("❓ 可能的原因 / Possible reasons:")
        print("  1. Git 仓库未初始化 / Git repository not initialized")
        print("  2. data 分支不存在 / data branch doesn't exist")
        print("  3. 没有 Git 提交权限 / No Git commit permission")
        print("  4. 网络连接问题 / Network connection issue")
        print()
        print("💡 解决步骤 / Resolution steps:")
        print("  1. 确保 Git 仓库已初始化: git init")
        print("  2. 确保已配置 Git 用户: git config user.name & git config user.email")
        print("  3. 检查远程仓库: git remote -v")
        print("  4. 尝试手动创建 data 分支: git checkout --orphan data")
        print()
        return False


def verify_git_configuration():
    """验证 Git 配置 / Verify Git configuration"""
    
    print("=" * 70)
    print("🔍 验证 Git 配置 / Verifying Git Configuration")
    print("=" * 70)
    print()
    
    import subprocess
    
    checks = [
        ("检查 Git 安装", ["git", "--version"]),
        ("检查仓库状态", ["git", "status"]),
        ("检查远程仓库", ["git", "remote", "-v"]),
        ("检查本地分支", ["git", "branch", "-a"]),
    ]
    
    for check_name, command in checks:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ {check_name} / {check_name}: 成功")
                if "git" not in command[0].lower():
                    for line in result.stdout.strip().split('\n')[:3]:
                        if line.strip():
                            print(f"   {line}")
            else:
                print(f"❌ {check_name} / {check_name}: 失败")
                if result.stderr:
                    print(f"   {result.stderr.strip()[:100]}")
        except Exception as e:
            print(f"⚠️  {check_name} / {check_name}: {str(e)[:50]}")
        print()


if __name__ == "__main__":
    # 验证 Git 配置 / Verify Git configuration
    verify_git_configuration()
    
    # 运行测试 / Run test
    success = test_git_based_saving()
    
    # 退出代码 / Exit code
    sys.exit(0 if success else 1)
