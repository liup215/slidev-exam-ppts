# Project Brief: slidev-exam-ppts

## 项目概述

**项目名称**: slidev-exam-ppts  
**项目目标**: 基于内容切片的考试幻灯片和笔记双输出系统  
**创建时间**: 2026-03-15  
**仓库**: https://github.com/liup215/slidev-exam-ppts

## 核心目标

构建一个能够从原始教材内容自动生成两种学习材料的系统：
1. **Slidev 幻灯片** - 用于课堂演示和教学
2. **VitePress 笔记** - 用于课后复习和自主学习

## 核心功能

| 功能模块 | 描述 |
|---------|------|
| 内容切片系统 | 将原始教材内容切分为结构化的知识单元 |
| PPT 生成 | 从切片内容生成 Slidev 格式的演示幻灯片 |
| 笔记生成 | 从切片内容生成 VitePress 格式的学习笔记 |
| 双输出构建 | 统一的构建流程同时生成两种输出 |
| 自动部署 | GitHub Actions 自动部署到 GitHub Pages |

## 目标用户

- **学生**: A-Level Biology 考生，需要高质量的学习材料
- **教师**: 需要制作教学演示和配套学习资料的教育工作者

## 支持的考纲

- CIE Biology 9700 (AS & A Level)
- AQA Biology 7402
- 生物竞赛相关教材 (如 Molecular Biology of the Cell)

## 关键成功指标

1. 内容保留率：原始教材的关键信息完整保留
2. 生成效率：自动化流程减少人工干预
3. 输出质量：幻灯片和笔记均达到可直接使用的标准
4. 可维护性：内容更新时能够快速同步到双输出

## 相关文档

- [Product Context](./productContext.md) - 产品背景和解决方案
- [Active Context](./activeContext.md) - 当前工作状态
- [System Patterns](./systemPatterns.md) - 系统架构设计
- [Tech Context](./techContext.md) - 技术环境详情
- [Progress](./progress.md) - 项目进度跟踪
