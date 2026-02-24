#!/bin/bash

# 飞书通知功能使用示例 / Feishu Notification Feature Example
# 
# 本脚本展示如何独立使用飞书通知功能
# This script demonstrates how to use Feishu notification independently

echo "=== 飞书机器人通知示例 / Feishu Robot Notification Example ==="
echo ""

# 检查环境变量 / Check environment variables
if [ -z "$FEISHU_WEBHOOK_URL" ]; then
    echo "⚠️  错误：未设置 FEISHU_WEBHOOK_URL 环境变量"
    echo "   Error: FEISHU_WEBHOOK_URL environment variable not set"
    echo ""
    echo "请按以下方式设置："
    echo "Please set it as follows:"
    echo ""
    echo "  export FEISHU_WEBHOOK_URL=\"https://open.feishu.cn/open-apis/bot/v2/hook/...\""
    echo "  export FEISHU_SECRET=\"your-secret-here\"  # 可选 / Optional"
    echo ""
    exit 1
fi

echo "✅ FEISHU_WEBHOOK_URL 已设置"
echo "   FEISHU_WEBHOOK_URL is set"
echo ""

# 获取数据文件路径 / Get data file path
if [ $# -eq 0 ]; then
    # 如果没有提供参数，使用默认的今日数据文件 / If no argument provided, use today's data file
    today=$(date -u "+%Y-%m-%d")
    data_file="data/${today}.jsonl"
else
    data_file=$1
fi

echo "📂 使用数据文件: $data_file"
echo "   Using data file: $data_file"
echo ""

# 检查文件是否存在 / Check if file exists
if [ ! -f "$data_file" ]; then
    echo "❌ 错误：数据文件不存在"
    echo "   Error: Data file not found: $data_file"
    exit 1
fi

# 发送通知 / Send notification
echo "📤 正在发送飞书通知..."
echo "   Sending Feishu notification..."
echo ""

python utils/feishu.py --data "$data_file" --date "$(date -u '+%Y-%m-%d')"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 通知发送成功！"
    echo "   Notification sent successfully!"
    echo ""
    echo "请检查飞书群组是否收到消息"
    echo "Please check if the message was received in Feishu group"
else
    echo ""
    echo "❌ 通知发送失败"
    echo "   Failed to send notification"
    echo ""
    echo "请检查以下内容:"
    echo "Please check:"
    echo "  1. FEISHU_WEBHOOK_URL 是否正确 / Whether FEISHU_WEBHOOK_URL is correct"
    echo "  2. FEISHU_SECRET 是否正确（如已设置） / Whether FEISHU_SECRET is correct (if set)"
    echo "  3. 网络连接是否正常 / Whether network connection is normal"
    echo "  4. 机器人是否被添加到群组 / Whether robot is added to the group"
    exit 1
fi
