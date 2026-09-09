# 手动安装与工具参考

主 WorldRole 连接不需要 Python。想启用额外来源或本地申请工作流时，安装以下本地补充 MCP（Python 3.11+）：

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

在 [examples/with-free-sources.json](../examples/with-free-sources.json) 中，把占位符换成上述可执行文件的**绝对路径**，再按客户端格式合并。保留远程 `worldrole`，额外添加本地 `worldrole-free-sources`。

| 补充工具 | 用途 | 是否需要密钥 |
|---|---|---|
| `search_free_jobs` | Himalayas / Jobicy / Arbeitnow，选源、缓存、链接去重、排除已看岗位、部分失败提示 | 不需要 |
| `list_free_company_jobs` | 获取已知公司的 Greenhouse / Ashby / Lever 招聘板 | 不需要 |

例如：“WorldRole 的结果不够时，再用免费来源查一下 Python 远程岗位；不要发送我的简历内容作为搜索词。”

这些来源有各自的限流、更新周期和使用要求。ATS 查询需要从公司招聘页得到 board ID，并不是全网关键词搜索。不要自动轮询所有来源。详见 [来源与分页](../docs/SOURCES.md)。

本地 0.2.0 的申请工具：

| 工具 | 用途 |
|---|---|
| `get_application_capabilities` | 查看本地能力，优先复用已有邮箱 |
| `prepare_application` / `get_applications` | 保存及修改草稿、校验附件、查看申请与待处理队列 |
| `send_application` | 在用户授权范围内通过可选 SMTP 发送，核对内容指纹、防重复投递 |
| `prepare_application_followup` | 检查邮箱后，准备一次已到期的线程内跟进 |
| `record_application_event` | 保存已有邮箱工具的真实回执，记录回复、拒信与本人交接 |
| `sync_application_replies` | 可选 IMAP 精确匹配回复引用头，收到非自动回复后暂停跟进 |


[WorldRole connection](../INSTALL.md) · [Agent installation](../INSTALL_FREE_SOURCES.md) · [Mail setup](APPLICATIONS.md) · [Contributing](../CONTRIBUTING.md)
