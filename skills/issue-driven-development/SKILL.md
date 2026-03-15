---
name: issue-driven-development
description: "DEPRECATED: This skill is no longer used for development workflow. Development now follows direct-demand-driven approach using Cline CLI. Keep for reference only."
---

# Issue Driven Development (DEPRECATED)

## ⚠️ 重要提示

**此技能已弃用！**

开发工作流程已更新为**直接需求驱动开发**，不再使用 GitHub issue 来跟踪开发任务。

## 新的开发流程

参见 `MEMORY.md` 中的「功能开发流程（直接需求驱动）」部分。

### 快速参考

```bash
# 1. 克隆项目
cd ~/workspace/projects
git clone https://github.com/liup215/<repo>.git

# 2. 启动 Cline 开发
cd <repo>
cline task "需求描述" --yolo -t 600 -m kimi-k2.5

# 3. 提交并推送
git add -A
git commit -m "feat: xxx"
git push origin main
```

## 何时仍使用 Issue

GitHub issue 仅用于：
- Bug 报告
- 功能建议（非开发任务）
- 项目讨论
- 外部用户反馈

**不用于**开发任务跟踪。

---

## 旧文档（仅供参考）

<details>
<summary>点击查看旧版 issue-driven-development 文档</summary>

### Core Workflow (OLD)

#### Step 1: Create Issue
Create well-structured GitHub issues with appropriate metadata, labels, and descriptions.

#### Step 2: Monitor New Issues
Set up monitoring to track newly created issues across repositories.

#### Step 3: Assign @copilot
Assign issues to AI copilots or team members for execution.

### GitHub CLI Commands

```bash
# Creating Issues
gh issue create --repo owner/repo --title "Title" --body "Description"

# Monitoring Issues
gh issue list --repo owner/repo --limit 10 --state open

# Assignment
gh issue edit <number> --repo owner/repo --add-assignee "@copilot"
```

</details>
