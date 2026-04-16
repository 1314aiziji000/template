# Scenario: git-upload-logger

## 正例

- 输入：真实本地 `git add / commit / push` 结果
- 预期：写入 `runtime/logs/YYYY-MM-DD.md`

## 反例

- 条件：上传失败、部分成功或有人试图缩小上传边界
- 预期：日志照实记录，且不能改写范围

## 验证重点

- 当前上下文与承接快照合并
- 真实 Git 结果引用
- `runtime/releases/` 与 `runtime/logs/` 分流
