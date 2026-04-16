# V3 Validation Pack

本目录承接当前 `V3` 的多模式验证。
它是临时验证包，不是正式真相源；稳定结论需要回填到 `V3/` 本体或父级 `V3真相源.md`。

## 目标

- 用两种仓态覆盖当前 12 个 skill
- 跑通一条完整闭环：
  `bootstrap -> intake -> dev-planner -> dev-builder -> code-review(Hold) -> bug-fixer -> code-review(Accept) -> release-builder -> git-upload-logger -> context-handoff`
- 追加验证 `correction-recorder -> steering-runner -> evolution memory`
- 追加验证 `user-dialogue-analyst` 的 `extract -> batch -> report -> purge`
- 追加验证 `skill-validator` 的官方基础校验 + 项目增强校验闭环
- 复核父级 `V3真相源.md` 是否与当前 `V3/` 一致
- 复核新的规则分层是否成立：
  - `AGENTS.md` 只保留常驻规则
  - skills 的 `description` 承担路由契约
  - `SKILL.md` 仍是主契约，`agents/openai.yaml` 是官方增强层
  - `docs/workflows/` 只保留阶段骨架
  - `docs/protocols/` 只保留共享 gate

## 目录

- `acceptance.manifest.yaml`：自动 gate 清单
- `modes/`：测试模式说明
- `scenarios/`：每个 skill 的正反例场景
- `reports/`：本轮验证结果
- `artifacts/`：新增 steering / self-memory 的样本输入与生成物

## 执行顺序

1. 跑基线脚本预检查
2. 进入 `source-mode` 跑 `project-bootstrap`
3. 基于初始化完成态跑 skill 覆盖和闭环
4. 跑 `skill-validator` 生成 skills 官方化报告
5. 回写父级 `V3真相源.md`
6. 重新跑基线检查，确认口径收口

说明：

- 当前 `V3/scripts/verify.sh` 在检测到本清单时，会自动串起 `run_validation_pack.py`
- 若只想单独回放自动 gate，也可直接运行 `python scripts/run_validation_pack.py`

## 自动 Gate

- 12 个 skill 都有对应 scenario，且每个 skill scenario 至少带 `正例 + 反例 + 验证重点`
- `source-mode-fixture` 与 `closure-fixture` 均可过 `verify.sh`
- 至少 1 份 skills 官方化报告，覆盖：
  - 全量 `quick_validate.py`
  - 全量 `interface` 可重建性
  - 全量 `policy.allow_implicit_invocation`
  - 旧 `.codex/skills` 残留扫描
- `steering` 阈值回归样本能稳定产出 `1` 条 `rule-graduation` proposal，且不会误产出单次 `protocol-hardening`
- `self-memory` 样本能稳定跑通 `raw -> extract -> batch -> report -> purge`

## 当前仍需人工复核的项

- 父级 `V3真相源.md` 与当前 `V3/` 的措辞、范围和分层说明是否完全对齐
- 自动 gate 未覆盖的可读性问题：
  - 文档是否足够直白
  - 解释是否过重
  - 是否还有对提交边界、交付边界的歧义表述

## 说明

- `artifacts/` 承接可回放的样本输入、样本输出和验证报告
- `sandboxes/`、`remotes/` 只用于本轮执行，默认不纳入版本管理
- 本目录是模板维护用验证包；若项目副本已移除本包，`verify.sh` 会跳过这组自动 gate
