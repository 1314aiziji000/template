---
name: git-upload-logger
description: 在 V3 项目里仅在当前任务明确涉及 `git add`、`commit`、`push`、同步 Git / GitHub、上传 GitHub，或明确要求记录上传批次时使用；负责把当前上下文、最近承接快照和真实 Git 结果写入 `runtime/logs/YYYY-MM-DD.md`，且不得擅自缩小上传范围。
---

# git-upload-logger

## 作用

- 负责一次 Git / GitHub 上传批次的正式日志
- 不替代 `release-builder`，也不把上传日志伪装成发布记录

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/intake.md`
- `docs/workflows/release-retro.md`
- `runtime/logs/README.md`
- `.agents/skills/git-upload-logger/templates/upload-log-template.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/`
- 当前任务相关的 `runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 最近一次承接快照
- 当前会话里已经形成的改动范围、验证结果、剩余风险
- 实际 Git 状态、commit、push、远端与分支结果

## 硬规则

- 先判断当前请求是不是 Git / GitHub 上传批次
- 合并当前任务要求、最近承接快照和当前会话中的有效上下文
- 以真实 Git 结果补齐上传目标、实际结果和已知边界
- 不得擅自缩小上传范围
- `commit hash`、推送区间和最终上传结果只能来自真实 Git 结果
- 上传失败、部分成功或待确认时，照实写入，不伪造“已完成”
- 一次上传批次只追加到对应日期文件，不覆盖同日已有记录

## 输出

- 当前上传批次日志
- 写入位置说明
- 当前上传结果、剩余风险和下一步

## 正式落点

- 默认写入或追加到 `runtime/logs/YYYY-MM-DD.md`
- 正式发布或交付事实仍由 `release-builder` 写入 `runtime/releases/`

## 退出条件

- 已明确当前上传批次范围
- 已基于真实 Git 结果记录实际结果
- 已写入或准备写入正确的 `runtime/logs/YYYY-MM-DD.md`
- 已说明剩余风险和下一步
