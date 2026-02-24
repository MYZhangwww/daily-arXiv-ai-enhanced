#!/usr/bin/env python3
"""
演示优先级论文选择和完整信息展示 / Demo: Priority Paper Selection and Full Information Display

这个脚本演示了：
1. 优先展示 autonomous driving 相关的论文
2. 完整展示论文标题和 AI 总结
3. 用 ⭐ 标记优先论文
"""

import json
import sys
from pathlib import Path

# 添加 utils 到路径
sys.path.insert(0, str(Path(__file__).parent / "utils"))

from feishu import get_featured_papers


def demo_priority_papers():
    """演示优先级论文选择"""
    
    print("\n" + "="*70)
    print("🎯 演示：优先级论文选择与完整信息展示 / Priority Paper Selection Demo")
    print("="*70)
    
    # 创建示例数据（模拟 JSONL 格式）
    sample_data = """
{"id": "2401.00001", "title": "Autonomous Driving System with Deep Learning", "authors": ["Alice", "Bob", "Charlie"], "categories": ["cs.CV"], "summary": "This paper presents a novel deep learning approach for autonomous driving systems.", "AI": {"tldr": "提出了一种基于深度学习的自主驾驶系统，结合了视觉感知和路径规划算法，在真实交通场景中展示了良好的性能。该方法相比传统方法有 30% 的性能提升。"}}
{"id": "2401.00002", "title": "Multi-Task Learning for Vision Transformers", "authors": ["David", "Eve", "Frank"], "categories": ["cs.CV"], "summary": "A comprehensive study on multi-task learning approaches.", "AI": {"tldr": "研究了多任务学习在视觉转换器中的应用，展示了如何通过共享特征表示提高模型效率。在 ImageNet 和 COCO 数据集上取得了最先进的结果。"}}
{"id": "2401.00003", "title": "Robust Perception for Autonomous Vehicles in Adverse Weather", "authors": ["Grace", "Henry", "Iris"], "categories": ["cs.RO"], "summary": "Addresses perception challenges in autonomous vehicles during adverse weather conditions.", "AI": {"tldr": "开发了一种鲁棒的感知系统，专门为自动驾驶车辆在恶劣天气条件下设计。使用对抗性训练和数据增强技术，在雨、雪和雾等条件下达到了 95% 的检测准确率。"}}
{"id": "2401.00004", "title": "Neural Architecture Search for Mobile Deployment", "authors": ["Jack", "Kate", "Leo"], "categories": ["cs.LG"], "summary": "Efficient neural architecture search methods for mobile devices.", "AI": {"tldr": "提出了移动设备上的高效神经架构搜索方法，能够在有限的计算资源下找到最优模型结构。相比手工设计的网络，推理速度提升了 2.5 倍。"}}
{"id": "2401.00005", "title": "End-to-End Learning for Self-Driving Cars", "authors": ["Mike", "Nancy", "Oscar"], "categories": ["cs.AI"], "summary": "End-to-end learning approaches for autonomous driving applications.", "AI": {"tldr": "提出了端到端的学习框架，直接从原始传感器输入学习驾驶策略。在虚拟驾驶环境中的成功率达到了 98%，并成功迁移到真实车辆。"}}
"""
    
    print("\n1️⃣  提取精选论文（优先级：autonomous driving）")
    print("-" * 70)
    
    # 获取精选论文
    priority_keywords = ["autonomous driving", "自动驾驶"]
    papers = get_featured_papers(sample_data, top_n=5, priority_keywords=priority_keywords)
    
    print(f"\n✅ 总共提取 {len(papers)} 篇精选论文")
    print(f"🎯 优先级关键词: {', '.join(priority_keywords)}\n")
    
    # 显示论文信息
    for idx, paper in enumerate(papers, 1):
        marker = "⭐ " if paper.get('is_priority') else "  "
        
        print(f"{marker}论文 {idx}: {paper['title']}")
        print(f"   📌 分类: {paper['category']}")
        print(f"   👥 作者: {paper['authors']}")
        print(f"   📝 ID: {paper['id']}")
        
        if paper.get('has_ai'):
            print(f"   🤖 AI总结: {paper['tldr']}")
        else:
            print(f"   📄 摘要: {paper['tldr']}")
        print()
    
    # 统计
    priority_count = sum(1 for p in papers if p.get('is_priority'))
    print("-" * 70)
    print(f"📊 统计信息:")
    print(f"   • 总论文数: {len(papers)}")
    print(f"   • 优先级论文 (autonomous driving): {priority_count}")
    print(f"   • 其他论文: {len(papers) - priority_count}")
    
    return papers


def demo_message_format(papers):
    """演示消息格式"""
    
    print("\n" + "="*70)
    print("📨 演示：飞书通知消息格式 / Feishu Message Format")
    print("="*70)
    
    from datetime import datetime
    
    # 构建消息内容
    message_content = {
        "更新日期": "2024-02-24",
        "精选论文数": str(len(papers)),
        "优先领域": "自动驾驶 (Autonomous Driving)",
    }
    
    # 添加论文信息
    for idx, paper in enumerate(papers, 1):
        priority_marker = "⭐ " if paper.get('is_priority') else "  "
        
        paper_entry = f"{priority_marker}[{idx}] {paper['title']}\n"
        paper_entry += f"📌 分类: {paper['category']} | 作者: {paper['authors']}\n"
        
        if paper.get('tldr') and paper['tldr'] != 'N/A':
            summary_prefix = "🤖 AI总结: " if paper.get('has_ai') else "📝 摘要: "
            paper_entry += f"{summary_prefix}{paper['tldr']}\n"
        
        if paper.get('id'):
            paper_entry += f"🔗 ID: {paper['id']}"
        
        message_content[f"论文 {idx}"] = paper_entry
    
    message_content["通知时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_content["数据来源"] = "arXiv + AI 增强分析"
    message_content["说明"] = "⭐ 标记表示包含 'autonomous driving' 相关内容，优先展示"
    
    # 显示消息内容
    print("\n📬 飞书卡片消息内容预览:")
    print("-" * 70)
    print("标题: 📚 arXiv 精选论文 - 2024-02-24\n")
    
    for key, value in message_content.items():
        if len(str(value)) > 100:
            print(f"📍 {key}:")
            print(f"   {value[:100]}...")
            print()
        else:
            print(f"📍 {key}: {value}\n")


def main():
    """主函数"""
    
    print("\n🚀 开始演示...\n")
    
    # 演示 1: 优先级论文选择
    papers = demo_priority_papers()
    
    # 演示 2: 消息格式
    demo_message_format(papers)
    
    print("\n" + "="*70)
    print("✅ 演示完成！/ Demo Complete!")
    print("="*70)
    
    print("\n💡 关键改进:")
    print("   ✅ 完整展示论文标题（不截断）")
    print("   ✅ 完整展示 AI 总结（不截断）")
    print("   ✅ 优先展示 autonomous driving 相关论文")
    print("   ✅ 用 ⭐ 标记优先级论文")
    print("   ✅ 更清晰的信息组织结构")
    
    print("\n🎯 实际使用:")
    print("   python utils/feishu.py --from-git --mode featured")
    print("   python utils/feishu.py --data data/2024-02-24.jsonl --mode featured")
    print()


if __name__ == "__main__":
    main()
