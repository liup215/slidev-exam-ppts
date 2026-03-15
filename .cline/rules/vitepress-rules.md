# VitePress Rules - slidev-exam-ppts

> 笔记生成规则：从内容切片到学习笔记

## 目录

- [VitePress页面结构](#vitepress页面结构)
- [切片到笔记的映射规则](#切片到笔记的映射规则)
- [导航和链接规范](#导航和链接规范)
- [搜索优化要求](#搜索优化要求)
- [模板系统](#模板系统)
- [示例输出](#示例输出)

---

## VitePress页面结构

### 生成的笔记文件结构

```markdown
---
# Frontmatter（从切片元数据转换）
title: 细胞膜的结构与功能
description: 学习细胞膜的基本结构、磷脂双分子层特点及膜蛋白功能
outline: deep
---

# 细胞膜的结构与功能

> **学科**：生物学 | **年级**：A-Level | **预计时长**：8分钟

## 考点概览

- 细胞膜的结构识别
- 磷脂双分子层的功能
- 膜蛋白的作用

## 正文内容

### 基本结构

细胞膜主要由**磷脂双分子层**构成...

## 相关切片

- [细胞核的结构与功能](./nucleus-structure)
- [细胞器的功能](./organelles)

## 练习题目

<!-- 从题库动态加载 -->
```

### 页面类型

| 类型 | 用途 | 文件位置 |
|------|------|----------|
| `topic` | 主题笔记页 | `{subject}/{topic}/index.md` |
| `exam-point` | 考点详解页 | `{subject}/exam-points/{point}.md` |
| `index` | 索引/目录页 | `{subject}/index.md` |

---

## 切片到笔记的映射规则

### 基本映射

```
切片文件 → 笔记页面片段

映射规则：
├── 切片标题 → 页面标题/章节标题
├── 切片正文 → 页面正文
├── 列表 → 列表（保持原样）
├── 表格 → 表格（添加样式）
├── 图片 → 图片（优化路径）
├── 考点标记 → 高亮框/标签
└── 元数据 → Frontmatter + 信息框
```

### 内容转换规则

#### 标题映射

```markdown
# 切片中的标题
## 细胞膜的结构与功能

# 生成的VitePress
# 细胞膜的结构与功能
（作为页面主标题，从Frontmatter读取）
```

#### 元数据信息框

```markdown
# 切片元数据
---
subject: biology
grade: A-Level
duration: 8
difficulty: medium
exam_points:
  - "细胞膜结构识别"
  - "磷脂双分子层功能"
---

# 生成的信息框
> **学科**：生物学 | **年级**：A-Level | **预计时长**：8分钟 | **难度**：中等

## 考点概览

- 细胞膜结构识别
- 磷脂双分子层功能
```

#### 考点标记转换

```markdown
# 切片中的标记
📌 **考点**：细胞膜的选择透过性

# 生成的VitePress
::: tip 考点
细胞膜的选择透过性
:::

# 或带样式的版本
<div class="exam-point">
  <span class="badge">考点</span>
  细胞膜的选择透过性
</div>
```

#### 注意提醒转换

```markdown
# 切片中的标记
⚠️ **注意**：原核细胞没有细胞核

# 生成的VitePress
::: warning 注意
原核细胞没有细胞核
:::
```

#### 图片路径转换

```markdown
# 切片中的路径（相对于切片文件）
![细胞膜结构图](../assets/cell-membrane.png)

# 生成的VitePress路径（相对于笔记文件）
![细胞膜结构图](./assets/cell-membrane.png)
```

### 多切片组合

```
当多个切片组成一个主题笔记时：

切片1 (bio-cell-001) → 页面第1节
切片2 (bio-cell-002) → 页面第2节
切片3 (bio-cell-003) → 页面第3节

自动生成：
- 页面标题和描述
- 目录（TOC）
- 上一页/下一页导航
- 相关页面链接
```

---

## 导航和链接规范

### 目录结构

```
generated/notes/
├── biology/
│   ├── index.md                    # 生物学首页
│   ├── cell-structure/
│   │   ├── index.md               # 细胞膜主题笔记
│   │   └── assets/
│   │       └── cell-membrane.png
│   ├── nucleus-structure/
│   │   └── index.md
│   └── exam-points/
│       ├── cell-membrane.md       # 考点详解
│       └── organelles.md
├── chemistry/
│   └── ...
└── index.md                        # 笔记首页
```

### 导航配置

```typescript
// 自动生成的导航配置
// .vitepress/config.ts

export default {
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '生物学', link: '/biology/' },
      { text: '化学', link: '/chemistry/' }
    ],
    sidebar: {
      '/biology/': [
        {
          text: '细胞生物学',
          items: [
            { text: '细胞膜的结构与功能', link: '/biology/cell-structure/' },
            { text: '细胞核的结构与功能', link: '/biology/nucleus-structure/' }
          ]
        },
        {
          text: '考点详解',
          items: [
            { text: '细胞膜', link: '/biology/exam-points/cell-membrane' }
          ]
        }
      ]
    }
  }
}
```

### 链接格式

```markdown
# 内部链接（使用相对路径）
[细胞膜的结构与功能](./cell-structure/)
[返回生物学首页](../)

# 考点链接
[考点：细胞膜结构](../exam-points/cell-membrane)

# 跨学科链接
[相关化学知识](../../chemistry/atomic-theory/)

# 外部链接
[维基百科](https://en.wikipedia.org/wiki/Cell_membrane){target="_blank"}
```

### 上一页/下一页

```markdown
---
# 自动生成的页面导航
prev:
  text: '细胞概述'
  link: '/biology/cell-overview/'
next:
  text: '细胞核的结构与功能'
  link: '/biology/nucleus-structure/'
---
```

---

## 搜索优化要求

### Frontmatter 规范

```markdown
---
# 必需
title: 细胞膜的结构与功能

# 推荐
description: 详细讲解细胞膜的磷脂双分子层结构、流动镶嵌模型及膜蛋白功能，包含A-Level生物考试重点
outline: deep

# 可选（用于搜索优化）
keywords:
  - 细胞膜
  - 磷脂双分子层
  - 流动镶嵌模型
  - 膜蛋白
  - A-Level生物
tags:
  - 细胞生物学
  - 考试重点
---
```

### 内容优化

#### 标题层级

```markdown
# 页面标题（H1）- 从Frontmatter生成
## 主要章节（H2）
### 小节（H3）
#### 细节（H4，尽量少用）
```

#### 关键词布局

```markdown
# 在以下位置包含关键词：
1. 页面标题（title）
2. 描述（description）
3. 正文第一段
4. 章节标题
5. 图片alt文本

# 示例
## 细胞膜的结构（含关键词"细胞膜"）

细胞膜（cell membrane）是细胞的重要组成部分...

![细胞膜结构示意图](./assets/cell-membrane.png)
（图片alt包含"细胞膜"）
```

### 结构化数据

```markdown
# 使用表格展示对比信息
| 特征 | 原核细胞 | 真核细胞 |
|-----|---------|---------|
| 细胞核 | 无 | 有 |
| 膜结合细胞器 | 无 | 有 |

# 使用列表展示要点
- **流动性**：磷脂分子可以横向移动
- **不对称性**：膜内外层磷脂种类不同

# 使用代码块展示术语
```
流动镶嵌模型（Fluid Mosaic Model）
```
```

### 搜索配置

```typescript
// .vitepress/config.ts
export default {
  themeConfig: {
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索笔记',
                buttonAriaLabel: '搜索笔记'
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭'
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## 模板系统

### 模板文件位置

```
templates/vitepress/
├── page.md           # 笔记页面模板
├── topic-index.md    # 主题索引模板
├── exam-point.md     # 考点详解模板
└── subject-index.md  # 学科首页模板
```

### 页面模板

```markdown
<!-- templates/vitepress/page.md -->
---
title: {{ title }}
description: {{ description }}
outline: deep
prev: {{ prev }}
next: {{ next }}
---

# {{ title }}

> **学科**：{{ subject }} | **年级**：{{ grade }} | **预计时长**：{{ duration }}分钟
{{#if difficulty}}
> **难度**：{{ difficultyText }}
{{/if}}

{{#if examPoints}}
## 考点概览

{{#each examPoints}}
- {{ this }}
{{/each}}
{{/if}}

## 正文

{{ content }}

{{#if relatedSlices}}
## 相关主题

{{#each relatedSlices}}
- [{{ title }}]({{ link }})
{{/each}}
{{/if}}

{{#if examPointsDetail}}
## 考点详解

{{#each examPointsDetail}}
### {{ point }}

{{ description }}

{{/each}}
{{/if}}
```

### 模板变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `title` | string | 页面标题 |
| `description` | string | 页面描述 |
| `subject` | string | 学科名称 |
| `grade` | string | 年级 |
| `duration` | number | 预计学习时长 |
| `difficulty` | string | 难度等级 |
| `examPoints` | array | 考点列表 |
| `content` | string | 正文内容（Markdown） |
| `relatedSlices` | array | 相关切片 |
| `prev` | object | 上一页信息 |
| `next` | object | 下一页信息 |

---

## 示例输出

### 完整生成的VitePress页面

```markdown
---
title: 细胞膜的结构与功能
description: 学习细胞膜的基本结构、磷脂双分子层特点及膜蛋白功能，包含A-Level生物考试重点
outline: deep
prev:
  text: '细胞概述'
  link: '/biology/cell-overview/'
next:
  text: '细胞核的结构与功能'
  link: '/biology/nucleus-structure/'
keywords:
  - 细胞膜
  - 磷脂双分子层
  - 流动镶嵌模型
  - 膜蛋白
tags:
  - 细胞生物学
  - 考试重点
---

# 细胞膜的结构与功能

> **学科**：生物学 | **年级**：A-Level | **预计时长**：8分钟 | **难度**：中等

## 考点概览

- 细胞膜的结构识别
- 磷脂双分子层的功能
- 膜蛋白的作用

## 基本结构

细胞膜主要由**磷脂双分子层**构成，具有以下特点：

- 🌊 **流动性**：磷脂分子可以横向移动
- ⚖️ **不对称性**：膜内外层的磷脂种类不同
- 🧩 **镶嵌性**：蛋白质分子镶嵌或贯穿其中

::: tip 考点
细胞膜的选择透过性是A-Level考试的重点内容
:::

## 膜蛋白的功能

| 蛋白类型 | 主要功能 | 考试频率 |
|---------|---------|---------|
| 通道蛋白 | 允许特定离子通过 | ⭐⭐⭐ |
| 载体蛋白 | 主动运输物质 | ⭐⭐⭐⭐ |
| 受体蛋白 | 接收信号分子 | ⭐⭐⭐ |
| 酶蛋白 | 催化膜表面反应 | ⭐⭐ |

::: warning 易错点
不要混淆通道蛋白和载体蛋白的作用机制：
- 通道蛋白：形成通道，被动运输
- 载体蛋白：结合物质，可主动运输
:::

## 相关主题

- [细胞核的结构与功能](./nucleus-structure/)
- [细胞器的功能](./organelles/)
- [物质跨膜运输](../exam-points/transport/)

## 练习题目

<!-- 从题库动态加载 -->
<Quiz topic="cell-membrane" count="5" />
```

---

## 构建输出规范

### 输出文件

```
generated/notes/
├── .vitepress/
│   ├── config.ts           # VitePress配置
│   └── theme/
│       └── custom.css      # 自定义样式
├── biology/
│   ├── index.md            # 学科首页
│   ├── cell