# protocols

本目录只放 `V3` 的共享协议入口与跨 skill gate 模板。  
这里只定启用条件和固定字段，不展开长样例。

## 当前范围

- 共享 gate 模板继续放这里，例如：
  - `adr-lite-template.md`
  - `security-checklist.md`
  - `ai-eval-template.md`
- 单一 skill 直接拥有的私有模板，不再平铺在本目录，而是放回对应 skill：
  - `.agents/skills/dev-planner/templates/plans-template.md`
  - `.agents/skills/code-review/templates/review-template.md`
  - `.agents/skills/release-builder/templates/release-card-template.md`

## 与运行层的关系

- 共享 gate 模板写在这里
- skill 私有模板写在对应 `.agents/skills/` 目录
- 协议对应的运行对象放在 `../runtime/`
- 例如计划对象最终落到 `../runtime/PLANS.md`，review 运行协议最终落到 `../runtime/code_review.md`
