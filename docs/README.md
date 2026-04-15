# docs

本目录只放 `V3` 的说明文档。  
这里负责解释流程怎么跑、协议怎么用，不负责承载运行中的正式记录对象。

## 递进式展开

- 先看 `workflows/`，决定任务当前处于哪一段
- 再看对应 `.agents/skills/` 目录，读取当前 skill 的私有模板或辅助脚本
- 再看 `protocols/`，决定这一段需要哪些共享 gate
- 命中条件后，回到 `../runtime/` 去使用 `PLANS.md`、`plans/`、`reviews/`、`errors/`、`releases/`、`adr/`

## 阅读顺序

1. `docs/README.md`
2. `docs/workflows/README.md`
3. 对应 workflow 正文
4. 对应 `.agents/skills/` 目录
5. `docs/protocols/README.md`
6. 对应共享 protocol 正文
7. 需要时再回到 `../runtime/` 运行对象

## 分层职责

- `workflows/`：写任务怎么流转、什么时候抬级、每一步产出什么
- `.agents/skills/`：写单一 skill 的私有模板、私有脚本和局部工序说明
- `protocols/`：写跨 skill 共用的 gate 协议、固定字段和证据格式
- 正式记录和多计划对象不放在 `docs/`，统一放到 `../runtime/`

## 使用边界

- `docs/` 负责解释和收口，不替代正式实现
- 流程规则先于单次聊天记忆
- 正式记录和计划目录只在命中条件时创建，不为了“看起来完整”而空铺对象
