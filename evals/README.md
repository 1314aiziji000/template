# evals

## 作用

- 本目录放 AI 行为评测物料
- `evals/README.md` 是混合文档：只做启用条件、边界和联动说明
- 目录仅在当前存在或已启用时纳入联动

## 启用条件

- Prompt 变更
- 模型切换
- RAG 策略变化
- tool routing / output parser / safety policy 变化

## 边界

- 没命中 `AI Eval Gate` 时，不必机械铺开评测物料
- 一旦启用，应和 `prompts/`、相关 `schemas/`、`scripts/run-evals.sh` 一起维护
- 具体最低检查和证据要求回到 `docs/protocols/ai-eval-gate.md`

## 联动

- 改评测物料时，检查 `prompts/`、相关 `schemas/`、`scripts/run-evals.sh` 和命中的 skill 是否要同步
