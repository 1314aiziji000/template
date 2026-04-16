# intake

## 作用

- 本文件是任务入口骨架，owner 属于 workflow
- 本文件允许最少导航，但只回答进入条件、`Size + Risk`、必备产物和下一跳
- 路由契约仍以各 skill 的 `description` 为准；本文件不写 skill 内部规则

## 进入前检查

- 如果根级仍存在 `项目说明书.md`，先进入 `bootstrap.md`
- 如果 `.agents/skills/project-bootstrap/` 仍存在且用户目标是初始化，先完成一次性 bootstrap，再回到普通任务接入

## 特殊入口

| 请求特征 | 典型去向 | 说明 |
| --- | --- | --- |
| 用户输入 `下一个窗口` 或 `下一窗口` | `context-handoff` | 进入承接生成或承接确认 |
| 新窗口收到承接快照 | `context-handoff` | 第一条回复只允许 `明白` 或 `不明白` |
| 命中 `git add`、`commit`、`push`、同步 Git / GitHub、上传 GitHub | `git-upload-logger` | 上传范围与结果由真实 Git 结果记录 |
| 新项目首次接入且用户输入 `开始` | `project-bootstrap` | 仍属初始化，不进入日常主链 |

## 常规接入

未命中特殊入口时，先完成下面 4 项判断：

1. 读取根级入口文件
2. 判断任务类型
3. 判断 `Size`
4. 判断 `Risk`

## `Size + Risk`

每个任务都必须同时判断两个维度：

- `Size`: `Small / Medium / Large`
- `Risk`: `Low / Medium / High`

### `Size`

| 等级 | 典型特征 | 默认处理 |
| --- | --- | --- |
| `Small` | 单点修正、`1-2` 个文件、无结构变化 | 可直接进入实施，但仍要最小验证 |
| `Medium` | 多文件联动、同模块新增或调整 | 先做简计划，再实施 |
| `Large` | 跨模块、多步骤、重构、迁移、跨会话推进 | 必须进入正式计划 |

### `Risk`

高风险典型场景：

- 权限、鉴权、密钥、外部服务权限
- 数据迁移、结构变更、删除或回填
- 公开 API、对外契约、公共模块行为变更
- 发布配置、环境切换、基础设施操作
- Prompt、模型、RAG、tool routing、安全策略变化

## 抬级规则

- 高风险任务自动抬升一个执行等级
- `Small + High Risk` 按 `Medium` 执行
- `Medium + High Risk` 按 `Large` 执行

## 常见下一跳

| 条件 | 典型去向 |
| --- | --- |
| 边界未清、风险抬级、跨会话、多阶段 | `dev-planner` |
| 边界已清、准备实施 | `dev-builder` |
| 已有失败证据、报错、复现步骤或 findings | `bug-fixer` |
| 一轮实施完成，需要正式审查 | `code-review` |
| 需要交付、部署、发布或正式收口 | `release-builder` |
| 命中共享 gate | 先读相关 `docs/protocols/`，再回到对应 skill |

## 本阶段必须产出

- 当前任务类型判断
- 当前 `Size` 与 `Risk` 结论
- 是否需要计划
- 当前阶段下一步动作

没有这 4 项，就不进入正式实施。

## 退出去向

- 进入对应 skill
- 需要时创建或更新 `runtime/PLANS.md`
- 需要时抬级到共享 gate
- 明确是否进入 `build-verify-review` 或 `release-retro`
