# 直接需求驱动开发流程

## 变更记录

**日期**: 2026-03-15
**变更原因**: 简化开发流程，提高效率
**变更内容**: 从「Issue 驱动开发」改为「直接需求驱动开发」

## 旧流程 vs 新流程

### 旧流程（Issue 驱动）
```
需求 → 创建 Issue → 分配给 Cline → 开发 → 提交代码 → 关闭 Issue
```

### 新流程（直接需求驱动）
```
需求 → Cline 开发 → 提交代码 → 推送 GitHub
```

## 优势

1. **更简洁**: 减少 Issue 创建和管理的步骤
2. **更高效**: 直接开始开发，无需等待 Issue 创建
3. **更灵活**: 适合快速迭代和小型功能开发
4. **减少噪音**: GitHub issue 只用于真正的 Bug 报告和功能建议

## 具体实施

### 1. 项目准备
```bash
cd ~/workspace/projects
git clone https://github.com/liup215/<repo>.git
```

### 2. 启动 Cline 开发
```bash
cd <repo>
cline task "详细需求描述" --yolo -t 600 -m kimi-k2.5
```

**推荐模型**: `kimi-k2.5`
- 表现稳定
- 适合复杂开发任务
- 支持长上下文

### 3. 监控开发进度
```bash
# 查看 Cline 任务状态
process poll <session-id>

# 查看 Cline 日志
tail -f ~/.cline/data/logs/cline-cli.2.log
```

### 4. 提交代码
```bash
git add -A
git commit -m "feat: 描述"
git push origin main
```

## 注意事项

### Cline 使用技巧

1. **使用 --yolo 模式**: 自动批准操作，适合信任的环境
2. **设置足够超时**: `-t 600` (10分钟) 或更长
3. **指定工作目录**: `-c ~/workspace/projects/<repo>`
4. **选择合适模型**: `kimi-k2.5` 适合开发任务

### 常见问题

**Q: Cline 任务失败怎么办？**
A: 检查日志，重试或手动完成剩余工作。

**Q: 如何知道 Cline 完成了？**
A: 查看进程状态或日志中的完成标记。

**Q: 推送代码失败怎么办？**
A: 检查网络连接，使用 gh auth token 认证。

## 经验总结

### 成功案例
- slidev-exam-ppts 笔记功能开发
- 使用 Kimi K2.5 模型
- 开发时间约 20 分钟
- 代码质量良好

### 失败教训
- glm-5 模型不适合复杂开发任务
- 必须使用非交互模式 (`--yolo`)
- 网络不稳定时推送可能失败

## 相关文件

- `MEMORY.md` - 主文档
- `skills/issue-driven-development/SKILL.md` - 已弃用的旧技能
- `skills/cline/SKILL.md` - Cline 使用指南
