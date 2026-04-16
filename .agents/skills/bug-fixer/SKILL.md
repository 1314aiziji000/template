---
name: bug-fixer
description: 当已有明确问题、失败证据、回归缺陷或 review findings，下一步需要围绕最可能根因做定向修复时使用。
---

# bug-fixer

## 作用

- 负责围绕已知失败证据做定向修复
- 不在无证据场景下代替计划或普通实施

## 输入

必读：

- 当前任务要求
- 当前失败证据，至少一项：
- 报错信息
- 失败命令
- 复现步骤
- 回归场景
- `code-review` finding
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/build-verify-review.md`

按需读取：

- `runtime/PLANS.md`
- `runtime/plans/active/*.md`
- `runtime/code_review.md`
- 当前任务相关 `runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 当前任务相关实现、测试入口和已有验证结果

## 硬规则

- 先固定失败证据，不在证据不足时直接开修
- 说明 `1-3` 个可验证根因假设，并锁定当前最可能根因
- 围绕当前根因做最小必要修复
- 修后必须重新运行原失败验证与相关回归验证
- 命中 `Security Lite`、`ADR-Lite`、`AI Eval Gate` 时显式抬级

## 输出

- 失败证据
- 根因判断
- 修复范围
- 重新验证证据
- 未解决风险
- 下一步去向

## 正式落点

- 默认不新建计划或发布对象
- 如果这次修复暴露出明确返工原因、反复模式或需要正式沉淀的错误教训，可按需写入 `runtime/errors/`

## 退出条件

- 当前根因已说明清楚，或已明确证据不足
- 修后已重新验证原问题与相关回归路径
- 已明确回到哪个 skill 或哪个 `Gate`
