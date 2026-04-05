# Multi-Team Agentic Coding: Orchestrator, Agents & Teams

## Architecture: Three-Tier Hierarchy

```
Orchestrator (lead-tier model)
  ├── Planning Lead (lead-tier model)
  │     ├── Planner Worker (worker-tier model)
  │     └── ...
  ├── Engineering Lead (lead-tier model)
  │     ├── Frontend Developer (worker-tier model)
  │     └── Backend Developer (worker-tier model)
  └── Validation Lead (lead-tier model)
        ├── QA Engineer (worker-tier model)
        └── Security Reviewer (worker-tier model)
```

- **Orchestrator** — single interface, delegates to team leads, composes final results
- **Leads** — thinkers/coordinators, delegate to workers, never execute raw file changes
- **Workers** — execute tasks, verbose and detail-oriented

## Configuration

YAML config file defines the entire system:
- Orchestrator: system prompt path, model
- Teams: each has a lead (system prompt + name), team color, and members (system prompt paths)
- Adding/removing teams = updating the config file

## Agent Anatomy (Frontmatter)

Each agent has:
- **Name** and **Model profile** (lead-tier for orchestrators/leads, worker-tier for execution agents)
- **Workflow context** — current conversation plus explicit repo artifacts from prior phases
- **Skills** — composable, shared across agents where needed
- **Tools** — e.g., `delegate` for orchestrator and leads
- **Domain** — read/write access boundaries per agent

## Key Concepts

### Domain Locking
- Agents can only read/write within their assigned directories
- Frontend dev: read everything, write only frontend directory
- Backend dev: read everything, write only backend directory
- Planning lead: read entire codebase, write only approved planning artifacts; must delegate implementation changes
- Enforced via hooks system (Pi hooks or Claude Code hooks)

### Agent Context And Handoffs
- Persistent per-agent memory is out of scope for this repository
- Agents rely on the active conversation, the current repo state, and explicit artifacts written by prior phases
- Durable handoff state should live in repo artifacts such as research docs, design docs, plan directories, boundary policies, implementation handoff packages, and validation outputs
- If additional state is needed, write it into a named repo artifact instead of assuming an implicit runtime memory layer

### Skills (Composable Prompts)
Key shared skills:
- **Zero Micromanagement** — shared by orchestrator and all leads; delegate, never execute
- **Conversational Response** — shared by orchestrator and leads (not workers); keeps responses concise
- **Active Context Reader** — all agents use the current conversation and explicit phase artifacts before acting
- **Artifact Discipline** — shared rules for writing durable state into explicit repo outputs

Workers intentionally lack the conversational response skill — they should be verbose and detailed.

### Delegation Flow
1. User talks only to orchestrator
2. Orchestrator delegates to relevant team lead(s)
3. Lead reads context, delegates to workers
4. Workers execute, report back to lead
5. Lead composes results, reports to orchestrator
6. Orchestrator synthesizes all team results into a unified response

### Session Management
- The packaged workflow guarantees only artifacts explicitly written into the repo or produced by the current command flow
- The current conversation is the only guaranteed transient shared context
- Optional local logs or session directories may exist in the surrounding environment, but they are not part of the plugin contract and must not be relied on by packaged prompts

## Model Strategy

| Role | Model | Reasoning |
|------|-------|-----------|
| Orchestrator | Lead-tier model | Coordination requires the strongest reasoning available in the active Codex environment |
| Team Leads | Lead-tier model | Thinking, planning, decision-making |
| Workers | Worker-tier model | Instruction following and execution |

Leverage the 1M context window — don't be afraid to spend tokens on context loading.

## System Prompt Composition

Variables injected at runtime before agent loads:
- Teams configuration (from YAML)
- Tools definitions
- Available repo artifacts for the current phase
- Skills content (extracted from frontmatter into system prompt where supported by the host)

## Workflow Pattern: Plan → Build → Validate

A reusable prompt/command that:
1. Planning team creates the plan
2. Engineering team implements
3. Validation team reviews (QA + security)

Each phase runs through the full delegation hierarchy.

## Next-Generation Ideas

- **Meta agent/team** — helps fine-tune and improve other teams
- **Team-based slash commands** — reusable workflows designed for multi-team execution
- **Specialized reference packs** — inject domain knowledge (billing, migrations, DevOps) as explicit repo references or packaged skill references
- **Domain-locked specialists** — DevOps agent is the only one that touches DevOps files
- **Fine-tuned artifact discipline skills** — teach agents exactly how to record durable results in repo artifacts relevant to their domain

## Core Principles

1. **Spend tokens to win** — load full context, use powerful models for leads
2. **Trust and scale** — specialize agents until you trust them to ship on Enter
3. **Artifacts over implicit memory** — durable state should live in explicit repo outputs
4. **Configuration over code** — teams are defined in YAML, easily modified
5. **Domain boundaries** — prevent agents from touching code outside their scope
6. **Cognitive load stays flat** — adding more agents doesn't increase user effort (single orchestrator interface)
7. **Build where the ball is going** — models get smarter and cheaper; invest in the architecture now
