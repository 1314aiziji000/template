# guardrail-mode

## 用途

- 专门验证每个 skill 的阻断条件和边界
- 防止“会跑”但边界失控

## 关注点

- `project-bootstrap`：缺少一次性输入时不能重入
- `dev-planner`：`Small + Low Risk` 不被误抬级
- `dev-builder`：边界失控时必须回 planner
- `bug-fixer`：无失败证据不能硬修
- `code-review`：证据不足不能给 `Accept`
- `release-builder`：缺 review / 缺验证必须阻断
- `context-handoff`：不能混淆生成承接和接收承接
- `git-upload-logger`：不能擅自缩小上传范围
