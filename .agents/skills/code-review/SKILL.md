---
name: code-review
description: 当当前改动需要正式结构化审查，尤其是在 fix 回环之后或发布之前，并且结论必须明确为 `Accept / Hold / Reject` 时使用。
---

# code-review

## 作用

- 负责正式结构化审查
- 只输出 review 结论，不实施代码改动

## 输入

必读：

- 当前任务要求
- 当前改动范围或实现结果
- 当前验证证据
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/build-verify-review.md`
- `runtime/code_review.md`
- `.agents/skills/code-review/templates/review-template.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/*.md`
- `runtime/reviews/`
- 当前任务相关 `runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 当前任务相关实现、测试入口和验证结果

## 硬规则

- 先对照当前目标、范围、非目标和计划对象检查是否做对
- 再对照验证证据判断是否做实
- 识别剩余风险和命中的共享 gate
- 固定输出顺序：`Findings`、`Risks not fully verified`、`Evidence checked`、`Final recommendation`
- `Final recommendation` 只允许 `Accept`、`Hold`、`Reject`
- 没有足够证据时，不给 `Accept`

## 输出

- 结构化 review 结论
- 明确 findings
- 未充分验证风险
- 已检查证据
- 下一步去向：`dev-builder`、`bug-fixer`、`dev-planner`、`release-builder` 或其他 `Gate`

## 正式落点

- 当任务属于中改及以上、高风险、正式发布前审查或需要留痕时，按需写入 `runtime/reviews/`
- 默认 review 协议以 `runtime/code_review.md` 为准

## 退出条件

- 已输出结构化结论
- 已明确下一步去向
- 需要正式留痕时，已按需写入 `runtime/reviews/`
