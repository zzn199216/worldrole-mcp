# WorldRole MCP

**让 AI 帮你找工作、整理求职资料，必要缺项一次补齐。**

免费连接 [WorldRole](https://worldrole.work) 的远程 MCP；需要更广覆盖时，可选接入本仓库的免费职位源 MCP，直接查询 Himalayas、Greenhouse、Ashby 和 Lever。

English: [README.en.md](README.en.md)

## 直接开始，无需安装本地服务

把下面这句话交给支持 MCP 的 Agent：

> 请按 https://worldrole.work/install.md 安装 WorldRole。优先使用免费游客模式，保留其他连接和已有密钥，然后根据我们已经聊过的目标和经历帮我找工作。先用已知资料，自己能完成的先完成；剩余必要资料一次告诉我，让我集中补齐。

远程地址：`https://mcp.worldrole.work/mcp`，传输 `Streamable HTTP`。游客不需要 API Key，完全省略 Authorization。注册账号后可免费使用账号额度和个人摘要；免费有额度限制，不代表无限请求。实际限额以 `boardwork_start` 返回为准。你的 Agent / 模型供应商可能另外收费。

常见 JSON 配置见 [examples/mcpServers.json](examples/mcpServers.json)。不同客户端配置格式不同，按客户端支持的 MCP 配置方式合并，不能覆盖整个配置。完整说明见 [INSTALL.md](INSTALL.md)。

## 会帮用户做什么

- 查找和比较有来源的工作机会，保留地区、工作许可、工资等限制。
- 在用户允许记忆时，从当前对话和已提供资料补充精简档案，复用已经了解的信息。
- 先准备能完成的材料；剩余必要缺项集中补问，避免反复问一项。
- 选定岗位后指导 Agent 检查实际招聘页；来信和 offer 到来时按阶段核验。
- 使用宿主已具备的工具，在用户已有授权范围内继续工作。

WorldRole 云端提供 8 个工具：`boardwork_start`、`search_jobs`、`get_jobs`、`get_company`、`search_companies`、`get_profile`、`update_profile`、`delete_profile`。**实际工具名以连接后的 tools/list 为准。**

本仓库包含客户端连接资料、[Agent 技能](skills/worldrole/SKILL.md)及独立的免费来源适配器。它不包含 WorldRole 云端账号服务、后台采集器或招聘数据库，不会在本地启动这些后台服务。

## 可选：添加其他免费职位源

主 WorldRole 连接不需要 Python。只有想启用额外来源时，才安装以下本地补充 MCP（Python 3.11+）：

```sh
git clone https://github.com/zzn199216/worldrole-mcp.git
cd worldrole-mcp
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\worldrole-free-sources.exe
```

macOS / Linux：

```sh
.venv/bin/python -m pip install .
.venv/bin/worldrole-free-sources
```

最后一行是 stdio MCP 进程，等待客户端协议输入属于正常现象；通常由 MCP 客户端启动，不需手动常驻终端。

在 [examples/with-free-sources.json](examples/with-free-sources.json) 中，把占位符换成上述可执行文件的**绝对路径**，再按客户端格式合并。保留远程 `worldrole`，额外添加本地 `worldrole-free-sources`。

| 补充工具 | 用途 | 是否需要密钥 |
|---|---|---|
| `search_free_jobs` | 用公开岗位关键词查询 Himalayas，可传国家和页码 | 不需要 |
| `list_free_company_jobs` | 获取已知公司的 Greenhouse / Ashby / Lever 招聘板 | 不需要 |

例如：“WorldRole 的结果不够时，再用免费来源查一下 Python 远程岗位；不要发送我的简历内容作为搜索词。”

这些来源有各自的限流、更新周期和使用要求。ATS 查询需要从公司招聘页得到 board ID，并不是全网关键词搜索。不要自动轮询所有来源。详见 [来源与分页](docs/SOURCES.md)。

## 隐私和能力范围

- 游客查询无需账号；云端档案需要个人密钥。个人密钥只放客户端私有配置，不能提交到 GitHub。
- 本地补充 MCP 仅发公开 GET 请求，不保存档案、简历或查询数据库。关键词、公司 ID 会发给对应提供方。
- 地区匹配、雇主身份和岗位有效性仍需核验；“remote”不等于全球可申请。
- 当前不提供收发邮件、自动提交申请、后台跟进或通知执行器。技能只能协调宿主实际可用且已获授权的能力。
- 第三方数据不因本仓库采用 MIT 许可而变成 MIT 数据；显示结果时保留来源及链接。

## 开发和贡献

安装后运行 `python -m unittest discover -s tests -v`。测试使用模拟数据，并验证真实本地 stdio MCP 协议，不调用付费服务。

欢迎通过 Issues 反馈安装体验、公开来源失效和适配建议。请不要上传个人简历、邮件、凭证或服务器日志中的隐私内容。详情见 [CONTRIBUTING.md](CONTRIBUTING.md)。

原创代码与技能使用 [MIT License](LICENSE)。
