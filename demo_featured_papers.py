#!/usr/bin/env python3
"""
飞书精选文章模式演示脚本
Feishu Featured Papers Mode Demo Script

演示如何使用精选文章模式发送飞书通知
Demonstrates how to use the featured papers mode to send Feishu notifications
"""

import json
import os
import sys
import tempfile
from datetime import datetime

# 添加项目路径 / Add project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feishu import send_daily_crawl_notification, get_featured_papers


def create_demo_data():
    """创建示例数据文件 / Create demo data file"""
    demo_papers = [
        {
            "id": "2401.00001",
            "title": "Vision Transformers for Dense Prediction Tasks in Computer Vision",
            "authors": ["Alice Smith", "Bob Johnson", "Charlie Brown"],
            "categories": ["cs.CV"],
            "abs": "https://arxiv.org/abs/2401.00001",
            "summary": "This paper proposes an efficient transformer-based approach for dense prediction tasks in computer vision, achieving state-of-the-art results on multiple benchmarks.",
            "AI": {
                "tldr": "Introduces Vision Transformers for dense tasks with improved efficiency and accuracy",
                "motivation": "Dense prediction tasks require understanding spatial relationships",
                "method": "Adapted transformer architecture with positional embeddings",
                "result": "SOTA on Cityscapes and ADE20K benchmarks",
                "conclusion": "Transformers are effective for dense vision tasks"
            }
        },
        {
            "id": "2401.00002",
            "title": "Language Models as Zero-Shot Planners for Robotics",
            "authors": ["Diana Prince", "Eve Wilson"],
            "categories": ["cs.CL"],
            "abs": "https://arxiv.org/abs/2401.00002",
            "summary": "Large language models can be effectively used for robotics planning without task-specific training.",
            "AI": {
                "tldr": "Demonstrates LLMs can perform robot planning tasks zero-shot",
                "motivation": "Bridge gap between NLP and robotics",
                "method": "Prompt engineering for planning with LLMs",
                "result": "90% success rate on simulated tasks",
                "conclusion": "LLMs have potential for robotic control"
            }
        },
        {
            "id": "2401.00003",
            "title": "Efficient Attention Mechanisms for Large-Scale Transformer Models",
            "authors": ["Frank Miller", "Grace Lee", "Henry Zhang"],
            "categories": ["cs.AI"],
            "abs": "https://arxiv.org/abs/2401.00003",
            "summary": "We propose several improvements to attention mechanisms for better scalability.",
            "AI": {
                "tldr": "Proposes efficient attention reducing complexity from O(n²) to O(n log n)",
                "motivation": "Attention is bottleneck in large models",
                "method": "Hierarchical attention with local and global windows",
                "result": "2x faster training, 30% memory reduction",
                "conclusion": "Efficient attention enables larger models"
            }
        },
        {
            "id": "2401.00004",
            "title": "3D Object Detection with Point Clouds Using Graph Neural Networks",
            "authors": ["Isabella Martinez", "Jack Wilson"],
            "categories": ["cs.CV"],
            "abs": "https://arxiv.org/abs/2401.00004",
            "summary": "Novel graph-based approach for 3D object detection from point clouds.",
            "AI": {
                "tldr": "Graph neural networks improve 3D detection accuracy by 15%",
                "motivation": "Points have complex spatial relationships",
                "method": "Construct graphs, apply GNNs, regress boxes",
                "result": "Top results on KITTI and nuScenes",
                "conclusion": "Graph structure captures 3D geometry well"
            }
        },
        {
            "id": "2401.00005",
            "title": "Multimodal Learning for Cross-Domain Understanding",
            "authors": ["Kevin Brown"],
            "categories": ["cs.CL"],
            "abs": "https://arxiv.org/abs/2401.00005",
            "summary": "Explores synergies between different modalities for robust understanding.",
            "AI": {
                "tldr": "Multimodal approach achieves 25% improvement over single modality",
                "motivation": "Different modalities provide complementary information",
                "method": "Fusion architecture with shared and modality-specific encoders",
                "result": "SOTA on 5 cross-domain benchmarks",
                "conclusion": "Multimodal learning is more robust"
            }
        }
    ]
    
    # 创建临时文件 / Create temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.jsonl', text=True)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        for paper in demo_papers:
            f.write(json.dumps(paper, ensure_ascii=False) + '\n')
    
    return temp_path


