---
name: steering-runner
description: 仅在用户明确要求检查进化建议、分析重复错误，或在 `release-retro` 固定节点明确需要从 `runtime/errors/`、`runtime/logs/`、`runtime/reviews/` 生成 `runtime/evolution/` proposal 时使用。只提议，不自动毕业。
---

# steering-runner

## 作用

- 负责扫描正式 incident 记录，生成进化 proposal
- 负责在 proposal 已确认且验证通过后沉淀 lesson / strategy
- 不替代 `correction-recorder`、`release-builder` 或 owner 文档

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/release-retro.md`
- `docs/protocols/steering-lite.md`
- `runtime/evolution/README.md`
- `.agents/skills/steering-runner/templates/evolution-proposal-template.md`
- `.agents/skills/steering-runner/templates/evolution-memory-template.md`
- `.agents/skills/steering-runner/references/strategy-map.md`

按需读取：

- `runtime/errors/`
- `runtime/logs/`
- `runtime/reviews/`
- 现有 `runtime/evolution/proposals/`
- 现有 `runtime/evolution/archive/`
- 现有 `runtime/evolution/memory/`
- `.agents/skills/steering-runner/scripts/run-steering-scan.py`

## 硬规则

- 只允许手动触发，或在 `release-retro` 固定节点触发
- 先跑确定性扫描，再决定是否形成 proposal
- proposal 只允许写一个 `target_owner`
- 未经用户确认，不得自动毕业到 owner 文档
- lesson / strategy 只有在 proposal 已确认且验证通过后才允许写入 `runtime/evolution/memory/`
- 没有足够证据时必须安静返回“暂无 proposal”

## 输出

- 新 proposal，或“暂无 proposal”
- 已确认 proposal 的归档结果
- 已确认且通过验证的 lesson / strategy

## 正式落点

- 新提议：`runtime/evolution/proposals/`
- 终态提议：`runtime/evolution/archive/`
- 已确认记忆：`runtime/evolution/memory/lessons/`、`runtime/evolution/memory/strategies/`

## 退出条件

- 已输出 proposal 或明确无提议
- 已归档本轮已处理 proposal
- 命中条件时，已补齐 lesson / strategy
