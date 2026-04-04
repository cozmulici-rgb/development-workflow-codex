# Implementation Plan: Orchestrator Workflow Alignment

**Based on:**
- Source workflow target: `docs/orchestrator_agents_teams.md`
- Current implementation references: `skills/development-pipeline/SKILL.md`
- Current team map: `skills/development-pipeline/references/teams.yaml`

**Phases:**
| Phase | File | Objective | Dependencies |
|-------|------|-----------|-------------|
| 1 | phase-01.md | Introduce an explicit Codex-native orchestrator and team architecture map | None |
| 2 | phase-02.md | Split implementation execution from validation coordination | Phase 1 |
| 3 | phase-03.md | Make configuration and shared behavior operational in Codex-native assets | Phase 1 |
| 4 | phase-04.md | Add session and memory conventions, then reconcile docs and packaged workflow | Phases 2, 3 |

**Total phases:** 4
**Estimated complexity:** High

**Key constraints:**
- Ignore Claude-specific runtime details such as model names or hook implementations
- Keep the Codex workflow as close as possible to `docs/orchestrator_agents_teams.md`
- Preserve the existing four-phase development pipeline while adding the missing orchestration layer
- Keep every phase boundary-policy derivable with explicit file lists

**Definition of Done (full feature):**
- [ ] A top-level orchestrator entrypoint exists and is documented as the single user-facing coordinator
- [ ] Planning, engineering, and validation team roles are represented explicitly in the shipped workflow
- [ ] Shared behavior currently described only in `teams.yaml` is implemented in Codex-native assets or removed from workflow claims
- [ ] Session and persistent-memory behavior are either implemented in Codex-native form or clearly downgraded from the architecture contract
- [ ] All repo docs and packaged workflow references describe the same operating model

