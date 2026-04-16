# runtime

## 作用

- 本目录是 `V3` 的正式结果对象层
- `runtime/README.md` 是混合文档：只做对象定位和必要硬边界
- 本文件不拥有对象内部字段或任务流程；细节以各 `runtime/*.md` owner 文档为准

## 当前对象

- `PLANS.md`：单活跃长任务的当前计划，也承接 bootstrap 初始化结论
- `code_review.md`：默认 review 协议
- `plans/`：多活跃长任务计划目录
- `reviews/`：正式审查记录
- `errors/`：错误与返工记录
- `releases/`：发布与交付记录
- `adr/`：关键结构决策记录
- `logs/`：skill 驱动日志落点，默认承接上传批次记录
- `evolution/`：进化提议、归档和已确认的 lesson / strategy 记忆

## 边界

- `runtime/*.md` 只定义对象是什么、什么时候创建、和谁不同
- `runtime/` 不定义任务怎么跑，不替代 workflow、protocol 或 skill
- `runtime/logs/` 只作为 skill 驱动日志落点，不替代 review、release、error 或 ADR
- `runtime/evolution/` 只承接 proposal、archive 和已确认 memory；不替代原始 incident 记录
- 只在命中条件时创建或更新对象
