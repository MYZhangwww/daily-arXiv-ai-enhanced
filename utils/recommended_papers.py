#!/usr/bin/env python3
"""
推荐论文管理模块 / Recommended Papers Management Module

功能说明 / Features:
- 保存发送到飞书的精选论文到 Git data 分支 / Save featured papers sent to Feishu to Git data branch
- 管理推荐论文历史 / Manage recommended papers history
- 支持查询、统计、导出推荐论文 / Support query, statistics, export recommended papers
- 自动 Git 提交和推送 / Automatic Git commit and push
- 自动恢复原分支 / Auto restore original branch
"""

import json
import os
import sys
import subprocess
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# 导入 Git 辅助工具 / Import Git helper
try:
    from feishu_git_helper import GitDataHelper, GitDataManager
except ImportError:
    # 如果在不同目录运行，尝试添加当前目录到路径 / Try adding current directory to path
    sys.path.insert(0, os.path.dirname(__file__))
    from feishu_git_helper import GitDataHelper, GitDataManager


class RecommendedPapersManager:
    """推荐论文管理器 (Git-based) / Recommended Papers Manager (Git-based)"""
    
    def __init__(self, repo_path: str = ".", branch_name: str = "data"):
        """
        初始化推荐论文管理器（基于 Git）
        Initialize Recommended Papers Manager (Git-based)
        
        Args:
            repo_path (str): Git 仓库路径 / Path to Git repository
            branch_name (str): 数据分支名称 / Data branch name (default: "data")
        """
        self.repo_path = Path(repo_path).resolve()
        self.branch_name = branch_name
        self.helper = GitDataHelper(str(self.repo_path))
    
    def save_recommended_papers(self, papers: List[Dict], date_str: str) -> bool:
        """
        保存推荐论文到 Git data 分支（发送到飞书的论文）
        Save recommended papers to Git data branch (papers sent to Feishu)
        
        Args:
            papers (list): 论文列表 / List of papers
            date_str (str): 日期字符串 / Date string (YYYY-MM-DD)
            
        Returns:
            bool: 是否成功保存和推送 / Whether saving and pushing succeeded
        """
        try:
            if not papers:
                print("⚠️  没有推荐论文需要保存 / No recommended papers to save", file=sys.stderr)
                return True
            
            # 保存原分支 / Save original branch
            self.helper._save_current_branch()
            
            # 确保 data 分支存在和最新 / Ensure data branch exists and is up to date
            print(f"📌 确保 {self.branch_name} 分支最新... / Ensuring {self.branch_name} branch is up to date...", file=sys.stderr)
            if not self.helper.fetch_branch(self.branch_name, auto_restore=False):
                print(f"⚠️  警告：无法获取最新 {self.branch_name} 分支 / Warning: Failed to fetch {self.branch_name} branch", file=sys.stderr)
                # 继续尝试，可能分支还不存在 / Continue trying, branch might not exist yet
            
            # 为每篇论文添加推荐元数据 / Add recommendation metadata for each paper
            for paper in papers:
                paper['recommended_date'] = date_str
                paper['recommended_at'] = datetime.now().isoformat()
                paper['priority_status'] = 'priority' if paper.get('is_priority') else 'normal'
            
            # 创建推荐论文文件（JSONL 格式）/ Create recommended papers file (JSONL format)
            # 文件名格式: recommended_YYYY-MM-DD.jsonl
            file_name = f"recommended_{date_str}.jsonl"
            
            # 生成临时文件内容 / Generate temp file content
            temp_file = self.repo_path / f".tmp_{file_name}"
            with open(temp_file, 'w', encoding='utf-8') as f:
                for paper in papers:
                    f.write(json.dumps(paper, ensure_ascii=False) + '\n')
            
            print(f"📝 创建推荐论文文件 / Creating recommended papers file: {file_name}", file=sys.stderr)
            
            # 调用 Git 命令添加文件到 data 分支 / Add file to data branch using Git
            code, stdout, stderr = self.helper._run_git_command(f"checkout {self.branch_name}")
            if code != 0:
                print(f"❌ 无法切换到 {self.branch_name} 分支 / Failed to checkout {self.branch_name} branch: {stderr}", file=sys.stderr)
                temp_file.unlink()  # 清理临时文件 / Clean up temp file
                return False
            
            # 确保 data 目录存在 / Ensure data directory exists
            data_dir = self.repo_path / "data"
            data_dir.mkdir(exist_ok=True)
            
            # 复制临时文件到 data 目录 / Copy temp file to data directory
            target_file = data_dir / file_name
            import shutil
            shutil.copy(temp_file, target_file)
            temp_file.unlink()  # 清理临时文件 / Clean up temp file
            
            print(f"✅ 文件已保存到 data 分支 / File saved to data branch: data/{file_name}", file=sys.stderr)
            
            # Git add 和 commit / Git add and commit
            code, _, stderr = self.helper._run_git_command(f"add data/{file_name}")
            if code != 0:
                print(f"❌ 无法 git add / Failed to git add: {stderr}", file=sys.stderr)
                self.helper._restore_original_branch()
                return False
            
            # 检查是否有变更 / Check if there are changes
            code, stdout, _ = self.helper._run_git_command("diff --staged --quiet")
            if code == 0:
                print("⚠️  没有变更需要提交 / No changes to commit", file=sys.stderr)
                self.helper._restore_original_branch()
                return True
            
            # 提交 / Commit
            commit_msg = f"update: recommended papers for {date_str}"
            code, _, stderr = self.helper._run_git_command(f'commit -m "{commit_msg}"')
            if code != 0:
                print(f"❌ 无法 git commit / Failed to git commit: {stderr}", file=sys.stderr)
                self.helper._restore_original_branch()
                return False
            
            print(f"📝 已提交到 {self.branch_name} 分支 / Committed to {self.branch_name} branch: {commit_msg}", file=sys.stderr)
            
            # 推送到远程 / Push to remote
            print(f"🚀 推送到远程 {self.branch_name} 分支... / Pushing to remote {self.branch_name} branch...", file=sys.stderr)
            code, _, stderr = self.helper._run_git_command(f"push origin {self.branch_name}")
            if code != 0:
                print(f"❌ 无法推送到远程 / Failed to push to remote: {stderr}", file=sys.stderr)
                self.helper._restore_original_branch()
                return False
            
            print(f"✅ 推送成功 / Successfully pushed to remote", file=sys.stderr)
            print(f"✅ 保存 {len(papers)} 篇推荐论文 / Saved {len(papers)} recommended papers", file=sys.stderr)
            
            # 恢复原分支 / Restore original branch
            self.helper._restore_original_branch()
            return True
            
        except Exception as e:
            print(f"❌ 保存推荐论文失败 / Failed to save recommended papers: {e}", file=sys.stderr)
            try:
                self.helper._restore_original_branch()
            except:
                pass
            return False


