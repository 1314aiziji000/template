---
name: dev-builder
description: 当当前任务边界或计划已经明确，需要受控实施改动、补最小验证证据，并把结果送入 review、release 或下一道 gate 时使用。
---

# dev-builder

## 作用

- 负责在既定边界内实施改动并补最小验证证据
- 不负责重写计划、给最终 review 结论或替代发布收口

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/build-verify-review.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/*.md`
- `runtime/code_review.md`
- 当前任务相关 `runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 当前任务相关实现、测试入口和已有验证结果
- 命中时再读 `docs/protocols/`、`docs/integrations/`、`docs/ui/`

## 硬规则

- 先确认当前实施边界、主文件和从文件
- 边界未清时，先回 `dev-planner`
- 在既定范围内完成最小必要改动
- 补最小验证、功能验证和必要回归验证
- 明确未验证项、剩余风险和下一步去向
- 命中门禁时显式抬级，不在 builder 内口头带过

## 输出

- 当前实施范围
- 实际改动结果
- 已执行的验证命令与结果
- 未验证项与剩余风险
- 下一步去向：`code-review`、`release-builder`、`bug-fixer` 或回 `dev-planner`

## 正式落点

- 默认不新建正式记录对象
- 如果当前任务已绑定正式计划对象，可按需同步 `runtime/PLANS.md` 或 `runtime/plans/active/*.md` 的阶段状态与下一步

## 退出条件

- 当前改动已实现或已明确阻塞
- 验证证据真实可复查
- 已说明未验证项和剩余风险
- 已明确交回哪个 skill 或哪个 `Gate`
