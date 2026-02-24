#!/usr/bin/env python3
"""
Git 辅助工具 / Git Helper Utilities

功能说明 / Features:
- 从 Git data 分支读取数据文件 / Read data files from Git data branch
- 支持从远程分支获取最新数据 / Support fetching latest data from remote branch
- 自动化处理 Git 操作，无需手动切换分支 / Automate Git operations without manual branch switching
"""

import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import sys


class GitDataHelper:
    """Git 数据辅助类 / Git Data Helper Class"""
    
    def __init__(self, repo_path: str = "."):
        """
        初始化 Git 辅助工具
        Initialize Git helper
        
        Args:
            repo_path (str): Git 仓库路径 / Path to Git repository
        """
        self.repo_path = Path(repo_path).resolve()
        if not self._is_git_repo():
            raise ValueError(f"指定路径不是 Git 仓库 / Path is not a Git repository: {self.repo_path}")
        self._original_branch = None  # 存储原分支名 / Store original branch name
    
    def _is_git_repo(self) -> bool:
        """检查是否为 Git 仓库 / Check if path is a Git repository"""
        return (self.repo_path / ".git").exists()
    
    def _get_current_branch(self) -> Optional[str]:
        """
        获取当前分支名
        Get current branch name
        
        Returns:
            str: 分支名称，如果失败返回 None
        """
        code, stdout, _ = self._run_git_command("rev-parse --abbrev-ref HEAD")
        if code == 0:
            return stdout.strip()
        return None
    
    def _save_current_branch(self) -> None:
        """保存当前分支名 / Save current branch name"""
        self._original_branch = self._get_current_branch()
        if self._original_branch:
            print(f"📌 保存原分支 / Saved original branch: {self._original_branch}", file=sys.stderr)
    
    def _restore_original_branch(self) -> bool:
        """
        恢复原分支
        Restore original branch
        
        Returns:
            bool: 是否成功
        """
        if not self._original_branch:
            return True
        
        current = self._get_current_branch()
        if current == self._original_branch:
            return True
        
        print(f"🔄 切换回原分支 / Switching back to original branch: {self._original_branch}", file=sys.stderr)
        code, _, stderr = self._run_git_command(f"checkout {self._original_branch}")
        if code != 0:
            print(f"⚠️  警告 / Warning: 无法切换回原分支 / Failed to switch back: {stderr}", file=sys.stderr)
            return False
        
        print(f"✅ 成功切换回原分支 / Successfully switched back to: {self._original_branch}", file=sys.stderr)
        return True
    
    def _run_git_command(self, command: str) -> tuple[int, str, str]:
        """
        运行 Git 命令
        Run Git command
        
        Args:
            command (str): Git 命令（不包含 git 前缀）/ Git command without 'git' prefix
            
        Returns:
            tuple: (return_code, stdout, stderr)
        """
        try:
            full_command = f"git -C {self.repo_path} {command}"
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "命令超时 / Command timeout"
        except Exception as e:
            return -1, "", str(e)
    
    def branch_exists(self, branch_name: str) -> bool:
        """
        检查分支是否存在（包括远程分支）
        Check if branch exists (including remote branches)
        
        Args:
            branch_name (str): 分支名称 / Branch name
            
        Returns:
            bool: 分支是否存在
        """
        # 检查本地分支 / Check local branch
        code, stdout, _ = self._run_git_command(f"branch --list {branch_name}")
        if code == 0 and branch_name in stdout:
            return True
        
        # 检查远程分支 / Check remote branch
        code, stdout, _ = self._run_git_command(f"branch -r --list origin/{branch_name}")
        if code == 0 and f"origin/{branch_name}" in stdout:
            return True
        
        return False
    
    def fetch_branch(self, branch_name: str, auto_restore: bool = True) -> bool:
        """
        从远程获取指定分支（如果不存在则创建）
        Fetch branch from remote (create if not exists)
        
        Args:
            branch_name (str): 分支名称 / Branch name
            auto_restore (bool): 是否完成后自动恢复原分支 / Auto restore original branch after done
            
        Returns:
            bool: 是否成功
        """
        # 保存当前分支 / Save current branch
        if auto_restore:
            self._save_current_branch()
        
        try:
            # 先尝试 fetch / Try to fetch first
            code, _, stderr = self._run_git_command("fetch origin")
            if code != 0:
                print(f"警告 / Warning: Git fetch 失败 / failed: {stderr}", file=sys.stderr)
                return False
            
            # 检查远程分支是否存在 / Check if remote branch exists
            code, stdout, _ = self._run_git_command(f"branch -r --list origin/{branch_name}")
            if code != 0 or f"origin/{branch_name}" not in stdout:
                print(f"错误 / Error: 远程分支不存在 / Remote branch does not exist: {branch_name}", file=sys.stderr)
                return False
            
            # 检查本地分支是否存在 / Check if local branch exists
            code, stdout, _ = self._run_git_command(f"branch --list {branch_name}")
            if code == 0 and branch_name in stdout:
                # 本地分支已存在，更新到最新 / Local branch exists, update to latest
                code, _, stderr = self._run_git_command(f"checkout {branch_name}")
                if code != 0:
                    print(f"错误 / Error: 无法切换到分支 / Failed to checkout branch: {stderr}", file=sys.stderr)
                    return False
                
                code, _, stderr = self._run_git_command(f"pull origin {branch_name}")
                if code != 0:
                    print(f"警告 / Warning: 更新分支失败 / Failed to pull branch: {stderr}", file=sys.stderr)
            else:
                # 创建本地分支跟踪远程分支 / Create local branch tracking remote
                code, _, stderr = self._run_git_command(f"checkout --track origin/{branch_name}")
                if code != 0:
                    print(f"错误 / Error: 无法创建分支 / Failed to create branch: {stderr}", file=sys.stderr)
                    return False
            
            return True
        finally:
            # 无论成功或失败，都尝试恢复原分支 / Always try to restore original branch
            if auto_restore:
                self._restore_original_branch()
    
    def read_file_from_branch(self, branch_name: str, file_path: str) -> Optional[str]:
        """
        从指定分支读取文件内容（不切换分支）
        Read file content from branch without switching branch
        
        Args:
            branch_name (str): 分支名称 / Branch name
            file_path (str): 文件路径（相对于仓库根目录）/ File path relative to repo root
            
        Returns:
            str: 文件内容，如果失败返回 None
        """
        code, stdout, stderr = self._run_git_command(f"show {branch_name}:{file_path}")
        if code != 0:
            print(f"错误 / Error: 无法读取文件 / Failed to read file: {stderr}", file=sys.stderr)
            return None
        return stdout
    
    def get_latest_file_in_branch(self, branch_name: str, directory: str = "data", pattern: str = "*.jsonl") -> Optional[str]:
        """
        获取指定分支中目录下的最新文件内容
        Get latest file content from directory in branch
        
        Args:
            branch_name (str): 分支名称 / Branch name
            directory (str): 目录名称 / Directory name
            pattern (str): 文件模式 / File pattern
            
        Returns:
            str: 文件内容，如果失败返回 None
        """
        # 列出目录中的文件 / List files in directory
        code, stdout, stderr = self._run_git_command(f"ls-tree -r --name-only {branch_name} {directory}/")
        if code != 0:
            print(f"错误 / Error: 无法列出分支文件 / Failed to list files in branch: {stderr}", file=sys.stderr)
            return None
        
        files = stdout.split('\n')
        files = [f for f in files if f and f.endswith('.jsonl')]
        
        if not files:
            print(f"警告 / Warning: 分支中没有 JSONL 文件 / No JSONL files found in branch", file=sys.stderr)
            return None
        
        # 获取最新的文件 / Get latest file (last one when sorted)
        latest_file = sorted(files)[-1]
        
        print(f"📄 从 {branch_name} 分支读取文件 / Reading file from {branch_name} branch: {latest_file}", file=sys.stderr)
        
        return self.read_file_from_branch(branch_name, latest_file)
    
    def get_file_date_from_branch(self, branch_name: str, directory: str = "data") -> Optional[str]:
        """
        从分支获取最新数据文件的日期
        Get date of latest data file from branch
        
        Args:
            branch_name (str): 分支名称 / Branch name
            directory (str): 目录名称 / Directory name
            
        Returns:
            str: 日期字符串 (YYYY-MM-DD)，如果失败返回 None
        """
        code, stdout, stderr = self._run_git_command(f"ls-tree -r --name-only {branch_name} {directory}/")
        if code != 0:
            return None
        
        files = stdout.split('\n')
        jsonl_files = [f for f in files if f and f.endswith('.jsonl')]
        
        if not jsonl_files:
            return None
        
        # 从文件名提取日期 (假设格式为 YYYY-MM-DD.jsonl)
        latest_file = sorted(jsonl_files)[-1]
        filename = Path(latest_file).stem  # 获取文件名（不含扩展名）
        
        return filename


