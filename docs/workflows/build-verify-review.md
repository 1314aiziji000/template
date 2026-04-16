# build-verify-review

## 定位

本文件只描述实施闭环的阶段骨架。
具体实施、修复、审查规则分别由 `dev-builder`、`bug-fixer`、`code-review` 承担；共享 gate 细节回到 `docs/protocols/`。
本文件只回答阶段顺序、进入条件、必备产物和下一跳，不写 skill 内部规则。

## 进入条件

- 任务已进入实施阶段
- 需要补最小验证证据
- 需要把改动送入正式审查

## 本阶段关注什么

- 当前切片边界是否仍然成立
- 最小必要验证与必要回归如何补证据
- 当前结果是否需要正式审查
- 是否进入 `fix -> verify -> review` 回环
- 是否命中共享 gate 或正式收口

## 审查闭环

正式收口必须走：

`implement -> verify -> review -> fix -> verify -> review`

规则固定如下：

- review 不是走过场
- fix 之后不能直接结束
- 每次修正都要重新进入验证和 review

## 阶段骨架

1. `dev-builder` 在既定边界内实施改动并补最小验证
2. 需要正式审查时，进入 `code-review`
3. 有明确失败证据或 findings 时，进入 `bug-fixer`
4. fix 后回到验证与审查，直到结论清楚
5. 收口后决定是否进入 `release-retro`

## 本阶段必须产出

- 实施结果
- `Verification Evidence`
- 当前审查结论或继续回环的理由
- 未验证项与剩余风险

## 退出去向

- 继续 `bug-fixer -> code-review` 回环
- 回 `dev-planner`
- 进入 `release-retro`
