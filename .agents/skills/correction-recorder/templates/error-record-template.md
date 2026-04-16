# 错误记录模板

建议文件：

- `runtime/errors/YYYY-MM-DD-事件名.md`

建议骨架：

```md
---
id:
created_at:
signal_type:
source_skill:
severity:
related_records:
  - runtime/reviews/
  - runtime/logs/
---

# 错误记录标题

## 问题现象
- 

## 触发场景
- 

## 根因判断
- 

## 影响范围
- 

## 修复动作
- 

## 防再发建议
- 
```

使用要求：

- `related_records` 只引用真实 `runtime/` 记录
- 单次 incident 只写当前事实，不提前扩写成跨 incident 规律
