# prompts

本目录用于 Prompt 物料。  

## 什么时候启用

- 项目存在系统 Prompt、角色 Prompt、工具调用 Prompt 或输出约束 Prompt
- Prompt 变更需要进入 `AI Eval Gate`

## 建议内容

- Prompt 文件正文
- 适用场景说明
- 版本或变更说明
- 与对应 eval case 的关联

## 使用边界

- Prompt 物料是正式对象，不放到 `workspaces/` 长期悬空
- Prompt 变更后要同步更新 `evals/` 与相关模型配置说明
