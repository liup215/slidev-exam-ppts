# Cline 并行开发技能

## 概述

使用 Git Worktree + Cline CLI 实现真正的并行开发。多个功能同时在独立的 worktree 中开发，互不干扰，最后合并到主分支。

## 核心概念

### 什么是 Git Worktree？

Git Worktree 允许你在同一个仓库中同时检出多个分支到不同的目录：

```
原始仓库 (main)
├── .git/                    # 共享的 Git 历史
├── src/                     # main 分支代码
└── ...

Worktree A (feature-a)
├── src/                     # feature-a 分支代码
└── ...

Worktree B (feature-b)
├── src/                     # feature-b 分支代码
└── ...
```

### 为什么需要并行开发？

- **效率提升**: 多个功能同时开发，无需等待
- **隔离安全**: 每个功能独立分支，不会互相影响
- **灵活测试**: 可以同时测试不同方案
- **快速迭代**: 并行尝试多种实现，选择最佳方案

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    并行开发流程                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 创建 Worktrees                                      │
│     ├── git worktree add ../project-feature-a -b feature/a
│     └── git worktree add ../project-feature-b -b feature/b
│                                                         │
│  2. 并行启动 Cline 开发                                  │
│     ├── cd ../project-feature-a                         │
│     │   cline -y "开发功能A" &                          │
│     ├── cd ../project-feature-b                         │
│     │   cline -y "开发功能B" &                          │
│     └── wait                                            │
│                                                         │
│  3. 自动 Code Review                                     │
│     ├── cline -y "Review 功能A" &                       │
│     └── cline -y "Review 功能B" &                       │
│                                                         │
│  4. 合并到主分支                                         │
│     ├── git checkout main                               │
│     ├── git merge feature/a                             │
│     └── git merge feature/b                             │
│                                                         │
│  5. 清理 Worktrees                                       │
│     ├── git worktree remove ../project-feature-a        │
│     └── git worktree remove ../project-feature-b        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 创建 Worktrees

```bash
cd ~/workspace/projects/my-project

# 创建 feature-a worktree
git worktree add ../my-project-feature-a -b feature/a

# 创建 feature-b worktree
git worktree add ../my-project-feature-b -b feature/b

# 查看所有 worktree
git worktree list
```

### 2. 并行启动 Cline 开发

```bash
# 在 worktree-a 中启动 Cline
cd ~/workspace/projects/my-project-feature-a
cline -y -m kimi-k2.5 -t 600 "实现功能A" &

# 在 worktree-b 中启动 Cline
cd ~/workspace/projects/my-project-feature-b
cline -y -m kimi-k2.5 -t 600 "实现功能B" &

# 等待所有任务完成
wait
echo "所有开发任务完成！"
```

### 3. 自动 Code Review

```bash
# Review 功能A
cd ~/workspace/projects/my-project-feature-a
cline -y -m kimi-k2.5 -t 300 "Code Review: 检查代码质量" &

# Review 功能B
cd ~/workspace/projects/my-project-feature-b
cline -y -m kimi-k2.5 -t 300 "Code Review: 检查代码质量" &

wait
echo "所有 Review 完成！"
```

### 4. 合并代码

```bash
cd ~/workspace/projects/my-project

# 合并 feature-a
git merge feature/a

# 合并 feature-b
git merge feature/b

# 推送
git push origin main
```

### 5. 清理 Worktrees

```bash
cd ~/workspace/projects/my-project

# 删除 worktree
git worktree remove ../my-project-feature-a
git worktree remove ../my-project-feature-b

# 删除分支（可选）
git branch -d feature/a
git branch -d feature/b
```

## 完整自动化脚本

### parallel-dev.sh

