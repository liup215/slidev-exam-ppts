# Content Slice Rules - slidev-exam-ppts

> 内容切片规范：定义内容的基本单元

## 目录

- [切片文件格式](#切片文件格式)
- [切片大小限制](#切片大小限制)
- [元数据字段规范](#元数据字段规范)
- [切片边界原则](#切片边界原则)
- [内容格式规范](#内容格式规范)
- [示例切片](#示例切片)

---

## 切片文件格式

每个切片文件由两部分组成：**Frontmatter** + **Markdown内容**

### 基本结构

```markdown
---
# Frontmatter（YAML格式）
id: bio-cell-001
topic: cell-structure
source: "Biology A-Level Textbook Chapter 3"
exam_points:
  - "细胞结构识别"
  - "细胞器功能"
difficulty: medium
duration: 5
---

# Markdown内容

## 标题

正文内容...
```

### Frontmatter 分隔符

- 开始标记：`---`（必须独占一行）
- 结束标记：`---`（必须独占一行）
- 使用标准YAML格式
- 不支持多行字符串值（使用数组代替）

---

## 切片大小限制

### 字符数限制

| 属性 | 最小值 | 推荐值 | 最大值 |
|------|--------|--------|--------|
| 总字符数 | 500 | 2000-2500 | 3000 |
| 正文内容 | 300 | 1500-2000 | 2500 |
| Frontmatter | - | - | 500 |

### 限制原因

- **PPT适配**：一个切片对应1-2张幻灯片
- **注意力跨度**：适合5-10分钟讲解
- **笔记长度**：适合单页笔记展示
- **搜索优化**：便于精准检索

### 超限处理

```
当内容超过2500字符时：
1. 优先在段落边界处拆分
2. 创建新的切片文件
3. 使用 sequence 字段标记顺序
4. 在元数据中标注 `part_of_series: true`
```

---

## 元数据字段规范

### 必需字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `id` | string | 唯一标识符 | `bio-cell-001` |
| `topic` | string | 主题标识 | `cell-structure` |
| `source` | string | 内容来源 | `"Biology A-Level Textbook Ch.3"` |

### 推荐字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `exam_points` | array | 考点列表 | `["细胞结构识别", "细胞器功能"]` |
| `difficulty` | string | 难度等级 | `easy`, `medium`, `hard` |
| `duration` | number | 预计时长（分钟） | `5` |
| `tags` | array | 标签 | `["细胞", "显微镜"]` |
| `sequence` | number | 系列中的顺序 | `1` |
| `part_of_series` | boolean | 是否属于系列 | `true` |
| `related_slices` | array | 相关切片ID | `["bio-cell-002", "bio-cell-003"]` |

### 可选字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `author` | string | 作者 | `"Alex Liu"` |
| `created_at` | string | 创建日期 | `"2026-03-15"` |
| `updated_at` | string | 更新日期 | `"2026-03-15"` |
| `subject` | string | 学科 | `"biology"` |
| `grade` | string | 年级 | `"A-Level"` |

### 字段值规范

#### id 格式

```yaml
# 格式: {subject}-{topic}-{sequence}
id: bio-cell-001

# 组成:
# - subject: 学科缩写 (bio, chem, phy, math...)
# - topic: 主题标识 (kebab-case)
# - sequence: 3位数字序号
```

#### difficulty 枚举

```yaml
difficulty: easy      # 基础概念，适合预习
difficulty: medium    # 标准难度，常规教学
difficulty: hard      # 复杂内容，需要深入理解
```

#### exam_points 格式

```yaml
# 使用数组，每个考点简洁明了
exam_points:
  - "细胞结构识别"
  - "细胞器功能区分"
  - "原核与真核细胞比较"
```

---

## 切片边界原则

### 基本原则

```
✅ 好的切片边界：
├── 在段落结束时拆分
├── 在主题转换时拆分
├── 在逻辑完整的知识点后拆分
└── 在示例/练习开始前拆分

❌ 不好的切片边界：
├── 切断句子（词组未完）
├── 切断列表项（列表未完）
├── 切断代码块
├── 切断表格
└── 切断示例说明
```

### 具体规则

#### 1. 句子完整性

```markdown
❌ 错误：切断句子
"细胞膜的主要功能是控制物质进出细胞，同时"
（切片结束，句子未完）

✅ 正确：完整句子
"细胞膜的主要功能是控制物质进出细胞，同时保护细胞内部结构。"
（句子完整，可以结束切片）
```

#### 2. 段落完整性

```markdown
✅ 正确：完整段落
细胞膜具有选择透过性，这意味着：

1. 允许水分子自由通过
2. 允许需要的离子和小分子通过
3. 阻止大分子和有害物质进入

（列表完整，可以结束切片）
```

#### 3. 主题单一性

```markdown
❌ 错误：混合主题
- 前半部分：细胞膜结构
- 后半部分：细胞核功能

✅ 正确：单一主题
- 切片1：细胞膜结构（完整）
- 切片2：细胞核功能（完整）
```

#### 4. 系列切片处理

```markdown
# 当内容需要多个切片时

# 切片1: bio-cell-001.md
---
id: bio-cell-001
topic: cell-structure
sequence: 1
part_of_series: true
---
# 细胞膜结构（上）
...

# 切片2: bio-cell-002.md
---
id: bio-cell-002
topic: cell-structure
sequence: 2
part_of_series: true
related_slices: ["bio-cell-001"]
---
# 细胞膜结构（下）
...
```

---

## 内容格式规范

### Markdown 支持

```markdown
# 标题
## 二级标题
### 三级标题

**粗体文本**
*斜体文本*

- 无序列表
- 列表项

1. 有序列表
2. 列表项

> 引用块

| 表格 | 表头 |
|------|------|
| 数据 | 数据 |

```代码块```

[链接文本](url)
![图片alt](图片url)
```

### 特殊标记

#### 重点标记

```markdown
<!-- 用于PPT高亮和笔记重点 -->
**重点**：细胞膜的选择透过性

<!-- 用于考点标记 -->
📌 考点：细胞器的功能识别

<!-- 用于注意提醒 -->
⚠️ 注意：原核细胞没有细胞核
```

#### 交互标记

```markdown
<!-- 用于PPT动画标记 -->
<!-- @animation: fade-in -->

<!-- 用于笔记折叠标记 -->
<!-- @collapsible: true -->

<!-- 用于PPT分页标记 -->
<!-- @slide-break -->
```

### 图片规范

```markdown
<!-- 相对路径，图片存放在 assets/ 目录 -->
![细胞膜结构图](../assets/cell-membrane.png)

<!-- 图片属性 -->
<img src="../assets/cell-membrane.png" width="600" alt="细胞膜结构">
```

---

## 示例切片

### 完整示例

```markdown
---
id: bio-cell-001
topic: cell-structure
source: "Biology A-Level Textbook Chapter 3, Section 2"
exam_points:
  - "细胞膜的结构识别"
  - "磷脂双分子层的功能"
  - "膜蛋白的作用"
difficulty: medium
duration: 8
tags:
  - "细胞膜"
  - "磷脂"
  - "膜蛋白"
sequence: 1
part_of_series: true
subject: "biology"
grade: "A-Level"
---

## 细胞膜的结构与功能

### 基本结构

细胞膜主要由**磷脂双分子层**构成，具有以下特点：

1. **流动性**：磷脂分子可以横向移动
2. **不对称性**：膜内外层的磷脂种类不同
3. **镶嵌性**：蛋白质分子镶嵌或贯穿其中

### 膜蛋白的功能

| 蛋白类型 | 主要功能 |
|---------|---------|
| 通道蛋白 | 允许特定离子通过 |
| 载体蛋白 | 主动运输物质 |
| 受体蛋白 | 接收信号分子 |
| 酶蛋白 | 催化膜表面反应 |

### 考点提示

📌 **常见考点**：
- 磷脂分子的亲水头部和疏水尾部
- 流动镶嵌模型的证据
- 膜蛋白与物质运输的关系

⚠️ **易错点**：不要混淆通道蛋白和载体蛋白的作用机制。
```

---

## 验证清单

创建切片后，检查以下项目：

- [ ] Frontmatter 包含必需的 `id`, `topic`, `source`
- [ ] `id` 格式符合规范
- [ ] 字符数在 2000-2500 范围内
- [ ] 没有切断句子或段落
- [ ] 主题单一，内容聚焦
- [ ] 图片路径使用相对路径
- [ ] 特殊标记语法正确
