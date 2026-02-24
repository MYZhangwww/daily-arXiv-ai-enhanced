#!/usr/bin/env python3
"""
今日推荐功能演示脚本 / Today's Recommendations Feature Demo

展示如何使用推荐论文管理器和飞书集成功能
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# 假设脚本在项目根目录运行
from utils.recommended_papers import RecommendedPapersManager


def demo_recommended_papers():
    """演示推荐论文功能"""
    
    print("\n" + "="*70)
    print("🎯 今日推荐功能演示 / Today's Recommendations Feature Demo")
    print("="*70)
    
    manager = RecommendedPapersManager()
    
    # 1. 生成演示数据
    print("\n1️⃣ 生成演示推荐论文数据 / Generate Demo Recommended Papers")
    print("-" * 70)
    
    demo_papers = [
        {
            "title": "Autonomous Driving System with Deep Learning and Computer Vision",
            "authors": "Alice Johnson, Bob Smith, Charlie Lee",
            "category": "cs.CV",
            "id": "2024.01001",
            "url": "https://arxiv.org/abs/2024.01001",
            "tldr": "提出了一种革新性的自动驾驶系统，结合了最新的深度学习技术和计算机视觉算法。系统在真实交通场景中表现出色，相比传统方法有 35% 的性能提升。该研究还涵盖了恶劣天气条件下的鲁棒性测试。",
            "summary": "本文介绍了一个完整的自主驾驶感知系统...",
            "is_priority": True,
            "has_ai": True
        },
        {
            "title": "Robust Perception for Autonomous Vehicles in Adverse Weather Conditions",
            "authors": "David Wang, Emma Chen, Frank Zhang",
            "category": "cs.LG",
            "id": "2024.01002",
            "url": "https://arxiv.org/abs/2024.01002",
            "tldr": "本研究专注于在恶劣天气条件（雨、雪、雾）下的自驾车感知系统。提出了一种新的数据增强技术和鲁棒的特征提取方法。在多个基准数据集上实现了最先进的性能。",
            "summary": "研究在雨雪雾等恶劣天气下的自动驾驶感知...",
            "is_priority": True,
            "has_ai": True
        },
        {
            "title": "Vision Transformers for End-to-End Learning in Robotics",
            "authors": "Grace Lee, Henry Liu, Iris Kim",
            "category": "cs.AI",
            "id": "2024.01003",
            "url": "https://arxiv.org/abs/2024.01003",
            "tldr": "探索了视觉Transformer在机器人端到端学习中的应用。该方法使用自监督学习框架，显著减少了标注数据需求。在多个机器人控制任务上展示了卓越的泛化能力。",
            "summary": "研究了ViT在机器人学习中的应用...",
            "is_priority": False,
            "has_ai": True
        },
        {
            "title": "Multi-Modal Fusion for Semantic Understanding",
            "authors": "Jack Morrison, Karen Brown, Leo Jackson",
            "category": "cs.CL",
            "id": "2024.01004",
            "url": "https://arxiv.org/abs/2024.01004",
            "tldr": "提出了一个创新的多模态融合架构，用于语义理解任务。结合了文本、图像和音频信息。在VQA和图像描述任务上达到了新的SOTA。",
            "summary": "研究多模态数据融合方法...",
            "is_priority": False,
            "has_ai": True
        },
        {
            "title": "Efficient Neural Architecture Search with Limited Computational Budget",
            "authors": "Maria Garcia, Nathan Wilson, Olivia Taylor",
            "category": "cs.LG",
            "id": "2024.01005",
            "url": "https://arxiv.org/abs/2024.01005",
            "tldr": "提出了一种新的神经架构搜索方法，专为计算资源有限的场景设计。使用进化算法和强化学习的混合方法。在移动设备上实现了快速高效的模型搜索。",
            "summary": "研究在有限计算资源下的NAS...",
            "is_priority": False,
            "has_ai": True
        }
    ]
    
    # 生成两个日期的推荐数据
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"✅ 生成了 {len(demo_papers)} 篇演示论文")
    print(f"   📅 日期: {today} (3篇), {yesterday} (2篇)\n")
    
    # 2. 保存推荐论文
    print("2️⃣ 保存推荐论文 / Save Recommended Papers")
    print("-" * 70)
    
    # 保存今天的论文
    today_papers = demo_papers[:3]
    if manager.save_recommended_papers(today_papers, today):
        print(f"✅ 保存 {len(today_papers)} 篇论文到 {today}")
    
    # 保存昨天的论文
    yesterday_papers = demo_papers[3:5]
    if manager.save_recommended_papers(yesterday_papers, yesterday):
        print(f"✅ 保存 {len(yesterday_papers)} 篇论文到 {yesterday}\n")
    
    # 3. 获取统计信息
    print("3️⃣ 获取统计信息 / Get Statistics")
    print("-" * 70)
    
    stats = manager.get_recommended_papers_statistics()
    print(f"📊 推荐论文统计:")
    print(f"   • 总推荐数: {stats['总推荐数']}")
    print(f"   • 优先级论文 (⭐): {stats['优先级论文']}")
    print(f"   • 普通论文: {stats['普通论文']}")
    print(f"   • 推荐日期数: {len(stats['推荐日期'])}\n")
    
    # 4. 按日期获取推荐论文
    print("4️⃣ 按日期获取推荐论文 / Get Papers by Date")
    print("-" * 70)
    
    today_recommended = manager.get_recommended_papers_by_date(today)
    print(f"📅 {today} 推荐论文 ({len(today_recommended)} 篇):")
    for idx, paper in enumerate(today_recommended, 1):
        marker = "⭐" if paper.get('is_priority') else "  "
        print(f"   {marker} {idx}. {paper['title'][:60]}...")
    
    print()
    
    # 5. 获取最新推荐
    print("5️⃣ 获取最新推荐论文 / Get Latest Recommended Papers")
    print("-" * 70)
    
    latest = manager.get_latest_recommended_papers(limit=5)
    print(f"📚 最新推荐论文 ({len(latest)} 篇):")
    for idx, paper in enumerate(latest, 1):
        priority = "⭐ 优先级" if paper.get('is_priority') else "普通"
        date = paper.get('recommended_date', 'Unknown')
        print(f"   {idx}. [{priority}] {paper['title'][:50]}... ({date})")
    
    print()
    
    # 6. 导出功能演示
    print("6️⃣ 导出功能演示 / Export Functionality")
    print("-" * 70)
    
    # 导出为 JSON
    json_output = "data/recommended_papers_export.json"
    if manager.export_to_json(json_output):
        print(f"✅ 已导出为 JSON: {json_output}")
    
    # 导出为 Markdown
    md_output = "data/recommended_papers_export.md"
    if manager.export_to_markdown(md_output):
        print(f"✅ 已导出为 Markdown: {md_output}\n")
    
    # 7. 网站功能说明
    print("7️⃣ 网站功能说明 / Website Features")
    print("-" * 70)
    
    print("""
