# release-retro

## 定位

本文件只描述发布、交付和沉淀阶段骨架。
具体发布条件与固定字段看 `release-builder` 和 `docs/protocols/release-gate.md`；错误、决策和规则升级仍回写正式对象。
本文件只回答阶段顺序、进入条件、必备产物和下一跳，不写 release-builder 内部规则。

## 进入条件

- 改动已通过主要验证
- 需要交付、部署或正式发布
- 需要沉淀错误、决策或复盘

## 本阶段关注什么

- 当前任务是不是真正进入正式交付路径
- 发布条件是否齐备
- 哪些正式记录需要写回 `runtime/`
- 是否需要通过固定节点触发 `correction-recorder` 或 `steering-runner`
- 是否需要把复盘结论升级回规则层

## 记录系统路由

默认正式记录只走下面这些目录：

- `runtime/reviews/`：正式审查结果
- `runtime/errors/`：错误、返工原因、反复模式和可升级教训
- `runtime/releases/`：正式发版或交付节点
- `runtime/adr/`：关键结构决策
- `runtime/logs/`：`git-upload-logger` 维护的上传批次记录与必要节点日志，不替代上面 4 类专项记录
- `runtime/evolution/`：经确认的进化提议、归档和 lesson / strategy 记忆

## 进化策略

阶段复盘后，如果出现以下情况，可以把结论升级回规则层：

- 同类错误反复出现
- 多次 review 都指出同一类缺口
- 当前模板字段不足以承接真实任务
- 当前脚本或 gate 经常被手工补位

升级顺序建议仍保持：

`workflow / skill-template / shared-protocol / checklist / scripts -> skill -> 更强自动化`

## 阶段骨架

1. 判断当前是不是正式交付路径
2. 通过 `release-builder` 统一收口发布条件
3. 根据任务类型写入 `runtime/releases/`、`runtime/errors/`、`runtime/adr/`
4. 命中 Git / GitHub 上传节点时，由 `git-upload-logger` 写入 `runtime/logs/`
5. 如有需要，在本固定节点手动触发 `correction-recorder` 或 `steering-runner`
6. 如有需要，把复盘结论升级回 workflow、protocol、skill 或脚本

## 本阶段必须产出

- 当前交付结论
- 对应正式记录
- 剩余风险与后续动作
- 需要时的规则升级建议

## 退出去向

- 正式交付完成
- 回到前一环补条件
- 进入规则升级或后续任务
