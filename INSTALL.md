# 安装 WorldRole：把这份说明交给你的 AI

WorldRole 帮你寻找跨境工作，在聊天中了解你的求职方向，并在你准备投递、试做或签约时指导 AI 核验机会。默认游客可直接用；注册后仍免费，可使用更多信息和精简云端档案。

## 给负责安装的 Agent

这是通用的 Agent 安装包，包含标准 `SKILL.md`、参考流程和 MCP 连接描述；不是某个客户端专用的可执行程序或原生插件。安装只需你已有的文件与配置能力，无需安装 Python、Node 或本地 WorldRole 服务。

1. 识别当前客户端和版本，检查其 MCP、Agent Skills 支持及实际配置位置。按当前客户端的正式配置方式安装；不要猜路径或覆盖整个配置文件。用户只说“安装 WorldRole”时，默认游客；用户已选注册或已有有效个人密钥时，保留该选择。
2. 获取 https://worldrole.work/downloads/worldrole-bundle.json ，下载其中的 HTTPS 安装包，并核对 SHA256。这个清单是 WorldRole 的包描述，不是所有客户端自动识别的插件格式。解压前检查成员路径不能越界，不执行压缩包内任意程序。包只有文本文件。
3. MCP 名称 `worldrole`，地址 `https://mcp.worldrole.work/mcp`，传输 `Streamable HTTP`。游客完全省略 Authorization。保留其他 MCP 和现有 WorldRole 密钥；已有相同连接就复用。客户端只支持 stdio 时，不要把 HTTPS 地址当成命令：查看该客户端支持的桥接方式，说明尚缺的能力；不要无依据引入一个 npm 包。
4. 支持 Agent Skills：将包内 `skills/worldrole/` 完整安装到该客户端可发现的用户技能目录，保留 references 相对路径。修改前保存仅受影响配置的本地私有备份；相同版本不重复安装。有同名但内容不同的技能时先检查并合并本地修改，不能直接覆盖。不要修改其他 skill、全局指令、权限或自动执行策略。
5. 不支持技能文件：MCP 仍可用。通过 `boardwork_start` 获取流程，需要核验时读取资源 `worldrole://guides/verification` 或 prompt `worldrole_verify`。如果资源和 prompt 也不支持，读取 https://worldrole.work/guides/verification.md 。明确告诉用户是否具备持久化 skill，不把一次读取冒充安装完成。
6. 用户需要账号时，打开 https://mcp.worldrole.work/join 注册，从 https://mcp.worldrole.work/account 生成密钥，配置 `Authorization: Bearer <个人密钥>`。请用户在客户端安全输入或私有配置中粘贴一次，不在聊天、截图、网址或日志展示密钥，不把密钥放进共享项目。不要重复执行 OAuth，也不要把有效密钥改成游客。其他排错见 https://worldrole.work/setup.md 。
7. 重载该连接（必要时告知需重启客户端），实际读取工具列表、调用 `boardwork_start`，再调用 `search_jobs(count=1)`。应能看到 8 个工具，普通客户端仍可用；支持的客户端还可看到 1 个 prompt 和 1 个指南资源。确认 skill 已被客户端发现，不只确认文件存在。若当前环境不能重载，说明配置已写入、连接验证待重启，而不是声称全部成功。
8. 简短报告：MCP 是否连通、skill 是否已安装/可发现、搜索浏览能力是否可用。然后根据用户目标开始交流，不要求先填简历表。缺少搜索能力不阻止查询数据库，但不能声称实时核验过雇主。安装没有授权代投递、联系雇主、发送私人材料或付费。

## 配置描述

安装包的 `mcp.json` 只描述连接能力。常见 `mcpServers` JSON 示例见 `examples/mcpServers.json`；它不是对所有客户端通用的配置文件。TOML 或其他格式请使用客户端自己的 MCP 配置能力，将同一个地址正确映射进去。客户端已连接其他服务器时只合并 worldrole 条目。

## 更新和移除

更新时读取清单版本，保留有效密钥和本地修改，只更新 WorldRole 技能文件及必要连接字段。检查清单不会自动授权后台更新。MCP 返回当前流程，通常不需要每次更新都重新安装 skill。

移除时仅删除此次安装的 worldrole MCP 条目和对应技能；保留其他配置。移除连接不删除云端档案；用户希望清空档案时，先通过已连接 MCP 明确执行 `delete_profile`。不要上传本地安装备份。
