# bootstrap-checklist

## 使用方式

- 读取根级 `项目说明书.md` 后，用本清单收口
- 先给用户确认，再执行裁剪与删除
- 最终结论必须写回 `runtime/PLANS.md`

## 项目判断

- 项目名称：
- 项目类型：
- 目标用户 / 交付形态：
- 当前初始化模式：`Small / Medium / Large`

## 模式判定

### `Small`

- 目标：最小起盘
- 保留：Core + 最少 Optional Packs
- 输出：精简版 `runtime/PLANS.md`

### `Medium`

- 目标：标准起盘
- 保留：Core + 已启用 Optional Packs
- 输出：首份正式 `runtime/PLANS.md`

### `Large`

- 目标：深度起盘
- 保留：Core + 已启用 Optional Packs
- 输出：多阶段初始化结论写入 `runtime/PLANS.md`

## Optional Packs 决策

- 默认保留：`schemas/`、`resources/`、`runtime/logs/`
- [ ] `docs/integrations/`
- [ ] `docs/ui/`
- [ ] `prompts/`
- [ ] `evals/`

未勾选项在用户确认后可从项目副本删除。

## 根级入口适配

- `README.md` 已贴合当前项目
- `AGENTS.md` 已贴合当前项目
- `PROJECT_RULES.md` 已贴合当前项目

## 写回 `runtime/PLANS.md`

- 当前项目模式：
- 已启用 Packs：
- 命名 / 文档架构适配结果：
- 非目标：
- 下一步动作：

## 删除清单

- [ ] 根级 `项目说明书.md`
- [ ] `.agents/skills/project-bootstrap/`
- [ ] 未启用 Optional Packs

## 最终确认

- 用户已确认初始化方案
- 项目副本已恢复为干净的日常主链状态
