# protocols

本目录放 `V3` 的 protocol 导航。
owner 在各 protocol 文件；这里不重写 workflow、skill 或 runtime 规则。

## 当前范围

- `security-lite.md`
- `ai-eval-gate.md`
- `adr-lite.md`
- `release-gate.md`
- `steering-lite.md`
- `adr-lite-template.md`
- `security-checklist.md`
- `ai-eval-template.md`

## protocol 停笔规则

- 只定义最低检查、固定字段和证据要求
- 不承担路由契约；路由优先依赖 skills 的 `description`
- 不负责分流，不讲完整流程
- `steering-lite.md` 只定义进化系统的状态机、阈值、证据与 purge 规则，不替代 `runtime/evolution/` 或 meta skill
- 机器可校验契约写到根级 `schemas/`
- 正式对象写回根级 `runtime/`
