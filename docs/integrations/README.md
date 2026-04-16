# integrations

## 作用

- 本目录放正式外部接入说明
- `docs/integrations/README.md` 是混合文档：只做接入定位和必要硬边界
- 目录仅在当前存在或已启用时纳入联动

## 边界

- 这里收口接入目标、权限边界、协议映射和联动入口
- 不写密钥、token 或真实敏感配置
- 不写只存在于聊天里的临时口头结论
- 具体固定字段和最低证据回到 `docs/protocols/`
- 机器契约回到 `schemas/`

## 联动

- 改接入边界时，检查 `docs/workflows/`、`docs/protocols/`、相关 `.agents/skills/`、`schemas/`、`prompts/`、`evals/` 是否要同步
