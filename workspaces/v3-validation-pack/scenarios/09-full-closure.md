# Scenario: full-closure

## 目标

- 用一条中等规模任务跑完整条日常主链

## 固定步骤

1. `dev-planner`
2. `dev-builder`
3. `code-review` 输出 `Hold`
4. `bug-fixer`
5. `code-review` 输出 `Accept`
6. `release-builder`
7. `git-upload-logger`
8. `context-handoff`

## 验证重点

- 闭环是否真实发生
- review/fix/review 是否形成回环
- `runtime/PLANS.md`、`runtime/releases/`、`runtime/logs/` 是否各归其位
