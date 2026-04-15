# runtime

本目录是 `V3` 的运行层。  
这里放当前任务直接读写、承接和留痕的运行对象，不放解释型说明文档。

## 当前对象

- `PLANS.md`：单活跃长任务的当前计划
- `code_review.md`：默认 review 协议
- `plans/`：多活跃长任务计划目录
- `reviews/`：正式审查记录
- `errors/`：错误与返工记录
- `releases/`：发布与交付记录
- `adr/`：关键结构决策记录

## 使用原则

- 看规则怎么跑：去 `../docs/`
- 看当前对象怎么承接、怎么留痕：先看本目录
- 运行对象只在命中条件时创建或更新，不为了“看起来完整”而空铺内容

## 阅读顺序

1. `runtime/README.md`
2. `runtime/PLANS.md`
3. `runtime/code_review.md`
4. 需要时再进入 `runtime/plans/`、`runtime/reviews/`、`runtime/errors/`、`runtime/releases/`、`runtime/adr/`
