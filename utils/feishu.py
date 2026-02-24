#!/usr/bin/env python3
"""
飞书(Feishu)机器人通知模块 / Feishu Robot Notification Module

功能说明 / Features:
- 通过飞书webhook发送每日爬取统计信息 / Send daily crawl statistics via Feishu webhook
- 支持签名校验，提高安全性 / Support signature verification for enhanced security
- 支持卡片消息格式，展现更丰富的信息 / Support card message format for richer information display
"""

import json
import os
import sys
import hmac
import hashlib
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# 导入 Git 辅助工具 / Import Git helper
try:
    from feishu_git_helper import get_data_from_branch, get_latest_date
except ImportError:
    # 如果无法导入，使用本地文件读取 / Fall back to local file reading
    get_data_from_branch = None
    get_latest_date = None

# 导入推荐论文管理器 / Import recommended papers manager
try:
    from recommended_papers import RecommendedPapersManager
except ImportError:
    RecommendedPapersManager = None


class FeishuRobot:
    """飞书机器人类 / Feishu Robot Class"""
    
    def __init__(self, webhook_url: str, secret: Optional[str] = None):
        """
        初始化飞书机器人
        Initialize Feishu Robot
        
        Args:
            webhook_url (str): 飞书webhook URL / Feishu webhook URL
            secret (str, optional): 机器人密钥，用于签名校验 / Robot secret for signature verification
        """
        self.webhook_url = webhook_url
        self.secret = secret
    
    def _generate_signature(self) -> tuple:
        """
        生成签名和时间戳
        Generate signature and timestamp
        
        Returns:
            tuple: (timestamp, sign) 时间戳和签名 / Timestamp and signature
        """
        if not self.secret:
            return None, None
        
        timestamp = int(time.time())
        string_to_sign = f"{timestamp}\n{self.secret}"
        
        hmac_code = hmac.new(
            string_to_sign.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Base64 encode
        import base64
        sign = base64.b64encode(hmac_code).decode()
        
        return timestamp, sign
    
    def send_text_message(self, content: str) -> bool:
        """
        发送文本消息
        Send text message
        
        Args:
            content (str): 消息内容 / Message content
            
        Returns:
            bool: 发送是否成功 / Whether sending succeeded
        """
        try:
            timestamp, sign = self._generate_signature()
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "msg_type": "text",
                "content": {
                    "text": content
                }
            }
            
            # 添加签名参数到URL / Add signature parameters to URL
            url = self.webhook_url
            if timestamp and sign:
                url = f"{url}&timestamp={timestamp}&sign={sign}"
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    return True
                else:
                    print(f"飞书API错误: {result.get('msg', 'Unknown error')}", file=sys.stderr)
                    return False
            else:
                print(f"HTTP错误: {response.status_code}", file=sys.stderr)
                return False
                
        except Exception as e:
            print(f"发送飞书消息失败: {e}", file=sys.stderr)
            return False
    
    def send_card_message(self, title: str, content_dict: Dict) -> bool:
        """
        发送卡片消息（更丰富的格式）
        Send card message (richer format)
        
        Args:
            title (str): 卡片标题 / Card title
            content_dict (dict): 卡片内容信息 / Card content information
            
        Returns:
            bool: 发送是否成功 / Whether sending succeeded
        """
        try:
            timestamp, sign = self._generate_signature()
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # 构建字段列表 / Build field list
            fields = []
            for key, value in content_dict.items():
                fields.append({
                    "is_short": False,
                    "text": {
                        "content": f"**{key}**: {value}",
                        "tag": "lark_md"
                    }
                })
            
            payload = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": f"# {title}"
                        },
                        {
                            "tag": "div",
                            "fields": fields
                        }
                    ]
                }
            }
            
            # 添加签名参数到URL / Add signature parameters to URL
            url = self.webhook_url
            # if timestamp and sign:
            #     url = f"{url}&timestamp={timestamp}&sign={sign}"
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    return True
                else:
                    print(f"飞书API错误: {result.get('msg', 'Unknown error')}", file=sys.stderr)
                    return False
            else:
                print(f"HTTP错误: {response.status_code}", file=sys.stderr)
                return False
                
        except Exception as e:
            print(f"发送飞书卡片消息失败: {e}", file=sys.stderr)
            return False


