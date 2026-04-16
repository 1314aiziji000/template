# ai-eval-gate

## 命中条件

- Prompt 变更
- 模型切换
- RAG 策略变化
- tool routing / output parser / safety policy 变化

## 最低检查

1. 准备相关 `prompts/`、`evals/` 与必要的 `schemas/`
2. 运行 `bash scripts/run-evals.sh`
3. 对照 `ai-eval-template.md` 检查 baseline、目标 case、回归 case 与关键风险

## 证据要求

- 当前评测输入范围
- 已执行的 eval 命令或 skip 原因
- 当前结果摘要与剩余风险

## 正式落点

- 审查结论：`runtime/reviews/`
- 需要长期保留的评测结论：按任务写入对应 `runtime/` 对象
