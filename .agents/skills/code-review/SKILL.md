---
name: code-review
description: 当需要对当前改动做正式结构化审查时使用。它按 `V3` 的 `build-verify-review` 主链，对照当前任务边界、计划对象和 `Verification Evidence` 输出 `Accept / Hold / Reject`，并把修正或发布去向显式路由给后续 skill / gate。
---

[任务]
    对照当前任务边界、轻计划或 `runtime/PLANS.md`，审查本次改动是否达成目标、证据是否充分、风险是否已被识别并控制。
    输出固定结构的 review 结果，不直接偷偷改代码。

[依赖检测]
    Skill 启动时第一步自动执行：

    必需：
    - 当前任务要求
    - 当前改动对应的实现或变更范围
    - 当前验证证据或最小验证结果
    - `README.md`、`AGENTS.md`、`PROJECT_RULES.md`
    - `docs/workflows/build-verify-review.md`
    - `runtime/code_review.md`

    按需必读：
    - `runtime/PLANS.md` → 当前任务已沉淀为正式计划时必须读取
    - `runtime/plans/active/*.md` → 多计划模式时必须读取对应计划对象
    - `runtime/reviews/` → 当前任务已有正式 review 记录或需要补正式记录时读取
    - 当前任务相关的 `runtime/errors/`、`runtime/releases/`、`runtime/adr/`
    - 当前任务直接相关的实现、测试入口和验证结果

    当前会话可复用：
    - 当前会话里的边界、轻计划、`Verification Evidence`、builder / fixer 输出
    - 但它们不是仓库真相源；如已沉淀到 `runtime/`，以 `runtime/` 为准

    可选（必要时核验）：
    - `Product-Spec.md`、`Design-Brief.md`、设计稿或其他正式材料 → 只有仓库本身明确要求时才作为补充比对源
    - 外部依赖官方资料 → 只在风险判断依赖最新规则时核验

[第一性原则]
    **不信任口头完成声明**：没有代码、边界和证据支撑的“已完成”不算完成。review 只基于当前事实，不基于上一轮印象。

    **先看目标有没有达成，再看证据够不够**：`code-review` 先判断这次任务是否做对了、有没有跑出范围，再判断证据是否足以支撑当前结论。

    **结论必须结构化**：输出顺序严格对齐 `runtime/code_review.md`：
    1. `Findings`
    2. `Risks not fully verified`
    3. `Evidence checked`
    4. `Final recommendation`

    **最终结论只允许三种**：`Accept`、`Hold`、`Reject`。不使用“大致通过”“基本完成”“建议先这样”等软性替代结论。

    **review 不直接改代码**：发现问题后，由主链把功能 / 实现问题交回 `dev-builder`，把定向缺陷修复交给 `bug-fixer`。review 本身只负责判断和路由。

    **范围与非目标必须被检查**：如果改动明显跑出当前任务边界、平行扩写了计划外内容或遗漏了关键目标，必须在 findings 中指出。

    **证据不足就是问题，不是备注**：缺验证、缺回归、缺手工检查或未说明未验证项时，不能给 `Accept`。

    **门禁必须显式抬级**：发现任务已命中 `Release Card`、`ADR-Lite`、`Security Lite`、`AI Eval Gate` 时，必须写入 findings 或风险说明，并在结论里明确下一步，不口头带过。

[输出风格]
    **语态**：
    - 像正式审查结论，不像聊天反馈
    - 每个判断都对应边界、实现或证据

    **原则**：
    - x 不给模糊结论
    - x 不跳过当前边界或证据检查
    - x 不用“看起来没问题”替代审查
    - x 不在没有证据时给 `Accept`
    - ✓ findings 明确、可执行
    - ✓ 未充分验证风险单独列出
    - ✓ 已检查证据写清命令、结果或手工检查来源
    - ✓ 最终结论明确下一步去向

    **典型表达**：
    - "`Findings`：当前目标已基本达成，但 `delete flow` 缺回归验证，且这次改动已触及公共契约。"
    - "`Risks not fully verified`：未验证 staging 环境、未覆盖 AI 回归 case。"
    - "`Final recommendation`：`Hold`。先补回归验证，再决定是否进入 `release-builder`。"

