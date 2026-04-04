# Implementation Plan: Artifact Memory And Handoffs

**Based on:**
- Replaced architecture notes in `docs/orchestrator_agents_teams.md`
- Runtime contract in `docs/codex-agent-memory-and-sessions.md`
- Current packaged workflow references under `skills/development-pipeline/`

**Phases:**
| Phase | File | Objective | Dependencies |
|-------|------|-----------|-------------|
| 1 | phase-01.md | Define a durable handoff-package contract for phase-to-phase coordination | None |
| 2 | phase-02.md | Add explicit artifact-memory files and shared authoring rules | Phase 1 |
| 3 | phase-03.md | Add governance and approval-state rules for durable workflow artifacts | Phases 1, 2 |
| 4 | phase-04.md | Add role-specific context compilers derived from approved artifacts | Phases 1, 2, 3 |
| 5 | phase-05.md | Extend boundary tooling to cover artifact-memory and handoff outputs | Phases 1, 2, 3 |
| 6 | phase-06.md | Add optional maintainer-only session recording that does not affect the packaged contract | Phases 1, 2, 3 |

**Total phases:** 6
**Estimated complexity:** High

**Key constraints:**
- Do not reintroduce hidden per-agent memory or required shared session-log paths
- Keep durable state in explicit repo artifacts with phase-local ownership
- Preserve the existing orchestrator, planning, engineering, and validation split
- Keep every phase boundary-policy derivable with explicit file lists
- Treat optional local tooling as non-contractual unless the package explicitly ships and documents it

**Definition of Done (full feature):**
- [ ] The workflow defines a portable handoff package for every approved phase transition
- [ ] Durable project knowledge can be stored in explicit artifact-memory files instead of implicit agent memory
- [ ] Approval state and freshness rules exist for durable workflow artifacts
- [ ] Role-specific context can be compiled deterministically from approved artifacts
- [ ] Boundary tooling can enforce artifact-memory and handoff write scope
- [ ] Optional session recording, if added, is clearly documented as maintainer-only and non-required
