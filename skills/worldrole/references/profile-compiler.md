# Career profile compiler — evidence-rich V1 summaries

This guide changes how the host agent summarizes, not the Profile V1 schema. Keep the existing twelve natural-language fields, provenance state, versioned patch protocol, 500-character field limit and 8192-byte merged-profile limit. Omitted fields are preserved; null deletes only on explicit user intent. Do not add fact/item hierarchies, confidence scores or normalized salary/skill fields. Instructions and examples are not evidence about the current user.

## Preserve decision-useful evidence

For each representative capability, preserve: what the user can do; what they personally did; the result or operational depth; and important limits. Prefer a few concrete contributions over a list of project names or technologies. Distinguish personal implementation, leadership, team output and AI-assisted work. Do not attribute all team or agent output to the user, infer production deployment from a prototype, or invent dates, metrics, seniority or proficiency. Qualitative outcomes are useful when numbers are unavailable.

Keep material eligibility constraints and conditional preferences first where needed for matching. Within career evidence, prioritize results, personal contributions, system complexity/production depth and known limits over project names, technology lists, titles and employer names. This ordering is a compression aid, not permission to discard material facts. Preserve currencies, time periods and qualifications of numeric claims; approximate self-reported results remain approximate self-reports.

## One home per fact

Use direction for desired work; skills for reusable abilities and depth; experience for representative contributions and outcomes; education for education; languages for actual reading/writing/speaking and translation needs; location_authorization for residence and work permission; salary for conditional pay expectations; availability for timing/time zones; preferences for priorities; constraints for exclusions; materials for document knowledge/access; next_step for the next action. Avoid repeating the same remote-work preference or project in several fields. A brief cross-reference is enough if needed. Do not spill experience into unrelated fields to bypass length limits.

Preserve conditions: willingness to consider a particular salary for a suitable international role is not a permanent salary floor. A preferred country is not an exclusive location. Unknown authorization or unconfirmed technical depth is valuable when it changes the next decision; omit irrelevant checklist gaps.

## Understanding is not independent verification

Detailed user-reported accounts can provide strong understanding of claimed contributions, results and boundaries without third-party proof. Preserve user_reported provenance and the lack of independent verification; do not lower career understanding solely because there is no audit, payslip, public repository or resume attachment. Missing contribution detail, ambiguous scope or contradictions can reduce understanding. Do not force a score upward: assess actual available evidence, using integer bands rather than copying a previous agent's score. Understanding scores, match scores and hiring probabilities are different concepts.

Materials must distinguish known existence, contents actually read, known version, current access and readiness for the specific application. A remembered resume is not an available attachment, and a restored summary does not restore files. Missing originals affects material knowledge, not necessarily career understanding. Follow the existing verification workflow for actual applications and commitments; never relabel a self-report as independently verified.

## Merge and recompress

Read current fields and classify new information as addition, correction or conflict. Recompose affected fields to preserve valid old evidence and useful additions while removing semantic repetition; do not blindly append. Keep provenance unchanged unless new accessible evidence actually supports a change. With only one state per field, do not label a mixed field document_supported when it contains unsupported claims. Keep unresolved inference separate in natural language and do not insert it as an established fact; omit it or defer the conflicting update if V1 cannot represent it safely.

Before saving, check each field length and the UTF-8 byte size of the complete merged profile, not just the patch. Deduplicate and shorten wording before dropping evidence. Never truncate mid-sentence silently. If important evidence still cannot fit, retain the current profile and surface the specific tradeoff instead of expanding the schema. Re-read before saving and preserve intervening corrections, deletions and paused memory as described in profile-sync.md. No semantic improvement means no write.

## Handoff check

Read the draft as if you had no other history. Can it explain suitable role families, concrete evidence, personal contribution, important unknowns, self-reported claims, whether job exploration can start, and whether application files are actually accessible? Do not invent five examples if fewer are known. Repair keyword-only passages from accessible evidence before saving. A score alone is not acceptance. Keep only information whose absence would materially worsen another agent's career decisions, not full chats, project logs or attachments.
