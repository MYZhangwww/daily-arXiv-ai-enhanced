#!/usr/bin/env python3
"""
今日推荐功能 - 快速参考 / Today's Recommendations - Quick Reference
"""

def print_quick_reference():
    reference = """
╔════════════════════════════════════════════════════════════════════════════╗
║           📌 今日推荐专栏 - 快速参考 / Quick Reference                    ║
║              一站式推荐论文展示系统 / One-Stop Recommendation Display      ║
╚════════════════════════════════════════════════════════════════════════════╝

🌐 网页访问
═════════════════════════════════════════════════════════════════════════════

  方式1: 直接访问
    → https://your-site.com/today-recommended.html

  方式2: 从主页导航
    → 主页 → 导航栏 → 😊 按钮 (Today's Recommendations)

┌─────────────────────────────────────────────────────────────────────────┐
│ 📄 推荐专栏页面结构                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ 📌 今日推荐 / Today's Recommendations                         │   │
│  │ 精选发送到飞书的论文 / Featured papers sent to Feishu       │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │ 📊 总推荐数: -     ⭐ 优先级论文: -     📅 推荐日期数: -    │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ 选择日期 / Select Date              [列表][网格]            │   │
│  │ [2026-02-24(3)] [2026-02-23(2)] [2026-02-22(1)]            │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │ 2026-02-24 - 3 篇推荐论文           全部[v]               │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │                                                                 │
│  │ ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │ │ ⭐ 论文1               │  │    论文2                │   │
│  │ │ Autonomous Driving...  │  │ Vision Transformers... │   │
│  │ │ 📌 cs.CV               │  │ 📌 cs.AI               │   │
│  │ │ 📅 2026-02-24          │  │ 📅 2026-02-24          │   │
│  │ │ 提出了一种革新的...   │  │ 探索了ViT在机器...     │   │
│  │ │ [📖 详情] [🔗 arXiv]   │  │ [📖 详情] [🔗 arXiv]   │   │
│  │ └──────────────────────────┘  └──────────────────────────┘   │
│  │                                                                 │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


💻 命令行工具
═════════════════════════════════════════════════════════════════════════════

  查看最新推荐（限20篇）
    $ python utils/recommended_papers.py --list latest

  查看特定日期推荐
    $ python utils/recommended_papers.py --list date --date 2026-02-24

  查看所有推荐论文
    $ python utils/recommended_papers.py --list all

  显示统计信息
    $ python utils/recommended_papers.py --stats

  导出为 JSON
    $ python utils/recommended_papers.py --export json --output recommended.json

  导出为 Markdown
    $ python utils/recommended_papers.py --export markdown --output recommended.md


🎯 主要功能
═════════════════════════════════════════════════════════════════════════════

  1️⃣ 推荐统计
     • 显示总推荐论文数
     • 显示优先级论文数 (⭐ autonomous driving相关)
     • 显示推荐日期数

  2️⃣ 日期选择
     • 显示所有推荐日期按钮
     • 点击按钮查看该日期的推荐
     • 按钮上显示论文数量 (如 "2026-02-24(3)")

  3️⃣ 优先级过滤
     • 全部论文 (All) - 显示全部
     • 优先级论文 (Priority) - 仅显示⭐标记的论文
     • 普通论文 (Normal) - 仅显示普通论文

  4️⃣ 多视图模式
     • 网格视图 🔲: 3列卡片布局 (桌面端)
     • 列表视图 ☰: 单列详细布局 (手机端)
     • 响应式自动调整

  5️⃣ 论文详情
     • 完整论文标题 (无截断)
     • 所有作者信息
     • 论文分类 (cs.CV, cs.LG等)
     • ArXiv ID
     • 完整AI生成总结
     • 原始论文摘要
     • 直接链接到ArXiv


📊 推荐论文字段说明
═════════════════════════════════════════════════════════════════════════════

  字段          类型    说明
  ────────────────────────────────────────────────────────────────────
  title         str     完整论文标题 (无截断)
  authors       str     作者列表 (逗号分隔)
  category      str     arXiv分类 (cs.CV, cs.LG, etc.)
  id            str     arXiv ID (2024.01001)
  url           str     arXiv链接
  tldr          str     AI生成总结 (完整)
  summary       str     原始摘要
  has_ai        bool    是否有AI总结
  is_priority   bool    是否为优先级论文 (⭐)
  recommended_date str 推荐日期 (YYYY-MM-DD)
  priority_status str  优先级状态 (priority/normal)


🔄 数据流向
═════════════════════════════════════════════════════════════════════════════

  1. 日常爬虫运行 (Nightly crawler runs)
     ↓
  2. 生成AI总结 (Generate AI summaries)
     ↓
  3. 提取优先级论文 (Extract priority papers)
     ↓
  4. 发送飞书通知 (Send Feishu notification)
     ↓
  5. RecommendedPapersManager 保存 (Save recommended papers)
     ↓
  6. data/recommended_papers.jsonl (JSONL格式存储)
     ↓
  7. today-recommended.html 加载展示 (Web page display)
     ↓
  8. 用户浏览推荐论文 (User browses recommendations)


📁 文件清单
═════════════════════════════════════════════════════════════════════════════

  新增文件:
    ✨ today-recommended.html         推荐论文主页面
    ✨ css/today-recommended.css      推荐论文样式
    ✨ js/today-recommended.js        推荐论文脚本
    ✨ utils/recommended_papers.py    推荐论文管理器
    ✨ demo_today_recommended.py      功能演示脚本
    ✨ data/recommended_papers.jsonl  推荐论文数据存储

  修改文件:
    ✏️ index.html                     添加导航链接
    ✏️ utils/feishu.py               集成推荐保存功能


🚀 快速开始
═════════════════════════════════════════════════════════════════════════════

  1. 生成演示数据
     $ python demo_today_recommended.py

  2. 查看推荐
     浏览器 → http://localhost/today-recommended.html

  3. 测试功能
     • 点击日期按钮 → 论文列表更新
     • 选择过滤选项 → 列表过滤
     • 点击论文卡片 → 详情弹窗显示
     • 点击arXiv按钮 → 打开原文


⚙️ 配置选项
═════════════════════════════════════════════════════════════════════════════

  修改优先级关键词 (feishu.py):
    priority_keywords = ["autonomous driving", "自动驾驶", "your_keyword"]

  修改推荐论文数量 (feishu.py):
    featured_papers = get_featured_papers(data_content, top_n=10)

  修改数据源 (today-recommended.js):
    const API_BASE = dataSource.baseUrl || './data';


📈 统计信息示例
═════════════════════════════════════════════════════════════════════════════

  $ python utils/recommended_papers.py --stats

  📊 推荐论文统计 / Recommended Papers Statistics:
     总推荐数: 127
     优先级论文 (⭐): 32
     普通论文: 95

     分类统计 / Category Statistics:
        cs.CV: 45
        cs.LG: 38
        cs.AI: 25
        cs.CL: 19


🎨 视觉元素
═════════════════════════════════════════════════════════════════════════════

  ⭐  优先级论文标记 (Priority paper - contains autonomous driving)
  📌  论文分类 (Category)
  ✍️  作者信息 (Authors)
  📅  推荐日期 (Recommendation date)
  🤖  AI生成总结 (AI summary)
  🔗  ArXiv链接 (ArXiv link)
  👁️  视图切换 (View mode toggle)
  🔍  搜索功能 (Search - future feature)


💡 使用技巧
═════════════════════════════════════════════════════════════════════════════

  1. 快速查看最新推荐
     → 直接打开 today-recommended.html，自动显示最新日期

  2. 比较不同日期推荐
     → 点击多个日期按钮，观察推荐趋势

  3. 关注优先级论文
     → 使用优先级过滤，只看⭐论文

  4. 导出推荐列表
     → 使用命令行工具导出为JSON或Markdown

  5. 批量查看论文详情
     → 使用列表视图浏览更多论文

  6. 分享推荐
     → 从浏览器复制URL分享给同事


🔗 相关链接
═════════════════════════════════════════════════════════════════════════════

  主页导航
    https://your-site.com/index.html → 点击😊 → 今日推荐

  推荐论文页面
    https://your-site.com/today-recommended.html

  统计页面
    https://your-site.com/statistic.html

  完整文档
    README_TODAY_RECOMMENDED.md


❓ 常见问题
═════════════════════════════════════════════════════════════════════════════

  Q: 推荐论文来自哪里?
  A: 每日通过飞书发送的精选论文会自动保存到推荐数据库

  Q: 优先级论文是怎么确定的?
  A: 标题或摘要中包含 "autonomous driving" 或 "自动驾驶" 的论文

  Q: 数据多久更新一次?
  A: 根据爬虫运行频率，通常每天更新一次

  Q: 如何自定义推荐规则?
  A: 修改 feishu.py 中的 priority_keywords 参数

  Q: 能否导出推荐列表?
  A: 可以，使用命令行工具导出为 JSON 或 Markdown


✅ 完成情况
═════════════════════════════════════════════════════════════════════════════

  版本: v1.0
  状态: ✅ 完全完成
  发布: 2026-02-24

  已完成功能:
    ✅ 网页专栏创建完成
    ✅ 推荐论文自动保存
    ✅ 数据展示功能完整
    ✅ 用户交互设计优良
    ✅ 后端集成完成
    ✅ 命令行工具齐全
    ✅ 文档详尽完善

  可立即投入生产环境使用! 🚀


═════════════════════════════════════════════════════════════════════════════
📌 更多信息，请查看 README_TODAY_RECOMMENDED.md
═════════════════════════════════════════════════════════════════════════════
    """
    print(reference)


if __name__ == "__main__":
    print_quick_reference()
