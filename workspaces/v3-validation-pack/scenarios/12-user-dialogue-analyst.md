# Scenario: user-dialogue-analyst

## 正例

- 输入：本地 raw `.md` / `.txt` 投递，且累计内容达到 `micro` 或 `periodic` 阈值
- 预期：生成 extract、batch、report，并在命中条件后 purge raw

## 反例

- 条件：raw 未达到阈值，或没有 extract / report 证据
- 预期：上传前固定节点安静跳过，不生成多余报告，也不提前 purge

## 验证重点

- 一份 raw 对应一份 extract
- batch 固定按月滚动
- report 门槛与 `72` 小时 purge 规则生效
- self-memory 不进入 AI 侧默认真相源
