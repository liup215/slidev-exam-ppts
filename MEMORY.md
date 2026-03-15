# 工作方法论

## ⚠️ 必须遵守的操作规范（重要！）

### 1. 经验库优先原则
**执行任何操作前，必须先查阅 `memory/lessons/` 中的相关经验文件！**

- **Docker 相关** → 读取 `memory/lessons/docker/`
- **SearXNG 相关** → 读取 `memory/lessons/searxng/`
- **飞书相关** → 读取 `memory/lessons/feishu/operations-guide.md`
- **文件组织** → 读取 `memory/lessons/file-organization/`
- **工作流程** → 读取 `memory/lessons/workflow/`

**此步骤不可跳过！** 经验库中记录了经过验证的最佳实践和常见陷阱。

### 2. 飞书工具使用规范
**必须使用 `workspace/skills/` 下的飞书技能，禁止使用内置工具！**

- ✅ **正确**: 使用 `skills/feishu/` 或 `skills/feishu_sdk/`
- ❌ **错误**: 使用 `openclaw tool feishu_drive` 或内置 feishu 工具

**原因**: workspace 下的技能是专门为你的环境定制的，包含正确的错误处理和参数格式。

## 工具搜索
- 当用户要求搜索相关工具时，默认使用`find-skills`技能进行搜索

## Cline CLI 编程能力
- **安装状态**: 已安装 (v2.7.0)
- **技能文件**: `skills/cline/SKILL.md`
- **使用场景**: 本地代码开发、代码重构、调试、分析
- **重要限制**: 必须使用非交互模式 (`--yolo`, `--json` 等)
- **工作方式**: 对于耗时较长的编程任务，使用 sub-agent 异步执行

## 代码项目存放规范
- **统一目录**: 所有代码项目必须存放在 `~/workspace/projects/` 目录下
- **禁止位置**: 不得在 workspace 根目录或其他位置直接创建项目文件夹
- **目录结构**:
  ```
  workspace/
  ├── projects/          # 所有代码项目
  │   ├── project-a/
  │   ├── project-b/
  │   └── ...
  ├── skills/            # 技能文件
  ├── memory/            # 经验记录
  └── ...
  ```
- **原因**: 避免项目增多导致 workspace 根目录混乱，保持环境整洁

## 飞书操作规范（已整合到上方必须遵守的规范中）
- ~~每次使用飞书相关操作前，必须先读取 `/home/admin/.openclaw/workspace/feishu-operations-guide.md`~~
- **更新**: 统一遵循"经验库优先原则"，飞书操作前读取 `memory/lessons/feishu/operations-guide.md`
- **关键**: 使用 `workspace/skills/feishu/` 下的技能，禁止使用内置工具
- **交流约定：当用户说"发给我"时，必须将内容发送到用户的飞书**

## 正式文档处理技能
- **触发条件**：当用户提到"创建文档"、"创建学校文档"、"创建PDF文档"或需要正式格式化输出时
- **使用技能**：formal-document-processor
- **适用范围**：正式的、格式化的、输出为PDF的文档（如考试试卷、正式报告等）
- **不适用范围**：代码编写、简单记录等非正式文档
- **当前模板**：exam模板（位于~/.local/share/typst/packages/depu/exam/1.0.0/）
- **引用方式**：#import "@depu/exam:1.0.0": *

## 教育数据管理原则
- **所有教育相关功能必须使用edu-cli完成**
- **本地不存储任何教育相关信息**（学生数据、班级信息、教学材料等）
- 所有教育操作通过LTEdu backend API进行
- 本地workspace仅包含配置文件、脚本和非敏感操作文件

## 个人线上教育项目
- **网站地址**: https://www.alevel.icu/
- **源码仓库**: liup215/ltedu
- **工作流程**: 当用户提到"为我的网站***"时，直接使用 Cline 在本地开发，完成后推送代码到 liup215/ltedu 仓库
- **开发流程**: 克隆仓库 → Cline 开发 → 提交代码 → 推送 GitHub

## 经验库（操作前必读）

> ⚠️ **重要提醒**: 根据"经验库优先原则"，执行任何操作前必须先查阅相关主题的经验文件！

经验按主题分类存放于 `memory/lessons/`，操作前查阅相关主题：

| 主题 | 路径 | 内容 |
|------|------|------|
| Docker | `memory/lessons/docker/` | 端口映射、容器管理 |
| SearXNG | `memory/lessons/searxng/` | 配置、部署 |
| 飞书 | `memory/lessons/feishu/` | API操作、消息发送、日历 |
| 文件组织 | `memory/lessons/file-organization/` | 一致性、目录结构 |
| 通用原则 | `memory/lessons/general/` | 避免重复、第一性原理 |
| 工作流程 | `memory/lessons/workflow/` | 创建前检查、决策流程 |

