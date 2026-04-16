---
name: dev-planner
description: 当任务边界未清、需要判断 `Size + Risk`、工作跨会话或多阶段、风险已抬级，或需要创建 / 更新 `runtime` 计划对象时使用。
---

# dev-planner

## 作用

- 负责当前任务的计划强度判断和计划对象落点
- 不负责直接实施、正式审查或发布收口

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/intake.md`
- `.agents/skills/dev-planner/templates/plans-template.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/`
- `runtime/plans/archive/`
- 当前任务相关的 `runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 当前任务相关实现、验证结果和正式资料
- 当前会话里已经形成的计划内容
- 命中时再读 `docs/protocols/`、`docs/integrations/`、`docs/ui/`

## 硬规则

- 按 `intake` 先判断任务类型与 `Size + Risk`
- 计划强度只允许在下面几类中选择：
- 边界说明：极小或一次性小改，默认不沉淀
- 轻计划：`Small + Low Risk`
- 正式计划：`Medium / Large`、高风险、跨会话、多阶段
- 更新已有计划：已有计划对象且仍应沿用
- 计划必须写清目标、范围、非目标、验收标准、验证路线、风险和下一步
- 已有正式计划优先更新，不并行新开平行计划
- 当前会话计划可以复用，但不自动等于仓库正式真相源

## 输出

- 当前任务类型与 `Size + Risk` 结论
- 当前应走的计划强度
- 结构化计划结果
- 下一步去向：`dev-builder`、`bug-fixer`、`release-builder` 或对应 `Gate`

## 正式落点

- 极小修改或轻计划：默认不写 `runtime/`
- 单一正式计划：写入或更新 `runtime/PLANS.md`
- 多活跃长任务：升级到 `runtime/plans/active/` 与 `runtime/plans/archive/`

## 退出条件

- 当前目标、范围、非目标、验证方式和下一步已明确
- 需要正式承接时，计划对象已写入正确 `runtime/` 位置
- 如果高影响歧义仍未解决，继续读真相源或向用户确认