class GitDataManager:
    """Git 数据管理器 / Git Data Manager"""
    
    def __init__(self, repo_path: str = ".", branch_name: str = "data"):
        """
        初始化管理器
        Initialize manager
        
        Args:
            repo_path (str): Git 仓库路径 / Path to Git repository
            branch_name (str): 数据分支名称 / Data branch name
        """
        self.repo_path = Path(repo_path).resolve()
        self.branch_name = branch_name
        self.helper = GitDataHelper(repo_path)
    
    def get_data_for_notification(self, date_str: Optional[str] = None) -> Optional[str]:
        """
        获取用于发送通知的数据（自动恢复原分支）
        Get data for notification (auto restore original branch)
        
        Args:
            date_str (str, optional): 日期字符串 / Date string (YYYY-MM-DD)
                                      如果不指定，将获取最新的数据文件
                                      If not specified, will get latest data file
            
        Returns:
            str: 文件内容（JSONL 格式），如果失败返回 None
        """
        # 检查分支是否存在 / Check if branch exists
        if not self.helper.branch_exists(self.branch_name):
            print(f"错误 / Error: 分支不存在 / Branch does not exist: {self.branch_name}", file=sys.stderr)
            return None
        
        # 确保分支是最新的（自动恢复原分支）/ Ensure branch is up to date (auto restore)
        if not self.helper.fetch_branch(self.branch_name, auto_restore=True):
            print(f"警告 / Warning: 无法获取最新分支 / Failed to fetch latest branch", file=sys.stderr)
        
        # 获取文件内容 / Get file content
        if date_str:
            # 从指定日期获取文件 / Get file from specified date
            file_path = f"data/{date_str}.jsonl"
            return self.helper.read_file_from_branch(self.branch_name, file_path)
        else:
            # 获取最新文件 / Get latest file
            return self.helper.get_latest_file_in_branch(self.branch_name)
    
    def get_latest_data_date(self) -> Optional[str]:
        """
        获取最新数据文件的日期
        Get date of latest data file
        
        Returns:
            str: 日期字符串 (YYYY-MM-DD)，如果失败返回 None
        """
        if not self.helper.branch_exists(self.branch_name):
            return None
        
        return self.helper.get_file_date_from_branch(self.branch_name)


