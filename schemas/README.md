# schemas

## 作用

- 本目录放机器可校验契约
- `schemas/README.md` 是混合文档：只做契约定位和必要硬边界
- 本文件不拥有具体 schema 字段；具体契约以目录内正式 schema 文件为准

## 边界

- `docs/protocols/` 负责给人看的 gate、固定字段和证据要求
- `schemas/` 负责给脚本、测试、评测或实现共同依赖的结构契约
- 不放叙述性设计说明
- 不放运行记录

## 联动

- 改 `schemas/` 时，检查 `docs/protocols/`、`docs/integrations/`、`src/`、`tests/`、`evals/` 是否要同步
- `schemas/steering/` 负责 `error record`、`evolution proposal`、`evolution memory` 的机器契约
