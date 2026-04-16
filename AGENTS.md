# AGENTS.md

## 作用

- 本文件是 `V3` 的仓库级 AI 执行文档。
- owner 只负责全局执行原则、完成标准和少量 repo-critical 守卫。
- 默认主链：`AGENTS -> skill -> runtime`
- 人看任务入口概览时，优先看 `docs/workflows/intake.md`
- 本文件不拥有完整路由表、skill 内部规则或共享 gate 细则

## 真相源

1. 当前任务要求
2. `README.md`、`AGENTS.md`、`PROJECT_RULES.md`
3. 当前任务命中的 owner 文档、正式对象和验证结果
4. 命中机器契约时，`schemas/`

- `resources/`、`me/`、`workspaces/`、历史聊天、仓外笔记不是默认正式真相源
- `me/self-memory/` 只给维护者复盘使用；即使启用，也不自动进入 AI 侧默认真相源
- `workspaces/self-memory-staging/` 只承接本地 raw / manifest，不是正式记录层

## bootstrap 守卫

- 根级若仍存在 `项目说明书.md`，先完成一次性 `project-bootstrap`
- 只有用户确认后，才允许裁剪目录和删除一次性资产
- 必须先将初始化结论写回 `runtime/PLANS.md`，再删除 `项目说明书.md` 和 `.agents/skills/project-bootstrap/`
- bootstrap 完成后，不保留一次性初始化资产和平行说明源

## 全局硬规则

- 先确认边界，再进入对应 skill；边界失效时，先回计划或重新判路由
- 优先最小必要改动，不顺手扩写
- 不新增平行计划、平行记录或平行真相源
- 需要计划、实施、修复、审查、发布或伴随记录时，优先进入对应 owner 文档，不在根级重写下层细则
- 官方最低标准里 `agents/openai.yaml` 不是必需件；`V3` 项目内把它升为每个自制 skill 的强制增强层
- 新建自制 skill 必须用官方 `skill-creator/init_skill.py` 初始化；已有 skill 允许跳过 `init`，但必须补齐 `agents/openai.yaml` 并通过官方 `quick_validate.py` 与项目级整包校验
- `SKILL.md` 仍是 skill 的主契约与主维护对象；`agents/openai.yaml` 只承接 UI / policy / dependencies 增强，不替代 `name` / `description`
- 改对外契约、共享字段或 AI 结构化输入输出时，同步检查 `schemas/`
- 无法验证时，明确说明原因和风险
- 不默认自动派发子代理
- `correction-recorder`、`steering-runner`、`user-dialogue-analyst`、`skill-validator` 默认不隐式触发；它们的触发边界必须同时靠 `description` 和 `policy.allow_implicit_invocation` 双层收紧
- `default_prompt` 不作为 `V3` 首轮验收硬门槛；若官方生成器产出就保留，不要求开发者手填或手改
- 进化提议只能先进入 `runtime/evolution/proposals/`；未确认前不得直接改 owner 文档
- 不允许在激活规则文档、skill 包或验证物里残留旧 `.codex/skills` 口径

## 完成标准

- 已执行与当前风险相称的最小必要验证
- 验证证据真实、可复查、可回链
- 命中修复回环时，fix 后已重新验证并重新进入审查
- 已说明未验证项、剩余风险和下一步

## 记录守卫

- 正式计划、审查、错误、发布、ADR 和日志对象统一落 `runtime/`
- `runtime/evolution/` 只承接提议、归档和已确认的进化记忆，不替代 `errors/`、`reviews/`、`logs/`
- 新窗口收到承接快照时，承接确认第一条只允许回复 `明白` 或 `不明白`
- 上传批次日志只依据真实 Git 结果记录；不得擅自缩小上传范围
- `runtime/logs/` 只承接 skill 驱动日志，不替代 `reviews/`、`releases/`、`errors/`、`adr/`
