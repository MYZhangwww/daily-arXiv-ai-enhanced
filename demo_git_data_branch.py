#!/usr/bin/env python3
"""
Git Data 分支读取演示脚本 / Git Data Branch Reading Demo Script

展示如何从 Git data 分支读取数据并发送飞书通知
Demonstrates how to read data from Git data branch and send Feishu notification
"""

import sys
import os

# 添加项目路径 / Add project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feishu_git_helper import GitDataManager, GitDataHelper, get_data_from_branch, get_latest_date
import json


def demo_git_helper():
    """演示 Git 辅助工具 / Demo Git helper"""
    print("\n" + "="*70)
    print("演示 1: Git 数据辅助工具 / Demo 1: Git Data Helper")
    print("="*70)
    
    try:
        helper = GitDataHelper(".")
        
        # 检查分支 / Check branch
        print("\n📋 检查分支 / Checking branches...")
        branches_to_check = ["main", "data"]
        for branch in branches_to_check:
            exists = helper.branch_exists(branch)
            status = "✅ 存在" if exists else "❌ 不存在"
            print(f"   分支 '{branch}': {status} / Branch '{branch}': {status}")
        
        # 如果有 data 分支，尝试读取数据
        if helper.branch_exists("data"):
            print("\n📂 尝试从 data 分支读取数据 / Trying to read data from data branch...")
            
            # 列出文件
            code, stdout, _ = helper._run_git_command("ls-tree -r --name-only data data/")
            if code == 0 and stdout:
                files = stdout.split('\n')
                jsonl_files = [f for f in files if f and f.endswith('.jsonl')]
                print(f"   找到 {len(jsonl_files)} 个 JSONL 文件 / Found {len(jsonl_files)} JSONL files")
                if jsonl_files:
                    print(f"   最新文件 / Latest file: {sorted(jsonl_files)[-1]}")
            else:
                print("   ⚠️ data 分支为空或不存在 / data branch is empty or doesn't exist")
    
    except Exception as e:
        print(f"❌ 错误 / Error: {e}")


def demo_git_manager():
    """演示 Git 数据管理器 / Demo Git Data Manager"""
    print("\n" + "="*70)
    print("演示 2: Git 数据管理器 / Demo 2: Git Data Manager")
    print("="*70)
    
    try:
        manager = GitDataManager(repo_path=".", branch_name="data")
        
        print("\n🔍 获取最新数据日期 / Getting latest data date...")
        date = manager.get_latest_data_date()
        if date:
            print(f"   ✅ 最新日期 / Latest date: {date}")
        else:
            print("   ⚠️ 无法获取日期 / Failed to get date")
            return
        
        print(f"\n📥 获取数据 / Getting data for date {date}...")
        data = manager.get_data_for_notification()
        
        if data:
            lines = [l for l in data.split('\n') if l.strip()]
            print(f"   ✅ 成功读取 {len(lines)} 行数据 / Successfully read {len(lines)} lines")
            
            # 显示前 3 篇论文 / Show first 3 papers
            print(f"\n📄 前 3 篇论文 / First 3 papers:")
            for i, line in enumerate(lines[:3]):
                try:
                    obj = json.loads(line)
                    title = obj.get('title', 'N/A')[:60]
                    has_ai = "🤖" if obj.get('AI') else "  "
                    print(f"   {i+1}. {has_ai} {title}")
                except:
                    pass
        else:
            print("   ❌ 无法读取数据 / Failed to read data")
    
    except Exception as e:
        print(f"❌ 错误 / Error: {e}")


def demo_quick_functions():
    """演示快速函数 / Demo quick functions"""
    print("\n" + "="*70)
    print("演示 3: 快速函数 / Demo 3: Quick Functions")
    print("="*70)
    
    print("\n🚀 快速获取最新日期 / Quick get latest date...")
    date = get_latest_date("data")
    if date:
        print(f"   ✅ 最新日期 / Latest date: {date}")
    else:
        print("   ⚠️ 无法获取 / Failed to get")
    
    print("\n🚀 快速获取数据 / Quick get data...")
    data = get_data_from_branch("data")
    if data:
        lines = [l for l in data.split('\n') if l.strip()]
        print(f"   ✅ 成功读取 {len(lines)} 行 / Successfully read {len(lines)} lines")
    else:
        print("   ⚠️ 无法读取 / Failed to read")


def demo_cli_commands():
    """演示命令行用法 / Demo CLI commands"""
    print("\n" + "="*70)
    print("演示 4: 命令行用法 / Demo 4: CLI Commands")
    print("="*70)
    
    print("\n📝 以下是推荐的命令行使用方式：\n")
    
    commands = [
        ("自动获取最新数据", 
         "python utils/feishu.py --from-git --mode featured"),
        ("指定日期读取",
         "python utils/feishu.py --from-git --date 2024-02-24"),
        ("发送统计通知",
         "python utils/feishu.py --from-git --mode statistics"),
        ("使用本地文件",
         "python utils/feishu.py --data data/2024-02-24.jsonl --date 2024-02-24"),
    ]
    
    for i, (desc, cmd) in enumerate(commands, 1):
        print(f"{i}. {desc}")
        print(f"   $ {cmd}\n")


def main():
    """主函数 / Main function"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*10 + "Git Data 分支读取功能演示 / Git Data Branch Demo" + " "*12 + "║")
    print("╚" + "="*68 + "╝")
    
    # 演示 1: Git 辅助工具
    demo_git_helper()
    
    # 演示 2: Git 数据管理器
    demo_git_manager()
    
    # 演示 3: 快速函数
    demo_quick_functions()
    
    # 演示 4: CLI 命令
    demo_cli_commands()
    
    print("\n" + "="*70)
    print("💡 提示 / Tips:")
    print("="*70)
    print("""
1. Git data 分支是存储爬取数据的地方
   Git data branch stores crawled data

2. 使用 --from-git 参数可以直接读取 data 分支，无需手动切换
   Use --from-git to read from data branch without manual switching

3. 如果 data 分支不存在，会自动降级到本地文件读取
   Falls back to local file if data branch doesn't exist

4. 建议在 CI/CD 中使用自动获取模式：
   Recommended for CI/CD (auto get latest):
   $ python utils/feishu.py --from-git

5. 完整的使用指南请查看 GIT_DATA_BRANCH_GUIDE.md
   See GIT_DATA_BRANCH_GUIDE.md for complete guide
    """)
    
    print("="*70)
    print("✨ 演示完成！/ Demo completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
