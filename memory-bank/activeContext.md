# Active Context: slidev-exam-ppts

**最后更新**: 2026-03-15  
**当前会话**: Memory Bank 初始化

## 当前开发重点

### VitePress 整合方案

当前的核心任务是完成 VitePress 与 Slidev 的深度整合，实现：

1. **统一导航**: 从 VitePress 笔记页面直接链接到对应的 Slidev 幻灯片
2. **嵌入预览**: 在笔记中嵌入幻灯片预览或链接
3. **样式一致性**: 保持两种输出在视觉风格上的一致性
4. **构建协调**: 确保构建流程正确处理双输出的依赖关系

## 最近完成的工作

### ✅ 项目结构搭建
- [x] 初始化 Node.js 项目
- [x] 配置 GitHub 仓库
- [x] 设置 GitHub Actions 工作流
- [x] 创建基础目录结构

### ✅ Slidev 幻灯片创建
- [x] CIE Biology 9700 Chapter 1 (Cell Structure)
- [x] CIE Biology 9700 Chapter 2 (Biological Molecules)
- [x] Bio Competition - Molecular Biology Chapter 7 (Control of Gene Expression)

### ✅ VitePress 基础配置
- [x] 安装 VitePress 依赖
- [x] 配置 `docs/.vitepress/config.mts`
- [x] 设置导航栏和侧边栏
- [x] 配置 GitHub Pages 部署

## 下一步计划

### 短期目标 (1-2 周)

1. **内容切片系统**
   - 设计切片数据结构
   - 创建切片导入工具
   - 建立切片存储规范

2. **双输出构建流程**
   - 实现从切片到 Slidev 的转换
   - 实现从切片到 VitePress 的转换
   - 统一构建脚本

3. **VitePress-Slidev 整合**
   - 完成幻灯片嵌入方案
   - 实现双向链接
   - 测试整合效果

### 中期目标 (1 个月)

1. **自动化流程**
   - GitHub Actions 自动构建
   - 内容更新自动触发重新生成
   - 构建状态通知

2. **内容扩展**
   - 添加更多章节内容
   - 支持更多考纲
   - 建立内容模板库

## 活跃决策

### 已确定的决策

| 决策 | 状态 | 说明 |
|-----|------|------|
| 采用内容切片作为统一内容源 | ✅ 已确定 | 所有输出都基于切片，而非直接编辑 |
| 使用 Slidev + VitePress 双输出 | ✅ 已确定 | 幻灯片用于演示，笔记用于复习 |
| GitHub Pages 部署 | ✅ 已确定 | 免费、可靠、与 GitHub 集成 |
| Node.js + npm 技术栈 | ✅ 已确定 | 与 Slidev/VitePress 生态一致 |

### 待决策事项

| 决策 | 选项 | 优先级 |
|-----|------|--------|
| 切片存储格式 | JSON / YAML / Markdown | 高 |
| 内容导入方式 | 飞书 API / 本地文件 / 手动 | 中 |
| 图片资源管理 | 相对路径 / CDN / Base64 | 中 |

## 当前阻塞项

暂无阻塞项。

## 相关文档

- [Progress](./progress.md) - 详细进度跟踪
- [System Patterns](./systemPatterns.md) - 架构决策记录
- [Tech Context](./techContext.md) - 技术细节
