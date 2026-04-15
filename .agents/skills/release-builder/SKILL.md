---
name: release-builder
description: 当改动已通过主要验证、需要进入交付、部署或正式发布收口时使用。它按 `V3` 的 `release-retro` 主链检查发布前条件、补 `Release Card`、明确冒烟与回滚路径，并判断是否需要沉淀到 `runtime/releases/`、`runtime/errors/` 或 `runtime/adr/`。
---

[任务]
    **正式交付检查模式**：当前任务需要交付构建产物、部署结果或面向下游的版本更新时，检查发布前条件、确认 `Release Card`、补齐冒烟检查和回滚路径。

    **发布阻塞判定模式**：当前任务想进入交付或发布，但验证证据、review 结论、冒烟条件或回滚路径不完整时，明确阻塞原因，不硬推发布。

    **收口沉淀模式**：当前任务已进入正式交付或发布节点，需要判断是否沉淀到 `runtime/releases/`、`runtime/errors/`、`runtime/adr/`，并输出交付说明或后续改进项。

[依赖检测]
    Skill 启动时第一步自动执行：

    必需：
    - 当前任务要求
    - 当前交付 / 发布目标
    - 当前验证证据
    - 当前 review 结论或等效正式审查结果
    - `docs/workflows/release-retro.md`
    - `.agents/skills/release-builder/templates/release-card-template.md`
    - `runtime/code_review.md`

    按需必读：
    - `runtime/releases/` → 当前任务已有发布 / 交付记录时读取
    - `runtime/errors/` → 当前交付节点暴露明确错误或返工原因时读取
    - `runtime/adr/` → 当前发布涉及关键结构决策时读取
    - `runtime/PLANS.md` 或 `runtime/plans/active/*.md` → 当前发布与正式计划强相关时读取
    - 当前任务相关的实现、验证结果、部署说明或现有交付材料

    当前会话可复用：
    - 当前会话里已经形成的 review 结论、验证证据、交付目标、回滚说明
    - 但它们不是仓库真相源；如已沉淀到 `runtime/`，以 `runtime/` 为准

    可选（必要时核验）：
    - `.agents/skills/release-builder/scripts/release-check.sh`、`scripts/security-check.sh`、`scripts/run-evals.sh` → 只有仓库明确启用时才作为辅助
    - 真实渠道脚本、部署平台或发布工具说明 → 只有仓库已经定义并需要核验时才读取

    不作为默认前置：
    - Web / Desktop / CLI 的平台型渠道检测
    - 自动安装 / 登录认证 / 平台签名 / 公证
    - `npm publish`、`vercel --prod`、`netlify deploy` 等具体平台发布操作

[第一性原则]
    **release-builder 是交付门禁，不是平台控制面**：本 Skill 默认负责发布前条件检查和收口判断，不把 `V2` 的多平台重型发布流程原样搬进 `V3` Core。

    **没有 review 和证据，就没有交付**：没有明确的 review 结论、验证证据和剩余风险说明时，不能进入正式发布或交付。

    **`Release Card` 必须完整**：命中正式发布、构建产物交付、部署、配置切换或面向下游版本更新时，必须至少补：
    - `Target`
    - `Smoke checks`
    - `Rollback`
    - `Notes`

    **冒烟检查和回滚路径不能省略**：即使当前只是“先交付给别人测试”，也要说明最少验什么、失败后怎么撤回。

    **沉淀是正式对象，不是聊天备注**：交付节点暴露的正式发布记录、错误教训和关键决策，要按需沉淀到 `runtime/releases/`、`runtime/errors/`、`runtime/adr/`，不留在过程对话里。

    **剩余风险必须说清**：release-builder 可以允许“带说明交付”，但不能允许“带未知交付”。未验证项、环境限制和后续动作必须明确写出。

    **门禁显式抬级**：命中 `Security Lite`、`AI Eval Gate` 或关键结构决策时，在发布收口中显式指出，不把高风险问题掩盖成普通发布备注。

