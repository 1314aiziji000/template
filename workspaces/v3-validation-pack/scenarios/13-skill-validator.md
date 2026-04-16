# Scenario: skill-validator

## 正例

- 触发词：用户明确要求检查 `.agents/skills/` 是否符合官方 `skill-creator` 流程，或要求生成 skills 官方化报告
- 前提：当前 `V3/.agents/skills/` 已补齐 `agents/openai.yaml`
- 预期：运行官方 `quick_validate.py`、比较 `interface` 可重建性、校验 `policy.allow_implicit_invocation`，并输出结构化报告

## 反例

- 条件：普通日常 build / fix / review 主链
- 预期：`skill-validator` 不应隐式触发，也不应替代 `verify.sh`

## 验证重点

- 官方基础校验与项目增强校验是否分层
- `default_prompt` 缺省是否不会误判失败
- `.codex/skills` 与旧 skill 路由头残留扫描是否有效
