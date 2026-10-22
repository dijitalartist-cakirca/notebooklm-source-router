# NotebookLM retrieval protocol

## Adapter contract

This is a conceptual contract, not an API or an implementation requirement. Map it to tools actually available in the host. No particular provider, package, authentication method, MCP name, command or browser is required. Do not install software or bypass access controls to satisfy the contract.

Discover whether the adapter can: identify notebooks; list sources and stable IDs; expose source URLs, revision/import dates and status; query a notebook; constrain source selection; return resolvable citations/passages; limit response length. Record unsupported features as unknown or unavailable. A textual request for a length limit or source restriction is best effort, not an enforced capability.

A minimal query-capable adapter permits discovery. A verified answer additionally needs traceable evidence, either through the adapter or a permitted original-source channel. If multiple notebooks plausibly match, inspect metadata or ask which one; do not search unrelated private notebooks. Use only authorized accounts and relevant sources. If the user provides a notebook ID, confirm identity rather than enumerating everything.

Suggested logical request fields: notebook ID, question, selected source IDs, required revision/as-of date, evidence fields, response budget. Suggested result fields: status, answer, source identities, passages, locators, limitations. These describe data to request, not callable functions.

## Retrieval and context budget

Default policy values below belong to this skill, not NotebookLM product limits. Adapt downward to host limits and upward only when the task warrants it and the user's budget permits.

| Resource | Default ceiling |
| --- | --- |
| Total retrieval content returned/loaded for a task | 3,000 tokens |
| One returned answer | 600 tokens |
| Notebook query attempts across all subquestions, including retries | 4 |
| Corrective queries for the same evidence gap | 1 |
| Original-source fallback reads across the task | 2 targeted reads |

Use the smaller of the user's cap and these defaults. Reserve about one third of the total evidence budget for verification/fallback before querying. Budget counts the entire returned/loaded response, including discovery metadata, source lists, excerpts and cached evidence, even if later discarded. Request targeted metadata or paginate instead of enumerating large inventories; final response and instruction overhead still consume the host context separately. Decomposition does not reset limits. If exact token counts are unavailable, estimate conservatively (for English prose, roughly four characters per token; other languages/code may require more) and label estimates. A requested output cap cannot prevent a tool from returning excess text: select excerpts, avoid loading more, record the overrun and stop retrieval. Track requested, actual returned/loaded and retained totals separately; discarding text does not replenish the budget. For images/video frames use host-reported costs when available; otherwise mark cost unknown and bound frame count, without treating text-character estimates as image-token measurements. Never promise strict token enforcement by an unconstrained adapter.

Stop when every decision-relevant question has adequate evidence, the budget is exhausted, the same gap persists after one narrowing attempt, or an access error prevents progress. A transient error may be retried once within the same total attempt budget; do not loop on authentication, authorization, unsupported-source or missing-caption errors. After exhaustion, provide supported partial findings and the exact missing evidence. Ask to expand scope only when the unresolved part matters.

## Query decomposition

Build a short list of atomic questions tied to the requested outcome, not a source-by-source reading plan. Dependencies come first: identify applicable document/version, retrieve the relevant clause, then compare exceptions. Batch independent questions only if returned claims retain separate provenance and fit the response budget. Start with the narrowest source set; widen only when that set lacks relevant evidence. Deduplicate repeated passages.

## Evidence packet

Retain only fields relevant to the task, but each material claim needs a source and verification state:

```yaml
claim: "Retry limit is 3 at revision abc."
source_id: "repo-config"
source_title: "worker configuration"
original_locator: "config/worker.yaml at commit abc, retry_limit key"
notebook_id: "project-notebook"
notebook_citation: null
source_revision: "abc"
source_updated_at: null
imported_at: null
retrieved_at: "2026-10-22T09:00:00Z"
evidence: "retry_limit: 3"
verification: "original-verified"
limitations: "Current deployed revision unknown; notebook source scope not verified."
```

Example values are illustrative. Allowed verification labels: `original-verified`, `notebook-supported`, `unverified`. These are evidence states, not numerical confidence scores. `original-verified` covers only the inspected claim and revision; it does not prove deployment state. Include source title/ID and an original URL or file/revision locator where available. Keep notebook-local markers separate. If pagination or timestamp alignment is unknown, state it. Do not create a publicly accessible link for private material. Quote only inspected text and limit excerpts to what is necessary.

## Freshness and cache

Imported content may differ from its original. Retrieval time alone proves neither source freshness nor import synchronization. For time-sensitive claims inspect current original evidence or an independently established revision; for historical questions use the requested historical version. Do not invent product-wide automatic synchronization guarantees or fixed validity periods.

Cache key: authorized account/workspace + notebook ID + selected source IDs/revisions + normalized question + as-of requirement + evidence/output constraints. Store only the evidence packet, verification time, expiry/revalidation condition and unresolved questions. Unknown source revision means revalidate before reuse for current-state claims. Invalidate on source edits/removal, changed notebook scope, conflicting evidence, changed task/as-of date, access changes or expiry. Invalidate individual changed packets and recheck every synthesis that depends on them; retain independent valid packets. Do not reuse evidence across permission boundaries. A negative search result expires with the same conditions and cannot establish global absence.

Keep session-local memory by default. Persist only where the task authorizes it, excluding secrets and unnecessary personal data; respect deletion/retention requirements. Do not store whole source text as a cache. Decision-log entry: question → chosen source/revision → evidence state → conflict/fallback reason → result/remaining gap → budget used. A log records reasoning outcomes, not hidden chain-of-thought. Persistence does not authorize notebook writes or third-party uploads.

## Fallback and final response

Use [source priority](source-priority.md) to choose the smallest original passage needed. Read original files for precise code/config, official pages for current public facts, and timestamped transcripts or the video itself for exact video claims. A transcript cannot verify charts or demonstrations visible only on screen. If a permitted fallback is unavailable, say which evidence is missing; do not fabricate a transcript or invoke nonexistent tools.

Return: direct answer; claim-level source locators; distinction between quotation, paraphrase and inference; material conflicts/freshness limits; unresolved gaps. A short answer need not expose every internal query or the full log. Report estimated rather than measured budget use when necessary.