[输出风格]
    **语态**：
    - 像交付 / 发布检查结果
    - 结论明确、阻塞明确、去向明确

    **原则**：
    - x 不在验证明显不足时硬推发布
    - x 不跳过 `Release Card`
    - x 不跳过冒烟和回滚说明
    - x 不把正式记录沉淀混成口头备注
    - ✓ 先写发布前条件是否满足
    - ✓ 明确交付目标、冒烟检查、回滚路径和剩余风险
    - ✓ 说明是否需要沉淀到 `runtime/`

    **典型表达**：
    - "当前 review 已 `Accept`，验证证据明确，`Release Card` 已补齐，可以进入正式交付。"
    - "当前缺少回滚路径和下游冒烟检查，结论是 `需先补发布条件`，不进入交付。"
    - "本次交付同时暴露可复用返工教训，除发布说明外，还应补到 `runtime/errors/`。"

[文件结构]
    ```
    release-builder/
    ├── SKILL.md                           # 主 Skill 定义（本文件）
    ├── templates/
    │   └── release-card-template.md       # Release Card 固定字段模板
    └── scripts/
        └── release-check.sh               # 按需启用的本地发布 gate 脚本
    ```

[发布检查清单]
    发布或交付前，至少检查以下内容：

    [前置门槛]
        - 当前目标已进入正式交付 / 发布路径
        - 当前验证证据明确
        - 当前 review 结论明确
        - 剩余风险和未验证项已说明

    [Release Card]
        `Release Card` 至少包含：
        - `Target`
        - `Smoke checks`
        - `Rollback`
        - `Notes`

    [冒烟与回滚]
        - 冒烟检查写清最少要验什么
        - 回滚路径写清失败后怎么撤回或停止扩散
        - 如果当前无法给出回滚路径，不能继续往下推

    [正式记录沉淀]
        - 正式发布 / 交付节点 → 需要时进入 `runtime/releases/`
        - 明确错误、返工原因、反复模式 → 需要时进入 `runtime/errors/`
        - 关键结构决策 → 需要时进入 `runtime/adr/`

    [状态分支]
        当前结果只允许落在下面几种状态之一：
        - `可进入交付`
        - `需先补发布条件`
        - `需补回滚路径`
        - `需沉淀正式记录`
        - `阻塞待确认`

[发布策略]
    **第一步：判断当前是不是正式交付路径**
    - 如果当前只是普通实现或普通修复，留在 `build-verify-review`
    - 只有命中交付、部署、配置切换或下游版本更新，才进入本 Skill

    **第二步：核对前置门槛**
    - 确认 review 结论、验证证据和剩余风险说明已经齐备
    - 缺任一关键前置条件时，结论落为 `需先补发布条件`

    **第三步：补齐 Release Card**
    - 按 `release-card-template` 组织最小发布说明
    - 没有 `Rollback` 时，结论至少落为 `需补回滚路径`

    **第四步：判断正式沉淀**
    - 需要正式发布 / 交付记录时，进入 `runtime/releases/`
    - 需要记录错误或返工教训时，进入 `runtime/errors/`
    - 涉及关键结构决策时，进入 `runtime/adr/`

    **第五步：输出交付去向**
    - 条件满足 → `可进入交付`
    - 条件不满足 → 明确阻塞项和需要回到的前一环

[工作流程]
    [加载阶段]
        第一步：依赖检测
            执行 [依赖检测]

        第二步：识别当前交付类型
            判断当前属于：
            - 正式发布
            - 构建产物交付
            - 部署 / 配置切换
            - 面向下游的版本更新

        第三步：读取交付上下文
            读取当前验证证据、review 结论、交付目标和按需运行对象

    [检查阶段]
        第一步：核对前置门槛
            检查验证证据、review 结论、剩余风险说明是否齐备

        第二步：补齐 `Release Card`
            写清：
            - `Target`
            - `Smoke checks`
            - `Rollback`
            - `Notes`

        第三步：判断正式沉淀
            检查是否需要进入：
            - `runtime/releases/`
            - `runtime/errors/`
            - `runtime/adr/`

    [输出阶段]
        第一步：输出当前状态
            只从下面几种中选择：
            - `可进入交付`
            - `需先补发布条件`
            - `需补回滚路径`
            - `需沉淀正式记录`
            - `阻塞待确认`

        第二步：输出交付说明
            至少包含：
            - `Release Card`
            - 当前冒烟检查
            - 当前回滚路径
            - 剩余风险
            - 下一步去向

        第三步：指向下一步
            - 条件满足 → 进入实际交付 / 发布动作
            - 条件不足 → 回到 `dev-builder`、`bug-fixer`、`code-review` 或相应 `Gate`

[初始化]
    执行 [加载阶段]
