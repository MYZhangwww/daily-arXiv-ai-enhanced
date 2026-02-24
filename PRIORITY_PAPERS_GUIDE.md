# 🎯 优先级论文选择与完整信息展示 / Priority Papers & Full Information Display

## 🎉 新功能说明 / Feature Overview

### 核心改进 / Key Improvements

✅ **完整展示信息**
- 论文标题 - 完整显示，不再截断
- AI 总结 - 完整显示，保留所有细节
- 作者信息 - 显示前 3 位作者
- 论文分类 - 完整分类信息
- 论文 ID - 便于查阅

✅ **优先级展示**
- 自动识别 "autonomous driving" / "自动驾驶" 相关论文
- 优先论文用 ⭐ 标记
- 优先论文在列表前面
- 支持自定义关键词

✅ **更清晰的消息格式**
- 🤖 标记 AI 总结
- 📌 标记分类信息
- 👥 标记作者信息
- 🔗 标记论文 ID
- ⭐ 标记优先论文

---

## 📊 变更对比 / Before & After

### 之前 / Before
```
[1] Autonomous Driving System with Deep Le...
分类: cs.CV | 作者: Alice, Bob, Charlie
摘要: 提出了一种基于深度学习的自主驾驶系统...
```

### 现在 / After
```
⭐ [1] Autonomous Driving System with Deep Learning
📌 分类: cs.CV | 作者: Alice, Bob, Charlie
🤖 AI总结: 提出了一种基于深度学习的自主驾驶系统，结合了视觉感知和路径规划算法，在真实交通场景中展示了良好的性能。该方法相比传统方法有 30% 的性能提升。
🔗 ID: 2401.00001
```

---

## 🚀 使用方法 / Usage

### 1️⃣ 发送精选论文通知（自动优先级）
```bash
# 从 Git data 分支发送（自动恢复分支）
python utils/feishu.py --from-git --mode featured

# 从本地文件发送
python utils/feishu.py --data data/2024-02-24.jsonl --mode featured

# 指定日期
python utils/feishu.py --from-git --date 2024-02-24 --mode featured
```

### 2️⃣ 测试演示
```bash
# 查看优先级论文选择演示
python demo_priority_papers.py
```

### 3️⃣ 自定义关键词（代码中修改）
```python
from utils.feishu import get_featured_papers

# 自定义优先级关键词
custom_keywords = ["autonomous driving", "self-driving", "无人车"]
papers = get_featured_papers(data_content, top_n=5, priority_keywords=custom_keywords)
```

---

## 🎯 优先级逻辑 / Priority Logic

### 关键词匹配范围
优先级关键词会在以下位置匹配：
- ✅ 论文标题 / Paper title
- ✅ 摘要 / Summary
- ✅ AI 总结 / AI summary

### 默认关键词 / Default Keywords
```python
priority_keywords = ["autonomous driving", "自动驾驶"]
```

### 排序规则 / Sorting Rules
1. **第一阶段** - 筛选有 AI 总结的论文
2. **第二阶段** - 按关键词分组
   - 优先级论文（包含关键词）
   - 其他论文（不包含关键词）
3. **第三阶段** - 合并并取前 N 篇

---

## 📋 消息格式 / Message Format

### 飞书卡片结构
```
标题: 📚 arXiv 精选论文 - 2024-02-24

字段 1: 更新日期
字段 2: 精选论文数
字段 3: 优先领域: 自动驾驶 (Autonomous Driving)

字段 4-8: 论文 1-5
   ⭐ [1] 完整论文标题
   📌 分类: cs.CV | 作者: Author1, Author2, Author3
   🤖 AI总结: [完整总结文本]
   🔗 ID: 2401.00001

字段 9: 通知时间
字段 10: 数据来源
字段 11: 说明（关于 ⭐ 标记）
```

---

## 📊 代码改进 / Code Changes

### 修改的函数 / Modified Functions

