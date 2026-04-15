# workflows

本目录放任务从接入到收口的流程骨架。  
这里只写流程顺序、抬级条件、进入条件、退出条件与最小产物，不展开协议字段细节。

## 阅读顺序

1. `intake.md`
2. `build-verify-review.md`
3. `release-retro.md`

## 主链关系

`V3` 的默认主链是：

`intake -> build / verify / review -> release / retro`

其中：

- `intake` 负责判断当前任务走不走计划路径、会不会命中门禁
- `build-verify-review` 负责把实施、验证、审查和修正连成正式闭环
- `release-retro` 负责发布、交付、记录沉淀和规则升级

## 使用原则

- workflow 先回答“怎么流转”，不抢对应 skill 私有模板或共享 protocol 的字段职责
- 一条 workflow 写清进入条件、关键步骤、出口产物和升级条件
- 命中高风险、发布、AI 行为变更时，workflow 必须明确指向后续 `Gate`
