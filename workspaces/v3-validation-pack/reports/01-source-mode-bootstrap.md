# 01-source-mode-bootstrap

## Sandbox

- 路径：`workspaces/v3-validation-pack/sandboxes/source-mode-fixture/`
- 状态：ignored sandbox，只用于本轮验证

## 正例执行

1. 从当前 `V3/` 复制出 source sandbox
2. 补入一份已填写的 `项目说明书.md`
   - 模式：`Medium`
   - Packs：只保留 Core + `schemas/` + `resources/` + `runtime/logs/`
3. 在 bootstrap 前执行：
   - `bash scripts/verify.sh`
   - 结果：通过
   - 关键输出：`Detected bootstrap-ready template mode`
4. 按 `project-bootstrap` 的规则在 sandbox 内执行一次性初始化：
   - 写回 `runtime/PLANS.md`
   - 删除 `项目说明书.md`
   - 删除 `.agents/skills/project-bootstrap/`
   - 裁剪未启用的 `docs/integrations/`、`docs/ui/`、`prompts/`、`evals/`
5. 在 bootstrap 后执行：
   - `bash scripts/verify.sh`
   - 结果：通过
   - 关键输出：`Detected initialized project mode`

## 反例 / 守卫验证

- 初始化完成后的 source sandbox 中：
  - 根级已无 `项目说明书.md`
  - `.agents/skills/` 中已无 `project-bootstrap`
  - `docs/` 下只保留 `README.md`、`protocols/`、`workflows/`
- 这说明同一个 sandbox 已经不再满足 bootstrap 触发条件，后续必须回到日常主链

## 执行备注

- 第一次复制 sandbox 时误排除了整个 `workspaces/`，导致 `verify.sh` 报缺少 `workspaces/README.md`
- 修正 sandbox 准备方式后，source-mode 与 initialized-mode 都能通过 `verify.sh`
- 这个问题属于测试夹具准备问题，不是 `V3` 模板结构问题

## 结论

- `project-bootstrap` 的正例与退出守卫都已覆盖
- source-mode 到 initialized-mode 的切换成立
