# WorldRole privacy information

Updated 2026-10-24. Maintainer: [zzn199216](https://github.com/zzn199216). Product: [WorldRole](https://worldrole.work).

## Free marketplace plugin

The default plugin connects to `https://mcp.worldrole.work/mcp` without an account or API key. The hosted service receives the tool calls and search filters your agent sends. Send public job keywords and necessary eligibility filters, not full resumes, identification documents, passwords, private correspondence, or unrelated conversation history. Installing this package does not authorize uploading personal files or sending applications.

Anonymous usage is limited per network. The application uses a server-side HMAC of the client network address for its guest quota records; that quota table does not store the plaintext IP address. Network infrastructure necessarily handles connection addresses. This statement is not a claim that all infrastructure is log-free.

## Optional free account and career summary

Account registration, login, and authorization are separate from anonymous use. The account service stores account identifiers, password hashes, authorization and revocation state, and usage counters. Personal API keys are stored as hashes. OAuth and personal keys share the account's usage allowance.

An authorized agent can read, update, and clear the account's structured career summary, limited to 8 KiB. The summary is not a full chat transcript, resume archive, mailbox, or file-sync service. Only request summary access when you want this feature. Use `get_profile` to inspect/export it and `delete_profile` to clear it and pause further storage. Existing read-only OAuth grants do not automatically gain profile permissions. Keys and authorizations can be revoked in the account interface.

## Optional local companion

The separately installed free-source companion sends public search terms or company board identifiers to the selected job providers. It does not need a WorldRole account. Local application drafts and tracking remain in the companion's private data directory. Optional email operations require user-configured mail access and explicit user delegation; an installation alone does not authorize sending. No background monitoring starts merely by installing the plugin.

Your AI client and selected job or mail providers process data under their own policies. Provider links and behavior are documented in [Sources](SOURCES.md) and [Applications](APPLICATIONS.md). WorldRole cannot control the AI client's conversation storage or third-party logs.

## Support

Use [GitHub issues](https://github.com/zzn199216/worldrole-mcp/issues) for non-sensitive support requests. Do not post keys, private profiles, resumes, or mail in public issues. For a private vulnerability report, follow [SECURITY.md](../SECURITY.md). Account owners can clear their career summaries and revoke access through the existing tools and account interface.
