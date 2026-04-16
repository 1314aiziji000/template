# security-lite

## 命中条件

- `security`
- `data`
- `public-api`
- `infra`
- `ai-behavior` 且涉及外部数据、凭据或工具权限

## 最低检查

1. 运行 `bash scripts/security-check.sh`
2. 对照 `security-checklist.md` 复核共享安全项
3. 明确当前任务涉及的权限边界、输入校验、日志脱敏、secret 使用和外部依赖风险

## 证据要求

- 已执行的检查命令
- 当前发现的问题或剩余风险
- 当前是否允许继续实施、审查或发布

## 正式落点

- 审查留痕：`runtime/reviews/`
- 可复用错误教训：`runtime/errors/`
- 发布相关结论：继续回到 `release-builder`
