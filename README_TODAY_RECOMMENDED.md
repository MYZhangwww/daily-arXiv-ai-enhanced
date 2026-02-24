# 📌 今日推荐专栏 - 完整实现指南 / Today's Recommendations - Complete Implementation Guide

**版本:** v1.0  
**发布日期:** 2026-02-24  
**功能状态:** ✅ 完成  

---

## 🎯 功能概述 / Feature Overview

### 核心需求
在GitHub网站上新增一个"今日推荐"专栏，所有被发送到飞书的精选文章的相关内容会展示在此专栏下。

### 关键特性

| 特性 | 说明 |
|------|------|
| 📊 推荐统计 | 实时显示总推荐数、优先级论文数、推荐日期数 |
| 📅 日期选择 | 按日期浏览推荐论文，显示每日论文数量 |
| 🎯 优先级过滤 | 支持全部、优先级、普通论文过滤 |
| 👁️ 多视图模式 | 网格视图 & 列表视图切换 |
| 📖 论文详情 | 完整标题、作者、分类、总结、链接 |
| 🔄 数据同步 | 自动保存飞书发送的推荐论文 |
| 💾 导出功能 | 支持JSON/Markdown导出 |

---

## 📁 项目结构 / Project Structure

### 新增文件

```
daily-arXiv-ai-enhanced/
├── 📄 today-recommended.html          ✨ 推荐专栏主页
├── 📂 css/
│   └── today-recommended.css          ✨ 推荐专栏样式
├── 📂 js/
│   └── today-recommended.js           ✨ 推荐专栏脚本
├── 📂 utils/
│   ├── recommended_papers.py          ✨ 推荐论文管理器
│   └── feishu.py                      ✏️ 修改 - 集成推荐论文保存
├── 📂 data/
│   └── recommended_papers.jsonl       ✨ 推荐论文数据存储
├── demo_today_recommended.py          ✨ 功能演示脚本
└── README_TODAY_RECOMMENDED.md        ✨ 本文档
```

### 修改的文件

```
index.html                     ✏️ 添加"今日推荐"导航链接
utils/feishu.py               ✏️ 集成推荐论文保存
```

---

## 🔄 工作流程 / Workflow

### 数据流

```
每日爬虫完成
    ↓
飞书通知 (_send_featured_papers_notification)
    ↓
RecommendedPapersManager.save_recommended_papers()
    ↓
data/recommended_papers.jsonl
    ↓
today-recommended.html 加载并展示
    ↓
用户浏览推荐论文
```

### 时间流

1. **爬虫运行** - 定时爬取arXiv数据
2. **AI增强** - 生成AI总结
3. **精选论文** - 提取优先级论文（autonomous driving）
4. **飞书通知** - 发送到飞书（自动保存推荐论文）
5. **网页展示** - 用户访问专栏查看

---

## 🚀 使用方式 / Usage

### 1. 网页访问

**直接访问:**
```
https://your-site.com/today-recommended.html
```

**从主页导航:**
```
主页 → 导航栏 → 😊 按钮 → 今日推荐
```

### 2. 功能使用

#### 查看推荐统计
```
页面顶部显示:
- 📊 总推荐数
- ⭐ 优先级论文
- 📅 推荐日期数
```

#### 按日期筛选
```
1. 找到"选择日期"区域
2. 点击日期按钮（如 "2026-02-24"）
3. 查看该日期的推荐论文
```

#### 过滤论文
```
1. 在"优先级过滤"下拉菜单中选择:
   - 全部论文 (All Papers)
   - 优先级论文 (Priority Papers) - ⭐ 标记
   - 普通论文 (Normal Papers)
2. 列表自动更新
```

#### 切换视图
```
网格视图 🔲: 3列卡片布局
列表视图 ☰: 单列详细布局
```

#### 查看论文详情
```
1. 点击任意论文卡片
2. 弹窗显示完整信息:
   - 完整标题
   - 作者列表
   - 论文分类
   - ArXiv ID
   - AI生成总结
   - 原始摘要
3. 点击"arXiv"按钮打开原文
```

