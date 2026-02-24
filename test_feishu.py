#!/usr/bin/env python3
"""
飞书模块测试脚本 / Feishu Module Test Script

用于测试飞书机器人通知功能是否正常工作。
Used to test if Feishu robot notification feature works properly.

用法 / Usage:
    python test_feishu.py
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径 / Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feishu import FeishuRobot, send_daily_crawl_notification


def create_test_data_file():
    """创建测试数据文件 / Create test data file"""
    test_data = [
        {
            "id": "2401.00001",
            "title": "Vision Transformers for Dense Prediction Tasks",
            "authors": ["Alice Smith", "Bob Johnson"],
            "summary": "This paper proposes a new approach...",
            "abs": "https://arxiv.org/abs/2401.00001",
            "categories": ["cs.CV"]
        },
        {
            "id": "2401.00002",
            "title": "Language Models as Zero-Shot Planners",
            "authors": ["Charlie Brown", "Diana Prince"],
            "summary": "We investigate the capabilities...",
            "abs": "https://arxiv.org/abs/2401.00002",
            "categories": ["cs.CL"]
        },
        {
            "id": "2401.00003",
            "title": "Efficient Attention Mechanisms for Large-Scale Models",
            "authors": ["Eve Wilson"],
            "summary": "This work presents several improvements...",
            "abs": "https://arxiv.org/abs/2401.00003",
            "categories": ["cs.AI"]
        },
        {
            "id": "2401.00004",
            "title": "3D Object Detection with Point Clouds",
            "authors": ["Frank Miller", "Grace Lee"],
            "summary": "We propose a novel method for...",
            "abs": "https://arxiv.org/abs/2401.00004",
            "categories": ["cs.CV"]
        },
        {
            "id": "2401.00005",
            "title": "Multimodal Learning for Cross-Domain Tasks",
            "authors": ["Henry Zhang"],
            "summary": "This paper explores the synergies...",
            "abs": "https://arxiv.org/abs/2401.00005",
            "categories": ["cs.CL"]
        },
    ]
    
    # 创建临时文件 / Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False, encoding='utf-8') as f:
        for data in test_data:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
        return f.name


def test_signature_generation():
    """测试签名生成 / Test signature generation"""
    print("\n" + "="*60)
    print("测试1：签名生成 / Test 1: Signature Generation")
    print("="*60)
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/test"
    secret = "test_secret_key"
    
    robot = FeishuRobot(webhook_url, secret)
    timestamp, sign = robot._generate_signature()
    
    if timestamp and sign:
        print(f"✅ 签名生成成功 / Signature generated successfully")
        print(f"   时间戳 / Timestamp: {timestamp}")
        print(f"   签名 / Signature: {sign[:30]}...")
        return True
    else:
        print(f"❌ 签名生成失败 / Signature generation failed")
        return False


def test_message_without_sending():
    """测试消息构建（不发送） / Test message building (without sending)"""
    print("\n" + "="*60)
    print("测试2：消息内容构建 / Test 2: Message Content Building")
    print("="*60)
    
    # 创建测试数据 / Create test data
    test_file = create_test_data_file()
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            papers = [json.loads(line) for line in f if line.strip()]
        
        print(f"✅ 成功读取测试数据 / Successfully read test data")
        print(f"   论文总数 / Total papers: {len(papers)}")
        
        # 统计分类 / Count categories
        categories = {}
        for paper in papers:
            cat = paper.get('categories', ['unknown'])[0]
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"   分类统计 / Category statistics: {categories}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {e}")
        return False
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_with_environment_variables():
    """测试使用环境变量 / Test with environment variables"""
    print("\n" + "="*60)
    print("测试3：环境变量检查 / Test 3: Environment Variables Check")
    print("="*60)
    
    webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
    secret = os.environ.get('FEISHU_SECRET')
    
    if webhook_url:
        print(f"✅ FEISHU_WEBHOOK_URL 已设置")
        print(f"   URL: {webhook_url[:50]}...")
    else:
        print(f"⚠️  FEISHU_WEBHOOK_URL 未设置 / FEISHU_WEBHOOK_URL not set")
        print(f"   提示：设置此环境变量才能发送实际的飞书通知")
        print(f"   Tip: Set this environment variable to send actual Feishu notifications")
    
    if secret:
        print(f"✅ FEISHU_SECRET 已设置")
    else:
        print(f"⚠️  FEISHU_SECRET 未设置（可选，但建议设置以启用签名校验）")
        print(f"   Tip: Optional but recommended for signature verification")
    
    return True


def test_full_workflow():
    """测试完整工作流（如果配置了环境变量） / Test full workflow (if environment variables are set)"""
    print("\n" + "="*60)
    print("测试4：完整工作流 / Test 4: Full Workflow")
    print("="*60)
    
    webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
    
    if not webhook_url:
        print("⏭️  跳过完整工作流测试（未设置 FEISHU_WEBHOOK_URL）")
        print("   Skipped (FEISHU_WEBHOOK_URL not set)")
        return True
    
    # 创建测试数据 / Create test data
    test_file = create_test_data_file()
    
    try:
        print("📤 正在发送测试通知... / Sending test notification...")
        success = send_daily_crawl_notification(test_file, "2024-12-15-TEST")
        
        if success:
            print("✅ 测试通知发送成功！/ Test notification sent successfully!")
            return True
        else:
            print("❌ 测试通知发送失败 / Test notification failed")
            return False
    except Exception as e:
        print(f"❌ 异常发生 / Exception occurred: {e}")
        return False
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def main():
    """主测试函数 / Main test function"""
    print("\n" + "🧪 飞书机器人模块测试套件 / Feishu Robot Module Test Suite")
    print("="*60)
    
    results = {
        "签名生成": test_signature_generation(),
        "消息构建": test_message_without_sending(),
        "环境变量": test_with_environment_variables(),
        "完整工作流": test_full_workflow(),
    }
    
    # 总结 / Summary
    print("\n" + "="*60)
    print("📊 测试总结 / Test Summary")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 所有测试通过！/ All tests passed!")
    else:
        print("⚠️  部分测试失败，请检查配置 / Some tests failed, please check configuration")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
