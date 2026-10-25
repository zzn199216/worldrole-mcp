# WorldRole marketplace distribution

The free marketplace package connects to the current hosted WorldRole MCP. It does not require payment, registration, a local Python install, or a personal key to start. Daily hosted allowances and other limits apply. The optional local companion remains independently installable without a WorldRole account through [the free-source guide](../INSTALL_FREE_SOURCES.md).

## Install from this public repository

These are direct repository installations. They do **not** imply that a vendor has approved an official directory listing.

| Client | Installation |
| --- | --- |
| Gemini CLI | `gemini extensions install https://github.com/zzn199216/worldrole-mcp` |
| Qwen Code | `qwen extensions install https://github.com/zzn199216/worldrole-mcp` |
| Claude Code | `/plugin marketplace add zzn199216/worldrole-mcp`, then `/plugin install worldrole@worldrole` |
| Codex | Add this repository as a plugin marketplace, then install WorldRole from that source. See the current [Codex plugin instructions](https://developers.openai.com/plugins/build/plugins). |
| Cursor | Use the repository plugin package or the remote MCP URL with the current [Cursor plugin instructions](https://cursor.com/docs/reference/plugins). |
| Grok Build | Its documented Claude plugin compatibility can consume the Claude marketplace in this repository; host-specific installation validation is tracked separately. |
| Other MCP clients | Add `https://mcp.worldrole.work/mcp` using Streamable HTTP with no authorization header for guest access. |

For account features, use a client-supported private key or OAuth connection. Never put a real key in a shared project, public manifest, issue, or URL. Preserve an existing signed-in connection instead of replacing it with guest access.

## Google Antigravity

The standalone plugin directory is [`integrations/antigravity/worldrole`](../integrations/antigravity/worldrole). Clone this repository, then install that directory with `agy plugin install ./integrations/antigravity/worldrole`, or select it using the client's local-directory plugin installer. Do not install the repository root as an Antigravity plugin: its portable manifest serves other clients.

This directory follows Google's [plugin format](https://antigravity.google/docs/plugins) and [MCP configuration](https://antigravity.google/docs/mcp): `plugin.json` identifies the plugin and `mcp_config.json` uses `serverUrl` with Streamable HTTP. No credentials, executable hooks, or payment configuration are bundled. Anonymous access permits 20 distinct hosted jobs per network per UTC day; optional free accounts permit 50, with additional request limits. AI-client charges are separate. The full hosted server exposes optional account features requiring authorization; it does not send applications or emails. See [privacy](PRIVACY.md), [terms](TERMS.md), and [review scenarios](../distribution/review-cases.json).

The endpoint has passed MCP protocol checks. Antigravity in-client installation and execution have not yet been verified; an interest-form submission does not imply Marketplace approval.

## Versions and releases

`distribution/manifest.json` is the source of marketplace metadata. Its version describes the distribution package; `hostedVersion` and `companionVersion` separately identify the service and local Python package. These are different release streams.

Run `python scripts/build_marketplace.py` after changing metadata. Run `python scripts/build_marketplace.py --check --zip` before a release. CI checks generated manifests against the source so platform files cannot silently drift. The ZIP contains only an explicit set of public plugin assets, skills, and documentation.

New approved releases require a new package version. Use the client's extension/plugin updater to receive changes; installed clients may require a restart or user approval. A GitHub release, a submitted application, an approved listing, and an indexed gallery entry are separate states. Do not label a pending submission as live.

## Review scenarios

[`distribution/review-cases.json`](../distribution/review-cases.json) contains five positive and three negative expected scenarios for remote review. They are review instructions, not a claim that every vendor client has passed an end-to-end test. Each actual submission must include the testing evidence and other materials its platform requests.
