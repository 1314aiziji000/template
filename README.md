# V3

## 文件定位

本目录是 `V3` 的正式模板实现。  
它按 [`../V3落地方案/`](../V3落地方案/) 回填，面向 Codex 的轻量工程闭环。

## V3 是什么

`V3` 不是单纯的目录树模板，也不是平台型 agent runtime。  
它是一套面向 Codex 的工程闭环模板，目标是把下面这些动作收成正式主链：

- 任务接入
- 计划承接
- 实施控制
- 验证与证据
- 审查与修正
- 发布与收口
- 记录与规则进化

## V3 不是什么

- 不是 `V1/` 的同构替代版
- 不是 `V2/` 的直接搬运版
- 不是默认全自动的多 agent 控制面
- 不是强合规、高安全、重运维项目的默认完整方案
- 不是把所有高级能力一次性铺满的巨石模板

## 适用项目

默认适用：

- 个人项目
- `2-5` 人小团队项目
- 单仓 Web / Backend / CLI / SDK
- 小型 AI 应用，例如 Prompt、RAG、tool、agent 组合类项目

需要额外补强后再用：

- 多包 monorepo
- 多服务 / 微服务
- 有数据库迁移、公开 API、复杂权限的系统
- 明显依赖 AI 评测、安全、成本、延迟治理的项目

## 结构总览

- `Core` 默认骨架
- `Gates` 协议与门禁
- `Packs` 按需扩展目录

三者关系是：

- `Core` 负责默认最小正式闭环
- `Gates` 负责命中条件后不能绕过的硬门禁
- `Packs` 负责按项目类型启用的扩展层

## 分层边界

`V3` 现在按“说明文档 vs 运行对象”分层：

- 根级：只放总入口和顶层目录
- `.agents/skills/`：skill 目录是第一阅读单位，skill 私有模板和私有脚本随 skill 走
- `runtime/`：放当前执行入口和运行对象，例如 `PLANS.md`、`code_review.md`、`plans/`、`reviews/`、`errors/`、`releases/`、`adr/`
- `docs/`：只放说明文档，例如 `workflows/` 和共享 `protocols/`

一句人话：

- 看规则怎么跑，进 `docs/`
- 看当前对象在哪里用、在哪里留痕，进 `runtime/`

## 管理原则

`V3` 的管理采用递进式，不是默认把最重规则一次性全压上。

- 第一层 `Core`：所有任务先经过根级入口、基础流程和最小验证
- 第二层 `Gates`：命中中改、高风险、发布、AI 行为变更时，再加计划、review、release、security、eval 等正式门禁
- 第三层 `Packs`：只有项目类型真的需要时，才启用 `AI Pack`、发布增强或更重的自动化能力

一句人话：

- 先走最小闭环
- 命中条件再抬级
- 不命中就不硬加重流程

## 根级治理目标

根级入口文件要先回答 4 件事：

1. 这个模板适合什么项目，不适合什么项目
2. 当前任务先看哪里、按什么顺序读
3. 什么情况下继续走 `Core`，什么情况下必须抬级到 `Gates`
4. 哪些目录是正式真相源，哪些目录只是临时区或按需区

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

## 新手辅助阅读

如果是第一次看 `V3`，建议先加读两份根级辅助文档：

- `V3-新手说明.md`
- `V3-检查清单.md`

它们负责解释目录树、流程和检查顺序。  
如果与正式规则冲突，仍以 `README.md`、`AGENTS.md`、`PROJECT_RULES.md`、`docs/`、`runtime/` 为准。

## 默认使用方式

### 小改低风险

- 先读根级入口
- 经过 `docs/workflows/intake.md`
- 补最小验证和最小 review
- 不强制铺开长文档

### 中改 / 大改 / 高风险

- 先做 `Size + Risk` 判断
- 需要时立即启用 `runtime/PLANS.md`
- 按 workflow 主链推进
- 命中发布、安全、AI 行为变更时，叠加对应 `Gate`

### 正式发布或 AI 行为变更

- 不能只停留在 `Core`
- 必须进入对应 skill / protocol 和正式记录
- 必须说明证据、未验证项和剩余风险

## 默认与按需

默认使用 `Core` 内容。  
`runtime/` 作为运行层入口默认存在；`runtime/PLANS.md`、`runtime/plans/`、`runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`、`evals/`、`prompts/`、`configs/models/` 等目录或对象只有在命中条件时才写入正式内容，不要求项目实例默认全部启用。

## 与 V1 / V2 / V3落地方案 的关系

- `V1/`：最小项目骨架入口
- `V2/`：重型流程样本和高配参考
- `V3落地方案/`：唯一正式设计真相源
- `V3/`：按 `V3落地方案/` 回填的正式模板实现
