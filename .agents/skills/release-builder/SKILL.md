---
name: release-builder
description: 当改动已通过主要验证，需要进入交付、部署或正式发布收口，并补齐 `Release Card`、冒烟检查、回滚路径与正式发布记录时使用。
---

# release-builder

## 作用

- 负责交付、部署或正式发布收口
- 不替代平台型发布控制面

## 输入

必读：

- 当前任务要求
- 当前交付 / 发布目标
- 当前验证证据
- 当前 review 结论或等效正式审查结果
- `docs/workflows/release-retro.md`
- `docs/protocols/release-gate.md`
- `runtime/code_review.md`
- `.agents/skills/release-builder/templates/release-card-template.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/*.md`
- `runtime/releases/`
- `runtime/errors/`
- `runtime/adr/`
- 当前任务相关实现、验证结果、部署说明和交付材料
- `.agents/skills/release-builder/scripts/release-check.sh`
- `docs/protocols/security-lite.md`
- `docs/protocols/ai-eval-gate.md`
- `docs/protocols/adr-lite.md`

## 硬规则

- 先判断当前是不是真正的正式交付路径
- 核对 review、验证证据和剩余风险是否齐备
- 补齐 `Release Card`
- 明确冒烟检查与回滚路径
- review 或证据不足时，不进入正式发布
- 正式沉淀必须写回对应 `runtime/` 对象，不混成口头备注

## 输出

- 当前发布前条件是否满足
- `Release Card`
- 当前冒烟检查
- 当前回滚路径
- 剩余风险
- 下一步去向

## 正式落点

- 正式发布或交付节点：`runtime/releases/`
- 明确错误、返工原因、反复模式：`runtime/errors/`
- 关键结构决策：`runtime/adr/`

## 退出条件

- 已明确当前状态：`可进入交付`、`需先补发布条件`、`需补回滚路径`、`需沉淀正式记录` 或 `阻塞待确认`
- 已明确要不要写入对应 `runtime/` 对象
- 已指向下一步动作或前一环
