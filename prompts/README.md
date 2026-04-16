# prompts

## 作用

- 本目录放 Prompt 物料
- `prompts/README.md` 是混合文档：只做启用条件、边界和联动说明
- 目录仅在当前存在或已启用时纳入联动

## 启用条件

- 项目存在系统 Prompt、角色 Prompt、工具调用 Prompt 或输出约束 Prompt
- Prompt 变更需要进入 `AI Eval Gate`

## 边界

- Prompt 物料属于正式对象，不长期悬空在 `workspaces/`
- Prompt 变更后，要同步更新 `evals/` 与相关模型配置说明
- 具体评测要求回到 `evals/` 与 `docs/protocols/ai-eval-gate.md`

## 联动

- 改 Prompt 时，检查 `evals/`、相关 `schemas/`、`scripts/run-evals.sh` 和命中的 skill 是否要同步
