# initialized-mode

## 用途

- 验证初始化完成后的日常主链
- 覆盖 `dev-planner`、`dev-builder`、`bug-fixer`、`code-review`、`release-builder`、`context-handoff`、`git-upload-logger`
- 在固定维护节点补跑 `skill-validator`

## 前提

- 根级不再保留 `项目说明书.md`
- `.agents/skills/project-bootstrap/` 已删除

## 必测

- 正例：当前 7 个日常 / 伴随 skill 全部至少跑 1 次
- 正例：在官方化节点手动跑 1 次 `skill-validator`
- 反例：不该命中的 skill 不能误触发

## 预期产物

- 闭环链路跑通
- `runtime/PLANS.md`、`runtime/releases/`、`runtime/logs/` 边界清楚
- `agents/openai.yaml` 与 `policy.allow_implicit_invocation` 在当前仓态下保持一致
