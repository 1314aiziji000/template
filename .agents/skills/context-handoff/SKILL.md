---
name: context-handoff
description: 在 V3 项目里仅在明确处理多窗口承接时使用：用户输入 `下一个窗口` 或 `下一窗口` 需要生成累计承接快照，或新窗口收到承接快照需要先执行承接确认时使用。第一条回复只能是 `明白` 或 `不明白`。
---

# context-handoff

## 作用

- 负责多窗口承接快照与承接确认
- 不替代 `dev-planner`、`dev-builder`、`code-review`、`release-builder`

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/intake.md`
- `.agents/skills/context-handoff/templates/handoff-template.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/`
- 当前任务相关的 `runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 当前会话里已经形成的计划、验证结论、风险说明、上传结果
- 最近一次承接快照

## 硬规则

- 先区分当前是生成承接，还是接收承接
- 生成承接时，内容按累计方式整理，不只总结本窗口
- 生成承接时，固定使用模板骨架，并保持固定开头：`当前承接快照如下，下一窗口可直接继续：`
- 接收承接时，第一条回复只允许是 `明白` 或 `不明白`
- 完成承接确认前，不继续上个窗口任务
- 默认不把承接快照写成 `runtime/logs/`

## 输出

- 生成模式：累计承接快照
- 接收模式：只输出 `明白` 或 `不明白`

## 正式落点

- 第一版默认不写 `runtime/logs/`
- 只有其他 skill 明确要求节点留痕时，才由对应 skill 负责写盘

## 退出条件

- 生成模式：已输出可直接续做的累计承接快照
- 接收模式：已只用 `明白` 或 `不明白` 完成确认，并等待用户下一条消息