**关键原则**：
1. **操作前必读**: 执行任何操作前，先查阅相关主题经验
2. **避免重复**: 不要重复造轮子，复用已验证的方案
3. **飞书专用**: 飞书操作必须使用 `workspace/skills/` 下的技能

## 经验总结
- 每次经过多次尝试后成功的任务，都要分析失败和成功的经验，记住成功的方法以提高成功率
- **经验记录位置**：`memory/lessons/<主题>/`（按主题分类，不按日期）

## 第一性原理
- 记录时考虑第一性原理，避免记录过多细节，专注于核心原则

## 思维创新
- 在思考问题的方式上保持灵活性，防止墨守成规，要善于变通

## 安全原则
- **自主安装与快速迭代**：在明确任务上下文中，可自动安装经验证的安全依赖（PyPI/Conda官方源、GitHub官方仓库），记录操作日志，并提供一键回滚选项
- **结果导向**：优先交付可用结果而非过程说明；若方案无效则立即清理并尝试替代方法，直至成功
- **无密钥优先**：优先使用无需API key的本地工具或开源方案；仅在必要时请求权限
- 教育数据安全优先：绝不本地存储敏感教育信息

## 工作流程原则
- **技能文件优先**：在执行任何任务前，必须仔细阅读相关的技能文件（SKILL.md）中的具体代码示例和操作指南
- **严格遵循示例**：直接使用技能文档中提供的标准命令格式，避免自行推测或修改参数格式
- **验证后再执行**：对于关键操作，先确认技能文档中的最佳实践，再执行具体命令
- **用户模板优先**：当用户 has their own template or files, NEVER create content myself. Always wait for the user to provide their actual files before proceeding with setup or modification.

## 新项目创建标准化流程
1. **需求讨论**: 明确项目目标、范围、技术栈
2. **GitHub仓库创建**: 使用 `gh repo create` 直接在GitHub创建私有仓库
3. **初始化commit**: 立即进行初始化commit（包含README.md），确保仓库有main分支
4. **监控配置**: 自动将新仓库添加到统一监控列表 (`monitored_repos.txt`)
5. **本地开发**: 使用 Cline CLI 在 workspace 进行代码开发
6. **代码提交**: 开发完成后提交代码并推送到 GitHub

**重要区分**:
- **GitHub私有仓库**: 用于项目开发（工具、系统、应用等）
- **edu-cli**: 用于所有教育数据操作（学生、班级、课程、学习计划等）
- **Cline CLI**: 用于本地代码开发和编程任务

## 功能开发流程（直接需求驱动）

### 流程概述
**需求 → Cline 开发 → 提交代码 → 推送 GitHub**

不再创建 GitHub issue，直接将需求提交给 Cline 进行开发。

### 具体步骤

1. **明确需求**
   - 用户描述需要开发的功能
   - 确认项目仓库和目录位置

2. **克隆项目（如需要）**
   ```bash
   cd ~/workspace/projects
   git clone https://github.com/liup215/<repo>.git
   ```

3. **启动 Cline 开发**
   ```bash
   cd ~/workspace/projects/<repo>
   cline task "需求描述" --yolo -t 600 -m kimi-k2.5
   ```

4. **等待开发完成**
   - 使用 `process poll` 监控进度
   - 检查 Cline 日志确认状态

5. **提交并推送代码**
   ```bash
   git add -A
   git commit -m "feat: xxx"
   git push origin main
   ```

### Cline 使用规范

**推荐模型**: `kimi-k2.5`（表现稳定，适合复杂开发任务）

**命令模板**:
```bash
cline task "详细需求描述" \
  --yolo \
  -t 600 \
  -m kimi-k2.5 \
  -c ~/workspace/projects/<project-name>
```

**参数说明**:
- `--yolo`: 自动批准所有操作
- `-t 600`: 设置 600 秒超时
- `-m kimi-k2.5`: 使用 Kimi K2.5 模型
- `-c`: 指定工作目录

### 注意事项

- **不再创建 GitHub issue** 来跟踪开发任务
- **直接使用 Cline** 进行本地开发
- **开发完成后** 手动提交并推送代码
- **Issue 仅用于** Bug 报告、功能建议（非开发任务）

## A-Level Biology 9700 Exam Schedule (2026)

- **Paper 1 (P1)**: Thursday, June 4, 2026
- **Paper 2 (P2)**: Wednesday, May 13, 2026  
- **Paper 3 (P3)**: Tuesday, May 26, 2026
- **Paper 4 (P4)**: Friday, May 8, 2026
- **Paper 5 (P5)**: Wednesday, May 13, 2026

> ⚠️ Note: P2 and P5 are scheduled on the same day.

最后更新: 2026-03-12