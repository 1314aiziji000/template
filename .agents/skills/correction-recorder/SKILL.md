---
name: correction-recorder
description: 仅在用户明确纠正 AI、要求把高价值错误 / 返工 / 越权 / 边界误判正式写入 `runtime/errors/`，或在 `release-retro` 固定节点明确要求沉淀单次 incident 时使用。默认只允许手动触发或在 `release-retro` 固定节点触发。
---

# correction-recorder

## 作用

- 负责把单次高价值 incident 正式写入 `runtime/errors/`
- 不替代 `bug-fixer`、`code-review`、`steering-runner`

## 输入

必读：

- 当前任务要求
- `README.md`
- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/workflows/release-retro.md`
- `runtime/errors/README.md`
- `.agents/skills/correction-recorder/templates/error-record-template.md`

按需读取：

- 当前任务相关的 `runtime/reviews/`、`runtime/logs/`、`runtime/releases/`
- 当前会话里已经形成的错误事实、返工动作和验证结果

## 硬规则

- 只允许手动触发，或在 `release-retro` 固定节点触发
- 一次 incident 默认写一个文件，不跨 incident 合并
- 只记录值得复用或会影响后续治理的错误
- 记录事实、根因、修复和防再发建议，不复写完整聊天流水
- 需要跨 incident 聚合时，交给 `steering-runner` 处理，不在这里提前下结论

## 输出

- 单次 incident 的结构化错误记录
- 是否值得进入后续进化扫描的判断

## 正式落点

- 默认写入 `runtime/errors/YYYY-MM-DD-*.md`

## 退出条件

- 已形成单次 incident 的正式记录
- 或已明确判断当前问题不值得建档
