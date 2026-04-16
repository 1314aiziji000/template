# self-memory-staging

本目录是 `self-memory` 的本地 staging。  
它只承接原始对话投递与 manifest 台账，不进入默认正式真相源。

## 当前约定

- `raw/`：本地投递的 `.md` / `.txt`
- `manifests/`：覆盖率、提取与 purge 台账

## 边界

- `raw/` 与 `manifests/` 不进 Git
- raw 不是长期对象；完成提取、生成报告并核对后，应在 `72` 小时内 purge
- purge 后的 manifest 只保留最小元数据
