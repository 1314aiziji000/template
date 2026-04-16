# Scenario: release-builder

## 正例

- 输入：review 与验证齐备，进入发布收口
- 预期：生成 Release Card、冒烟、回滚，并能通过 release gate

## 反例

- 条件：缺 review 或缺验证
- 预期：被阻断，不能伪装成可发布

## 验证重点

- `runtime/releases/` 正式记录
- `release-check.sh` 激活后可通过
- 与 `runtime/logs/` 的边界