### 3. 命令行工具

```bash
# 查看最新推荐（限20篇）
python utils/recommended_papers.py --list latest

# 查看指定日期推荐
python utils/recommended_papers.py --list date --date 2026-02-24

# 查看所有推荐论文
python utils/recommended_papers.py --list all

# 显示统计信息
python utils/recommended_papers.py --stats

# 导出为 JSON
python utils/recommended_papers.py --export json --output recommended.json

# 导出为 Markdown
python utils/recommended_papers.py --export markdown --output recommended.md
```

---

## 💻 代码集成 / Code Integration

### Python 后端集成

#### 在飞书发送通知时自动保存

`feishu.py` 已修改，在发送通知时自动保存推荐论文：

```python
def _send_featured_papers_notification(robot, data_content, date_str):
    # ...获取精选论文...
    featured_papers = get_featured_papers(data_content, top_n=10)
    
    # ✨ 新增：保存推荐论文
    if RecommendedPapersManager:
        try:
            manager = RecommendedPapersManager()
            manager.save_recommended_papers(featured_papers, date_str)
        except Exception as e:
            print(f"保存推荐论文失败: {e}")
    
    # ...继续发送飞书通知...
```

#### 在自定义代码中使用

```python
from utils.recommended_papers import RecommendedPapersManager

# 初始化管理器
manager = RecommendedPapersManager()

# 保存推荐论文
manager.save_recommended_papers(papers_list, "2026-02-24")

# 获取特定日期的推荐
papers = manager.get_recommended_papers_by_date("2026-02-24")

# 获取最新推荐
latest = manager.get_latest_recommended_papers(limit=20)

# 获取统计信息
stats = manager.get_recommended_papers_statistics()

# 导出为 JSON
manager.export_to_json("output.json")

# 导出为 Markdown
manager.export_to_markdown("output.md")
```

### 前端网页集成

#### HTML 结构

```html
<!-- 今日推荐页面 -->
<div class="recommended-container">
    <!-- 推荐统计 -->
    <section class="recommended-header">
        <div class="stat-card">
            <div class="stat-value" id="totalRecommended">-</div>
        </div>
    </section>
    
    <!-- 日期选择 -->
    <section class="date-filter-section">
        <div class="date-buttons" id="dateButtons">
            <!-- 动态生成 -->
        </div>
    </section>
    
    <!-- 论文列表 -->
    <section class="recommended-papers-section">
        <div class="papers-container" id="papersContainer">
            <!-- 动态生成 -->
        </div>
    </section>
</div>
```

#### JavaScript 主要函数

```javascript
// 加载推荐论文数据
async function loadRecommendedPapers() {
    const response = await fetch('./data/recommended_papers.jsonl');
    const text = await response.text();
    // 处理并显示数据
}

// 按日期分组
function groupByDate() { /* ... */ }

// 渲染论文卡片
function renderPapers(date) { /* ... */ }

// 更新统计信息
function updateStatistics() { /* ... */ }
```

---

## 📊 数据格式 / Data Format

### 推荐论文数据结构

存储在 `data/recommended_papers.jsonl` 中，每行一个JSON对象：

