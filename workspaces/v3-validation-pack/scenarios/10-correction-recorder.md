# Scenario: correction-recorder

## 正例

- 输入：用户明确纠正 AI，且本次 incident 已具备复用价值
- 预期：生成一条独立 `runtime/errors/*.md` 记录

## 反例

- 条件：只是一次性小偏差，且无复用价值
- 预期：允许明确说明不建档，不机械制造 incident 文件

## 验证重点

- 一次 incident 一文件
- 不跨 incident 聚合
- 只记录事实、根因、修复和防再发建议
