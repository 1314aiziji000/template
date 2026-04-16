# evolution

本目录用于 `V3` 的进化提议、归档与已确认记忆。  
它是正式运行对象层，不是额外的说明文档目录。

## 当前对象

- `proposals/`：待确认或待毕业的进化提议
- `archive/`：已处理提议的归档
- `memory/lessons/`：已确认的可复用教训
- `memory/strategies/`：已确认的可复用策略

## 什么时候写入

- `steering-runner` 识别到重复模式，需要形成 proposal
- proposal 已被用户确认并完成 owner 落地，需要归档
- proposal 已确认且验证通过，需要沉淀 lesson / strategy

## 边界

- 本目录不承接原始 incident；原始错误仍写 `runtime/errors/`
- 本目录不承接原始 review finding；正式审查仍写 `runtime/reviews/`
- 本目录不承接节点流水；事件日志仍写 `runtime/logs/`
- `memory/` 只收确认后的 lesson / strategy，不收未经确认的猜测
- `archive/` 只归档已处理 proposal，不替代历史聊天或临时草稿
