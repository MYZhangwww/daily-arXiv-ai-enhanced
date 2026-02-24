#!/usr/bin/env python3
"""
推荐论文管理模块 / Recommended Papers Management Module

功能说明 / Features:
- 保存发送到飞书的精选论文 / Save featured papers sent to Feishu
- 管理推荐论文历史 / Manage recommended papers history
- 支持查询、统计、导出推荐论文 / Support query, statistics, export recommended papers
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class RecommendedPapersManager:
    """推荐论文管理器 / Recommended Papers Manager"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化推荐论文管理器
        Initialize Recommended Papers Manager
        
        Args:
            data_dir (str): 数据目录 / Data directory
        """
        self.data_dir = data_dir
        self.recommended_file = os.path.join(data_dir, "recommended_papers.jsonl")
        
        # 确保数据目录存在 / Ensure data directory exists
        Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    def save_recommended_papers(self, papers: List[Dict], date_str: str) -> bool:
        """
        保存推荐论文（发送到飞书的论文）
        Save recommended papers (papers sent to Feishu)
        
        Args:
            papers (list): 论文列表 / List of papers
            date_str (str): 日期字符串 / Date string (YYYY-MM-DD)
            
        Returns:
            bool: 是否成功保存 / Whether saving succeeded
        """
        try:
            # 为每篇论文添加推荐日期和元数据 / Add recommendation date and metadata for each paper
            for paper in papers:
                paper['recommended_date'] = date_str
                paper['recommended_at'] = datetime.now().isoformat()
                paper['priority_status'] = 'priority' if paper.get('is_priority') else 'normal'
            
            # 追加到推荐论文文件 / Append to recommended papers file
            with open(self.recommended_file, 'a', encoding='utf-8') as f:
                for paper in papers:
                    f.write(json.dumps(paper, ensure_ascii=False) + '\n')
            
            print(f"✅ 保存 {len(papers)} 篇推荐论文 / Saved {len(papers)} recommended papers")
            return True
            
        except Exception as e:
            print(f"❌ 保存推荐论文失败 / Failed to save recommended papers: {e}")
            return False
    
    def get_recommended_papers_by_date(self, date_str: str) -> List[Dict]:
        """
        获取指定日期的推荐论文
        Get recommended papers for a specific date
        
        Args:
            date_str (str): 日期字符串 / Date string (YYYY-MM-DD)
            
        Returns:
            list: 推荐论文列表 / List of recommended papers
        """
        papers = []
        
        if not os.path.exists(self.recommended_file):
            return papers
        
        try:
            with open(self.recommended_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        paper = json.loads(line)
                        if paper.get('recommended_date') == date_str:
                            papers.append(paper)
        
        except Exception as e:
            print(f"❌ 读取推荐论文失败 / Failed to read recommended papers: {e}")
        
        return papers
    
    def get_latest_recommended_papers(self, limit: int = 10) -> List[Dict]:
        """
        获取最新推荐的论文
        Get latest recommended papers
        
        Args:
            limit (int): 返回的论文数量 / Number of papers to return
            
        Returns:
            list: 推荐论文列表 / List of recommended papers
        """
        papers = []
        
        if not os.path.exists(self.recommended_file):
            return papers
        
        try:
            with open(self.recommended_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        papers.append(json.loads(line))
            
            # 按推荐时间倒序排列 / Sort by recommendation time in descending order
            papers.sort(
                key=lambda x: x.get('recommended_at', ''),
                reverse=True
            )
            
            return papers[:limit]
        
        except Exception as e:
            print(f"❌ 读取推荐论文失败 / Failed to read recommended papers: {e}")
        
        return papers
    
    def get_all_recommended_papers(self) -> List[Dict]:
        """
        获取所有推荐论文
        Get all recommended papers
        
        Returns:
            list: 所有推荐论文 / All recommended papers
        """
        papers = []
        
        if not os.path.exists(self.recommended_file):
            return papers
        
        try:
            with open(self.recommended_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        papers.append(json.loads(line))
        
        except Exception as e:
            print(f"❌ 读取推荐论文失败 / Failed to read recommended papers: {e}")
        
        return papers
    
    def get_recommended_papers_statistics(self) -> Dict:
        """
        获取推荐论文统计信息
        Get recommended papers statistics
        
        Returns:
            dict: 统计信息 / Statistics information
        """
        stats = {
            "总推荐数": 0,
            "优先级论文": 0,
            "普通论文": 0,
            "推荐日期": [],
            "分类统计": {},
            "关键字统计": {}
        }
        
        papers = self.get_all_recommended_papers()
        stats["总推荐数"] = len(papers)
        
        # 统计优先级 / Count priority
        for paper in papers:
            if paper.get('priority_status') == 'priority':
                stats["优先级论文"] += 1
            else:
                stats["普通论文"] += 1
        
        # 统计推荐日期 / Count recommendation dates
        recommended_dates = {}
        for paper in papers:
            date = paper.get('recommended_date')
            if date:
                recommended_dates[date] = recommended_dates.get(date, 0) + 1
        stats["推荐日期"] = dict(sorted(recommended_dates.items(), reverse=True))
        
        # 统计分类 / Count categories
        category_count = {}
        for paper in papers:
            category = paper.get('category', 'Unknown')
            category_count[category] = category_count.get(category, 0) + 1
        stats["分类统计"] = dict(sorted(category_count.items(), key=lambda x: x[1], reverse=True))
        
        return stats
    
    def export_to_json(self, output_file: str) -> bool:
        """
        导出推荐论文为 JSON 格式
        Export recommended papers to JSON format
        
        Args:
            output_file (str): 输出文件路径 / Output file path
            
        Returns:
            bool: 是否成功导出 / Whether exporting succeeded
        """
        try:
            papers = self.get_all_recommended_papers()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(papers, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 导出 {len(papers)} 篇推荐论文到 {output_file}")
            return True
        
        except Exception as e:
            print(f"❌ 导出推荐论文失败 / Failed to export recommended papers: {e}")
            return False
    
    def export_to_markdown(self, output_file: str, limit: int = None) -> bool:
        """
        导出推荐论文为 Markdown 格式
        Export recommended papers to Markdown format
        
        Args:
            output_file (str): 输出文件路径 / Output file path
            limit (int): 限制数量 / Limit number
            
        Returns:
            bool: 是否成功导出 / Whether exporting succeeded
        """
        try:
            papers = self.get_all_recommended_papers()
            if limit:
                papers = papers[:limit]
            
            # 按推荐日期分组 / Group by recommendation date
            papers_by_date = {}
            for paper in papers:
                date = paper.get('recommended_date', 'Unknown')
                if date not in papers_by_date:
                    papers_by_date[date] = []
                papers_by_date[date].append(paper)
            
            # 生成 Markdown 内容 / Generate Markdown content
            content = "# 推荐论文 / Recommended Papers\n\n"
            content += f"**更新时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # 按日期倒序显示 / Show in reverse order by date
            for date in sorted(papers_by_date.keys(), reverse=True):
                papers_for_date = papers_by_date[date]
                content += f"## {date}\n\n"
                content += f"推荐论文数: {len(papers_for_date)}\n\n"
                
                # 优先展示优先级论文 / Show priority papers first
                priority_papers = [p for p in papers_for_date if p.get('priority_status') == 'priority']
                normal_papers = [p for p in papers_for_date if p.get('priority_status') != 'priority']
                
                all_papers_for_date = priority_papers + normal_papers
                
                for idx, paper in enumerate(all_papers_for_date, 1):
                    priority_marker = "⭐ " if paper.get('is_priority') else ""
                    content += f"### {priority_marker}{idx}. {paper.get('title', 'N/A')}\n\n"
                    
                    content += f"- **分类:** {paper.get('category', 'N/A')}\n"
                    content += f"- **作者:** {paper.get('authors', 'N/A')}\n"
                    content += f"- **ID:** {paper.get('id', 'N/A')}\n"
                    
                    if paper.get('tldr') and paper['tldr'] != 'N/A':
                        content += f"- **AI 总结:** {paper.get('tldr')}\n"
                    
                    if paper.get('url'):
                        content += f"- **链接:** [{paper.get('id')}]({paper.get('url')})\n"
                    
                    content += "\n"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 导出推荐论文到 Markdown 文件: {output_file}")
            return True
        
        except Exception as e:
            print(f"❌ 导出推荐论文失败 / Failed to export recommended papers: {e}")
            return False


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
