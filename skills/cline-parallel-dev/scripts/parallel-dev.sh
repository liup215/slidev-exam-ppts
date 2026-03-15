#!/bin/bash
# Cline 并行开发自动化脚本
# Usage: ./parallel-dev.sh <project-name> "task-a-description" "task-b-description"

set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <project-name> \"task-a-description\" \"task-b-description\""
    echo "Example: $0 slidev-exam-ppts \"添加暗黑模式\" \"优化移动端\""
    exit 1
fi

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
echo "日志: $LOG_DIR"
echo "---"

# 检查项目目录
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 项目目录不存在: $PROJECT_DIR"
    exit 1
fi

# 1. 创建 Worktrees
echo "📁 创建 Worktrees..."
cd "$PROJECT_DIR"

# 删除已存在的 worktree（如果有）
git worktree remove "$WORKTREE_A" 2>/dev/null || true
rm -rf "$WORKTREE_A"
git worktree remove "$WORKTREE_B" 2>/dev/null || true
rm -rf "$WORKTREE_B"

# 创建新的 worktree
git worktree add "$WORKTREE_A" -b feature/parallel-a
git worktree add "$WORKTREE_B" -b feature/parallel-b

echo "✅ Worktrees 创建完成"

# 2. 并行开发
echo "💻 启动并行开发..."

cd "$WORKTREE_A"
nohup cline -y -m kimi-k2.5 -t 600 "$TASK_A" > "$LOG_DIR/feature-a.log" 2>&1 &
PID_A=$!
echo "Feature A 启动，PID: $PID_A"

cd "$WORKTREE_B"
nohup cline -y -m kimi-k2.5 -t 600 "$TASK_B" > "$LOG_DIR/feature-b.log" 2>&1 &
PID_B=$!
echo "Feature B 启动，PID: $PID_B"

# 3. 等待完成
echo "⏳ 等待开发完成..."
wait $PID_A
echo "✅ Feature A 完成"
wait $PID_B
echo "✅ Feature B 完成"

# 4. 自动 Code Review
echo "🔍 启动 Code Review..."

cd "$WORKTREE_A"
nohup cline -y -m kimi-k2.5 -t 300 "Code Review: 检查刚才的代码修改，确保质量良好" > "$LOG_DIR/review-a.log" 2>&1 &
REVIEW_A=$!

cd "$WORKTREE_B"
nohup cline -y -m kimi-k2.5 -t 300 "Code Review: 检查刚才的代码修改，确保质量良好" > "$LOG_DIR/review-b.log" 2>&1 &
REVIEW_B=$!

wait $REVIEW_A
echo "✅ Review A 完成"
wait $REVIEW_B
echo "✅ Review B 完成"

# 5. 合并代码
echo "🔀 合并代码到主分支..."
cd "$PROJECT_DIR"

# 确保在 main 分支
git checkout main

# 合并
git merge feature/parallel-a --no-edit || {
    echo "⚠️ Feature A 合并可能有冲突，请手动处理"
}

git merge feature/parallel-b --no-edit || {
    echo "⚠️ Feature B 合并可能有冲突，请手动处理"
}

# 6. 推送
echo "📤 推送到 GitHub..."
git push origin main || {
    echo "⚠️ 推送失败，请检查网络或权限"
}

# 7. 清理
echo "🧹 清理 Worktrees..."
git worktree remove "$WORKTREE_A"
git worktree remove "$WORKTREE_B"

echo ""
echo "🎉 完成！"
echo "日志目录: $LOG_DIR"
echo ""
echo "查看日志:"
echo "  tail -50 $LOG_DIR/feature-a.log"
echo "  tail -50 $LOG_DIR/feature-b.log"
