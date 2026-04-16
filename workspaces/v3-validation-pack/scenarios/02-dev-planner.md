# Scenario: dev-planner

## 正例

- 输入：`Medium / Large` 或高风险任务
- 预期：先计划，写清目标、范围、非目标、验证方式、下一步

## 反例

- 输入：`Small + Low Risk`
- 预期：不强制升级成正式计划

## 验证重点

- `Size + Risk` 判断
- 是否正确写入 `runtime/PLANS.md`
- 是否避免平行计划
