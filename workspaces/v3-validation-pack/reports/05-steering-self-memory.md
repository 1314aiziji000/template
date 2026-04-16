# 05-steering-self-memory

## 目标

- 为新增的 `correction-recorder`、`steering-runner`、`user-dialogue-analyst` 补充首版回归样本
- 覆盖 `runtime/evolution/`、`self-memory` 和 staging 的关键硬约束

## 回归案例矩阵

1. `correction-recorder` 正例：高价值 incident 正式建档
2. `correction-recorder` 反例：一次性小偏差不建档
3. `steering-runner` 正例：同类 incident `3` 次触发 `rule-graduation`
4. `steering-runner` 反例：不足阈值时闭嘴
5. `steering-runner` 守卫：proposal 只允许一个 `target_owner`
6. `steering-runner` 守卫：proposal 必须带 `source_records`
7. `steering-runner` 守卫：未确认 proposal 不得写入 lesson
8. `self-memory` 正例：一份 raw 对应一份 extract
9. `self-memory` 正例：月 batch 汇总多个 extract
10. `self-memory` 正例：达到阈值时生成 periodic report
11. `self-memory` 反例：未达到门槛时上传节点应安静跳过
12. `self-memory` 守卫：raw purge 后只保留最小 manifest

## 样本输入

- steering 输入：`artifacts/steering/errors/`
- self-memory raw：`artifacts/self-memory/raw/`

## 预期结果

- steering 样本能生成 `1` 条 `rule-graduation` proposal
- 单次 `protocol-gap` 样本不会误触发 proposal
- 两份 raw 样本能生成 `2` 份 extract、`1` 个月 batch、`1` 份 periodic report
- purge 后 manifest 只保留最小元数据
