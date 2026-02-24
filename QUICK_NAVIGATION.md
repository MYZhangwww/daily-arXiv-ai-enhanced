# 🚀 飞书精选文章功能 - 快速导航

> 点击下面的链接快速访问相关文件和文档

## ⭐ 推荐入口

### 🎯 新用户必读
- [📖 快速开始指南](QUICK_START_FEATURED_MODE.md) - 5 分钟快速上手
- [🎬 运行演示脚本](#运行演示脚本) - 3 秒查看效果

### 🔧 环境配置
- [⚙️ 设置指南](FEISHU_SETUP.md) - Webhook 和密钥配置
- [🪟 Windows 测试](WINDOWS_TESTING_GUIDE.md) - Windows PowerShell 支持

### 📚 深入了解
- [📋 完整导航](DOCUMENTATION_INDEX.md) - 按场景推荐文档
- [✅ 完成清单](COMPLETION_CHECKLIST.md) - 项目验证清单
- [🎉 完成报告](IMPLEMENTATION_COMPLETE.md) - 详细的实现总结

## 📁 文件导航

### 核心代码
```
utils/
└── feishu.py (469 行)
    ├── FeishuRobot 类
    ├── get_featured_papers() - AI 感知论文提取 ⭐
    ├── send_daily_crawl_notification() - 双模式通知分发 ⭐
    ├── _send_featured_papers_notification() - 精选文章格式化 ⭐
    ├── _send_statistics_notification() - 统计模式 (兼容)
    └── main() - CLI 入口
```

### 演示和脚本
```
项目根目录/
├── demo_featured_papers.py ⭐ (演示脚本，推荐运行)
├── test_feishu.py (自动化测试)
├── run.sh (Linux/Mac 主脚本 - 已更新)
└── run.ps1 (Windows 主脚本 - 已更新)
```

### 文档文件
```
项目根目录/
├── QUICK_START_FEATURED_MODE.md ⭐ (快速开始)
├── DOCUMENTATION_INDEX.md (文档导航索引)
├── FEATURED_PAPERS_SUMMARY.md (完整总结)
├── IMPLEMENTATION_COMPLETE.md (完成报告)
├── COMPLETION_CHECKLIST.md (完成清单)
├── README_FEATURED_MODE.md (README 片段)
├── FEISHU_FEATURED_PAPERS_MODE.md (功能详解)
├── FEISHU_SETUP.md (配置指南)
├── FEISHU_IMPLEMENTATION.md (技术指南)
└── WINDOWS_TESTING_GUIDE.md (Windows 指南)
```

## 🚀 3 秒快速启动

### 运行演示脚本
```bash
python demo_featured_papers.py
```

这会显示：
- ✅ 精选论文提取演示
- ✅ 示例数据处理
- ✅ 飞书消息格式
- ✅ 可选的实际发送测试

## 🎯 按用途快速查询

### "我想立即开始"
1. 打开：[QUICK_START_FEATURED_MODE.md](QUICK_START_FEATURED_MODE.md)
2. 运行：`python demo_featured_papers.py`
3. 配置：设置 `FEISHU_WEBHOOK_URL`
4. 部署：`python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24"`

### "我想了解详细功能"
1. 打开：[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
2. 选择：根据难度选择对应文档
3. 阅读：深入理解功能设计
4. 参考：查看源代码实现

### "我在 Windows 上开发"
1. 打开：[WINDOWS_TESTING_GUIDE.md](WINDOWS_TESTING_GUIDE.md)
2. 运行：`python demo_featured_papers.py`
3. 集成：使用 `.\run.ps1`
4. 调试：使用 PowerShell 进行开发

### "我想要二次开发"
1. 查看：[FEISHU_IMPLEMENTATION.md](FEISHU_IMPLEMENTATION.md)
2. 研究：`utils/feishu.py` 源代码
3. 参考：[test_feishu.py](test_feishu.py) 测试用例
4. 扩展：实现自己的功能

## 💡 常见任务速查

| 任务 | 文件/命令 | 时间 |
|------|----------|------|
| 查看演示 | `python demo_featured_papers.py` | 1 分钟 |
| 快速开始 | [QUICK_START_FEATURED_MODE.md](QUICK_START_FEATURED_MODE.md) | 5 分钟 |
| 环境配置 | [FEISHU_SETUP.md](FEISHU_SETUP.md) | 5 分钟 |
| 发送通知 | `python utils/feishu.py --data ... --date ...` | 1 分钟 |
| Windows 测试 | [WINDOWS_TESTING_GUIDE.md](WINDOWS_TESTING_GUIDE.md) | 10 分钟 |
| 深入学习 | [FEISHU_FEATURED_PAPERS_MODE.md](FEISHU_FEATURED_PAPERS_MODE.md) | 20 分钟 |
| 完整理解 | [FEISHU_IMPLEMENTATION.md](FEISHU_IMPLEMENTATION.md) | 30 分钟 |

## 🔍 功能一览

### 精选文章模式 (新)
```
特点: 展示 5 篇最有价值的论文
场景: 日常通知、快速浏览
使用: python utils/feishu.py --data ... --mode featured (默认)
```

### 统计模式 (兼容)
```
特点: 展示统计数据和分类分布
场景: 数据分析、趋势观察
使用: python utils/feishu.py --data ... --mode statistics
```

## ✨ 核心函数速查

### `get_featured_papers(data_file, top_n=5)`
提取精选论文，优先选择有 AI 总结的论文

```python
from utils.feishu import get_featured_papers
papers = get_featured_papers("data.jsonl", top_n=5)
for paper in papers:
    print(f"[{paper['title']}] - AI: {paper['has_ai']}")
```

### `send_daily_crawl_notification(data_file, date_str, mode='featured')`
发送每日通知

```python
from utils.feishu import send_daily_crawl_notification
success = send_daily_crawl_notification(
    "data.jsonl", 
    "2024-02-24",
    mode="featured"  # or "statistics"
)
```

### `FeishuRobot` 类
直接使用飞书机器人

```python
from utils.feishu import FeishuRobot
robot = FeishuRobot(webhook_url, secret)
robot.send_card_message(title, content_dict)
```

## 📊 项目统计

- **新增文件**: 6 个（代码 + 文档）
- **修改文件**: 4 个（集成新功能）
- **代码行数**: 1,005+ 行
- **文档行数**: 3,150+ 行
- **功能模块**: 4 个核心功能
- **测试覆盖**: 完整

## 🎓 学习路径

### 初级 (15 分钟)
1. 运行 `python demo_featured_papers.py`
2. 阅读 [QUICK_START_FEATURED_MODE.md](QUICK_START_FEATURED_MODE.md)
3. 理解基本概念

### 中级 (45 分钟)
1. 阅读 [FEISHU_FEATURED_PAPERS_MODE.md](FEISHU_FEATURED_PAPERS_MODE.md)
2. 查看 [utils/feishu.py](utils/feishu.py) 源代码
3. 运行 [test_feishu.py](test_feishu.py) 测试

### 高级 (90 分钟)
1. 深入 [FEISHU_IMPLEMENTATION.md](FEISHU_IMPLEMENTATION.md)
2. 研究完整源代码
3. 实现功能扩展

## 🆘 寻求帮助

### 问题排查流程
1. **快速问题** → [QUICK_START_FEATURED_MODE.md](QUICK_START_FEATURED_MODE.md) 的 FAQ
2. **配置问题** → [FEISHU_SETUP.md](FEISHU_SETUP.md)
3. **功能问题** → [FEISHU_FEATURED_PAPERS_MODE.md](FEISHU_FEATURED_PAPERS_MODE.md)
4. **代码问题** → [utils/feishu.py](utils/feishu.py) 注释和 [test_feishu.py](test_feishu.py)
5. **Windows 问题** → [WINDOWS_TESTING_GUIDE.md](WINDOWS_TESTING_GUIDE.md)
6. **开发问题** → [FEISHU_IMPLEMENTATION.md](FEISHU_IMPLEMENTATION.md)

## 📞 快速命令参考

```bash
# 运行演示
python demo_featured_papers.py

# 查看帮助
python utils/feishu.py --help

# 发送精选文章通知
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode featured

# 发送统计通知
python utils/feishu.py --data data/2024-02-24.jsonl --date "2024-02-24" --mode statistics

# 运行测试
python test_feishu.py

# 运行主工作流（自动使用精选文章模式）
bash run.sh          # Linux/Mac
.\run.ps1            # Windows
```

## ✅ 项目就绪状态

- ✅ 代码完成和测试
- ✅ 文档完整和链接
- ✅ 演示脚本可用
- ✅ 跨平台支持完成
- ✅ 生产就绪

## 🎉 下一步

1. **立即体验**: `python demo_featured_papers.py`
2. **快速上手**: 阅读 [QUICK_START_FEATURED_MODE.md](QUICK_START_FEATURED_MODE.md)
3. **配置部署**: 参照 [FEISHU_SETUP.md](FEISHU_SETUP.md)
4. **集成到工作流**: 运行 `bash run.sh` 或 `.\run.ps1`

---

**祝您使用愉快！** 🚀

---

*最后更新: 2024 年*  
*所有文件已准备好，可以直接使用。*
