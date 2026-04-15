# PROJECT_RULES.md

## 文件定位

本文件是 `V3` 模板的项目地图与改动路由入口。  
它负责说明先看哪里、改哪里、联动检查哪里。

## 阅读顺序

1. `README.md`
2. `AGENTS.md`
3. `PROJECT_RULES.md`
4. `V3-新手说明.md`
5. `V3-检查清单.md`
6. `docs/README.md`
7. `docs/workflows/`
8. 对应 `.agents/skills/`
9. `docs/protocols/`
10. `runtime/README.md`

## 文件职责

- `README.md`：说明 `V3` 是什么、适合什么项目、默认怎么用
- `AGENTS.md`：说明执行底线、抬级规则、验证与收口要求
- `PROJECT_RULES.md`：说明目录地图、任务路由和联动检查
- `V3-新手说明.md`：给初学者看的结构导读和流程说明
- `V3-检查清单.md`：人工分类检查入口
- `docs/README.md`：说明流程与协议说明层之间的关系
- `docs/workflows/`：说明任务如何流转
- `.agents/skills/`：说明 core skill、skill 私有模板和 skill 私有脚本
- `docs/protocols/`：说明跨 skill 共用的 gate 协议字段
- `runtime/README.md`：说明运行层对象如何承接、留痕与升级

## 项目地图

- `.agents/skills/`：核心 skill 包与 owner 模板 / 脚本
- `.codex/`：项目级 Codex 配置入口
- `docs/`：流程和协议的说明层
- `runtime/`：计划、审查、发布、错误、决策等运行对象层
- `scripts/`：全局验证、安全、eval 脚本入口
- `src/`：正式实现代码
- `tests/`：传统验证
- `workspaces/`：临时施工区
- `evals/`、`prompts/`、`configs/models/`：`AI Pack` 启用后的正式目录

## 递进式管理

`V3` 的管理不是平铺式，也不是默认全开。  
它采用“先最小闭环，再按条件抬级”的递进式规则。

### 规则加载顺序

1. 根级入口：先确认定位、真相源、目录职责
2. `docs/workflows/`：确认当前任务走哪条流程
3. 对应 `.agents/skills/`：命中条件后补当前 skill 的私有模板、私有脚本和局部工序
4. `docs/protocols/`：命中共享 gate 时补安全、ADR、AI eval 等共享协议
5. 正式记录与专项目录：只有实际进入对应阶段才启用

### 执行抬级顺序

- `Small + Low Risk`：走 `Core`，保留最小验证和最小 review
- `Medium`、跨会话、多阶段任务：升级到 `runtime/PLANS.md` 和正式 skill / protocol
- `High Risk`、发布、AI 行为变更：再叠加对应 `Gate`
- 只有项目长期需要时，才启用 `Packs`

### 根级判断优先级

1. 先判断是不是当前任务真正的真相源
2. 再判断当前任务属于哪类入口
3. 再判断当前应走 `Core`、`Gates` 还是 `Packs`
4. 最后才决定具体改哪个文件和跑哪些验证

## 路由表

- 改模板定位、适用范围、管理方式：看 `README.md`
- 改 AI 执行底线、抬级规则、验证要求：看 `AGENTS.md`
- 改目录职责、入口顺序、联动检查：看 `PROJECT_RULES.md`
- 改任务接入、实施、收口流程：看 `docs/workflows/`
- 改计划固定模板：看 `.agents/skills/dev-planner/templates/plans-template.md`
- 改 review 固定模板：看 `.agents/skills/code-review/templates/review-template.md`
- 改 `Release Card` 固定模板：看 `.agents/skills/release-builder/templates/release-card-template.md`
- 改共享 gate 协议：看 `docs/protocols/`
- 改运行层入口和对象边界：看 `runtime/README.md`
- 改正式记录模板：看 `runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 改长任务计划体系：看 `runtime/PLANS.md` 和 `runtime/plans/`
- 改全局自动化入口：看 `scripts/`
- 改 skill 私有发布 gate 脚本：看 `.agents/skills/release-builder/scripts/`
- 改临时试验：看 `workspaces/`
- 改 AI Pack 预留目录：看 `evals/`、`prompts/`、`configs/models/`

## 任务类型路由

- 新功能或需求变更：先看 `docs/workflows/intake.md`
- bug、异常、回归：先看 `docs/workflows/intake.md`，再决定是否进入失败证据优先路径
- 重构、结构调整、迁移：先看 `docs/workflows/intake.md`，通常会抬级到 `runtime/PLANS.md`
- 发布、交付、配置切换：先看 `docs/workflows/release-retro.md`
- AI 行为变更：先看 `docs/workflows/intake.md`，并准备进入 `AI Eval Gate`

## 联动检查

- 改根级入口文件时，检查 `README.md`、`AGENTS.md`、`PROJECT_RULES.md`
- 改根级治理口径时，检查是否仍与 `V3落地方案/` 的定位、原则和总图一致
- 改 `docs/README.md` 或 `docs/workflows/README.md` 时，检查阅读顺序和路由表是否仍一致
- 改 `runtime/README.md` 或 `runtime/` 下对象时，检查是否仍与 `docs/` 的说明层边界一致
- 改 workflow 时，检查相关 skill 模板、共享 gate 协议与 `runtime/PLANS.md`
- 改 `.agents/skills/` 下模板或脚本时，检查 owner `SKILL.md`、根级入口和 `runtime/` 对象是否仍一致
- 改 `docs/protocols/` 时，检查共享 gate、脚本入口和 `runtime/` 运行对象目录是否仍一致
- 改 `evals/`、`prompts/`、`configs/models/` 时，明确是否已正式启用 `AI Pack`
- 改递进式管理规则时，检查 `README.md`、`AGENTS.md`、`PROJECT_RULES.md`、`docs/workflows/`、`.agents/skills/`、`docs/protocols/` 是否仍一致
