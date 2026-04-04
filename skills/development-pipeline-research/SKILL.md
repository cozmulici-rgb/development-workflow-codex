---
name: development-pipeline-research
description: Start the development pipeline in the research phase by decomposing the ticket into factual repo questions, using only the research lead and matching research subagent references.
---

# Development Pipeline Research

## Use this skill when
Use this skill when the user wants to begin a new workstream in the research phase and no approved design or plan exists yet.

## Workflow
1. Load `../development-pipeline/references/research-lead.md` first.
2. Load only the matching `../development-pipeline/references/research-subagent-*.md` files needed for the ticket's architecture, pattern, integration, domain, API, testing, and optional fintech questions.
3. Produce factual findings about the repository, dependencies, constraints, and unknowns.
4. Stop after research outputs are ready for human review; do not design or implement code in this phase.

## Boundaries
- Treat research as fact-finding, not solution design.
- Do not write production code in this phase.
- Escalate missing facts and unresolved questions explicitly.
