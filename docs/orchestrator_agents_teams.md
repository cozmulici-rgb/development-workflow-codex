# Multi-Team Agentic Coding: Orchestrator, Agents & Teams

## Architecture: Three-Tier Hierarchy

```
Orchestrator (Opus - best model)
  ├── Planning Lead (Opus)
  │     ├── Planner Worker (Sonnet)
  │     └── ...
  ├── Engineering Lead (Opus)
  │     ├── Frontend Developer (Sonnet)
  │     └── Backend Developer (Sonnet)
  └── Validation Lead (Opus)
        ├── QA Engineer (Sonnet)
        └── Security Reviewer (Sonnet)
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
- **Name** and **Model** (Opus for leads/orchestrator, Sonnet for workers)
- **Expertise** — persistent mental model file, loaded at boot, updated after each session
- **Skills** — composable, shared across agents where needed
- **Tools** — e.g., `delegate` for orchestrator and leads
- **Domain** — read/write access boundaries per agent

## Key Concepts

### Domain Locking
- Agents can only read/write within their assigned directories
- Frontend dev: read everything, write only frontend directory
- Backend dev: read everything, write only backend directory
- Planning lead: read entire codebase, write only to expertise directory; must delegate all file changes
- Enforced via hooks system (Pi hooks or Claude Code hooks)

### Agent Expertise (Mental Models)
- Each agent maintains its own expertise file — a persistent, growing memory
- Loaded at the start of every session (read tool calls at boot)
- Agents autonomously update their mental model after each session
- Contains high-level observations: patterns noticed, risks, architecture notes, key decisions
- **Not micromanaged** — agents decide what's relevant to track
- Expertise can be a list: one updatable mental model + additional read-only expertise files (e.g., billing workflows, migration rules)
- Compounds over time — the more you use a team, the more specialized it becomes

### Skills (Composable Prompts)
Key shared skills:
- **Zero Micromanagement** — shared by orchestrator and all leads; delegate, never execute
- **Conversational Response** — shared by orchestrator and leads (not workers); keeps responses concise
- **Active Listener** — all agents read conversation log before every response
- **Mental Model** — guidelines for maintaining expertise files

Workers intentionally lack the conversational response skill — they should be verbose and detailed.

### Delegation Flow
1. User talks only to orchestrator
2. Orchestrator delegates to relevant team lead(s)
3. Lead reads context, delegates to workers
4. Workers execute, report back to lead
5. Lead composes results, reports to orchestrator
6. Orchestrator synthesizes all team results into a unified response

### Session Management
- Each session has a directory with:
  - Conversation log (JSONL) — visible to all agents
  - Tool call logs per team
  - Starting system prompts (for debugging/transparency)
  - Shared workspace for agent outputs (e.g., eval results, specs)

## Model Strategy

| Role | Model | Reasoning |
|------|-------|-----------|
| Orchestrator | Opus (best available) | Coordination requires highest intelligence |
| Team Leads | Opus | Thinking, planning, decision-making |
| Workers | Sonnet | Instruction following and execution |

Leverage the 1M context window — don't be afraid to spend tokens on context loading.

## System Prompt Composition

Variables injected at runtime before agent loads:
- Session directory path
- Conversation log path
- Teams configuration (from YAML)
- Tools definitions
- Expertise file paths
- Skills content (extracted from frontmatter into system prompt)

## Workflow Pattern: Plan → Build → Validate

A reusable prompt/command that:
1. Planning team creates the plan
2. Engineering team implements
3. Validation team reviews (QA + security)

Each phase runs through the full delegation hierarchy.

## Next-Generation Ideas

- **Meta agent/team** — helps fine-tune and improve other teams
- **Team-based slash commands** — reusable workflows designed for multi-team execution
- **Specialized read-only expertise** — inject domain knowledge (billing, migrations, DevOps) as non-updatable files
- **Domain-locked specialists** — DevOps agent is the only one that touches DevOps files
- **Fine-tuned mental model skills** — teach agents exactly how to track results relevant to their domain

## Core Principles

1. **Spend tokens to win** — load full context, use powerful models for leads
2. **Trust and scale** — specialize agents until you trust them to ship on Enter
3. **Agents that learn** — mental models compound over sessions
4. **Configuration over code** — teams are defined in YAML, easily modified
5. **Domain boundaries** — prevent agents from touching code outside their scope
6. **Cognitive load stays flat** — adding more agents doesn't increase user effort (single orchestrator interface)
7. **Build where the ball is going** — models get smarter and cheaper; invest in the architecture now
