# full-closure-mode

## 用途

- 只跑一条固定闭环，证明主链和伴随记录能力能串起来

## 固定链路

`dev-planner -> dev-builder -> code-review(Hold) -> bug-fixer -> code-review(Accept) -> release-builder -> git-upload-logger -> context-handoff`

## 闭环判定

- 路由没有串错
- `Hold -> fix -> Accept` 回环成立
- 发布记录和上传日志分流正确
- 最终承接快照能带出完整上下文
