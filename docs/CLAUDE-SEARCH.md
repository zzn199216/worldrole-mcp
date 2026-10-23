# WorldRole Free Job Search for Claude

Updated 2026-10-24. Maintainer: [zzn199216](https://github.com/zzn199216).

This separate anonymous edition provides five read-only tools: `search_jobs`,
`get_jobs`, `search_companies`, `get_company`, and `get_usage`.

Connect using Streamable HTTP at **https://mcp.worldrole.work/claude/mcp**.
No account, API key, payment method, or local installation is required.
Availability in Claude's public directory is subject to Anthropic review;
this documentation does not claim approval or listing.

## Free limits

20 distinct jobs per network per UTC day, shared with anonymous usage of the
standard WorldRole endpoint. Re-reading a previously counted job does not
consume another distinct job. Request and response-size limits also apply.
`get_usage` reports current allowance and reset information. This edition does
not support account upgrades, account credentials, referrals, or purchases.
Any Claude subscription or AI model charges are separate from WorldRole.

## Examples

- Find up to three remote software engineering jobs and show their original
  links and location restrictions.
- Read the requirements and salary for the first returned job, distinguishing
  known conditions from missing or unverified information.
- Find a named employer in the corpus and show its company details.
- Show my remaining free WorldRole job allowance and reset time.

Results are sourced from WorldRole's existing job corpus, may be cached or
incomplete, and do not establish that a vacancy is still open or that an
applicant is eligible. Original job content belongs to its respective owners.
The tools do not send applications, contact employers, or make hiring decisions.

## Privacy for this edition

The endpoint receives only the tool arguments sent to it: public search terms,
structured job preferences, selected record IDs, and pagination values. It does
not request or access Claude memory, chat history, conversation summaries,
resumes, uploaded files, email, or career profiles. Do not put private documents,
credentials or unrelated conversation text in search arguments.

Account and profile tools, workflow prompts, resources, and referral creation
are unavailable. Authorization and Cookie headers are rejected. This edition
cannot read or write WorldRole career summaries, and does not receive access
to the account database. The existing full edition remains a separate service.

Network addresses are processed to enforce the shared anonymous quota. The
upstream quota table uses a server-side HMAC identifier rather than a plaintext
IP address. Operational quota counters are retained under the shared service's
existing quota bookkeeping; there is no new career-profile or conversation
store in this edition. The facade does not persist tool request or response
bodies and disables HTTP access logging. Network infrastructure and Claude
have their own processing and logging policies. This is not a claim that all
infrastructure is log-free. See also the [general privacy information](PRIVACY.md).

## Testing and troubleshooting

All five tools can be tested without credentials using current public corpus
data. Start with `get_usage`, then `search_jobs` with `count: 1`. Pass its returned
job ID to `get_jobs`, its company name to `search_companies`, and its company ID
to `get_company` with `roles_limit: 0` to avoid consuming additional jobs.
Unknown/private tool names are rejected. For quota errors, consult the returned
allowance/reset information; for transient errors, retry later. `GET` requests
return 405 because this stateless endpoint uses POST requests, not a persistent
server event stream.

Report non-sensitive problems through [GitHub issues](https://github.com/zzn199216/worldrole-mcp/issues).
For security reports, see [SECURITY.md](../SECURITY.md). Never post private data
or credentials in public issues.
