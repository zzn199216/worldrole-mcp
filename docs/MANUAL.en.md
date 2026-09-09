# Manual installation and tool reference

The primary WorldRole connection does not require Python. Install the local companion if you want additional sources or the local application workflow. It requires Python 3.11+:

```sh
git clone https://github.com/zzn199216/worldrole-mcp.git
cd worldrole-mcp
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\worldrole-free-sources.exe
```

macOS / Linux:

```sh
.venv/bin/python -m pip install .
.venv/bin/worldrole-free-sources
```

The last command starts a stdio MCP process. Waiting for client protocol input is normal; usually your MCP client starts it, so you do not need to keep a separate terminal open.

In [examples/with-free-sources.json](../examples/with-free-sources.json), replace the placeholder with the executable's **absolute path**, then merge the entries using your client's configuration format. Keep the remote `worldrole` connection and add the local `worldrole-free-sources` connection.

| Companion tool | Purpose | API key required? |
|---|---|---|
| `search_free_jobs` | Select Himalayas / Jobicy / Arbeitnow, cache results, deduplicate URLs, exclude seen jobs and retain partial failures | No |
| `list_free_company_jobs` | Read a known company's Greenhouse, Ashby or Lever board | No |

For example: “If WorldRole's results are insufficient, try the free sources for remote Python roles. Do not use my resume content as search keywords.”

Each source has its own rate limits, refresh schedule and usage requirements. ATS queries require a board ID obtained from a company's careers page; they are not web-wide keyword searches. Do not automatically poll every source. See [sources and pagination](../docs/SOURCES.md).

Local 0.2.0 application tools:

| Tool | Purpose |
|---|---|
| `get_application_capabilities` | Inspect local capabilities; prefer an existing mailbox connection |
| `prepare_application` / `get_applications` | Save and revise drafts, check attachments, inspect applications and attention queues |
| `send_application` | Optional authorized SMTP sending with exact-content digest and duplicate prevention |
| `prepare_application_followup` | Prepare one due threaded follow-up after checking the mailbox |
| `record_application_event` | Retain real host-mail receipts and record replies, rejections and human handoffs |
| `sync_application_replies` | Optional IMAP reply-header matching; pause follow-up on nonautomatic replies |


[WorldRole connection](../INSTALL.md) · [Agent installation](../INSTALL_FREE_SOURCES.md) · [Mail setup](APPLICATIONS.md) · [Contributing](../CONTRIBUTING.md)
