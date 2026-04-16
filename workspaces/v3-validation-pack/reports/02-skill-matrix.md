# 02-skill-matrix

## 覆盖矩阵

| Skill | 正例覆盖 | 反例 / 守卫覆盖 | 证据类型 | 结果 |
| --- | --- | --- | --- | --- |
| `project-bootstrap` | source sandbox 里完成一次真实 bootstrap | 初始化完成后不再满足触发条件 | 执行 + 状态检查 | 通过 |
| `dev-planner` | closure sandbox 中把 `intent-router` 任务按 `Medium + Low Risk` 写入 `runtime/PLANS.md` | `Small + Low Risk` 不强制升级，按 skill / workflow 合同复核 | 执行 + 合同复核 | 通过 |
| `dev-builder` | 新增 `src/demo/intent-router.sh` 与 `tests/intent-router-smoke.sh`，smoke 通过 | 本轮未扩写根级入口、协议层、脚本层，边界受控 | 执行 + 范围检查 | 通过 |
| `bug-fixer` | 基于 review finding 修复 `下一窗口` 路由缺失并重跑验证 | 只有在拿到 finding 后才进入修复，没有无证据硬修 | 执行 + 过程检查 | 通过 |
| `code-review` | 输出 1 次 `Hold` 和 1 次 `Accept` 记录 | 第一次 review 因证据缺口未给 `Accept` | 执行 | 通过 |
| `release-builder` | 生成 release record，并让 `release-check.sh --allow-dirty` 真实通过 | 主仓预检查阶段无 release record 时正常 skip，不误判为发布态 | 执行 + 基线对照 | 通过 |
| `context-handoff` | 已生成累计承接快照，覆盖上传节点信息 | 接收承接时第一条只能 `明白 / 不明白`，按 skill 规则复核 | 执行 + 合同复核 | 通过 |
| `git-upload-logger` | closure sandbox 内完成真实 `commit + push` 到 mock remote，并写入 `runtime/logs/2026-04-16.md` | 上传边界按真实 push 范围完整记录；日志质量问题已在写入阶段被修正 | 执行 + 记录复核 | 通过 |

## 汇总

- 8 个日常 / 伴随 skill 都已覆盖
- 每个 skill 都有正例
- 每个 skill 都有反例或守卫条件复核
- 反例里有一部分是执行级验证，一部分是按当前 skill / workflow 合同复核；报告中已明确区分
- `correction-recorder`、`steering-runner`、`user-dialogue-analyst` 与 `skill-validator` 的覆盖另见专门报告
