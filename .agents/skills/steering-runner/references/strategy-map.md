# strategy-map

本文件只给 `steering-runner` 提供参考映射；  
合法状态、阈值与 owner 毕业规则仍以 `docs/protocols/steering-lite.md` 为准。

## 常用映射

- `rule-graduation`：当结论属于仓库级行为约束或单一 owner 规则升级
- `skill-adjustment`：当问题集中在单个 skill 的输入、输出或固定动作
- `protocol-hardening`：当共享 gate、字段、证据要求不足
- `verify-hardening`：当同类缺口主要依赖脚本自动拦截
- `new-skill-candidate`：当现有 owner 都无法稳定承接该模式

## 默认 owner 倾向

- 全局行为约束：`AGENTS.md`
- 分类、边界、联动：`PROJECT_RULES.md`
- 单一 skill：对应 `.agents/skills/*/SKILL.md`
- 共享 gate / 固定字段：`docs/protocols/*.md`
- 可自动检查的硬边界：`scripts/verify.sh`
