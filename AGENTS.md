# AGENTS.md

## 文件定位

本文件只放 `V3` 项目模板的仓库级 AI 执行规则。  
目录地图看 `PROJECT_RULES.md`，流程与协议看 `docs/`，当前运行对象看 `runtime/`。

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

## 真相源

1. 当前任务要求
2. `README.md`、`AGENTS.md`、`PROJECT_RULES.md`
3. `docs/workflows/`、对应 `.agents/skills/`、`docs/protocols/`
4. 当前任务对应的 `runtime/`、正式实现、验证与记录

## 执行目标

- 让小改低风险任务尽量快地通过
- 让中改、大改和高风险任务可接续、可解释、可验证
- 让收口结论基于证据，而不是基于口头说明
- 让高频问题反哺 workflow、protocol、脚本和 skill

## 全局执行规则

- 优先最小必要改动，不做无关扩写
- 不新增平行目录、平行文档、平行真相源
- 中改及以上、高风险或跨会话任务先更新 `runtime/PLANS.md`
- 验证结果必须可追溯，不能只写“已验证”
- 无法验证时，明确说明原因、影响和剩余风险
- `workspaces/` 只放临时施工内容，不是正式真相源
- 任务一旦变质，先停下更新计划或路由，不继续带着错误边界硬做

## 任务接入基线

所有任务正式实施前，至少明确下面 4 项：

- 当前任务类型
- 当前 `Size`
- 当前 `Risk`
- 当前下一步动作

没有这 4 项，就不算进入正式实施。

## 计划与承接规则

- `Small + Low Risk` 可以不写长计划，但仍要明确边界和最小验证
- `Medium`、跨会话、暂停恢复、多阶段推进任务，默认启用 `runtime/PLANS.md`
- `Large` 或高风险抬级任务，必须进入正式计划路径
- `runtime/PLANS.md` 是活文档，不是摆设；阶段推进、风险变化、范围变化后必须更新

## 实施控边界规则

- 只改当前切片需要的范围
- 不顺手做无关重构
- 多文件联动时，先确认主文件和从文件
- 原本改实现时，不顺手扩大到协议、规则、目录体系
- 原本修 bug 时，不顺手重做命名或结构

## 失败证据优先

下面这些情况，默认先有失败证据，再进入实现：

- bug 可复现
- 改公共模块逻辑
- 改接口或数据契约
- 修回归问题
- 改 AI 行为，例如 Prompt、模型、RAG、tool routing、安全策略

失败证据可以是：

- 失败测试
- 固定复现步骤
- 失败 eval case
- 已记录的回归场景

## 验证与收口规则

- 正式收口必须经过 `implement -> verify -> review`
- fix 之后不能直接结束，必须重新进入验证和 review
- 收口说明至少包含：改了什么、验了什么、没验什么、还剩什么风险
- 发布、交付、配置切换、AI 行为变更时，必须进入对应 `Gate`

## 记录系统路由

- `runtime/reviews/`：正式审查结论
- `runtime/errors/`：明确错误、返工原因、反复模式
- `runtime/releases/`：发布或交付节点
- `runtime/adr/`：关键结构决策
- `runtime/plans/`：多活任务计划升级
- `docs/logs/`：如果仓库本身已有日志规则，继续沿用原规则

## 进化策略

`V3` 默认不自动跑 evolution。  
先把规则写清，再把脚本写稳，再考虑更强自动化。

## 递进式规则继承

- 第一层先读根级入口：`README.md`、`AGENTS.md`、`PROJECT_RULES.md`
- 第二层再读 `docs/workflows/`，判断当前任务处于哪一段流程
- 第三层命中条件后再读对应 `.agents/skills/`，决定当前 skill 的私有模板、私有脚本和局部工序
- 第四层命中共享 gate 时再读 `docs/protocols/`，决定是否启用安全、ADR、AI eval 等共享门禁
- 第五层只有在任务真的进入对应场景时，才启用 `runtime/` 下对应对象或 `AI Pack` 预留目录

规则可以越往下越具体，但不能突破上层真相源、边界控制和验证底线。

## 规则升级顺序

同类问题反复出现时，默认按下面顺序升级：

`workflow / skill-template / shared-protocol / checklist / scripts -> skill -> hooks -> 自动 evolution`

## 完成前检查

- 路径、术语、路由一致
- 协议与证据对应得上
- 临时内容已回填，或已说明未回填原因
- 当前收口层级与实际风险匹配，没有低风险口径硬收高风险任务
