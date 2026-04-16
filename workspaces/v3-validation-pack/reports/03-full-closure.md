# 03-full-closure

## Sandbox

- 路径：`workspaces/v3-validation-pack/sandboxes/closure-fixture/`
- 基线：由 source-mode bootstrap 正例产出的 initialized-mode sandbox
- Git：本地真实 Git repo + mock bare remote

## 闭环任务

- 任务：新增 `intent-router` demo，用一个可执行的小实现验证 `planner -> build -> review -> fix -> release -> upload -> handoff`
- 交付对象：V3 模板维护者

## 闭环步骤

### 1. `dev-planner`

- 在 `runtime/PLANS.md` 中把任务定义为 `Medium + Low Risk`
- 明确范围：
  - `src/demo/intent-router.sh`
  - `tests/intent-router-smoke.sh`
  - `runtime/reviews/`
  - `runtime/releases/`
  - `runtime/logs/`

### 2. `dev-builder`

- 新增 `src/demo/intent-router.sh`
- 新增 `tests/intent-router-smoke.sh`
- Builder 阶段先暴露出一个真实语法问题，已在进入正式 review 前修正
- 之后执行：
  - `bash tests/intent-router-smoke.sh`
  - 结果：通过

### 3. `code-review` 第一次：`Hold`

- 手工验证：
  - `bash src/demo/intent-router.sh '下一窗口'`
  - 结果：`unknown`
- 形成记录：
  - `runtime/reviews/2026-04-16-intent-router-review-hold.md`
- Hold 原因：
  - `下一窗口` 没有命中 `context-handoff`
  - smoke test 也没有覆盖这个别名

### 4. `bug-fixer`

- 最小修复：
  - `intent-router` 同时支持 `下一个窗口` 和 `下一窗口`
  - smoke test 新增 `下一窗口` 用例
- 修后重跑：
  - `bash tests/intent-router-smoke.sh`
  - `bash src/demo/intent-router.sh '下一窗口'`
- 结果：
  - smoke test 通过
  - `下一窗口` 返回 `context-handoff`

### 5. `code-review` 第二次：`Accept`

- 形成记录：
  - `runtime/reviews/2026-04-16-intent-router-review-accept.md`
- 结论：
  - 当前 demo 目标达成
  - 剩余风险只保留“未联调真实 GitHub 远端”

### 6. `release-builder`

- 新增：
  - `runtime/releases/2026-04-16-intent-router-release.md`
- 激活 gate：
  - `bash .agents/skills/release-builder/scripts/release-check.sh --allow-dirty`
- 结果：
  - 真实通过

### 7. `git-upload-logger`

- 初始化 closure sandbox 本地 Git
- 建立 mock bare remote
- 完成真实本地上传链：
  - `git add`
  - `git commit`
  - `git push origin main`
- 实际提交：
  - `543cb52bc6c166093ed476416ed2d79b2245798b`
- 写入：
  - `runtime/logs/2026-04-16.md`
- 说明：
  - 日志文件是在 push 后生成，因此未并入同一批 commit

### 8. `context-handoff`

- 生成最终累计承接快照，已包含：
  - 前序阶段累计
  - 当前闭环状态
  - release 与 upload 结果
  - 剩余风险与下一步
- 接收模式守卫：
  - 第一条回复只能是 `明白` 或 `不明白`

## 闭环判定

- `dev-planner -> dev-builder -> code-review(Hold) -> bug-fixer -> code-review(Accept) -> release-builder -> git-upload-logger -> context-handoff` 已完整走通
- `Hold -> fix -> Accept` 回环成立
- `runtime/PLANS.md`、`runtime/releases/`、`runtime/logs/` 边界未混

## 剩余风险

- 未联调真实 GitHub 远端
- 未激活 AI Eval Gate
- 上传日志文件本身未并入同一批 push
