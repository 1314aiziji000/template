# 06-steering-self-memory-run

## 执行时间

- 日期：`2026-04-16`

## 实际命令

### steering proposal

- 命令：
  - `python scripts/scan-steering-signals.py --errors workspaces/v3-validation-pack/artifacts/steering/errors --logs workspaces/v3-validation-pack/artifacts/steering/empty-logs --reviews workspaces/v3-validation-pack/artifacts/steering/empty-reviews`

### self-memory end-to-end

- 在临时 fixture 中执行：
  - `extract_dialogue.py` x 2
  - `roll_batch.py`
  - `build_report.py --mode periodic`
  - `purge_raw.py --force`

## 结果

### steering

- 成功生成 `1` 条 proposal
- 结论：
  - `proposal_type`: `rule-graduation`
  - `signal_type`: `boundary-drift`
  - `repeat_count`: `3`
  - `target_owner`: `AGENTS.md`
- 单次 `protocol-gap` 样本未误触发 proposal

### self-memory

- 成功生成：
  - `2` 份 extract
  - `1` 个月 batch
  - `1` 份 periodic report
- periodic report 的触发来自：
  - `10` 个有效任务轮次
- purge 结果：
  - `2` 份 raw 已删除
  - manifest 只保留 `raw_id`、`source_date`、`hash`、`counts`、`extract_refs`、`report_refs`、`purged_at`

## 判定

- `error -> proposal` 路径已跑通
- `raw -> extract -> batch -> report -> purge` 路径已跑通
- 当前脚本足以支撑首版验证线；后续需要继续补更复杂的负例与 owner 路由样本
