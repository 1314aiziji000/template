# code_review.md

## 文件定位

本文件是 `runtime/` 下的 review 协议。  
正式审查记录归档到 `runtime/reviews/`。

## 固定输出顺序

1. `Findings`
2. `Risks not fully verified`
3. `Evidence checked`
4. `Final recommendation`

## 结论定义

- `Accept`：目标达成，证据足够，剩余风险已说明
- `Hold`：方向可接受，但仍缺验证、修正或关键信息
- `Reject`：目标未达成，或证据不足以支持当前结论

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
