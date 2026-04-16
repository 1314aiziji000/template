# logs

本目录是 `V3` 的 skill 驱动日志落点。
它默认承接 `git-upload-logger` 输出的 Git / GitHub 上传批次记录。

## 当前角色

- 承接 `runtime/logs/YYYY-MM-DD.md` 这类按天日志文件
- 记录一次上传批次的范围、验证、目标与实际结果
- 按需补少量节点级留痕

## 边界

- `context-handoff` 第一版默认不写这里，只输出承接快照
- 不替代 `runtime/releases/`、`runtime/reviews/`、`runtime/errors/`、`runtime/adr/`
- 不维护第二份 Git 历史；`commit hash`、推送区间和最终结果只写真实 Git 结果
- 不把原始聊天流水直接堆进来

## 使用方式

- 详细触发条件、字段和写法以相关 skill 为准
- 上传批次默认由 `git-upload-logger` 写入或追加
- 正式发布或交付事实仍由 `release-builder` 路由到 `runtime/releases/`
