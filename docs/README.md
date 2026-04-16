# docs

本目录放 `V3` 的正式规则披露。
这里放流程骨架、共享协议、外部接入规则和 UI 规范。

## 放什么

- `workflows/`：只写阶段骨架、人看总览和出口产物
- `protocols/`：只写共享 gate、固定字段和证据格式
- `integrations/`：写外部接入、权限边界、第三方能力和协议衔接
- `ui/`：写 UI 规则、页面标准和交互约束

## 不放什么

- `docs/` 不替代根级入口
- `docs/` 不承担 skill 的路由契约；路由优先依赖各 skill 的 `description`
- `docs/` 不替代 skill 本身
- `docs/` 不承接 `schemas/` 中的机器契约定义
- `docs/` 不承接 `runtime/` 中的正式运行对象
- 外部参考资料放 `resources/`，不把下载材料堆进 `docs/`
- 正式记录和正式计划不写在这里
