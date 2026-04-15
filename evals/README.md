# evals

本目录用于 AI 行为评测。  

## 什么时候启用

- Prompt 变更
- 模型切换
- RAG 策略变化
- tool routing / output parser / safety policy 变化

## 建议内容

- 基准 case
- 目标 case
- 回归 case
- 结果摘要或报告

## 使用边界

- 没命中 `AI Eval Gate` 时，不必机械铺开评测物料
- 一旦启用，应和 `prompts/`、`configs/models/`、`scripts/run-evals.sh` 一起维护
