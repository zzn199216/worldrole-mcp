# 安装 WorldRole

把本说明交给负责安装的 AI。远程 MCP + Skill 包不需要本地 Python 或 Node；游客可直接使用，注册后可保存精简职业档案。

## 安装与验证

1. 检查当前客户端的 MCP、Skill 支持和真实配置位置。只修改 WorldRole，保留其他配置、权限、有效密钥和本地修改；为受影响配置留私有备份。
2. 读取 https://worldrole.work/downloads/worldrole-bundle.json ，下载 HTTPS 包并核对 SHA256。检查解压路径不能越界。包是通用文本文件，不是任意客户端都能自动识别的原生插件。
3. 添加或复用 `worldrole`：地址 `https://mcp.worldrole.work/mcp`，传输 `Streamable HTTP`。游客省略 Authorization。账号用户可在 https://mcp.worldrole.work/account 生成密钥，私下配置 `Authorization: Bearer <key>`；支持 OAuth 的客户端也可申请 `boardwork:read profile:manage`。保留已有效的连接，不重复注册或切回游客。密钥不进入回复、日志、公开仓库或 URL。
4. 支持 Skill 时，安装完整 `skills/worldrole/`，保留相对引用。已有修改先比较合并。不支持 Skill 时，通过 `boardwork_start` 的流程及 https://worldrole.work/guides/ 继续使用，不把一次读取冒充持久安装。仅支持 stdio 时按该客户端已支持的桥接方法处理，不把 HTTPS 当命令或猜测依赖。
5. 重载连接，实际读取工具列表、调用 `boardwork_start` 和 `search_jobs(count=1)`。后者仅验证连通，不是个性化推荐。确认 Skill 是否被发现；无法重载时说明待完成步骤，不虚报成功。报告 MCP、Skill、客户端搜索能力的实际状态。
6. 进入 Skill 的首次使用流程：恢复已有档案，简短评估当前了解，直接开始有用的工作。了解评估、网页 AI 交接、档案合并与机会核验由对应指南维护，不在安装时重复问卷。安装不授权投递、发信或付费。

## 网页 AI 与账号接续

无法接入 MCP 时，使用 https://mcp.worldrole.work/onboarding ：复制包含已有档案的整理提示词，或生成只读临时链接；将 AI 的 JSON 粘回页面预览、确认保存。输出 JSON 不代表自动回写。不想注册可继续在当前对话工作。

转移到新 Agent 时，按 [交接与同步](https://worldrole.work/guides/profile-sync.md) 定向补齐重要缺口，由接收端整理后保存；不追求两端评分相同。编写摘要按 [档案整理](https://worldrole.work/guides/profile-compiler.md)，首次评估按 [了解度](https://worldrole.work/guides/understanding-scores.md)，投递前按 [核验](https://worldrole.work/guides/verification.md)。

## 更新、移除与可选扩展

更新只替换必要的 WorldRole 文件，保留密钥及本地修改；读取版本不代表授权后台更新。移除只删除 WorldRole 连接和对应 Skill，不自动删除云端档案；用户要求清空时使用 `delete_profile`。

需要免费外部来源或本地申请工具时，另按 https://github.com/zzn199216/worldrole-mcp/blob/main/INSTALL_FREE_SOURCES.md 安装可选 companion；它需要 Python，默认不装。GitHub 配套 Skill 包含扩展流程，不用远程精简包覆盖这些流程。客户端配置示例不能当成所有客户端通用的文件格式。排错：https://worldrole.work/setup.md 。
