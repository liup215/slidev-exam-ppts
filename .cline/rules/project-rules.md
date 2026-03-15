# Project Rules - slidev-exam-ppts

> 项目整体规则：内容切片驱动的双输出系统（PPT + 笔记）

## 目录

- [项目目标](#项目目标)
- [目录结构规范](#目录结构规范)
- [文件命名约定](#文件命名约定)
- [核心原则](#核心原则)
- [版本控制](#版本控制)

---

## 项目目标

**slidev-exam-ppts** 是一个基于内容切片的笔记/PPT双输出系统：

- **输入**：结构化的内容切片（Markdown + Frontmatter）
- **输出**：
  - 📊 PPT演示文稿（Slidev）
  - 📝 学习笔记（VitePress）
- **核心价值**：一份内容，多种呈现，维护成本最小化

---

## 目录结构规范

```
slidev-exam-ppts/
├── .cline/
│   └── rules/              # Cline工作规则（本目录）
├── slices/                 # 内容切片源文件
│   ├── biology/            # 生物学科
│   ├── chemistry/          # 化学学科
│   └── ...
├── templates/              # 生成模板
│   ├── slidev/             # Slidev模板
│   └── vitepress/          # VitePress模板
├── generated/              # 生成输出目录（不提交到git）
│   ├── slides/             # 生成的PPT文件
│   └── notes/              # 生成的笔记文件
├── scripts/                # 构建脚本
│   ├── build.js            # 主构建脚本
│   ├── slice-validator.js  # 切片验证
│   └── generators/         # 生成器模块
├── config/                 # 配置文件
│   ├── slidev.config.ts    # Slidev配置
│   └── vitepress.config.ts # VitePress配置
├── package.json
└── README.md
```

### 目录说明

| 目录 | 用途 | 是否提交Git |
|------|------|------------|
| `slices/` | 内容切片源文件 | ✅ 是 |
| `templates/` | 生成模板 | ✅ 是 |
| `generated/` | 生成输出 | ❌ 否（.gitignore） |
| `scripts/` | 构建脚本 | ✅ 是 |
| `config/` | 配置文件 | ✅ 是 |

---

## 文件命名约定

### 内容切片文件

```
slices/{subject}/{topic}-{sequence}.md

# 示例：
slices/biology/cell-structure-001.md
slices/biology/cell-structure-002.md
slices/chemistry/atomic-theory-001.md
```

**命名规则：**
- 使用小写字母和连字符（kebab-case）
- 主题（topic）使用英文或拼音
- 序号（sequence）使用3位数字，从001开始
- 文件扩展名：`.md`

### 模板文件

```
templates/slidev/{template-name}.vue
templates/vitepress/{template-name}.md

# 示例：
templates/slidev/title-slide.vue
templates/vitepress/note-page.md
```

### 生成文件

```
generated/slides/{subject}/{presentation-name}.md
generated/notes/{subject}/{topic}/index.md

# 示例：
generated/slides/biology/cell-structure.md
generated/notes/biology/cell-structure/index.md
```

---

## 核心原则

### 1. 源文件优先原则

```
❌ 禁止：直接修改 generated/ 目录下的任何文件
✅ 必须：修改 slices/ 目录下的源切片文件，然后重新生成
```

**原因**：
- 生成文件是派生产物，不应包含业务逻辑
- 直接修改生成文件会导致源文件与输出不一致
- 所有变更必须通过源文件驱动

### 2. 单一数据源原则

```
slices/ 目录是唯一的内容数据源
├── 所有PPT内容来自切片
├── 所有笔记内容来自切片
└── 模板只负责呈现，不包含内容
```

### 3. 可重复构建原则

```
删除 generated/ 目录 → 运行构建脚本 → 得到完全相同的输出
```

### 4. 增量更新原则

```
只重新生成变更的切片及其依赖的文件
├── 检测切片文件的修改时间
├── 比较源文件与生成文件的哈希
└── 跳过未变更的切片
```

---

## 版本控制

### .gitignore 配置

```gitignore
# 生成输出
generated/

# 依赖
node_modules/

# 日志
*.log
logs/

# 临时文件
.tmp/
.cache/

# 编辑器
.vscode/settings.json
.idea/
```

### 提交规范

```
提交信息格式：<type>(<scope>): <subject>

类型（type）：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式调整
- refactor: 重构
- perf: 性能优化
- test: 测试
- chore: 构建/工具

范围（scope）：
- slices: 内容切片
- slidev: PPT生成
- vitepress: 笔记生成
- build: 构建系统

示例：
feat(slices): 添加细胞分裂切片
fix(slidev): 修复标题样式问题
docs(vitepress): 更新导航文档
```

---

## 扩展性考虑

### 未来可能的支持

- [ ] 多语言支持（i18n）
- [ ] 更多输出格式（PDF、Word等）
- [ ] 插件系统
- [ ] 可视化编辑器
- [ ] 协作编辑

### 设计预留

- 切片元数据预留扩展字段
- 模板系统支持自定义模板
- 构建脚本模块化，易于添加新生成器