🌐 今日推荐专栏功能:

📄 访问页面:
   • 网址: https://your-site.com/today-recommended.html
   • 或从主页导航菜单点击 "今日推荐" 按钮

✨ 主要功能:
   
   1. 📊 推荐统计
      • 总推荐论文数
      • 优先级论文数 (⭐)
      • 推荐日期数
   
   2. 📅 日期选择
      • 显示所有推荐日期
      • 点击日期按钮查看该日期的推荐论文
      • 每个日期按钮显示论文数量
   
   3. 🎯 优先级过滤
      • 全部论文 (All Papers)
      • 优先级论文 (Priority Papers) - ⭐ 标记
      • 普通论文 (Normal Papers)
   
   4. 👁️ 多视图模式
      • 网格视图 (Grid): 3列卡片布局
      • 列表视图 (List): 单列详细布局
   
   5. 📖 论文详情
      • 完整论文标题
      • 作者列表
      • 论文分类
      • ArXiv ID
      • AI生成的总结
      • 原始摘要
      • 直接链接到 ArXiv

🔄 数据流向:
   
   飞书通知 → feishu.py 发送推荐
                  ↓
           recommended_papers.py 保存到文件
                  ↓
           today-recommended.html 网页展示
                  ↓
           用户浏览推荐论文

⚙️ 数据存储位置:
   • 文件: data/recommended_papers.jsonl
   • 格式: 每行一个JSON对象
   • 内容: 发送到飞书的所有推荐论文记录
    """)
    
    print("="*70)
    print("✅ 演示完成! / Demo Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_recommended_papers()
