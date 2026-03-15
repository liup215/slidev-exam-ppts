# Build Rules - slidev-exam-ppts

> 构建流程规则：从切片到双输出的完整流程

## 目录

- [构建顺序](#构建顺序)
- [依赖关系](#依赖关系)
- [缓存策略](#缓存策略)
- [错误处理](#错误处理)
- [构建脚本](#构建脚本)
- [CI/CD集成](#cicd集成)

---

## 构建顺序

### 三阶段构建流程

```
┌─────────────────────────────────────────────────────────────┐
│                    阶段1：验证（Validate）                    │
├─────────────────────────────────────────────────────────────┤
│  1.1 扫描所有切片文件                                        │
│  1.2 验证Frontmatter格式（YAML语法）                         │
│  1.3 验证必需字段（id, topic, source）                       │
│  1.4 验证ID唯一性                                            │
│  1.5 验证文件命名规范                                        │
│  1.6 验证字符数限制                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    阶段2：解析（Parse）                       │
├─────────────────────────────────────────────────────────────┤
│  2.1 解析Frontmatter元数据                                   │
│  2.2 解析Markdown内容                                        │
│  2.3 提取考点、标签、难度等信息                              │
│  2.4 建立切片之间的关系图谱                                  │
│  2.5 按topic分组切片                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    阶段3：生成（Generate）                    │
├─────────────────────────────────────────────────────────────┤
│  3.1 生成Slidev PPT文件                                      │
│  3.2 生成VitePress笔记文件                                   │
│  3.3 生成导航和索引                                          │
│  3.4 复制静态资源（图片等）                                  │
│  3.5 生成配置文件                                            │
└─────────────────────────────────────────────────────────────┘
```

### 阶段详细说明

#### 阶段1：验证

```javascript
// 验证流程
async function validateStage() {
  const slices = await scanSlices('./slices');
  const errors = [];
  
  for (const slice of slices) {
    // 1.1 验证YAML格式
    if (!validateYAML(slice.content)) {
      errors.push({ file: slice.path, error: 'Invalid YAML' });
      continue;
    }
    
    // 1.2 验证必需字段
    const required = ['id', 'topic', 'source'];
    for (const field of required) {
      if (!slice.frontmatter[field]) {
        errors.push({ file: slice.path, error: `Missing ${field}` });
      }
    }
    
    // 1.3 验证ID格式
    if (!validateIdFormat(slice.frontmatter.id)) {
      errors.push({ file: slice.path, error: 'Invalid ID format' });
    }
    
    // 1.4 验证字符数
    const charCount = slice.content.length;
    if (charCount > 3000) {
      errors.push({ file: slice.path, error: `Content too long (${charCount} chars)` });
    }
  }
  
  // 1.5 验证ID唯一性
  const ids = slices.map(s => s.frontmatter.id);
  const duplicates = findDuplicates(ids);
  if (duplicates.length > 0) {
    errors.push({ error: `Duplicate IDs: ${duplicates.join(', ')}` });
  }
  
  return { valid: errors.length === 0, errors };
}
```

#### 阶段2：解析

```javascript
// 解析流程
async function parseStage(slices) {
  const parsedSlices = [];
  const topicMap = new Map();
  
  for (const slice of slices) {
    const parsed = {
      id: slice.frontmatter.id,
      topic: slice.frontmatter.topic,
      subject: slice.frontmatter.subject || extractSubject(slice.path),
      metadata: slice.frontmatter,
      content: parseMarkdown(slice.content),
      examPoints: slice.frontmatter.exam_points || [],
      relatedSlices: slice.frontmatter.related_slices || [],
      sequence: slice.frontmatter.sequence || 1
    };
    
    parsedSlices.push(parsed);
    
    // 按topic分组
    if (!topicMap.has(parsed.topic)) {
      topicMap.set(parsed.topic, []);
    }
    topicMap.get(parsed.topic).push(parsed);
  }
  
  // 排序每个topic下的切片
  for (const [topic, slices] of topicMap) {
    slices.sort((a, b) => a.sequence - b.sequence);
  }
  
  return { slices: parsedSlices, topicMap };
}
```

#### 阶段3：生成

```javascript
// 生成流程
async function generateStage(parsedData) {
  const { slices, topicMap } = parsedData;
  
  // 3.1 生成Slidev
  for (const [topic, topicSlices] of topicMap) {
    await generateSlidev(topic, topicSlices);
  }
  
  // 3.2 生成VitePress
  for (const [topic, topicSlices] of topicMap) {
    await generateVitePress(topic, topicSlices);
  }
  
  // 3.3 生成导航和索引
  await generateNavigation(topicMap);
  await generateIndexes(topicMap);
  
  // 3.4 复制静态资源
  await copyAssets();
  
  // 3.5 生成配置文件
  await generateConfigs(topicMap);
}
```

---

## 依赖关系

### 文件依赖图

```
slices/*.md
    │
    ├──→ templates/slidev/*.vue ──→ generated/slides/*.md
    │
    ├──→ templates/vitepress/*.md ──→ generated/notes/**/*.md
    │
    └──→ config/*.ts ──→ generated/{slides,notes}/config files

static assets (images)
    │
    ├──→ generated/slides/**/assets/
    └──→ generated/notes/**/assets/
```

### 构建依赖规则

| 源文件 | 依赖 | 输出 |
|--------|------|------|
| `slices/{subject}/*.md` | `templates/slidev/*.vue` | `generated/slides/{subject}/*.md` |
| `slices/{subject}/*.md` | `templates/vitepress/*.md` | `generated/notes/{subject}/**/*.md` |
| `slices/{subject}/assets/*` | - | `generated/{slides,notes}/{subject}/**/assets/*` |
| `config/slidev.config.ts` | `slices/*` | `generated/slides/.vitepress/config.ts` |
| `config/vitepress.config.ts` | `slices/*` | `generated/notes/.vitepress/config.ts` |

### 增量构建依赖

```javascript
// 依赖追踪
const dependencyGraph = {
  // 切片文件 -> 生成的文件
  'slices/biology/cell-001.md': [
    'generated/slides/biology/cell-structure.md',
    'generated/notes/biology/cell-structure/index.md'
  ],
  
  // 模板 -> 所有使用该模板的生成文件
  'templates/slidev/content.vue': [
    'generated/slides/**/*.md'
  ],
  
  // 配置文件 -> 所有生成文件
  'config/slidev.config.ts': [
    'generated/slides/.vitepress/config.ts'
  ]
};
```

---

## 缓存策略

### 缓存层级

```
┌────────────────────────────────────────┐
│           层级1：内存缓存               │
│  - 解析后的切片数据                      │
│  - 模板编译结果                          │
│  - 构建过程中的临时状态                  │
└────────────────────────────────────────┘
            ↓
┌────────────────────────────────────────┐
│           层级2：文件缓存               │
│  - .cache/ 目录                         │
│  - 切片哈希值映射                        │
│  - 上次构建时间戳                        │
└────────────────────────────────────────┘
            ↓
┌────────────────────────────────────────┐
│           层级3：增量检测               │
│  - 文件修改时间比较                      │
│  - 内容哈希比较                          │
│  - 依赖关系追踪                          │
└────────────────────────────────────────┘
```

### 缓存文件结构

```
.cache/
├── slices/
│   ├── biology-cell-001.hash      # 切片内容哈希
│   ├── biology-cell-002.hash
│   └── ...
├── builds/
│   └── last-build.json            # 上次构建信息
└── dependencies/
    └── graph.json                 # 依赖关系图
```

### 增量构建逻辑

```javascript
// 增量构建
async function incrementalBuild() {
  const cache = await loadCache();
  const slices = await scanSlices('./slices');
  
  const toRebuild = [];
  const toSkip = [];
  
  for (const slice of slices) {
    const currentHash = await computeHash(slice.content);
    const cachedHash = cache.get(slice.path);
    
    if (currentHash !== cachedHash) {
      toRebuild.push(slice);
      cache.set(slice.path, currentHash);
    } else {
      toSkip.push(slice);
    }
  }
  
  // 检查依赖变更
  const changedTemplates = await checkTemplateChanges(cache);
  if (changedTemplates.length > 0) {
    // 模板变更，需要重新构建所有相关切片
    for (const slice of toSkip) {
      if (dependsOnTemplates(slice, changedTemplates)) {
        toRebuild.push(slice);
      }
    }
  }
  
  console