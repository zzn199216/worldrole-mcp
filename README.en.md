# WorldRole MCP

[简体中文](README.md) | **English**

**Let your AI help you find work and organize your career profile. Fill in essential missing details together, instead of answering repeated questions.**

Connect to the free [WorldRole](https://worldrole.work) hosted MCP. For broader coverage, optionally add this repository's local job-source MCP to query Himalayas, Jobicy, Arbeitnow, Greenhouse, Ashby and Lever, and manage private application drafts, receipts and replies locally.

## Get started without a local server

Give this request to an MCP-capable agent:

> Install WorldRole following https://worldrole.work/install.md. Prefer free guest access and preserve my other connections and any existing key. Then help me find work using the goals and experience we have already discussed. Reuse known information and finish what you can yourself. Collect any remaining essential missing details into one request so I can provide them together.

The remote endpoint is `https://mcp.worldrole.work/mcp`, using `Streamable HTTP`. Guests need no API key: omit Authorization entirely. A free account provides account quotas and a concise career summary. Free access is rate limited, not unlimited; check the limits returned by `boardwork_start`. Your agent or model provider may charge separately.

See [examples/mcpServers.json](examples/mcpServers.json) for a common JSON configuration. Client formats vary: merge the WorldRole entry using your client's supported MCP settings rather than replacing the entire configuration. Detailed agent installation instructions are in [INSTALL.md](INSTALL.md) (Chinese).

## What it helps with

- Find and compare sourced opportunities while retaining location, work authorization and salary restrictions.
- When the user allows memory, build a concise career profile from the current conversation and supplied materials, reusing known facts.
- Prepare what can be completed first, then ask for the remaining essential details together.
- Guide the agent through checking actual job pages before applying, and stage-appropriate verification when recruiter messages or offers arrive.
- Continue work using tools available in the host and within the user's existing authorization.

The hosted WorldRole MCP provides eight tools: `boardwork_start`, `search_jobs`, `get_jobs`, `get_company`, `search_companies`, `get_profile`, `update_profile`, and `delete_profile`. **The connected server's tools/list is authoritative.**

This repository contains client connection instructions, an [agent skill](skills/worldrole/SKILL.md), and independent adapters for free public sources. It does not include or start WorldRole's hosted account service, background collector or job database.

## Optional: add other free job sources

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

In [examples/with-free-sources.json](examples/with-free-sources.json), replace the placeholder with the executable's **absolute path**, then merge the entries using your client's configuration format. Keep the remote `worldrole` connection and add the local `worldrole-free-sources` connection.

| Companion tool | Purpose | API key required? |
|---|---|---|
| `search_free_jobs` | Select Himalayas / Jobicy / Arbeitnow, cache results, deduplicate URLs, exclude seen jobs and retain partial failures | No |
| `list_free_company_jobs` | Read a known company's Greenhouse, Ashby or Lever board | No |

For example: “If WorldRole's results are insufficient, try the free sources for remote Python roles. Do not use my resume content as search keywords.”

Each source has its own rate limits, refresh schedule and usage requirements. ATS queries require a board ID obtained from a company's careers page; they are not web-wide keyword searches. Do not automatically poll every source. See [sources and pagination](docs/SOURCES.md).

## From application letters to company replies

Local 0.2.0 application tools:

| Tool | Purpose |
|---|---|
| `get_application_capabilities` | Inspect local capabilities; prefer an existing mailbox connection |
| `prepare_application` / `get_applications` | Save and revise drafts, check attachments, inspect applications and attention queues |
| `send_application` | Optional authorized SMTP sending with exact-content digest and duplicate prevention |
| `prepare_application_followup` | Prepare one due threaded follow-up after checking the mailbox |
| `record_application_event` | Retain real host-mail receipts and record replies, rejections and human handoffs |
| `sync_application_replies` | Optional IMAP reply-header matching; pause follow-up on nonautomatic replies |

For example: “Prepare applications from what you already know about me, and collect essential missing details into one request. Prefer my connected mailbox. Send and handle routine document requests within my authorization; bring interviews, offers and personal decisions to me with context and a suggested reply.”

An existing mailbox tool is usually easiest; SMTP/IMAP is optional. Drafting is not sending, and server acceptance is not delivery. Ongoing checks require a running host scheduler; otherwise checks resume on the next run. See [applications and mail](docs/APPLICATIONS.md) for bilingual setup and boundaries, and [design references](docs/DESIGN_REFERENCES.md) for the projects informing this workflow. Update this repository's [agent skill](skills/worldrole/SKILL.md) for the latest workflow too.

## Privacy and capability boundaries

- Guest searches do not require an account; cloud career profiles require a personal key. Store it only in private client settings, never on GitHub.
- Job-source adapters make public GET requests. Search keywords and board IDs go to the selected provider. Public-response cache and private application records use a separate local directory; application text and attachments are not sent to job sources.
- Applicant eligibility, employer identity and current vacancy status still need verification. “Remote” does not mean applicants worldwide are eligible.
- Optional local mail capabilities require your own mailbox and valid delegation. Full-thread reading, web application forms and background notifications still require host tools. No continuous monitoring starts automatically.
- The repository's MIT license does not make third-party job data MIT-licensed. Retain source attribution and links when displaying results.

## Development and contributions

After installation, run `python -m unittest discover -s tests -v`. Tests use mocked source data and verify the actual local stdio MCP protocol without paid services.

Use Issues to report installation problems, broken public sources or adapter suggestions. Do not upload personal resumes, emails, credentials or private server logs. See [CONTRIBUTING.md](CONTRIBUTING.md).

Original code and the skill are available under the [MIT License](LICENSE).
