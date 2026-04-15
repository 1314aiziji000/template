# release-retro

## 进入条件

- 改动已通过主要验证
- 需要交付、部署或正式发布
- 需要沉淀错误、决策或复盘

## 什么时候进入本流程

下面这些任务默认进入正式发布或交付路径：

- 构建产物交付
- 部署
- 配置切换
- 面向用户或下游的版本更新

下面这些任务虽然不一定发布，但也可能进入本流程的沉淀部分：

- 明确错误或返工
- 关键结构决策
- 阶段回顾后需要升级规则

## 发布与收口要求

发布任务必须额外带：

- `Release Card`
- 冒烟检查
- 回滚路径

正式收口至少满足：

- 当前目标已完成
- 验证证据明确
- review 结论明确
- 剩余风险已说明
- 下一步是否继续已清楚

## 记录系统路由

- `runtime/reviews/`：正式审查结果
- `runtime/errors/`：错误、返工原因、反复模式和可升级教训
- `runtime/releases/`：正式发版或交付节点
- `runtime/adr/`：关键结构决策
- `docs/logs/`：如果仓库本身已有日志规则，继续沿用原规则

## 进化策略

`V3` 默认不自动跑 evolution。  
任务结束后和阶段回顾时，只做人工确认后的规则升级。

值得升级的信号包括：

- 同类错误重复出现
- 同类 review 意见反复出现
- 同一类验证动作反复手动执行
- 同一类 AI 行为回归反复暴露

升级顺序固定为：

`workflow / skill-template / shared-protocol / checklist / scripts -> skill -> hooks -> 自动 evolution`

## 关键步骤

- 补最小 `Release Card`
- 明确冒烟检查与回滚路径
- 判断是否要沉淀到 `runtime/errors/`、`runtime/releases/`、`runtime/adr/`
- 判断是否有规则、脚本或 skill 需要升级

## 出口产物

- 发布检查结果
- 正式记录或复盘入口
- 下一轮改进项
- 需要时把改进项回流到 workflow、skill-template、shared-protocol 或 script