```bash
#!/bin/bash
# Cline 并行开发自动化脚本

set -e

PROJECT_NAME="$1"
TASK_A="$2"
TASK_B="$3"

PROJECT_DIR="$HOME/workspace/projects/$PROJECT_NAME"
WORKTREE_A="$HOME/workspace/projects/${PROJECT_NAME}-feature-a"
WORKTREE_B="$HOME/workspace/projects/${PROJECT_NAME}-feature-b"
LOG_DIR="/tmp/cline-parallel-$(date +%s)"
mkdir -p "$LOG_DIR"

echo "🚀 启动并行开发流程"
echo "项目: $PROJECT_NAME"
echo "任务A: $TASK_A"
echo "任务B: $TASK_B"
echo "---"

# 1. 创建 Worktrees
echo "📁 创建 Worktrees..."
cd "$PROJECT_DIR"
git worktree add "$WORKTREE_A" -b feature/parallel-a 2>/dev/null || true
git worktree add "$WORKTREE_B" -b feature/parallel-b 2>/dev/null || true

# 2. 并行开发
echo "💻 启动并行开发..."
cd "$WORKTREE_A"
nohup cline -y -m kimi-k2.5 -t 600 "$TASK_A" > "$LOG_DIR/feature-a.log" 2>&1 &
PID_A=$!

cd "$WORKTREE_B"
nohup cline -y -m kimi-k2.5 -t 600 "$TASK_B" > "$LOG_DIR/feature-b.log" 2>&1 &
PID_B=$!

echo "Feature A PID: $PID_A"
echo "Feature B PID: $PID_B"

# 3. 等待完成
echo "⏳ 等待开发完成..."
wait $PID_A
wait $PID_B
echo "✅ 开发完成！"

# 4. 自动 Code Review
echo "🔍 启动 Code Review..."
cd "$WORKTREE_A"
nohup cline -y -m kimi-k2.5 -t 300 "Code Review: 检查代码质量" > "$LOG_DIR/review-a.log" 2>&1 &

cd "$WORKTREE_B"
nohup cline -y -m kimi-k2.5 -t 300 "Code Review: 检查代码质量" > "$LOG_DIR/review-b.log" 2>&1 &

wait
echo "✅ Review 完成！"

# 5. 合并代码
echo "🔀 合并代码..."
cd "$PROJECT_DIR"
git merge feature/parallel-a --no-edit
git merge feature/parallel-b --no-edit

# 6. 推送
echo "📤 推送到 GitHub..."
git push origin main

# 7. 清理
echo "🧹 清理 Worktrees..."
git worktree remove "$WORKTREE_A"
git worktree remove "$WORKTREE_B"

echo "🎉 完成！日志: $LOG_DIR"
```

## 使用示例

### 示例 1: 同时开发两个功能

```bash
./parallel-dev.sh \
  "slidev-exam-ppts" \
  "添加暗黑模式支持" \
  "优化移动端适配"
```

### 示例 2: 尝试两种不同方案

```bash
# 方案A: 使用 CSS 变量
git worktree add ../project-css -b feature/css-theme
cline -c ../project-css -y "使用 CSS 变量实现主题切换" &

# 方案B: 使用 CSS-in-JS
git worktree add ../project-js -b feature/js-theme
cline -c ../project-js -y "使用 CSS-in-JS 实现主题切换" &

wait
# 比较两种方案，选择更好的
```

### 示例 3: 批量修复 Bug

```bash
# Bug 1
git worktree add ../project-bug1 -b fix/bug-1
cline -c ../project-bug1 -y "修复登录问题" &

# Bug 2
git worktree add ../project-bug2 -b fix/bug-2
cline -c ../project-bug2 -y "修复数据显示问题" &

# Bug 3
git worktree add ../project-bug3 -b fix/bug-3
cline -c ../project-bug3 -y "修复表单验证问题" &

wait
# 合并所有修复
```

## 最佳实践

### DO ✅

- **使用 `-y` (YOLO) 模式** - 避免阻塞
- **使用 `&` 后台运行** - 实现真正的并行
- **使用 `wait` 等待完成** - 确保任务完成
- **创建描述性的分支名** - 便于识别
- **及时清理 worktree** - 避免磁盘浪费

### DON'T ❌

- **不要修改同一文件** - 会导致合并冲突
- **不要共享依赖** - 每个 worktree 独立
- **不要阻塞主线程** - 使用后台运行
- **不要忘记清理** - 定期删除无用 worktree

## 故障排除

### Worktree 已存在

```bash
# 删除已存在的 worktree
git worktree remove ../my-project-feature-a
rm -rf ../my-project-feature-a
```

### 合并冲突

```bash
# 手动解决冲突
cd ~/workspace/projects/my-project
git merge feature/a
# 解决冲突...
git add .
git commit -m "merge: resolve conflicts"
```

### Cline 任务失败

```bash
# 查看日志
tail -50 /tmp/cline-parallel-*/feature-a.log
```

## 测试验证

本技能已通过测试验证：

✅ **测试时间**: 2026-03-15  
✅ **测试项目**: slidev-exam-ppts  
✅ **并行任务**: 2 个 Cline 实例  
✅ **测试结果**: 成功  
✅ **修改验证**: Feature A 和 Feature B 同时修改不同文件  

## 相关资源

- [Cline Worktree 文档](https://docs.cline.com/worktrees)
- [Git Worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [Cline CLI 文档](https://docs.cline.com/cli)

## 更新记录

- **2026-03-15**: 初始版本，完成测试验证
