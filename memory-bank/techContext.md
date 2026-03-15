# Tech Context: slidev-exam-ppts

## 技术栈概览

| 层级 | 技术 | 版本 | 用途 |
|-----|------|------|------|
| 运行时 | Node.js | 20.x | JavaScript 运行时 |
| 包管理 | npm | 10.x | 依赖管理 |
| 幻灯片 | Slidev | ^0.49.0 | Markdown 驱动幻灯片 |
| 文档 | VitePress | ^1.6.3 | 静态站点生成 |
| 框架 | Vue | ^3.4.0 | UI 组件 |
| 构建 | Vite | ^5.0.0 | 构建工具 |
| 主题 | @slidev/theme-seriph | ^0.25.0 | Slidev 主题 |

## 核心依赖

### 生产依赖

```json
{
  "@slidev/theme-seriph": "^0.25.0",    // Slidev 幻灯片主题
  "katex": "^0.16.38",                   // 数学公式渲染
  "markdown-it": "^14.1.1",              // Markdown 解析
  "prismjs": "^1.30.0",                  // 代码高亮
  "vue": "^3.4.0",                       // Vue 框架
  "vue-router": "^4.6.4"                 // Vue 路由
}
```

### 开发依赖

```json
{
  "@slidev/cli": "^0.49.0",              // Slidev 命令行工具
  "@types/markdown-it": "^14.1.2",       // TypeScript 类型
  "@vitejs/plugin-vue": "^5.0.0",        // Vite Vue 插件
  "vite": "^5.0.0",                      // 构建工具
  "vite-plugin-static-copy": "^3.3.0",   // 静态资源复制
  "vitepress": "^1.6.3"                  // 文档站点生成
}
```

## 开发环境

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/liup215/slidev-exam-ppts.git
cd slidev-exam-ppts

# 安装依赖
npm install

# 启动 VitePress 开发服务器
npm run dev

# 启动 Slidev 开发服务器 (Chapter 1)
npm run dev:slides

# 构建
npm run build
```

### 开发服务器

| 命令 | 用途 | 端口 |
|-----|------|------|
| `npm run dev` | VitePress 文档 | 5173 |
| `npm run dev:slides` | Slidev 幻灯片 | 3030 |
| `npm run preview` | 预览构建结果 | 4173 |
| `npm run preview:slides` | 预览幻灯片 | 3030 |

## 部署环境

### GitHub Pages

- **类型**: 静态网站托管
- **URL**: `https://liup215.github.io/slidev-exam-ppts/`
- **分支**: `gh-pages` (自动创建)
- **自定义域名**: 暂不支持

### GitHub Actions 工作流

#### deploy.yml

触发条件:
- `push` 到 `main` 分支
- 手动触发 (`workflow_dispatch`)

构建步骤:
1. Checkout 代码
2. 设置 Node.js 20
3. 安装依赖 (`npm ci`)
4. 构建 VitePress (`npx vitepress build docs`)
5. 构建 Slidev 幻灯片到 VitePress dist 目录
6. 上传构建产物
7. 部署到 GitHub Pages

### 构建输出结构

```
docs/.vitepress/dist/
├── index.html                 # 首页
├── cie/                       # CIE 笔记
│   ├── index.html
│   └── as/
│       ├── chapter1.html
│       └── chapter2.html
├── bio-competition/           # 生物竞赛笔记
│   └── ...
└── slides/                    # Slidev 幻灯片
    ├── cie-9700/
    │   ├── index.html
    │   └── chapter-2/
    │       └── index.html
    └── bio-competition/
        └── molecular-biology-of-the-cell/
            └── chapter7/
                └── index.html
```

## 项目配置

### VitePress 配置 (`docs/.vitepress/config.mts`)

```typescript
export default defineConfig({
  title: "A-Level Biology",
  description: "A-Level Biology Study Notes and Slides",
  base: '/slidev-exam-ppts/',  // GitHub Pages 子路径
  
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'CIE', link: '/cie/' },
      { text: 'Bio Competition', link: '/bio-competition/' }
    ],
    sidebar: { /* 侧边栏配置 */ },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/liup215/slidev-exam-ppts' }
    ]
  }
})
```

### Package.json 脚本

```json
{
  "scripts": {
    "dev": "vitepress dev docs",
    "dev:slides": "slidev slides/cie-9700/slides.md",
    "build": "npm run build:vitepress && npm run build:slides",
    "build:vitepress": "vitepress build docs",
    "build:slides": "npm run build:slides:ch1 && npm run build:slides:ch2 && npm run build:slides:molbio-ch7",
    "build:slides:ch1": "npx slidev build slides/cie-9700/slides.md --base /slidev-exam-ppts/slides/cie-9700/ --out docs/.vitepress/dist/slides/cie-9700",
    "preview": "vitepress preview docs",
    "preview:slides": "slidev slides/cie-9700/slides.md"
  }
}
```

## 关键技术细节

### Slidev 构建参数

| 参数 | 说明 | 示例值 |
|-----|------|--------|
| `--base` | 基础路径 | `/slidev-exam-ppts/slides/cie-9700/` |
| `--out` | 输出目录 | `docs/.vitepress/dist/slides/cie-9700` |

### 路径配置要点

- VitePress 基础路径: `/slidev-exam-ppts/`
- Slidev 基础路径: `/slidev-exam-ppts/slides/<path>/`
- 所有资源路径使用相对路径或绝对路径（带 base）

### 数学公式支持

- **引擎**: KaTeX
- **语法**: `$...$` (行内), `$$...$$` (块级)
- **配置**: 在 Slidev 和 VitePress 中分别配置

## 开发工具

### 推荐 IDE 设置

- **VS Code** 扩展:
  - Volar (Vue 3 支持)
  - Markdown All in One
  - Slidev

### 代码规范

- **格式化**: 使用项目默认配置
- **提交规范**: 遵循常规提交格式

## 故障排除

### 常见问题

1. **构建路径错误**
   - 检查 `--base` 参数是否与 GitHub Pages 路径匹配
   - 确保 `vite.config.ts` 中的 base 配置正确

2. **资源加载失败**
   - 确认所有资源使用相对路径
   - 检查 `public/` 目录下的文件是否正确复制

3. **幻灯片样式问题**
   - 确保 `@slidev/theme-seriph` 正确安装
   - 检查自定义 CSS 是否覆盖主题样式

## 相关文档

- [Slidev 文档](https://sli.dev/)
- [VitePress 文档](https://vitepress.dev/)
- [Vue 3 文档](https://vuejs.org/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
