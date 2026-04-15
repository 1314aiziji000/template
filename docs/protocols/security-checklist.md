# security-checklist

## 启用条件

- 命中 `security`
- 命中 `data`
- 命中 `public-api`
- 命中 `infra`
- `ai-behavior` 且涉及外部数据或工具权限

## 固定检查项

- secret / token / 临时值排查
- 依赖安全检查
- 输入校验
- 鉴权边界
- 日志脱敏
- 外部权限最小化
