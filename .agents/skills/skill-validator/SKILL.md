---
name: skill-validator
description: 当需要检查 `.agents/skills/` 是否遵从官方 `skill-creator` 流程、核对 `agents/openai.yaml` / `policy.allow_implicit_invocation` / 旧 `.codex/skills` 残留，或在 `workspaces/v3-validation-pack/` 固定节点需要生成 skills 官方化报告时使用。默认只允许手动触发。
---

# skill-validator

## 作用

- 负责对当前 `V3` skills 执行官方基础校验与项目增强校验
- 负责生成可回放的 skills 官方化报告，给 validation pack 和人工复核使用
- 不替代 `verify.sh`、不重写其他 skill 的业务规则，也不自动改写 skill 文件

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `.agents/skills/skill-validator/references/validation-rules.md`
- `.agents/skills/skill-validator/scripts/run_skill_validator.py`

按需读取：

- `.agents/skills/*/SKILL.md`
- `.agents/skills/*/agents/openai.yaml`
- `workspaces/v3-validation-pack/`
- `scripts/verify.sh`
- 当前任务命中的 workflow / protocol / runtime 文档

## 硬规则

- 先跑官方 `quick_validate.py`，再做项目增强校验
- `interface` 只验证官方生成器可重建的字段，不做整文件字节级死比对
- `policy.allow_implicit_invocation` 必须单独校验，不和官方 `interface` 比对揉在一起
- `default_prompt` 缺省不判失败；若存在，只校验结构合法，不做人工作文案评分
- 必须扫描旧 `.codex/skills` 口径、旧 skill 路由文案和过宽 description 残留
- 默认只允许手动触发，不参与日常隐式主链

## 输出

- 校验摘要
- 按 skill 拆分的失败 / warning 列表
- 可选的 Markdown 报告

## 正式落点

- 日常校验结果：当前回复或终端输出
- validation pack 报告：`workspaces/v3-validation-pack/reports/`

## 退出条件

- 已完成官方基础校验、项目增强校验和旧口径扫描
- 已明确给出通过 / 失败结论
- 命中 validation pack 节点时，已写出报告
