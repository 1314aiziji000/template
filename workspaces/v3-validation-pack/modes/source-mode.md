# source-mode

## 用途

- 验证模板源态是否能正确命中 `project-bootstrap`
- 验证 bootstrap 完成后是否能退出一次性状态

## 前提

- 根级存在 `项目说明书.md`
- `.agents/skills/project-bootstrap/` 存在
- 当前自制 skill 已带 `agents/openai.yaml`

## 必测

- 正例：用户输入 `开始`，进入 bootstrap 链
- 反例：缺少 `项目说明书.md` 或已完成初始化时，不再进入 bootstrap

## 预期产物

- 初始化结论进入 `runtime/PLANS.md`
- 一次性资产删除结果明确
- 仓态从模板源态切换为初始化完成态
- 保留其余 skill 的官方增强层，不回退 `agents/openai.yaml`