#### 1. `get_featured_papers()`
```python
def get_featured_papers(
    data_content: str, 
    top_n: int = 5, 
    priority_keywords: List[str] = None
) -> List[Dict]:
    """
    改进：
    ✅ 添加 priority_keywords 参数
    ✅ 完整显示标题（不截断）
    ✅ 完整显示 AI 总结（不截断）
    ✅ 添加 is_priority 标记
    ✅ 按优先级排序论文
    """
```

**新增返回字段：**
- `is_priority` - 是否是优先级论文 (bool)

**默认优先级关键词：**
```python
["autonomous driving", "自动驾驶"]
```

#### 2. `_send_featured_papers_notification()`
```python
def _send_featured_papers_notification(
    robot: FeishuRobot, 
    data_content: str, 
    date_str: str
) -> bool:
    """
    改进：
    ✅ 调用 get_featured_papers 时传入优先级关键词
    ✅ 在消息中添加 ⭐ 标记
    ✅ 完整显示论文信息
    ✅ 改进消息格式和组织
    """
```

---

## 📈 新增字段 / New Fields

### 论文信息对象 / Paper Info Object

| 字段 | 类型 | 说明 |
|---|---|---|
| `title` | str | 完整论文标题 |
| `authors` | str | 前 3 位作者 |
| `category` | str | 论文分类 |
| `url` | str | arXiv URL |
| `id` | str | 论文 ID |
| `tldr` | str | 完整 AI 总结或摘要 |
| `has_ai` | bool | 是否有 AI 总结 |
| **`is_priority`** | bool | **✨ 新增** - 是否优先级论文 |

---

## 🔍 示例对比 / Example Comparison

### 示例数据集
```
5 篇论文，其中 2 篇包含 "autonomous driving"：
1. Autonomous Driving System with Deep Learning ⭐
2. Multi-Task Learning for Vision Transformers
3. Robust Perception for Autonomous Vehicles ⭐
4. Neural Architecture Search for Mobile Deployment
5. End-to-End Learning for Self-Driving Cars ⭐
```

### 优先级排序后
```
排序顺序 (top 5)：
1. Autonomous Driving System with Deep Learning ⭐
2. Robust Perception for Autonomous Vehicles ⭐
3. End-to-End Learning for Self-Driving Cars ⭐
4. Multi-Task Learning for Vision Transformers
5. Neural Architecture Search for Mobile Deployment
```

---

## 💡 高级用法 / Advanced Usage

### 自定义优先级关键词
```python
# 在 Python 脚本中修改
from utils.feishu import get_featured_papers

# 示例：优先展示深度学习和强化学习论文
custom_keywords = ["deep learning", "reinforcement learning", 
                   "深度学习", "强化学习"]
                   
papers = get_featured_papers(
    data_content, 
    top_n=5,
    priority_keywords=custom_keywords
)
```

### 多关键词搜索
```python
# 示例：多领域优先级
priority_keywords = [
    # 自动驾驶
    "autonomous driving", "self-driving", "自动驾驶", "无人驾驶",
    # 计算机视觉
    "computer vision", "object detection", "视觉", "目标检测",
    # 传感器融合
    "sensor fusion", "传感器", "融合"
]

papers = get_featured_papers(
    data_content,
    top_n=5,
    priority_keywords=priority_keywords
)
```

---

## ✨ 新功能特性 / New Features

### 🎯 智能优先级
- 自动识别关键领域
- 支持中英文双语关键词
- 灵活的关键词定制

### 📝 完整信息展示
- 标题不截断
- 总结保留完整细节
- 元数据详细显示

### 🎨 美观的消息格式
- 使用 emoji 标记不同信息类型
- 清晰的层级结构
- 易于阅读和理解

### 🔧 向后兼容
- 现有代码无需修改
- 默认参数智能选择
- 平滑升级

---

## 🧪 测试验证 / Testing

### 运行演示脚本
```bash
python demo_priority_papers.py
```

