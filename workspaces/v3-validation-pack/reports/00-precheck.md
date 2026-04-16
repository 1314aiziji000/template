# 00-precheck

## 范围

- 主仓当前 `templates/V-项目级模板/V3/`
- 不回退现有未提交改动，把当前工作区视为本轮测试基线

## 已执行命令

1. `bash scripts/verify.sh`
   - 结果：通过
   - 关键输出：`Detected bootstrap-ready template mode`
2. `bash scripts/security-check.sh`
   - 结果：通过
3. `bash scripts/run-evals.sh`
   - 结果：正常 skip
   - 关键输出：`No active AI Pack material detected under evals/ or prompts/. Nothing to run.`
4. `bash .agents/skills/release-builder/scripts/release-check.sh --allow-dirty`
   - 结果：正常 skip
   - 关键输出：`No release record detected under runtime/releases/. Release gate is not active; skipping.`

## 结论

- 当前主仓 `V3/` 的结构基线是健康的
- `run-evals.sh` 的 skip 属于当前仓态预期，不是失败
- `release-check.sh` 的 skip 说明主仓尚未激活 release gate，后续需要在 closure sandbox 中单独激活一次
