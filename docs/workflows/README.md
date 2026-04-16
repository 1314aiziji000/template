# workflows

本目录放 `V3` 的 workflow 导航。
owner 在各 workflow 文件；这里不重写 skill 细则。

## 当前范围

- `bootstrap.md`：初始化阶段骨架
- `intake.md`：任务入口骨架与 `Size + Risk` 概览
- `build-verify-review.md`：实施、验证、审查、fix 回环骨架
- `release-retro.md`：发布、交付、正式沉淀、规则升级骨架

## workflow 停笔规则

- 只写阶段顺序、进入条件、必备产物、下一跳
- `intake.md` 仍属 workflow owner；允许最少导航，但不拥有 skill 内部规则
- 路由契约仍以各 skill 的 `description` 为准
- 不写共享 gate 固定字段
- 不新增 companion workflow 来承接 `context-handoff` 或 `git-upload-logger`
