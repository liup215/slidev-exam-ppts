# Slidev Rules - slidev-exam-ppts

> PPT生成规则：从内容切片到演示文稿

## 目录

- [Slidev文件结构](#slidev文件结构)
- [切片到PPT的映射规则](#切片到ppt的映射规则)
- [视觉设计约束](#视觉设计约束)
- [动画和交互规范](#动画和交互规范)
- [模板系统](#模板系统)
- [示例输出](#示例输出)

---

## Slidev文件结构

### 生成的PPT文件结构

```markdown
---
# 全局Frontmatter（从配置和切片元数据合并）
theme: default
title: 细胞膜的结构与功能
info: |
  ## 课程信息
  - 学科：生物学
  - 年级：A-Level
  - 课时：8分钟
---

# 第1页：标题页

# 细胞膜的结构与功能

<div class="pt-12">
  <span class="px-4 py-2 rounded bg-blue-500 text-white">A-Level Biology</span>
</div>

---

# 第2页：内容页（来自切片1）

## 基本结构

细胞膜主要由**磷脂双分子层**构成...

---

# 第3页：内容页（续）

## 膜蛋白的功能

| 蛋白类型 | 主要功能 |
|---------|---------|
| 通道蛋白 | 允许特定离子通过 |
...

---

# 第4页：结束页

# Q & A

感谢聆听
```

### 页面类型

| 类型 | 用途 | 来源 |
|------|------|------|
| `title` | 标题页 | 切片topic + 元数据 |
| `content` | 内容页 | 切片正文 |
| `section` | 章节分隔页 | topic变化时 |
| `end` | 结束页 | 自动生成 |

---

## 切片到PPT的映射规则

### 基本映射

```
切片文件 → 1-2张幻灯片

映射规则：
├── 切片标题 → 幻灯片标题
├── 切片正文 → 幻灯片内容
├── 列表 → 逐步动画列表
├── 表格 → 表格布局
├── 图片 → 图片幻灯片或图文混排
└── 考点标记 → 高亮样式
```

### 内容转换规则

#### 标题映射

```markdown
# 切片中的标题
## 细胞膜的结构与功能

# 生成的Slidev
## 细胞膜的结构与功能
（作为幻灯片标题）
```

#### 列表映射

```markdown
# 切片中的列表
- 流动性：磷脂分子可以横向移动
- 不对称性：膜内外层的磷脂种类不同
- 镶嵌性：蛋白质分子镶嵌或贯穿其中

# 生成的Slidev（带动画）
<v-clicks>

- 流动性：磷脂分子可以横向移动
- 不对称性：膜内外层的磷脂种类不同
- 镶嵌性：蛋白质分子镶嵌或贯穿其中

</v-clicks>
```

#### 表格映射

```markdown
# 切片中的表格
| 蛋白类型 | 主要功能 |
|---------|---------|
| 通道蛋白 | 允许特定离子通过 |
| 载体蛋白 | 主动运输物质 |

# 生成的Slidev
<div class="grid grid-cols-2 gap-4">

| 蛋白类型 | 主要功能 |
|---------|---------|
| 通道蛋白 | 允许特定离子通过 |
| 载体蛋白 | 主动运输物质 |

</div>
```

#### 图片映射

```markdown
# 切片中的图片
![细胞膜结构图](../assets/cell-membrane.png)

# 生成的Slidev
<div class="flex justify-center">
  <img src="/assets/cell-membrane.png" class="w-3/4 rounded-lg shadow-lg" />
</div>
```

### 多切片组合

```
当多个切片组成一个演示文稿时：

切片1 (bio-cell-001) → 幻灯片 1-2
切片2 (bio-cell-002) → 幻灯片 3-4
切片3 (bio-cell-003) → 幻灯片 5-6

自动插入：
- 标题页（第1页）
- 章节页（topic变化时）
- 结束页（最后）
```

---

## 视觉设计约束

### 颜色系统

```css
/* 主色调 */
--primary: #3b82f6;        /* 蓝色 - 主强调 */
--secondary: #10b981;      /* 绿色 - 次要强调 */
--accent: #f59e0b;         /* 橙色 - 高亮 */

/* 考点颜色 */
--exam-point: #ef4444;     /* 红色 - 考点标记 */
--warning: #f97316;        /* 橙色 - 注意提醒 */
--tip: #8b5cf6;            /* 紫色 - 提示 */

/* 中性色 */
--text-primary: #1f2937;   /* 深灰 - 正文 */
--text-secondary: #6b7280; /* 中灰 - 次要文字 */
--bg-light: #f3f4f6;       /* 浅灰 - 背景 */
```

### 字体规范

```css
/* 标题字体 */
font-family: 'Noto Sans SC', sans-serif;
font-weight: 700;

/* 正文字体 */
font-family: 'Noto Sans SC', sans-serif;
font-weight: 400;
font-size: 1.1rem;
line-height: 1.6;

/* 代码字体 */
font-family: 'Fira Code', monospace;
```

### 布局约束

```
页面布局：
├── 标题区域：顶部 15%
├── 内容区域：中部 70%
└── 页脚区域：底部 15%

内容约束：
├── 每页最多 6 个要点
├── 每行最多 40 个汉字
├── 表格最多 4 列
└── 图片最大占页面 60%
```

### 响应式断点

```css
/* Slidev默认断点 */
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
```

---

## 动画和交互规范

### 动画类型

| 动画 | 用途 | 实现方式 |
|------|------|----------|
| `fade` | 淡入淡出 | `<v-click>` |
| `slide` | 滑动进入 | CSS动画类 |
| `zoom` | 缩放进入 | `<v-click>` + scale |
| `typewriter` | 打字机效果 | 代码块专用 |

### 点击动画

```markdown
<!-- 单个元素点击显示 -->
<v-click>

这是一个点击后显示的内容

</v-click>

<!-- 多个元素逐步显示 -->
<v-clicks>

- 第一点
- 第二点
- 第三点

</v-clicks>

<!-- 指定点击次数 -->
<v-click at="2">

在第2次点击时显示

</v-click>
```

### 列表动画

```markdown
<!-- 默认：每项依次显示 -->
<v-clicks>

- 流动性：磷脂分子可以横向移动
- 不对称性：膜内外层的磷脂种类不同
- 镶嵌性：蛋白质分子镶嵌或贯穿其中

</v-clicks>

<!-- 深度：嵌套列表 -->
<v-clicks depth="2">

- 一级项目
  - 二级项目1
  - 二级项目2
- 另一个一级项目

</v-clicks>
```

### 考点高亮动画

```markdown
<!-- 考点标记自动添加动画 -->
📌 **考点**：<span v-click class="text-red-500 font-bold">细胞膜的选择透过性</span>
```

### 过渡效果

```markdown
---
transition: slide-left
---

# 本页使用从左滑入的过渡

---
transition: fade
---

# 本页使用淡入淡出过渡
```

### 禁用动画

```markdown
---
clicks: 0
---

# 本页无点击动画，内容直接显示
```

---

## 模板系统

### 模板文件位置

```
templates/slidev/
├── title.vue       # 标题页模板
├── content.vue     # 内容页模板
├── section.vue     # 章节页模板
├── table.vue       # 表格页模板
├── image.vue       # 图片页模板
└── end.vue         # 结束页模板
```

### 模板变量

```vue
<!-- templates/slidev/content.vue -->
<template>
  <div class="slide-content">
    <h2>{{ title }}</h2>
    <div class="content-body" v-html="content"></div>
    <div v-if="examPoints" class="exam-points">
      <span class="badge">考点</span>
      <ul>
        <li v-for="point in examPoints" :key="point">{{ point }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    content: String,
    examPoints: Array,
    difficulty: String
  }
}
</script>
```

### 模板选择规则

```javascript
// 根据切片内容自动选择模板
function selectTemplate(slice) {
  if (slice.isTitle) return 'title';
  if (slice.hasTable && !slice.hasText) return 'table';
  if (slice.hasImage && !slice.hasText) return 'image';
  if (slice.isSectionBreak) return 'section';
  return 'content';
}
```

---

## 示例输出

### 完整生成的Slidev文件

```markdown
---
theme: default
title: 细胞膜的结构与功能
info: |
  ## 课程信息
  - 学科：生物学
  - 年级：A-Level
  - 课时：8分钟
  - 考点：细胞膜结构识别、磷脂双分子层功能、膜蛋白作用
class: text-center
highlighter: shiki
---

# 细胞膜的结构与功能

<div class="pt-12">
  <span class="px-4 py-2 rounded bg-blue-500 text-white">A-Level Biology</span>
  <span class="px-4 py-2 rounded bg-green-500 text-white ml-2">8分钟</span>
</div>

---

## 基本结构

细胞膜主要由**磷脂双分子层**构成，具有以下特点：

<v-clicks>

- 🌊 **流动性**：磷脂分子可以横向移动
- ⚖️ **不对称性**：膜内外层的磷脂种类不同
- 🧩 **镶嵌性**：蛋白质分子镶嵌或贯穿其中

</v-clicks>

---

## 膜蛋白的功能

<div class="grid grid-cols-2 gap-8">

| 蛋白类型 | 主要功能 |
|---------|---------|
| 通道蛋白 | 允许特定离子通过 |
| 载体蛋白 | 主动运输物质 |
| 受体蛋白 | 接收信号分子 |
| 酶蛋白 | 催化膜表面反应 |

<div>

<v-click>

📌 **考点提示**：
- 通道蛋白 vs 载体蛋白的区别
- 主动运输 vs 被动运输

</v-click>

</div>

</div>

---

# Q & A

<div class="pt-12 text-2xl">
感谢聆听
</div>

<div class="mt-8 text-gray-500">
下节预告：细胞核的结构与功能
</div>
```

---

## 构建输出规范

### 输出文件

```
generated/slides/
├── biology/
│   ├── cell-structure.md      # 源文件
│   └── cell-structure/        # 资源目录
│       └── assets/
├── chemistry/
│   └── atomic-theory.md
└── index.md                   # 演示文稿索引
```

### 资源处理

```javascript
// 图片资源复制规则
{
  // 源路径（相对于切片文件）
  source: 'slices/biology/assets/cell-membrane.png',
  
  // 目标路径（相对于生成的PPT文件）
  target: 'generated/slides/biology/cell-structure/assets/cell-membrane.png',
  
  // Slidev中的引用路径
  reference: './assets/cell-membrane.png'
}
```

### 索引生成

```markdown
# generated/slides/index.md

# 演示文稿索引

## 生物学

- [细胞膜的结构与功能](./biology/cell-structure.md)
- [细胞核的结构与功能](./biology/nucleus-structure.md)

## 化学

- [原子理论](./chemistry/atomic-theory.md)
```