```json
{
    "title": "Autonomous Driving System with Deep Learning",
    "authors": "Alice Johnson, Bob Smith, Charlie Lee",
    "category": "cs.CV",
    "id": "2024.01001",
    "url": "https://arxiv.org/abs/2024.01001",
    "tldr": "提出了一种革新性的自动驾驶系统...",
    "summary": "本文介绍了一个完整的自主驾驶感知系统...",
    "has_ai": true,
    "is_priority": true,
    "recommended_date": "2026-02-24",
    "recommended_at": "2026-02-24T10:30:45.123456",
    "priority_status": "priority"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| title | str | 完整论文标题 |
| authors | str | 作者列表（逗号分隔） |
| category | str | arXiv分类（如cs.CV） |
| id | str | arXiv ID |
| url | str | arXiv链接 |
| tldr | str | AI生成总结（完整） |
| summary | str | 原始摘要 |
| has_ai | bool | 是否有AI总结 |
| is_priority | bool | 是否为优先级论文 |
| recommended_date | str | 推荐日期（YYYY-MM-DD） |
| recommended_at | str | 推荐时间戳（ISO8601） |
| priority_status | str | 优先级状态（priority/normal） |

---

## 🎨 前端样式特性 / Frontend Features

### 响应式设计

```
桌面端 (1024px+)     → 3列网格布局
平板 (768px-1024px)  → 2列网格布局  
手机 (<768px)        → 1列列表布局
```

### 视觉元素

| 元素 | 含义 |
|------|------|
| ⭐ | 优先级论文（含autonomous driving关键词） |
| 📌 | 论文分类 |
| ✍️ | 作者信息 |
| 📅 | 推荐日期 |
| 🤖 | AI生成摘要 |
| 🔗 | arXiv链接 |

### 交互效果

- **卡片悬停** - 向上浮起，阴影增强
- **优先级标记** - 脉冲动画闪烁
- **按钮切换** - 平滑颜色过渡
- **模态弹窗** - 淡入淡出效果
- **页面加载** - 动画滑入

---

## 🧪 测试 / Testing

### 运行演示

```bash
python demo_today_recommended.py
```

**输出包含：**
- ✅ 生成5篇演示论文
- ✅ 保存到不同日期
- ✅ 统计信息验证
- ✅ 按日期查询验证
- ✅ 导出功能验证
- ✅ 功能说明

### 手动测试

1. **打开网页**
   ```
   浏览器 → http://localhost/today-recommended.html
   ```

2. **查看统计**
   ```
   ✓ 显示总推荐数
   ✓ 显示优先级论文数
   ✓ 显示推荐日期数
   ```

3. **测试过滤**
   ```
   ✓ 点击日期按钮 → 论文列表更新
   ✓ 选择优先级过滤 → 列表过滤正确
   ✓ 切换视图模式 → 布局改变
   ```

4. **测试详情**
   ```
   ✓ 点击论文卡片 → 弹窗显示
   ✓ 完整信息展示 → 无截断
   ✓ 链接可点击 → 打开arXiv
   ```

---

## 🔧 配置选项 / Configuration

### 优先级关键词

在 `feishu.py` 中修改：

```python
# 默认关键词
priority_keywords = ["autonomous driving", "自动驾驶", "self driving", "VLA"]

# 自定义关键词
priority_keywords = [
    "autonomous driving",
    "自动驾驶", 
    "computer vision",
    "深度学习"
]
```

### 推荐论文数量

在 `feishu.py` 中修改：

```python
# 默认前10篇
featured_papers = get_featured_papers(data_content, top_n=10)

# 改为前5篇
featured_papers = get_featured_papers(data_content, top_n=5)
```

### API 端点

在 `today-recommended.js` 中修改：

```javascript
// 默认数据源
const API_BASE = dataSource.baseUrl || './data';

// 推荐论文文件
const API_ENDPOINTS = {
    recommended: `${API_BASE}/recommended_papers.jsonl`,
};
```

---

## 📈 扩展功能 / Extended Features

### 可能的增强

1. **搜索功能**
   ```
   - 按标题搜索
   - 按作者搜索
   - 按分类搜索
   ```

2. **高级过滤**
   ```
   - 按时间范围过滤
   - 按作者过滤
   - 按分类过滤
   ```

3. **推荐排序**
   ```
   - 按推荐时间排序
   - 按被引用数排序
   - 自定义排序
   ```

4. **社交分享**
   ```
   - 分享单篇论文
   - 分享推荐列表
   - 导出图片
   ```

5. **收藏功能**
   ```
   - 收藏推荐论文
   - 创建自定义列表
   - 本地存储
   ```

### 实现步骤

```javascript
// 示例：添加搜索功能
function searchPapers(query) {
    const filtered = currentDisplayedPapers.filter(paper =>
        paper.title.toLowerCase().includes(query.toLowerCase()) ||
        paper.authors.toLowerCase().includes(query.toLowerCase())
    );
    return filtered;
}
```

---

## 🐛 故障排查 / Troubleshooting

### 问题1：推荐论文不显示

**原因：** 数据文件不存在或路径错误

**解决方案：**
```bash
# 检查数据文件
ls -la data/recommended_papers.jsonl

