# V3

## 定位

- `V3` 是当前面向 Codex 的正式标准版模板
- `README.md` 是混合文档：既做快速定位，也保留少量必须执行的硬边界
- 本文件不拥有下层细规则；与 owner 文档冲突时，以 `AGENTS.md`、`PROJECT_RULES.md`、skills、workflow、protocol、runtime owner 文档为准

## 适用范围

- 个人项目
- `2-5` 人小团队项目
- 单仓 Web / Backend / CLI / SDK
- 小型 AI 应用

重监管、重发布矩阵、多服务复杂协同项目，需要在此基础上再补强。

## 双态

- 模板源态：保留根级 `项目说明书.md` 与一次性 `project-bootstrap`
- 初始化完成态：删除一次性资产，只保留日常主链需要的正式对象

## 开始方式

模板源态固定按下面顺序开始：

1. 复制 `V3/`
2. 填写根级 `项目说明书.md`
3. 输入 `开始`
4. 进入一次性 `project-bootstrap`
5. 用户确认初始化方案
6. 写回 `runtime/PLANS.md`
7. 删除一次性资产
8. 回到日常主链

## 日常主链

- 默认主链：`AGENTS -> skill -> runtime`
- Codex 隐式路由优先依赖各 skill 的 `description`
- 官方最低标准里 `SKILL.md` 必需，`agents/openai.yaml` 属于可选 / 推荐层；`V3` 项目内把 `agents/openai.yaml` 升为每个自制 skill 的必带增强层
- `SKILL.md` 仍是主契约和主维护对象；`agents/openai.yaml` 只承接 UI / policy / dependencies 增强，不替代 `description`
- 新建 skill 必须走官方 `skill-creator/init_skill.py`；已有 skill 允许跳过 `init`，改走原地补齐 `agents/openai.yaml`、官方校验与项目回归
- 人看任务入口概览时，优先看 `docs/workflows/intake.md`
- 命中共享 gate 时，再读 `docs/protocols/`
- 命中机器契约时，再读 `schemas/`
- 正式结果对象统一落 `runtime/`
- `correction-recorder`、`steering-runner`、`user-dialogue-analyst`、`skill-validator` 属于 meta skill；默认只在手动或固定节点触发

## 分层

- `README.md`：混合入口，只做导航和必要硬边界
- `AGENTS.md`：仓库级常驻规则与完成标准
- `PROJECT_RULES.md`：目录职责、文档分类、目录边界、联动检查
- `.agents/skills/`：路由契约与 skill-specific 执行规则
- `docs/workflows/`：阶段骨架与下一跳
- `docs/protocols/`：共享 gate、固定字段、证据格式
- `schemas/`：机器可校验契约
- `runtime/`：正式结果对象

## 可选目录

- `docs/integrations/`、`docs/ui/`、`prompts/`、`evals/` 仅在当前存在或已启用时纳入联动
- `me/self-memory/` 是给维护者看的自我复盘可选包；启用后仍不进入默认正式真相源
- `workspaces/self-memory-staging/` 只承接本地原始投递与 manifest，不作为正式对象层
- `resources/`、`me/`、`workspaces/` 不是默认正式真相源
