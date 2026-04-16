# steering-lite

## 定位

本文件定义 `V3` 进化系统的最低协议：  
只负责状态机、初始阈值、证据回链、owner 毕业和 `self-memory` 的 raw / report 门控。  
它不替代 `runtime/evolution/` 的正式对象，也不替代 meta skill 的具体执行步骤。

## 固定对象

- 原始 incident 继续写回 `runtime/errors/`、`runtime/logs/`、`runtime/reviews/`
- 进化提议统一写入 `runtime/evolution/proposals/`
- 已处理提议统一归档到 `runtime/evolution/archive/`
- 已确认的 lesson / strategy 才允许写入 `runtime/evolution/memory/`

## proposal 状态机

只允许下面状态：

- `proposed`
- `confirmed`
- `graduated`
- `rejected`
- `superseded`
- `expired`

规则：

- 新提议只能从 `proposed` 开始
- 未经用户确认，不得从 `proposed` 直接进入 `graduated`
- `confirmed` 只表示用户同意继续落地，不代表已完成毕业
- 只有完成目标 owner 更新并补齐验证后，才允许进入 `graduated`
- `rejected`、`superseded`、`expired` 是终态；进入后只允许归档，不再复活

## proposal 类型

只允许下面类型：

- `rule-graduation`
- `skill-adjustment`
- `protocol-hardening`
- `verify-hardening`
- `new-skill-candidate`

## 初始阈值

- `rule-graduation`：同类 incident 或 review finding 默认 `3` 次
- `skill-adjustment`：同一 skill 默认 `3` 次连续低质量信号，或累计 `5` 次相关 incident
- `protocol-hardening`：共享字段、证据或 gate 缺口默认 `3` 次
- `verify-hardening`：同类验证补位或脚本缺口默认 `3` 次
- `new-skill-candidate`：无现有 owner 稳定覆盖、且模式已出现 `5` 次
- lesson / strategy 只有在 proposal 已确认且验证通过后才允许沉淀

这些数是第一版起始值，不是永久最优值；后续只能通过正式 proposal 调整。

## 证据回链

- 每个 proposal 必须写清 `source_records`
- `source_records` 只能指向真实 `runtime/` 记录，不允许只写聊天摘要
- 每个 lesson / strategy 必须回链到已处理 proposal 或验证证据
- 不能回链到证据的结论，不得写入 `runtime/evolution/memory/`

## owner 毕业规则

- 同一结论只能毕业到一个正式 owner
- 多个文件都需要同步时，只允许有一个主 owner；其他位置只能引用，不得重写
- `AGENTS.md` 只承接全局行为约束
- `PROJECT_RULES.md` 只承接分类、边界、目录和联动
- `.agents/skills/*/SKILL.md` 只承接该 skill 的独有规则
- `docs/protocols/*.md` 只承接共享 gate、固定字段和证据要求
- `scripts/verify.sh` 只承接可自动检查的硬边界

## meta skill 触发门槛

- `correction-recorder`：只允许手动触发，或在 `release-retro` 固定节点触发
- `steering-runner`：只允许手动触发，或在 `release-retro` 固定节点触发
- `user-dialogue-analyst`：手动触发；若 `self-memory` 已启用，则允许在上传前固定节点按阈值门控触发
- 日常 `build / fix / review` 主链不得隐式触发这 3 个 meta skill

## self-memory 与 raw 清理规则

- `me/self-memory/` 只给维护者复盘使用，不进入 AI 侧默认正式真相源
- 原始对话只接受 `workspaces/self-memory-staging/raw/` 中的本地 `.md` / `.txt` 投递
- staging 的 `manifest` 只承接覆盖率台账和 purge 状态，不升格为正式对象
- 单个 raw 成功提取、生成报告并完成核对后，应在 `72` 小时内 purge
- purge 后的 manifest 只保留最小元数据：
  - `raw_id`
  - `source_date`
  - `hash`
  - `counts`
  - `extract_refs`
  - `report_refs`
  - `purged_at`

## 上传固定节点门控

当 `self-memory` 已启用时，上传前只允许在下面条件命中时触发 `user-dialogue-analyst`：

- 存在 `pending` raw 尚未提取
- 或累计有效提取内容达到 `micro report` 门槛：`>= 400` 字或 `>= 4` 个有效任务轮次
- 或累计有效提取内容达到 `periodic report` 门槛：`>= 1200` 字或 `>= 10` 个有效任务轮次

未命中门槛时，上传节点应安静跳过，不制造额外噪声。