### 预期输出
✅ 5 篇精选论文  
✅ 2 篇优先级论文（包含 autonomous driving）  
✅ 3 篇其他论文  
✅ 完整的论文信息  
✅ 完整的 AI 总结  

### 输出示例
```
⭐ [1] Autonomous Driving System with Deep Learning
📌 分类: cs.CV | 作者: Alice, Bob, Charlie
🤖 AI总结: 提出了一种基于深度学习的自主驾驶系统...
🔗 ID: 2401.00001

  [2] Multi-Task Learning for Vision Transformers
📌 分类: cs.CV | 作者: David, Eve, Frank
🤖 AI总结: 研究了多任务学习在视觉转换器中的应用...
🔗 ID: 2401.00002
```

---

## 📱 飞书通知示例 / Feishu Notification Example

### 卡片预览
```
标题: 📚 arXiv 精选论文 - 2024-02-24

更新日期: 2024-02-24
精选论文数: 5
优先领域: 自动驾驶 (Autonomous Driving)

论文 1:
⭐ [1] Autonomous Driving System with Deep Learning
📌 分类: cs.CV | 作者: Alice, Bob, Charlie
🤖 AI总结: 提出了一种基于深度学习的自主驾驶系统，结合了视觉感知
和路径规划算法，在真实交通场景中展示了良好的性能...
🔗 ID: 2401.00001

论文 2:
⭐ [2] Robust Perception for Autonomous Vehicles in Adverse Weather
...

说明: ⭐ 标记表示包含 'autonomous driving' 相关内容，优先展示
```

---

## 🚀 快速开始 / Quick Start

### 第 1 步：查看演示
```bash
python demo_priority_papers.py
```

### 第 2 步：发送通知
```bash
# 自动优先级，完整信息
python utils/feishu.py --from-git --mode featured
```

### 第 3 步：验证结果
✅ 飞书群中收到通知  
✅ 优先级论文用 ⭐ 标记  
✅ 完整的论文标题和总结  
✅ 清晰的信息组织  

---

## 📝 更新日志 / Changelog

### v3.0 - 优先级论文与完整信息（当前版本）

**新增功能 / New Features:**
- ✅ 优先级论文选择（autonomous driving）
- ✅ 完整显示论文标题和 AI 总结
- ✅ ⭐ 标记优先级论文
- ✅ 改进的消息格式和组织

**代码改进 / Code Improvements:**
- ✅ `get_featured_papers()` 添加 priority_keywords 参数
- ✅ `get_featured_papers()` 返回完整信息
- ✅ `_send_featured_papers_notification()` 改进消息格式
- ✅ 添加 `is_priority` 标记

**文档完善 / Documentation:**
- ✅ 本使用指南
- ✅ 演示脚本 `demo_priority_papers.py`
- ✅ 代码注释更新

---

## ❓ 常见问题 / FAQ

### Q1: 如何修改优先级关键词？
**A:** 在 `_send_featured_papers_notification()` 函数中修改：
```python
priority_keywords = ["autonomous driving", "自动驾驶"]
```

### Q2: 是否支持多个关键词？
**A:** 支持！传入关键词列表即可：
```python
priority_keywords = ["autonomous driving", "self-driving", "无人驾驶"]
```

### Q3: 完整信息会不会太长？
**A:** 飞书卡片支持长文本，完整信息反而更有价值。

### Q4: 优先级论文必须在前面吗？
**A:** 是的，优先级论文会自动排到列表前面。

### Q5: 如何禁用优先级功能？
**A:** 传入空列表：`priority_keywords=[]`

---

## 📞 支持 / Support

如有任何问题或建议，欢迎反馈！

**关键文件：**
- `utils/feishu.py` - 核心实现
- `demo_priority_papers.py` - 演示脚本
- `PRIORITY_PAPERS_GUIDE.md` - 本文档

---

**版本:** v3.0  
**状态:** ✅ 完成  
**最后更新:** 2024-02-24
