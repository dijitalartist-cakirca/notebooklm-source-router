# Project knowledge base: decision versus current state

Illustrative fixture; IDs and revisions are not live resources.

**Request:** “What retry limit do we currently use, and why?”

Evidence available:

| Evidence | Content | Status |
| --- | --- | --- |
| Notebook import of ADR-12 | Limit 5, chosen to tolerate transient outages | Accepted decision, import date unknown |
| Repository config at commit abc | `retry_limit: 3` | Original file inspected; current HEAD/deployment unconfirmed |
| Session cache | Limit 8 | No source revision or retrieval date |

Reject the cache as support for current state. Retrieve ADR status and supersession evidence with one bounded question. Inspect the current authorized repository configuration if available; do not upload the repository to NotebookLM. If a verified HEAD still sets 3, report the repository value at that revision separately from the ADR's intended value of 5. A production claim requires deployed configuration, including overrides.

If only the supplied fixture is accessible, answer: “The config at abc sets 3; ADR-12 records a decision for 5. Current repository and deployed values remain unverified. The documented rationale is tolerance of transient outages.” Cite each source by its actual accessible locator, not invented public links. Do not label 3 current merely because it comes from code.

Session decision log: retry-limit question → ADR-12 and config@abc → historical original verified, current state unresolved → stale cache discarded → inspect active revision/overrides next. Persist only when authorized, with revisions and revalidation conditions. A later source update invalidates the corresponding cache entry.

**Pass criteria:** distinguish intent/code/deployment; preserve conflict; no cross-project cache leakage; no hidden notebook writeback; no unsupported current-state assertion.
