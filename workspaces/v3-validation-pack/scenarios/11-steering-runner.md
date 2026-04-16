# Scenario: steering-runner

## 正例

- 输入：`runtime/errors/` 中同类 incident 达到默认阈值
- 预期：生成单一 `target_owner` 的 proposal

## 反例

- 条件：同类 incident 不足阈值，或证据不能回链
- 预期：安静返回“暂无 proposal”，不制造噪声

## 验证重点

- proposal 状态机合法
- `target_owner` / `target_path` / `source_records` 完整
- lesson / strategy 只有在确认且验证通过后才允许写入
