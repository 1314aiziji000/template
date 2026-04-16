# 04-v3-truth-source-reaudit

## 复核范围

- 父级：`templates/V-项目级模板/V3真相源.md`
- 对照基准：
  - `templates/V-项目级模板/V3/README.md`
  - `templates/V-项目级模板/V3/AGENTS.md`
  - `templates/V-项目级模板/V3/PROJECT_RULES.md`
  - `templates/V-项目级模板/V3/docs/workflows/intake.md`
  - `templates/V-项目级模板/V3/docs/protocols/README.md`
  - `templates/V-项目级模板/V3/runtime/logs/README.md`

## 修订前确认到的问题

- 仍把根级入口、workflow、skill 讲成了三份重叠规则
- 没明确说明：
  - `AGENTS.md` 只保留仓库级常驻规则
  - skill `description` 负责路由契约
  - `docs/workflows/` 只保留阶段骨架
  - `docs/protocols/` 只保留共享 gate
- 旧版解析仍把重点放在 skill 数量和完整流程复述，而不是当前的规则分层
- `runtime/logs/` 的新口径虽已补齐，但没有放进新的六层分工里解释

## 本轮已同步的内容

- 父级解析改成当前六层分工：
  - 根级总览层
  - 根级主规则层
  - 目录职责层
  - 路由与执行层
  - 披露层
  - 正式结果层
- 明确根级主规则已经短化，不再承担完整路由表
- 明确 skills 的 frontmatter `description` 已承担路由契约
- 明确 `docs/workflows/intake.md` 现在是人看入口概览，不是唯一正式路由契约
- 明确共享 gate 已收口到 `docs/protocols/`
- `runtime/logs/` 继续按 skill 驱动日志落点解释，并保留上传批次语义

## 一致性结论

- 父级 `V3真相源.md` 已和当前 `V3/README.md`、`AGENTS.md`、`PROJECT_RULES.md`、`docs/workflows/intake.md`、`docs/protocols/README.md` 的分层口径对齐
- 以“主规则短化、路由契约归 skill description、workflow 只讲骨架、protocol 只讲共享 gate”这四条核心判断复核时，父级解析已不再与本体打架
- 当前未发现新的反向约束问题；仍保持“父级解析不反向约束 `V3/` 本体”的边界
