---
name: project-bootstrap
description: 仅在仓库仍保留根级 `项目说明书.md`，且用户输入“开始”或明确要求初始化刚复制出来的 V3 项目副本时使用。它是一次性 skill；初始化完成后，必须删除 `项目说明书.md` 与本 skill。
---

# project-bootstrap

## 作用

- 负责首次接入 `V3` 的一次性初始化
- 只在模板源态使用；初始化完成后必须从项目副本删除

## 输入

必读：

- 当前任务要求
- `项目说明书.md`
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/bootstrap.md`
- `.agents/skills/project-bootstrap/templates/bootstrap-checklist.md`

按需读取：

- `docs/integrations/`
- `docs/ui/`
- `schemas/`
- `prompts/`
- `evals/`
- 现有 `runtime/PLANS.md`

## 硬规则

- 先判断当前是否真的是新项目首次接入模板
- 先读取并校验 `项目说明书.md`，再判断初始化模式与启用 Packs
- 用户确认前，不裁剪目录，不删除一次性资产
- 先完成根级入口与目录适配，再写回 `runtime/PLANS.md`
- 必须先写好 `runtime/PLANS.md`，再删除 `项目说明书.md`
- 必须先完成所有根级入口适配，再删除 `.agents/skills/project-bootstrap/`
- 删除后不保留平行 bootstrap 说明源

## 输出

- 当前初始化模式结论
- 已启用 Packs 清单
- 根级入口适配结论
- `runtime/PLANS.md` 初始化结论
- 一次性资产删除结果
- 下一步去向：`dev-planner`、`dev-builder` 或首个正式任务

## 正式落点

- 初始化结论写入 `runtime/PLANS.md`

## 退出条件

- 用户已确认初始化方案
- 未启用目录已按确认结果裁剪
- `runtime/PLANS.md` 已写入初始化结论
- `项目说明书.md` 已删除
- `.agents/skills/project-bootstrap/` 已从项目副本删除
- 项目已回到标准主链