def get_crawl_statistics(data_file: str) -> Dict[str, any]:
    """
    从爬取的数据文件中获取统计信息
    Get statistics from crawled data file
    
    Args:
        data_file (str): 数据文件路径 / Path to data file
        
    Returns:
        dict: 统计信息 / Statistics information
    """
    stats = {
        "总论文数": 0,
        "分类统计": {},
        "首篇论文": "N/A",
        "最后论文": "N/A",
    }
    
    if not os.path.exists(data_file):
        return stats
    
    try:
        papers = []
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    papers.append(json.loads(line))
        
        stats["总论文数"] = len(papers)
        
        # 统计分类 / Count categories
        category_count = {}
        for paper in papers:
            categories = paper.get('categories', [])
            if categories:
                cate = categories[0]
                category_count[cate] = category_count.get(cate, 0) + 1
        
        # 按数量排序 / Sort by count
        sorted_cates = sorted(category_count.items(), key=lambda x: x[1], reverse=True)
        stats["分类统计"] = {cate: count for cate, count in sorted_cates[:5]}  # 只显示前5个
        
        # 获取第一篇和最后一篇论文 / Get first and last papers
        if papers:
            stats["首篇论文"] = papers[0].get('title', 'N/A')[:50]  # 截断长标题
            stats["最后论文"] = papers[-1].get('title', 'N/A')[:50]
        
    except Exception as e:
        print(f"读取统计信息失败: {e}", file=sys.stderr)
    
    return stats