# 快速访问函数 / Quick access functions

def get_data_from_branch(branch_name: str = "data", date_str: Optional[str] = None, repo_path: str = ".") -> Optional[str]:
    """
    快速从分支获取数据
    Quick function to get data from branch
    
    Args:
        branch_name (str): 分支名称 / Branch name
        date_str (str, optional): 日期字符串 / Date string (YYYY-MM-DD)
        repo_path (str): 仓库路径 / Repository path
        
    Returns:
        str: 文件内容，如果失败返回 None
    """
    try:
        manager = GitDataManager(repo_path, branch_name)
        return manager.get_data_for_notification(date_str)
    except Exception as e:
        print(f"错误 / Error: {e}", file=sys.stderr)
        return None


def get_latest_date(branch_name: str = "data", repo_path: str = ".") -> Optional[str]:
    """
    快速获取最新数据日期
    Quick function to get latest data date
    
    Args:
        branch_name (str): 分支名称 / Branch name
        repo_path (str): 仓库路径 / Repository path
        
    Returns:
        str: 日期字符串 (YYYY-MM-DD)，如果失败返回 None
    """
    try:
        manager = GitDataManager(repo_path, branch_name)
        return manager.get_latest_data_date()
    except Exception as e:
        print(f"错误 / Error: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    # 演示脚本 / Demo script
    import argparse
    
    parser = argparse.ArgumentParser(description="Git 数据辅助工具 / Git Data Helper")
    parser.add_argument("--branch", type=str, default="data", help="分支名称 / Branch name")
    parser.add_argument("--date", type=str, optional=True, help="日期 (YYYY-MM-DD) / Date (YYYY-MM-DD)")
    parser.add_argument("--repo", type=str, default=".", help="仓库路径 / Repository path")
    
    args = parser.parse_args()
    
    print(f"📂 获取数据 / Getting data from branch '{args.branch}'...\n")
    
    data = get_data_from_branch(args.branch, args.date, args.repo)
    if data:
        lines = data.split('\n')
        print(f"✅ 成功读取 {len(lines)} 行数据 / Successfully read {len(lines)} lines")
        print(f"📝 前 3 行数据示例 / First 3 lines preview:")
        for i, line in enumerate(lines[:3]):
            if line.strip():
                obj = json.loads(line)
                print(f"   {i+1}. {obj.get('title', 'N/A')[:60]}")
    else:
        print(f"❌ 读取失败 / Failed to read data")