# 快速访问函数 / Quick access functions

def save_recommended_papers(papers: List[Dict], date_str: str, repo_path: str = ".", branch_name: str = "data") -> bool:
    """
    快速保存推荐论文到 Git data 分支
    Quick function to save recommended papers to Git data branch
    
    Args:
        papers (list): 论文列表 / List of papers
        date_str (str): 日期字符串 / Date string (YYYY-MM-DD)
        repo_path (str): 仓库路径 / Repository path
        branch_name (str): 分支名称 / Branch name
        
    Returns:
        bool: 是否成功 / Whether succeeded
    """
    try:
        manager = RecommendedPapersManager(repo_path, branch_name)
        return manager.save_recommended_papers(papers, date_str)
    except Exception as e:
        print(f"❌ 错误 / Error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # 演示脚本 / Demo script
    import argparse
    
    parser = argparse.ArgumentParser(description="推荐论文管理器 / Recommended Papers Manager")
    parser.add_argument("--papers", type=str, help="论文文件路径 (JSONL格式) / Papers file path (JSONL format)")
    parser.add_argument("--date", type=str, help="推荐日期 (YYYY-MM-DD) / Recommendation date (YYYY-MM-DD)")
    parser.add_argument("--repo", type=str, default=".", help="仓库路径 / Repository path")
    parser.add_argument("--branch", type=str, default="data", help="分支名称 / Branch name")
    
    args = parser.parse_args()
    
    if args.papers and args.date:
        # 读取论文 / Read papers
        papers = []
        with open(args.papers, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    papers.append(json.loads(line))
        
        # 保存到 Git / Save to Git
        success = save_recommended_papers(papers, args.date, args.repo, args.branch)
        
        if success:
            print(f"✅ 成功保存 {len(papers)} 篇推荐论文 / Successfully saved {len(papers)} recommended papers")
        else:
            print(f"❌ 保存失败 / Failed to save")
    else:
        print("❌ 错误：需要指定 --papers 和 --date / Error: --papers and --date are required")
def main():
    """
    命令行入口 / Command line entry point
    
    用法 / Usage:
        # 获取最新推荐
        python recommended_papers.py --list latest
        
        # 获取指定日期的推荐
        python recommended_papers.py --list date --date 2024-02-24
        
        # 获取统计信息
        python recommended_papers.py --stats
        
        # 导出为 JSON
        python recommended_papers.py --export json --output recommended.json
        
        # 导出为 Markdown
        python recommended_papers.py --export markdown --output recommended.md
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="推荐论文管理 / Recommended Papers Management")
    parser.add_argument("--list", type=str, choices=["latest", "date", "all"],
                       help="列表显示方式 / List display mode")
    parser.add_argument("--date", type=str, help="日期 / Date (YYYY-MM-DD)")
    parser.add_argument("--stats", action="store_true", help="显示统计信息 / Show statistics")
    parser.add_argument("--export", type=str, choices=["json", "markdown"],
                       help="导出格式 / Export format")
    parser.add_argument("--output", type=str, help="输出文件 / Output file")
    
    args = parser.parse_args()
    
    manager = RecommendedPapersManager()
    
    # 显示统计信息 / Show statistics
    if args.stats:
        stats = manager.get_recommended_papers_statistics()
        print("\n📊 推荐论文统计 / Recommended Papers Statistics:")
        print(f"   总推荐数: {stats['总推荐数']}")
        print(f"   优先级论文: {stats['优先级论文']}")
        print(f"   普通论文: {stats['普通论文']}")
        print(f"\n   分类统计 / Category Statistics:")
        for category, count in stats["分类统计"].items():
            print(f"      {category}: {count}")
        print()
        return
    
    # 列表显示 / List display
    if args.list:
        if args.list == "latest":
            papers = manager.get_latest_recommended_papers(limit=20)
            print(f"\n📚 最新推荐论文 ({len(papers)} 篇) / Latest Recommended Papers:")
        elif args.list == "date":
            if not args.date:
                print("❌ 请指定日期 / Please specify date (--date YYYY-MM-DD)")
                return
            papers = manager.get_recommended_papers_by_date(args.date)
            print(f"\n📚 {args.date} 推荐论文 ({len(papers)} 篇) / Recommended Papers for {args.date}:")
        else:  # all
            papers = manager.get_all_recommended_papers()
            print(f"\n📚 所有推荐论文 ({len(papers)} 篇) / All Recommended Papers:")
        
        for idx, paper in enumerate(papers, 1):
            priority_marker = "⭐ " if paper.get('is_priority') else ""
            print(f"\n{idx}. {priority_marker}{paper.get('title', 'N/A')}")
            print(f"   分类: {paper.get('category', 'N/A')}")
            print(f"   日期: {paper.get('recommended_date', 'N/A')}")
            if paper.get('tldr') and paper['tldr'] != 'N/A':
                tldr = paper['tldr'][:150] + "..." if len(paper['tldr']) > 150 else paper['tldr']
                print(f"   AI总结: {tldr}")
        
        print()
        return
    
    # 导出 / Export
    if args.export:
        if not args.output:
            print("❌ 请指定输出文件 / Please specify output file (--output filename)")
            return
        
        if args.export == "json":
            manager.export_to_json(args.output)
        elif args.export == "markdown":
            manager.export_to_markdown(args.output)


if __name__ == "__main__":
    main()
