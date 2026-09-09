# Free source contracts

Verified against the providers' public documentation on 2026-09-10. Free access can be rate limited or change. This repository provides adapters, not a republished job database.

| Source | Official documentation | Adapter scope |
|---|---|---|
| WorldRole | https://worldrole.work/install.md | Separate hosted MCP, guest access without a key; account profile and limits via boardwork_start |
| Himalayas | https://himalayas.app/docs/remote-jobs-api | Public search API; q/country/page; display attribution and https://himalayas.app |
| Jobicy | https://jobicy.com/jobs-rss-feed | Public recent feed, up to 200 rows; one shared hourly local cache, local keyword matching, retain Jobicy URLs |
| Arbeitnow | https://www.arbeitnow.com/blog/job-board-api | Public European job feed, page parameter; local keyword matching within one page |
| Greenhouse | https://docs.greenhouse.io/job-board.html | Public GET /v1/boards/{board}/jobs; known company board only |
| Ashby | https://developers.ashbyhq.com/docs/public-job-posting-api | Public GET /posting-api/job-board/{board}; known company board only |
| Lever | https://github.com/lever/postings-api | Public GET /v0/postings/{board}; US and EU regions, skip/limit pagination |

## Pagination and limits

Himalayas search returns a provider page. The local limit truncates that page; use limit=20 to retain its usual maximum before advancing. The adapter reports truncation and does not invent a last-page indicator. Its browse API supports opaque cursors but is not used by this search adapter. API data is cached/refreshed daily; avoid repeated identical queries within a day. Honor HTTP 429 and stop rather than retrying in a loop.

Greenhouse and Ashby expose complete board responses; adapters download up to 8 MiB and slice results with offset/limit. Lever paginates remotely; a full response produces a candidate next offset, which may return an empty list. Board IDs come from actual careers links. No automatic board enumeration or name-based company merging is performed.

All public-source network operations use HTTPS, fixed provider hosts, a 20-second timeout and an 8 MiB response limit. Redirects are rejected. Only public job keywords and board IDs are sent. These source adapters do not use login credentials, submit applications or fetch arbitrary URLs. Separate optional mail tools are described in [APPLICATIONS.md](APPLICATIONS.md).

Each result carries source_url, retrieval time and applicant_eligibility=not_checked. Retrieval is not independent company verification. Source location restrictions and salary periods are preserved, not interpreted as guarantees. Missing fields remain unknown. Keep each provider's attribution when combining results and deduplicate by known canonical job URL/ID, not company name alone.

## Reuse and licensing

Adapter code is original and MIT licensed. Provider job text and data remain subject to provider terms and rights; MIT does not grant redistribution rights to third-party data. This project does not copy code from JobOps, Shortlist or other job MCP implementations. The skill is maintained by WorldRole and based on its published 0.5.0 workflow, with this repository's optional-source guidance added.

## Multi-source discovery in 0.2.0

`search_free_jobs(sources=["himalayas","jobicy","arbeitnow"])` explicitly opts into a small multi-source batch. The default remains Himalayas. Results are interleaved, exact URL duplicates removed, and `exclude_urls` applied locally. Errors remain in per-source reports. A provider outage is not a successful zero-result search.

Himalayas responses are cached locally for 24 hours. Other feed responses are cached for one hour; different Jobicy queries reuse the same latest-200 feed, including across process restarts. Failed requests are also cached to prevent repeated retries. Cache entries expire and successful writes retain at most 256 entries. Public source payloads are stored under the private data directory with hashed URL keys; it is not a personal-profile store.

Jobicy has no page 2 in this adapter. Arbeitnow exposes one provider page per call; its next link is converted to an integer next page, never followed as an arbitrary URL. Feed matching requires all supplied words in the title or bounded summary. This improves free coverage but may miss relevant results outside the page/summary. Country filtering applies only to Himalayas; the agent must inspect location restrictions for the other feeds. Never treat missing restrictions as worldwide eligibility. Returned retrieval timestamps reflect assembly time; cache freshness windows are disclosed separately.