[文件结构]
    ```
    code-review/
    ├── SKILL.md                           # 主 Skill 定义（本文件）
    └── templates/
        └── review-template.md             # review 固定字段模板
    ```

    本 Skill 维护私有 review 模板；运行中的正式审查协议仍以 `runtime/code_review.md` 为准。

[审查维度清单]
    审查分两层执行，先判断“做对了没有”，再判断“证据和风险是否可接受”。

    --- 第一层：目标与边界审查 ---

    [目标达成]
        - 当前任务目标是否已达成
        - 当前计划对象或轻计划的关键项是否已覆盖
        - 当前实现是否遗漏了应做内容

    [范围控制]
        - 改动是否跑出当前任务边界
        - 是否顺手引入了计划外实现、结构扩写或协议改写
        - 如有 `非目标`，是否仍被遵守

    [链路去向]
        - 如果当前目标未达成，应交回 `dev-builder` 还是 `bug-fixer`
        - 如果发现计划已失效，是否需要回 `dev-planner`

    --- 第二层：证据与风险审查 ---

    [证据完整性]
        - 是否已有最小验证证据
        - 中改及以上或高风险任务，是否对齐 `Verification Evidence`
        - `Commands`、`Results`、`Manual Checks`、`Not Verified Yet` 是否真实可审

    [风险与门禁]
        - 剩余风险是否被明确说明
        - 是否命中 `Release Card`、`ADR-Lite`、`Security Lite`、`AI Eval Gate`
        - 是否需要正式 review 记录进入 `runtime/reviews/`

    [结论规则]
        - `Accept`：目标达成，证据足够，剩余风险已在可接受范围说明
        - `Hold`：方向可接受，但仍缺验证、缺修正、缺发布条件或缺关键信息
        - `Reject`：目标未达成，或证据 / 风险不足以支持当前改动继续推进

[审查策略]
    **边界对照法**
    - 先读取当前任务边界、轻计划或正式计划对象
    - 再检查当前实现是否对齐目标、范围和非目标

    **证据优先法**
    - 先看验证证据，再决定结论
    - 如缺关键证据，不以主观判断补位

    **问题分流法**
    - 功能未达成、实现缺口、范围跑偏 → 交回 `dev-builder`
    - 明确缺陷、回归、失败证据对应的问题 → 交给 `bug-fixer`
    - 计划失效、阶段或风险变化 → 回 `dev-planner`
    - 已具备发布条件 → 可继续进入 `release-builder`

    **门禁抬级法**
    - 发现发布、结构决策、安全或 AI 行为变更条件时，在结论中明确写出后续 gate，不在 review 中吞掉

[工作流程]
    [加载阶段]
        第一步：依赖检测
            执行 [依赖检测]

        第二步：读取审查基准
            读取当前任务边界、轻计划或 `runtime/PLANS.md`
            读取当前验证证据和相关实现

        第三步：识别当前审查类型
            判断当前属于：
            - 正常实施后的首次 review
            - fix 回环后的复审
            - 发布前正式 review

    [审查阶段]
        第一步：目标与边界审查
            判断目标是否达成、范围是否失控、是否需要回 builder / planner

        第二步：证据与风险审查
            对照 `Verification Evidence` 和相关验证结果，判断证据是否足够、风险是否仍未控制、是否命中其他 `Gate`

        第三步：决定结论
            只从下面三种中选择：
            - `Accept`
            - `Hold`
            - `Reject`

    [输出阶段]
        第一步：按固定结构输出
            顺序固定为：
            1. `Findings`
            2. `Risks not fully verified`
            3. `Evidence checked`
            4. `Final recommendation`

        第二步：明确下一步
            - 功能 / 实现问题 → 回 `dev-builder`
            - 定向缺陷修复 → 回 `bug-fixer`
            - 计划失效 → 回 `dev-planner`
            - 审查通过且命中交付路径 → 进入 `release-builder`

        第三步：按需沉淀正式记录
            如果这次属于中改以上、高风险或正式发布前审查，按需补到 `runtime/reviews/`

[初始化]
    执行 [加载阶段]
