# Scenario: project-bootstrap

## 正例

- 触发词：`开始`
- 前提：根级存在 `项目说明书.md` 和 `.agents/skills/project-bootstrap/`
- 预期：进入 bootstrap，写入初始化结论，删除一次性资产

## 反例

- 条件：已初始化完成或缺少 `项目说明书.md`
- 预期：不再走 bootstrap，直接按日常主链判断

## 验证重点

- 初始化模式结论
- Optional Packs 裁剪
- `runtime/PLANS.md` 写回顺序
- 删除顺序是否正确
