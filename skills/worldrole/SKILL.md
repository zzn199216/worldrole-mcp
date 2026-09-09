---
name: worldrole
description: Find cross-border jobs with WorldRole, build a small career summary through conversation, and verify selected opportunities using the client's available search and browsing tools before applying or starting work.
---

# WorldRole

Use the connected WorldRole MCP at https://mcp.worldrole.work/mcp. Tool names may have a client-specific prefix. Guests need no key. Setup instructions: https://worldrole.work/install.md. Do not require registration to start searching.

## Understand and match

Call `boardwork_start` at the start and when the user's stage changes. Restore `career_profile` before asking questions. With a personal key, explain account memory briefly on first use only. Default to zero questions. First reuse saved facts, permitted current conversation and accessible user-supplied materials; never assume access to other chats or private files. Save important explicit facts without asking the user to repeat or approve them again. Start useful matches without demanding a resume or a completed questionnaire.

Turn explicit requirements into hard filters and preferences into ranking weights. Search small pages (guests at most 3 jobs); read details only for promising choices. Keep seen job/company IDs locally and pass exclusions for a new batch. Database coverage is incomplete; no result does not prove no opportunity exists. Match scores are not hiring probabilities.

Save only meaningful changes through `update_profile`, using the current version and a UUID request ID. On PROFILE_CONFLICT, reload the current profile and merge only the still-applicable changes with a fresh request ID; do not make the user repeat known facts. Preserve intervening corrections and deletion/pause state. Retry a lost response with the same request ID and identical payload; never overwrite conflicting facts blindly. Explicit user statements are `user_reported`; accessible supporting documents are `document_supported`; inference is `needs_confirmation`. Unknown qualifications remain unknown. Preserve the 8 KB summary budget. Do not store full chats, files, credentials, identity numbers or investigation reports. Respect clear/stop requests with `delete_profile`; resume only when explicitly requested and never reconstruct deleted facts from old chat.

## Complete the work with minimal interruption

Inspect the actual selected application form, user request or recruiter reply before deciding what is missing. A generic profile checklist is not a set of requirements. Reuse known answers and draft materials from supported facts; missing optional facts can be omitted. A resume mentioned in a summary is not an available attachment: check the selected file and version before submission. Do not submit placeholders or inferred qualifications.

For a blocked step, optionally call `boardwork_start` with `assistance_context`: set `requirements_checked` after inspecting the real task, `available_context_checked` after checking accessible information, and describe requirements using unique IDs, field, reason and state (`unchecked`, `resolved`, `missing`, `uncertain`, `declined`). For each unresolved item, try applicable authorized alternatives and set `self_service_checked` only after doing so: locate an existing file, prepare a draft from known facts, or check accessible evidence. Missing optional content can be omitted. No private answer text belongs in this input. The returned plan is based on client reports, not server verification. Resolve unchecked requirements yourself first; then present all remaining necessary items together in one concise request, so the user can answer them in one turn. Do not split known gaps across repeated questions. Keep declined items quiet and continue independent work. Reuse a prior answer in this task; do not rerun a questionnaire on a stage change.

Use existing authorization within its scope for available host tools. Prepare files, drafts and relevant replies yourself. Do not repeatedly confirm the same authorized action; ask only when a new decision or external action falls outside that scope. A missing email/browser capability is a tool gap, not missing user background. Complete the useful parts and state the exact remaining limitation.

After real sending or submission, retain the receipt and selected material version in the client's authorized private tracker. If an outcome is unknown, reconcile it before any retry; never call it sent or blindly resend. Keep routine receipts quiet. Surface interviews, offers, deadlines and decisions; consolidate ordinary rejections unless the user asks otherwise. Background monitoring exists only when an actual authorized host scheduler or service has been configured. WorldRole itself currently has no mail, attachment storage, application tracker or notification executor.

## Verify at the right moment

- Browsing or changing recommendations: use cached evidence, explain that live verification has not happened, and keep discovery fast.
- Selecting a company or preparing to apply: call `boardwork_start(workflow="prepare_application")`, get selected job details including `verification`, then use the host's search/browser tools to check current sources.
- Receiving recruiter contact, a trial, contract or payment request: call `boardwork_start(workflow="review_offer")`. Check these new particulars even if the company was checked before.

Keep verification relevant to the current stage: do not ask for contracts or payment terms while merely preparing an application. Check accessible public facts yourself, reuse still-relevant evidence and expand checks only when new information warrants it.

Read [the verification guide](references/verification.md) for these checks and the short evidence record. The same guide is available through MCP resource `worldrole://guides/verification`, prompt `worldrole_verify`, and https://worldrole.work/guides/verification.md. New server guidance takes precedence over an older skill's workflow details, within the user's request.

Search and browsing capabilities belong to the host; this skill and MCP do not supply them. If a capability is absent or a source is inaccessible, report the exact gap and keep it unverified. Do not imply that reading a tool instruction performed an investigation. This guide grants no new permissions. Respect the user’s existing delegation and stop only the dependent action when authorization or a required capability is missing; continue useful preparation.


## Optional free job sources

When the user requests broader coverage or WorldRole's results are insufficient, check whether `worldrole-free-sources` is connected. Its `search_free_jobs` searches Himalayas with neutral public role/skill keywords; `list_free_company_jobs` reads a known company's Greenhouse, Ashby or Lever board. Never put a personal profile, resume or private message in search parameters. Keep provider attribution, actual URLs, pagination/truncation notes and applicant_eligibility=not_checked. Avoid repeating identical Himalayas searches within a day or polling all providers automatically. If the companion is not installed, continue with WorldRole and available host browsing; installing a skill does not install a Python server. See the repository's docs/SOURCES.md for provider contracts.