# 运行演示生成测试数据
python demo_today_recommended.py
```

### 问题2：页面加载缓慢

**原因：** 推荐论文数据过多

**解决方案：**
```javascript
// 在 today-recommended.js 中限制显示数量
const MAX_PAPERS_TO_LOAD = 1000;  // 限制
```

### 问题3：日期按钮不显示

**原因：** 没有该日期的推荐论文

**解决方案：**
```bash
# 生成演示数据
python demo_today_recommended.py

# 或手动保存推荐
python utils/recommended_papers.py
```

### 问题4：飞书通知成功但推荐没保存

**原因：** RecommendedPapersManager 导入失败

**解决方案：**
```python
# 检查导入
python -c "from utils.recommended_papers import RecommendedPapersManager; print('OK')"

# 确保data目录存在
mkdir -p data
```

---

## 📝 维护指南 / Maintenance

### 定期检查

**每周：**
- [ ] 检查推荐论文数据文件大小
- [ ] 验证网页可访问
- [ ] 检查错误日志

**每月：**
- [ ] 备份推荐论文数据
- [ ] 导出统计报告
- [ ] 清理过期数据

### 数据备份

```bash
# 备份推荐论文
cp data/recommended_papers.jsonl data/recommended_papers_backup_$(date +%Y%m%d).jsonl

# 导出为 JSON
python utils/recommended_papers.py --export json --output backup_$(date +%Y%m%d).json

# 导出为 Markdown
python utils/recommended_papers.py --export markdown --output backup_$(date +%Y%m%d).md
```

### 数据清理

```python
# 删除某个日期之前的推荐
import os
from utils.recommended_papers import RecommendedPapersManager

manager = RecommendedPapersManager()
papers = manager.get_all_recommended_papers()

# 保留最近30天
from datetime import datetime, timedelta
cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# 手动编辑 JSONL 文件...
```

---

## 📚 相关文档 / Related Documentation

- [飞书集成指南](FEISHU_INTEGRATION.md)
- [优先级论文说明](PRIORITY_PAPERS_GUIDE.md)
- [Git自动恢复说明](BRANCH_AUTO_RESTORE.md)
- [API文档](API.md)

---

## ✅ 检查清单 / Checklist

### 安装检查
- [x] `today-recommended.html` 已创建
- [x] `css/today-recommended.css` 已创建
- [x] `js/today-recommended.js` 已创建
- [x] `utils/recommended_papers.py` 已创建
- [x] `feishu.py` 已修改集成推荐保存
- [x] `index.html` 已添加导航链接
- [x] 演示脚本 `demo_today_recommended.py` 已创建

### 功能检查
- [x] 推荐统计显示正确
- [x] 日期过滤功能可用
- [x] 优先级过滤功能可用
- [x] 多视图模式切换正常
- [x] 论文详情弹窗正确显示
- [x] 导出功能可用
- [x] 响应式布局正确

### 集成检查
- [x] 飞书通知时自动保存推荐
- [x] 数据文件正确生成
- [x] 网页能正确加载数据
- [x] 命令行工具可用

---

## 🎉 完成情况 / Completion Status

**实现状态:** ✅ **完全完成**

所有需求功能已实现：
- ✅ 网页专栏创建完成
- ✅ 推荐论文自动保存
- ✅ 数据展示功能完整
- ✅ 用户交互设计优良
- ✅ 后端集成完成
- ✅ 命令行工具齐全
- ✅ 文档详尽完善

**可立即投入生产环境使用！** 🚀

---

**版本:** v1.0 | **状态:** ✅ 完成 | **日期:** 2026-02-24