def get_data_content(data_source: str, date_str: Optional[str] = None, from_git: bool = False) -> Optional[str]:
    """
    读取数据内容（支持本地文件或 Git 分支）
    Get data content (support local file or Git branch)
    
    Args:
        data_source (str): 数据源 / Data source
                          - 如果 from_git=False: 本地文件路径 / Local file path
                          - 如果 from_git=True: Git 分支名称 / Git branch name
        date_str (str, optional): 日期字符串 / Date string (YYYY-MM-DD)
        from_git (bool): 是否从 Git 分支读取 / Whether to read from Git branch
        
    Returns:
        str: 文件内容，如果失败返回 None
    """
    if from_git:
        # 从 Git 分支读取 / Read from Git branch
        if get_data_from_branch is None:
            print("⚠️ Git 辅助工具不可用，使用本地文件 / Git helper not available, using local file", file=sys.stderr)
            from_git = False
        else:
            print(f"📂 从 Git 分支读取数据 / Reading data from Git branch: {data_source}", file=sys.stderr)
            try:
                content = get_data_from_branch(data_source, date_str)
                if content:
                    return content
                else:
                    print(f"❌ 从分支读取失败，尝试本地文件 / Failed to read from branch, trying local file", file=sys.stderr)
                    from_git = False
            except Exception as e:
                print(f"⚠️ Git 读取出错: {e} / Git read error: {e}", file=sys.stderr)
                from_git = False
    
    # 从本地文件读取 / Read from local file
    if not from_git:
        if not os.path.exists(data_source):
            print(f"❌ 文件不存在 / File not found: {data_source}", file=sys.stderr)
            return None
        
        try:
            with open(data_source, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 读取本地文件失败 / Failed to read local file: {e}", file=sys.stderr)
            return None


def get_featured_papers(data_content: str, top_n: int = 5, priority_keywords: List[str] = None) -> List[Dict]:
    """
    获取精选论文（带 AI 总结的论文，优先级支持）
    Get featured papers (papers with AI summaries, with priority support)
    
    Args:
        data_content (str): 数据内容（JSONL 格式）/ Data content (JSONL format)
        top_n (int): 返回的论文数量 / Number of papers to return
        priority_keywords (list): 优先级关键词列表 / Priority keywords list (e.g., ["autonomous driving"])
        
    Returns:
        list: 精选论文列表，每个包含完整title、authors、tldr、category等信息
    """
    if priority_keywords is None:
        priority_keywords = ["autonomous driving", "自动驾驶"]
    
    featured = []
    
    if not data_content or not data_content.strip():
        return featured
    
    try:
        papers = []
        for line in data_content.split('\n'):
            if line.strip():
                papers.append(json.loads(line))
        
        # 筛选有 AI 总结的论文（优先级高）
        papers_with_ai = [p for p in papers if p.get('AI') and p['AI'].get('tldr')]
        
        # 按优先级关键词分组
        priority_papers = []  # 包含关键词的论文
        other_papers = []     # 其他论文
        
        for paper in papers_with_ai:
            title_lower = paper.get('title', '').lower()
            summary_lower = paper.get('summary', '').lower()
            ai_summary_lower = paper.get('AI', {}).get('tldr', '').lower()
            
            # 检查是否包含优先级关键词
            has_priority = any(
                keyword.lower() in title_lower or 
                keyword.lower() in summary_lower or
                keyword.lower() in ai_summary_lower
                for keyword in priority_keywords
            )
            
            if has_priority:
                priority_papers.append(paper)
            else:
                other_papers.append(paper)
        
        # 合并：优先级论文在前，然后是其他论文
        selected_papers = (priority_papers + other_papers)[:top_n]
        
        for paper in selected_papers:
            # 获取完整标题（不截断）
            full_title = paper.get('title', 'N/A')
            
            # 获取完整 AI 总结（不截断或只做合理的限制）
            ai_tldr = 'N/A'
            has_ai = False
            if paper.get('AI'):
                ai_data = paper['AI']
                ai_tldr = ai_data.get('tldr', 'N/A')  # 完整显示
                has_ai = True
            else:
                # 如果没有 AI 总结，使用摘要
                summary = paper.get('summary', 'N/A')
                ai_tldr = summary if summary else 'N/A'
            
            paper_info = {
                "title": full_title,  # 完整标题
                "authors": ", ".join(paper.get('authors', ['N/A'])[:3]),  # 前3个作者
                "category": paper.get('categories', ['N/A'])[0],
                "url": paper.get('abs', ''),
                "id": paper.get('id', ''),
                "tldr": ai_tldr,  # 完整 AI 总结
                "has_ai": has_ai,
                "is_priority": any(
                    keyword.lower() in full_title.lower() or
                    keyword.lower() in ai_tldr.lower()
                    for keyword in priority_keywords
                )
            }
            
            featured.append(paper_info)
        
    except Exception as e:
        print(f"获取精选论文失败: {e}", file=sys.stderr)
    
    return featured


def send_daily_crawl_notification(data_file: str, date_str: str, mode: str = "featured", from_git: bool = False, git_branch: str = "data") -> bool:
    """
    发送每日爬取的通知
    Send daily crawl notification
    
    Args:
        data_file (str): 数据文件路径或 Git 分支名 / Path to data file or Git branch name
        date_str (str): 日期字符串 / Date string
        mode (str): 通知模式 / Notification mode
                   - "featured": 精选5篇文章（带AI总结）/ Featured 5 papers with AI summaries
                   - "statistics": 统计信息模式 / Statistics mode
        from_git (bool): 是否从 Git 分支读取 / Whether to read from Git branch
        git_branch (str): Git 分支名称 / Git branch name (used when from_git=True)
        
    Returns:
        bool: 是否成功发送 / Whether sending succeeded
    """
    # 从环境变量获取配置 / Get configuration from environment variables
    webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
    secret = os.environ.get('FEISHU_SECRET')
    
    if not webhook_url:
        print("未设置FEISHU_WEBHOOK_URL，跳过飞书通知 / FEISHU_WEBHOOK_URL not set, skipping Feishu notification", file=sys.stderr)
        return False
    
    # 获取数据内容 / Get data content
    data_content = get_data_content(
        data_source=git_branch if from_git else data_file,
        date_str=date_str if from_git else None,
        from_git=from_git
    )
    
    if not data_content:
        print("❌ 无法获取数据 / Failed to get data", file=sys.stderr)
        return False
    
    # 创建机器人实例 / Create robot instance
    robot = FeishuRobot(webhook_url, secret)
    
    # 根据模式选择不同的通知内容 / Choose notification content based on mode
    if mode == "featured":
        return _send_featured_papers_notification(robot, data_content, date_str)
    else:
        return _send_statistics_notification(robot, data_content, date_str)


def _send_statistics_notification(robot: FeishuRobot, data_content: str, date_str: str) -> bool:
    """
    发送统计信息通知（旧模式）
    Send statistics notification (legacy mode)
    
    Args:
        robot: FeishuRobot 实例
        data_content: 数据内容（JSONL 格式）
        date_str: 日期字符串
        
    Returns:
        bool: 是否成功发送
    """
    # 解析数据并获取统计信息 / Parse data and get statistics
    stats = {
        "总论文数": 0,
        "分类统计": {},
        "首篇论文": "N/A",
        "最后论文": "N/A",
    }
    
    try:
        papers = []
        for line in data_content.split('\n'):
            if line.strip():
                papers.append(json.loads(line))
        
        stats["总论文数"] = len(papers)
        
        # 统计分类 / Count categories
        category_count = {}
        for paper in papers:
            categories = paper.get('categories', [])
            if categories:
                cate = categories[0]
                category_count[cate] = category_count.get(cate, 0) + 1
        
        # 按数量排序 / Sort by count
        sorted_cates = sorted(category_count.items(), key=lambda x: x[1], reverse=True)
        stats["分类统计"] = {cate: count for cate, count in sorted_cates[:5]}
        
        # 获取第一篇和最后一篇论文 / Get first and last papers
        if papers:
            stats["首篇论文"] = papers[0].get('title', 'N/A')[:50]
            stats["最后论文"] = papers[-1].get('title', 'N/A')[:50]
    
    except Exception as e:
        print(f"解析数据失败 / Failed to parse data: {e}", file=sys.stderr)
    
    # 构建消息内容 / Build message content
    title = f"🤖 arXiv 每日爬取统计 - {date_str}"
    
    message_content = {
        "爬取日期": date_str,
        "总论文数": str(stats["总论文数"]),
    }
    
    # 添加分类统计 / Add category statistics
    if stats["分类统计"]:
        cate_str = ", ".join([f"{cate}: {count}" for cate, count in stats["分类统计"].items()])
        message_content["分类统计 (TOP 5)"] = cate_str
    
    if stats["首篇论文"] != "N/A":
        message_content["首篇论文"] = stats["首篇论文"]
    
    if stats["最后论文"] != "N/A":
        message_content["最后论文"] = stats["最后论文"]
    
    message_content["爬取完成时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 发送消息 / Send message
    success = robot.send_card_message(title, message_content)
    
    if success:
        print("✅ 飞书通知发送成功 / Feishu notification sent successfully", file=sys.stderr)
    else:
        print("❌ 飞书通知发送失败 / Feishu notification failed", file=sys.stderr)
    
    return success


def _send_featured_papers_notification(robot: FeishuRobot, data_content: str, date_str: str) -> bool:
    """
    发送精选论文通知（新模式，完整显示）
    Send featured papers notification (new mode, full display)
    
    Args:
        robot: FeishuRobot 实例
        data_content: 数据内容（JSONL 格式）
        date_str: 日期字符串
        
    Returns:
        bool: 是否成功发送
    """
    # 获取精选论文（优先级：autonomous driving）
    priority_keywords = ["autonomous driving", "自动驾驶", "self driving", "VLA"]
    featured_papers = get_featured_papers(data_content, top_n=10, priority_keywords=priority_keywords)
    
    # 保存推荐论文到 Git data 分支 / Save recommended papers to Git data branch
    if RecommendedPapersManager:
        try:
            # 使用 Git-based 管理器保存论文 / Use Git-based manager to save papers
            manager = RecommendedPapersManager(repo_path=".", branch_name="data")
            success = manager.save_recommended_papers(featured_papers, date_str)
            if success:
                print(f"✅ 推荐论文已保存到 Git data 分支 / Recommended papers saved to Git data branch", file=sys.stderr)
            else:
                print(f"⚠️ 推荐论文保存到 Git data 分支失败 / Failed to save recommended papers to Git data branch", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ 保存推荐论文失败: {e} / Failed to save recommended papers: {e}", file=sys.stderr)
    
    if not featured_papers:
        print("没有可用的论文数据 / No available paper data", file=sys.stderr)
        return False
    
    # 构建消息内容 / Build message content
    title = f"📚 arXiv 精选论文 - {date_str}"
    
    message_content = {
        "更新日期": date_str,
        "精选论文数": str(len(featured_papers)),
        "优先领域": "自动驾驶 (Autonomous Driving)",
    }
    
    # 添加每篇论文的完整信息 / Add complete information for each paper
    for idx, paper in enumerate(featured_papers, 1):
        # 构建论文条目 - 完整显示标题和总结
        priority_marker = "⭐ " if paper.get('is_priority') else "  "
        
        # 完整标题
        paper_entry = f"{priority_marker}[{idx}] {paper['title']}\n"
        
        # 作者和分类
        paper_entry += f"📌 分类: {paper['category']} | 作者: {paper['authors']}\n"
        
        # 完整 AI 总结或摘要
        if paper.get('tldr') and paper['tldr'] != 'N/A':
            summary_prefix = "🤖 AI总结: " if paper.get('has_ai') else "📝 摘要: "
            paper_entry += f"{summary_prefix}{paper['tldr']}\n"
        
        # 论文链接
        if paper.get('id'):
            paper_entry += f"🔗 ID: {paper['id']}"
        
        message_content[f"论文 {idx}"] = paper_entry
    
    # 添加底部信息 / Add footer
    message_content["通知时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_content["数据来源"] = "arXiv + AI 增强分析"
    message_content["说明"] = "⭐ 标记表示包含 'autonomous driving' 相关内容，优先展示"
    message_content["查看更多"] = "https://myzhangwww.github.io/daily-arXiv-ai-enhanced/index.html"
    
    # 发送消息 / Send message
    success = robot.send_card_message(title, message_content)
    
    if success:
        print("✅ 飞书通知发送成功 / Feishu notification sent successfully", file=sys.stderr)
    else:
        print("❌ 飞书通知发送失败 / Feishu notification failed", file=sys.stderr)
    
    return success


def main():
    """
    命令行入口 / Command line entry point
    
    用法 / Usage:
        # 从本地文件发送
        python feishu.py --data <data_file> --date <date_str> [--mode featured|statistics]
        
        # 从 Git 分支发送
        python feishu.py --from-git --branch <branch_name> --date <date_str> [--mode featured|statistics]
        
        # 自动获取最新数据
        python feishu.py --from-git --branch data [--mode featured|statistics]
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书通知模块 / Feishu Notification Module")
    parser.add_argument("--data", type=str, default=None, help="本地数据文件路径 / Path to local data file")
    parser.add_argument("--date", type=str, default=None, help="日期字符串 / Date string (YYYY-MM-DD)")
    parser.add_argument("--mode", type=str, default="featured", choices=["featured", "statistics"],
                       help="通知模式 / Notification mode")
    
    # Git 相关参数 / Git-related arguments
    parser.add_argument("--from-git", action="store_true", help="从 Git 分支读取数据 / Read data from Git branch")
    parser.add_argument("--branch", type=str, default="data", help="Git 分支名称 / Git branch name (default: data)")
    
    args = parser.parse_args()
    
    # 验证参数 / Validate arguments
    if not args.from_git and not args.data:
        parser.error("必须指定 --data 或 --from-git / Must specify either --data or --from-git")
    
    # 如果从 Git 分支读取且没有指定日期，自动获取最新日期
    if args.from_git and not args.date and get_latest_date:
        args.date = get_latest_date(args.branch)
        if not args.date:
            print("❌ 无法获取最新日期 / Failed to get latest date", file=sys.stderr)
            sys.exit(1)
        print(f"📅 使用最新日期 / Using latest date: {args.date}", file=sys.stderr)
    
    # 确保有日期信息 / Ensure we have a date
    if not args.date:
        print("❌ 必须指定日期 / Date is required (--date YYYY-MM-DD)", file=sys.stderr)
        sys.exit(1)
    
    # 发送通知 / Send notification
    success = send_daily_crawl_notification(
        data_file=args.data,
        date_str=args.date,
        mode=args.mode,
        from_git=args.from_git,
        git_branch=args.branch
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
