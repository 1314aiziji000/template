# errors

本目录用于错误、返工和判断失误记录。

## 最小内容

- 问题现象
- 触发场景
- 根因判断
- 影响范围
- 修复动作
- 防再发建议

## 边界

- 只有值得留痕或可复用时才建档
- 一次性小偏差且无复用价值的问题，不必机械建档
- 命中 `correction-recorder` 时，默认一条 incident 写一个文件；跨 incident 聚合交给 `steering-runner`
- 需要规则升级时，再把结论回推到 workflow、skill、protocol 或脚本
