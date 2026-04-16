---
name: user-dialogue-analyst
description: 仅在用户明确要求提取自我记忆、生成提问改进报告，或在启用 `me/self-memory/` 后于上传前明确命中阈值门控节点时使用。原始对话只接受 `workspaces/self-memory-staging/raw/` 下的本地 `.md` / `.txt` 投递。
---

# user-dialogue-analyst

## 作用

- 负责把本地 raw 提取为维护者可读的 `self-memory`
- 负责按月滚动 batch，并生成 `micro / periodic` 报告
- 不替代 AI 侧进化系统，也不把 `self-memory` 自动写回正式真相源

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `me/README.md`
- `me/self-memory/README.md`
- `workspaces/self-memory-staging/README.md`
- `.agents/skills/user-dialogue-analyst/templates/extract-template.md`
- `.agents/skills/user-dialogue-analyst/templates/batch-template.md`
- `.agents/skills/user-dialogue-analyst/templates/report-template.md`
- `.agents/skills/user-dialogue-analyst/references/analysis-rubric.md`

按需读取：

- `workspaces/self-memory-staging/raw/`
- `workspaces/self-memory-staging/manifests/`
- `me/self-memory/extracts/`
- `me/self-memory/batches/`
- `me/self-memory/reports/`
- `me/self-memory/profile/`
- `.agents/skills/user-dialogue-analyst/scripts/*.py`

## 硬规则

- raw 只接受本地 `.md` / `.txt` 投递
- 一份 raw 只允许对应一份 extract
- batch 固定按月滚动
- `micro report` 门槛固定为 `>= 400` 有效字或 `>= 4` 个有效任务轮次
- `periodic report` 门槛固定为 `>= 1200` 有效字或 `>= 10` 个有效任务轮次
- 生成报告并完成核对后，raw 应在 `72` 小时内 purge
- `self-memory` 只给维护者使用，不自动进入 AI 侧默认真相源

## 输出

- 单个 raw 的 extract
- 月批次 batch
- `micro` 或 `periodic` 报告
- 覆盖率与 purge 回执

## 正式落点

- 长期保留：`me/self-memory/extracts/`、`me/self-memory/batches/`、`me/self-memory/reports/`、`me/self-memory/profile/`
- 本地 staging：`workspaces/self-memory-staging/manifests/`

## 退出条件

- 本轮 raw 已提取或明确跳过
- 命中阈值时，已生成对应报告
- 命中 purge 条件时，已更新 manifest 并删除 raw
