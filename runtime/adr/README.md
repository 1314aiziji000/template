# adr

本目录用于 `ADR-Lite` 记录。  
它是运行对象，不属于 `docs/` 说明层。  

## 什么时候写入

- 跨模块结构调整
- 新建公共抽象
- 替换关键依赖
- 改核心接口契约
- 会影响后续多轮迭代的设计决策

## 文件建议

- 命名：`YYYY-MM-DD-决策名.md`
- 一次关键决策对应一个文件

## 最小内容

- `Context`
- `Decision`
- `Alternatives considered`
- `Consequences`
- `Follow-up`

## 使用边界

- 局部实现细节不必升级成 ADR
- 一旦写入本目录，后续相关实现和 review 都应以该决策为准
