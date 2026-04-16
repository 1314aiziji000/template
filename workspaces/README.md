# workspaces

本目录放临时施工、试验和草稿内容。  
它不是正式真相源，定稿后必须回填到正式目录。

## 当前约定

- `workspaces/v3-validation-pack/`：模板验证包
  - `acceptance.manifest.yaml` 与 `reports/08-validation-pack-automation.md` 承接自动 gate 清单和结果
- `workspaces/self-memory-staging/`：本地原始对话投递与 manifest staging

## 边界

- `workspaces/self-memory-staging/` 只承接本地 raw / manifest，不回写 AI 正式对象
- 原始对话成功提取并生成报告后，应按规则 purge，只保留最小 manifest 元数据
