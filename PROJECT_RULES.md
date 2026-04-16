# PROJECT_RULES.md

## 作用

- 本文件是 `V3` 的目录 owner 文档。
- owner 负责目录职责、文档分类、目录边界和联动检查。

## 文档分类规则

- 主要职责是解释、背景、导航、表单填写、复盘阅读的，归人看文档
- 主要职责是触发、约束、分流、gate、输出格式、正式落点的，归 AI 执行文档
- 同时承担导航和必要硬约束的，归混合文档
- 混合文档发生冲突时，AI 约束优先于解释性文字

## 文档 owner 规则

- `AGENTS.md` 负责全局 AI 执行原则与完成标准
- `PROJECT_RULES.md` 负责目录职责、文档分类、目录边界、联动检查
- `.agents/skills/*/SKILL.md` 负责本 skill 的独有执行规则
- `.agents/skills/*/agents/openai.yaml` 负责该 skill 的官方元数据增强层；在 `V3` 中属于项目强制件，但不替代 `SKILL.md`
- `docs/workflows/*.md` 负责阶段骨架与下一跳
- `docs/protocols/*.md` 负责最低检查、固定字段、证据要求
- `runtime/*.md` 负责正式对象定义、创建条件、边界与区别
- README 类文档只负责导航与定位；混合 README 不拥有下层细规则
- 若同一事实在多处出现，以 owner 文档为准；其他文档只允许引用，不允许重写

## 当前分类

当前存在或已启用的对象，按下面分类：

### 人看文档

- `V3真相源.md`
- `项目说明书.md`
- `docs/README.md`
- `docs/workflows/README.md`
- `docs/protocols/README.md`
- `src/README.md`
- `tests/README.md`
- `resources/README.md`
- `workspaces/README.md`
- `me/README.md`
- `me/self-memory/` 下的说明、批次、报告和画像文档
- `workspaces/self-memory-staging/README.md`
- `workspaces/v3-validation-pack/` 下的说明、报告、场景、模式文档

### AI 执行文档

- `AGENTS.md`
- `PROJECT_RULES.md`
- `.agents/skills/*/SKILL.md`
- `docs/workflows/*.md`，但 `docs/workflows/README.md` 例外
- `docs/protocols/*.md`，但 `docs/protocols/README.md` 例外
- `runtime/code_review.md`
- 其他直接定义正式对象、创建条件、输出格式、记录边界的 `runtime/*.md`

### 混合文档

- `README.md`
- `runtime/README.md`
- `schemas/README.md`
- `docs/integrations/README.md`
- `prompts/README.md`
- `evals/README.md`

## 目录边界

- `README.md`：混合导航入口；只保留最少导航和必要硬边界，不拥有下层细规则
- `AGENTS.md`：仓库级常驻规则和完成标准
- `.agents/skills/`：按官方 `skill-creator` 流程维护的 skill 包；官方最低标准里 `SKILL.md` 必需、`agents/openai.yaml` 可选 / 推荐，而 `V3` 把 `agents/openai.yaml` 升为项目强制增强层；frontmatter `description` 继续承担路由契约，正文只写 skill-specific 规则
- `docs/workflows/`：只写阶段顺序、进入条件、必备产物、下一跳；`intake.md` 仍属 workflow owner，可保留最少导航，但不写 skill 内部规则
- `docs/protocols/`：只写最低检查、固定字段、证据要求；不负责分流，不讲完整流程；`steering-lite.md` 负责进化系统的状态机、阈值、证据与 purge 规则
- `schemas/`：机器可校验契约层
- `runtime/`：只写正式对象定义、创建条件、边界与区别；不定义任务怎么跑
- `scripts/`：验证与检查脚本；`verify.sh` 可聚合结构校验、owner 合同校验与可选的 validation pack 自动 gate
- `src/`、`tests/`：实现与验证入口

## Bootstrap-only Assets

- `项目说明书.md`：复制模板后先填写的一次性正式输入
- `.agents/skills/project-bootstrap/`：一次性初始化 skill

规则：

- 只在模板源和初始化未完成的项目副本中存在
- bootstrap 完成后，必须先将结论写回 `runtime/PLANS.md`
- 写回完成后，必须从项目副本删除这些一次性资产

## Optional Packs 与辅助目录

- `docs/integrations/`：外部接入边界
- `docs/ui/`：UI 规范
- `prompts/`：Prompt 物料
- `evals/`：AI 行为评测
- `resources/`：外置参考资料，不是正式真相源
- `me/`：维护者导航层，不是正式真相源；`me/self-memory/` 是其中的可选复盘包
- `workspaces/`：临时施工区，不是正式真相源；`workspaces/self-memory-staging/` 只承接本地 raw / manifest

规则：

- 仅当对象当前存在或已启用时，才纳入本轮文档分类与联动范围
- 不存在的目录、占位目录或未启用 pack，不作为固定改造对象
- Optional Packs 一旦启用，就要和相关 workflow、skill、protocol、脚本保持一致
- 不允许再保留旧 `.codex/skills` 路径、旧 skill 目录口径或平行 skill 配置源

## runtime 对象

- `runtime/PLANS.md`：单活跃长任务计划，也承接 bootstrap 初始化结论
- `runtime/plans/`：多活跃长任务计划
- `runtime/reviews/`：正式审查记录
- `runtime/errors/`：错误与返工记录
- `runtime/releases/`：发布或交付记录
- `runtime/adr/`：关键结构决策
- `runtime/logs/`：skill 驱动日志落点
- `runtime/evolution/`：进化提议、归档与已确认 lesson / strategy 记忆

## 改动联动

- 改根级入口：一起检查 `README.md`、`AGENTS.md`、`PROJECT_RULES.md`
- 改 bootstrap：一起检查 `项目说明书.md`、`docs/workflows/bootstrap.md`、`.agents/skills/project-bootstrap/`、`runtime/PLANS.md` 和 `scripts/verify.sh`
- 改 workflow：确认它仍只写阶段顺序、进入条件、必备产物、下一跳，并检查相关 skill、protocol 和 `runtime/` 落点
- 改 protocol：确认它仍只写最低检查、固定字段、证据要求，不把分流和完整流程写回 protocol
- 改 skill：检查是否仍遵从官方 `skill-creator` 流程；新增 skill 必须用 `init_skill.py` 初始化，已有 skill 至少要补齐 `agents/openai.yaml`、通过 `quick_validate.py`，并确认 `description` 仍承担路由契约、正文仍只写 skill-specific 规则、`policy.allow_implicit_invocation` 与模板、脚本和 `runtime/` 承接一致
- 改 `schemas/`：检查 `docs/protocols/`、`docs/integrations/`、`src/`、`tests/`、`evals/` 是否要同步
- 改 `runtime/`：确认它仍只写正式对象定义、创建条件、边界与区别，不把任务流程写回 `runtime/`
- 改 `runtime/evolution/`：同步检查 `docs/protocols/steering-lite.md`、相关 meta skill、`schemas/steering/` 和 `scripts/verify.sh`
- 改 Optional Packs：检查是否当前存在或已启用，再同步 bootstrap 裁剪规则、`scripts/verify.sh`、相关 protocol 和相关 skill
- 改 `resources/`、`me/`、`workspaces/`：确认没有新增独有事实，也没有反向升格成正式真相源