def demo_featured_papers_mode():
    """演示精选文章模式 / Demo featured papers mode"""
    print("\n" + "="*70)
    print("演示 1: 精选文章模式 / Demo 1: Featured Papers Mode")
    print("="*70)
    
    # 创建示例数据 / Create demo data
    demo_file = create_demo_data()
    
    try:
        # 显示精选论文 / Display featured papers
        print("\n📚 获取精选论文 / Fetching featured papers...\n")
        featured = get_featured_papers(demo_file, top_n=5)
        
        if featured:
            print(f"✅ 成功获取 {len(featured)} 篇精选论文 / Successfully fetched {len(featured)} papers\n")
            
            for idx, paper in enumerate(featured, 1):
                print(f"📄 论文 {idx} / Paper {idx}:")
                print(f"   标题 / Title: {paper['title']}")
                print(f"   作者 / Authors: {paper['authors']}")
                print(f"   分类 / Category: {paper['category']}")
                print(f"   AI标记 / AI Tag: {'✅ 有' if paper.get('has_ai') else '❌ 无'}")
                print(f"   摘要 / TL;DR: {paper['tldr'][:80]}...")
                print()
        else:
            print("❌ 未获取到任何论文 / No papers fetched")
            
    finally:
        # 清理临时文件 / Clean up temp file
        if os.path.exists(demo_file):
            os.remove(demo_file)


def demo_send_notification():
    """演示发送通知（需要配置环境变量）/ Demo sending notification (requires env vars)"""
    print("\n" + "="*70)
    print("演示 2: 发送飞书通知 / Demo 2: Send Feishu Notification")
    print("="*70)
    
    webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
    
    if not webhook_url:
        print("\n⚠️  未设置 FEISHU_WEBHOOK_URL，跳过此演示")
        print("   Set FEISHU_WEBHOOK_URL environment variable to enable this demo")
        return
    
    # 创建示例数据 / Create demo data
    demo_file = create_demo_data()
    
    try:
        print("\n📤 发送精选文章模式通知 / Sending featured papers notification...\n")
        
        success = send_daily_crawl_notification(
            demo_file, 
            datetime.now().strftime("%Y-%m-%d"),
            mode="featured"
        )
        
        if success:
            print("\n✅ 通知发送成功！/ Notification sent successfully!")
            print("请查看飞书群组中的消息 / Check the message in Feishu group")
        else:
            print("\n❌ 通知发送失败 / Notification failed")
            
    finally:
        # 清理临时文件 / Clean up temp file
        if os.path.exists(demo_file):
            os.remove(demo_file)


def main():
    """主函数 / Main function"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "飞书精选文章模式演示 / Featured Papers Mode Demo" + " "*10 + "║")
    print("╚" + "="*68 + "╝")
    
    # 演示 1: 获取精选论文 / Demo 1: Get featured papers
    demo_featured_papers_mode()
    
    # 演示 2: 发送通知（如果配置了）/ Demo 2: Send notification (if configured)
    demo_send_notification()
    
    print("\n" + "="*70)
    print("💡 提示 / Tips:")
    print("="*70)
    print("""
1. 精选文章模式默认优先选择有 AI 总结的论文
   Featured mode prioritizes papers with AI summaries by default

2. 如果没有 AI 总结，会使用原始摘要的前 150 字
   If no AI summary, uses first 150 chars of abstract

3. 最多显示 5 篇论文
   Shows up to 5 papers maximum

4. 使用方式:
   Usage:
   
   # 精选文章模式（默认）
   python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"
   
   # 统计模式
   python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics

5. 在 Python 中使用:
   In Python:
   
   from utils.feishu import send_daily_crawl_notification
   send_daily_crawl_notification("data.jsonl", "2024-02-24", mode="featured")
    """)
    
    print("="*70)
    print("✨ 演示完成！/ Demo completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
