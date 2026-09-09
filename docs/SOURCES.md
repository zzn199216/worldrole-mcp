# Free source contracts

Verified against the providers' public documentation on 2026-09-10. Free access can be rate limited or change. This repository provides adapters, not a republished job database.

| Source | Official documentation | Adapter scope |
|---|---|---|
| WorldRole | https://worldrole.work/install.md | Separate hosted MCP, guest access without a key; account profile and limits via boardwork_start |
| Himalayas | https://himalayas.app/docs/remote-jobs-api | Public search API; q/country/page; display attribution and https://himalayas.app |
| Greenhouse | https://docs.greenhouse.io/job-board.html | Public GET /v1/boards/{board}/jobs; known company board only |
| Ashby | https://developers.ashbyhq.com/docs/public-job-posting-api | Public GET /posting-api/job-board/{board}; known company board only |
| Lever | https://github.com/lever/postings-api | Public GET /v0/postings/{board}; US and EU regions, skip/limit pagination |

## Pagination and limits

Himalayas search returns a provider page. The local limit truncates that page; use limit=20 to retain its usual maximum before advancing. The adapter reports truncation and does not invent a last-page indicator. Its browse API supports opaque cursors but is not used by this search adapter. API data is cached/refreshed daily; avoid repeated identical queries within a day. Honor HTTP 429 and stop rather than retrying in a loop.

Greenhouse and Ashby expose complete board responses; adapters download up to 8 MiB and slice results with offset/limit. Lever paginates remotely; a full response produces a candidate next offset, which may return an empty list. Board IDs come from actual careers links. No automatic board enumeration or name-based company merging is performed.

All network operations use HTTPS, fixed provider hosts, a 20-second timeout and an 8 MiB response limit. Redirects are rejected. Only public job keywords and board IDs are sent. No login credentials, application submissions or external arbitrary URL fetches are supported.

Each result carries source_url, retrieval time and applicant_eligibility=not_checked. Retrieval is not independent company verification. Source location restrictions and salary periods are preserved, not interpreted as guarantees. Missing fields remain unknown. Keep each provider's attribution when combining results and deduplicate by known canonical job URL/ID, not company name alone.

## Reuse and licensing

Adapter code is original and MIT licensed. Provider job text and data remain subject to provider terms and rights; MIT does not grant redistribution rights to third-party data. This project does not copy code from JobOps, Shortlist or other job MCP implementations. The skill is maintained by WorldRole and based on its published 0.5.0 workflow, with this repository's optional-source guidance added.
