# System Patterns: slidev-exam-ppts

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                     内容切片层 (Content Slices)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   切片 1    │  │   切片 2    │  │   切片 N    │          │
│  │ (知识单元)   │  │ (知识单元)   │  │ (知识单元)   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   转换器 1      │ │   转换器 2      │ │   转换器 N      │
│ (Slice→Slidev)  │ │ (Slice→VitePress)│ │  (其他格式)      │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Slidev PPT    │ │  VitePress Docs │ │   其他输出      │
│   (演示用)      │ │   (笔记用)      │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 核心原则

1. **单一数据源**: 所有输出都基于内容切片，避免多源维护
2. **转换器模式**: 每个输出格式对应一个转换器，便于扩展
3. **声明式配置**: 通过配置文件定义切片结构和输出规则
4. **构建时生成**: 静态生成输出，运行时零依赖

## 目录结构

```
slidev-exam-ppts/
├── memory-bank/           # 项目记忆库 (Memory Bank)
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── activeContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   └── progress.md
│
├── content/               # 内容切片存储 (规划中)
│   ├── cie-9700/
│   │   ├── as/
│   │   │   ├── chapter-1/
│   │   │   │   ├── slice-001.json
│   │   │   │   └── slice-002.json
│   │   │   └── chapter-2/
│   │   └── a2/
│   └── bio-competition/
│
├── slides/                # Slidev 幻灯片源文件
│   ├── cie-9700/
│   │   ├── slides.md           # Chapter 1
│   │   └── chapter-2/
│   │       └── slides.md
│   └── bio-competition/
│       └── molecular-biology-of-the-cell/
│           └── chapter7/
│               └── slides.md
│
├── docs/                  # VitePress 文档源文件
│   ├── .vitepress/
│   │   ├── config.mts         # VitePress 配置
│   │   └── dist/              # 构建输出
│   ├── index.md               # 首页
│   ├── cie/                   # CIE 考纲笔记
│   │   ├── index.md
│   │   └── as/
│   │       ├── chapter1.md
│   │       └── chapter2.md
│   └── bio-competition/       # 生物竞赛笔记
│       ├── index.md
│       └── molecular-biology/
│           └── chapter7.md
│
├── scripts/               # 构建和工具脚本
│   ├── download-feishu-files.py
│   ├── import-slices.js       # (规划中) 切片导入
│   ├── build-ppt.js           # (规划中) PPT 生成
│   └── build-notes.js         # (规划中) 笔记生成
│
├── src/                   # Vue 组件和工具
│   ├── components/
│   ├── utils/
│   └── App.vue
│
├── public/                # 静态资源
├── .github/
│   └── workflows/
│       ├── deploy.yml         # 部署工作流
│       └── ci.yml
├── package.json
├── README.md
└── vite.config.ts
```

## 构建流程