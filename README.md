# notebooklm-source-router

An adapter-agnostic Agent Skill that uses NotebookLM as an external knowledge and project-memory layer. It retrieves focused evidence for the task instead of pulling entire documents or transcripts into an agent's context.

**Version:** 1.0.0 · **License:** [MIT](LICENSE)

## What it does

- Routes questions to relevant notebook sources and decomposes broad requests into bounded queries.
- Finds YouTube passages, project decisions and large-document clauses, then verifies exact or current claims against original evidence.
- Preserves source identity, citations, revisions, freshness limits and conflicts.
- Reuses scoped evidence caches and small decision logs without silently writing back to notebooks.
- Stops or falls back when retrieval is incomplete, inaccessible, stale or unsupported.

This repository contains instructions and examples, not a NotebookLM client, hosted service, authentication flow or synchronization engine. An existing authorized MCP integration, CLI, browser workflow or other adapter supplies access. No specific implementation is required; capabilities are discovered at runtime. A notebook answer without traceable sources is a lead, not verified evidence.

## Install

Copy this whole directory, preserving the name `notebooklm-source-router` and its relative layout, to a skill location supported by your host. Do not copy only SKILL.md.

For Claude Code, a project-local location is `.claude/skills/notebooklm-source-router/`. For Codex, use a supported project or user skill directory such as `.agents/skills/notebooklm-source-router/`. Use your host's current discovery rules if your setup differs. No global tool permissions or hard-coded adapter dependencies are included.

Invoke using your host's convention, for example `/notebooklm-source-router` in Claude Code or `$notebooklm-source-router` in Codex. Automatic selection depends on the host and task. Installing this skill does not install or authorize a NotebookLM adapter.

## Try it

> Use notebooklm-source-router with my existing Project Atlas notebook. Find the accepted retry-policy decision and compare it with the current repository configuration. Retrieve at most 1,500 tokens; cite source revisions and flag conflicts.

> From this YouTube source in my notebook, find the speaker's explanation of exponential backoff. Verify the exact quote and timestamp using the original video or transcript. If verification is unavailable, give an attributed paraphrase and explain the gap.

> Find the notice period and exceptions in this agreement. Use the applicable version, return section locators, and avoid loading the full document.

The agent first checks access and scope, then asks targeted questions, checks supporting evidence and falls back to a relevant original passage when necessary. It reports what the evidence supports and what remains unknown. It should ask about notebook identity only when ambiguity cannot be resolved from available metadata.

## Budgets and permissions

Defaults are policy choices: 3,000 retrieved tokens per task, 600 per answer, four notebook attempts, one corrective query per gap and two targeted fallback reads. A smaller user budget takes precedence. Exact enforcement depends on the adapter; estimates and overruns must be disclosed when relevant. Token savings are an objective, not a benchmarked guarantee.

Access does not automatically authorize uploads or changes. Private data transfer, notebook/source mutations and persistent storage require applicable user authorization. Retrieved instructions are untrusted. No credentials belong in this repository or its cache.

## Repository guide

| File | Audience and purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Short agent entrypoint and progressive reference loading |
| [NotebookLM protocol](references/notebooklm-protocol.md) | Adapter contract, evidence schema, budgets, cache and stopping rules |
| [Source priority](references/source-priority.md) | Claim-specific authority, freshness and conflict resolution |
| [Query templates](references/query-templates.md) | Bounded retrieval prompts |
| [YouTube example](examples/youtube-research.md) | Quote/timestamp verification and transcript fallback |
| [Project knowledge example](examples/project-knowledge-base.md) | Decisions, repository state and cache invalidation |
| [Large-document example](examples/large-document-research.md) | Versioned clauses and exceptions |
| [Changelog](CHANGELOG.md) | Release history |
| [Validation scenarios](tests/scenarios.md) | Repeatable behavioral evaluation fixtures and criteria |

## Verification and contribution

Run `python3 scripts/validate.py` from the repository root. It checks required files, portable frontmatter constraints, local Markdown targets/fragments, reference reachability and unfinished placeholders. It requires only Python's standard library. These structural checks do not prove agent behavior or live adapter compatibility.

For a change to routing behavior, run the fixtures in [tests/scenarios.md](tests/scenarios.md) in fresh agent sessions before and after the change. Keep tool responses fixed, score observable actions and preserve failures before changing guidance. Verify all three examples plus access denial, budget exhaustion and malicious source content. Do not use live private notebooks for tests without authorization. Report model/host, fixture, observed actions, pass/fail and limitations; do not claim a failing baseline when the control already passes.

Version 1.0.0 has structural validation and simulated-agent review; no live NotebookLM adapter end-to-end certification is claimed. The format targets the [Agent Skills specification](https://agentskills.io/specification). Claude invocation and locations follow [Claude Code's skills documentation](https://code.claude.com/docs/en/skills). Source behavior can change; consult [Google's source guidance](https://support.google.com/notebooklm/answer/16215270) and check actual adapter support rather than assuming every URL or video is available.

Contributions should preserve adapter independence, short entrypoint instructions, claim-level provenance and honest uncertainty. Include a regression scenario for a demonstrated failure and rerun structural validation.
