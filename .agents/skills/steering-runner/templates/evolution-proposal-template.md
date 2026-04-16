# 进化 proposal 模板

建议文件：

- `runtime/evolution/proposals/YYYY-MM-DD-主题.md`

建议骨架：

```md
---
id:
created_at:
status: proposed
proposal_type:
signal_type:
repeat_count:
target_owner:
target_path:
source_records:
  - runtime/errors/
summary:
suggested_change:
validation_plan:
---

# proposal 标题

## 结论摘要
- 

## 为什么是现在
- 

## 证据
- 

## 建议动作
- 

## 待确认项
- 
```

使用要求：

- `status` 只允许合法状态机值
- `source_records` 只引用真实 `runtime/` 对象
- `target_owner` 只能写一个正式 owner
