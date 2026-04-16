# code_review.md

## 作用

- 本文件定义默认 review 协议
- 正式审查记录归档到 `runtime/reviews/`
- 本文件不承担任务分流或代码实施规则

## 固定输出顺序

1. `Findings`
2. `Risks not fully verified`
3. `Evidence checked`
4. `Final recommendation`

## 硬规则

- review 先对照目标与边界，再看证据与风险
- review 不直接偷偷改代码
- `Final recommendation` 只允许 `Accept / Hold / Reject`
- 没有足够证据时，不给 `Accept`

## 记录条件

- 中改及以上任务
- 高风险任务
- 发布前正式审查
- AI 行为变更且需要正式 review 留痕

命中这些条件时，按需把结果写入 `runtime/reviews/*.md`

## 最小正式 review 骨架

```md
# Review Record

## Meta
- Date:
- Task:
- Scope:

## Findings
- ...

## Risks not fully verified
- ...

## Evidence checked
- Commands:
  - `...`
- Results:
  - ...
- Manual checks:
  - ...

## Final recommendation
- Status: `Accept | Hold | Reject`
- Next step:
  - 回 `dev-builder`
  - 回 `bug-fixer`
  - 回 `dev-planner`
  - 进入 `release-builder`
  - 进入其他 Gate
```

## Verification Evidence

```md
## Verification Evidence

### Environment
- local / CI / staging

### Commands
- `...`

### Results
- pass / fail / partial

### Manual Checks
- ...

### Not Verified Yet
- ...
```
