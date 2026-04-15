# models

本目录用于模型配置物料。  

## 什么时候使用

- Prompt 变更
- 模型切换
- RAG 策略变化
- tool / agent routing 或 output parser 变化

## 建议内容

- 模型用途说明
- 默认路由或优先级
- 评测关注点
- 成本 / 延迟 / 安全约束

## 使用边界

- 这里只放项目级配置和说明，不放真实密钥
- 如果模型配置变化影响行为验证，要同步更新 `evals/` 与 `scripts/run-evals.sh`
