# DevOS Roadmap

DevOS grows in phases: specification first, then reference implementation, then ecosystem.
Phases are sequential but not rigid; a phase may begin before the previous one fully closes.
Dates are intentionally omitted — phases complete when their goals are met.

## Phases at a Glance

| Phase | Name                          | Focus                                        | Status      |
| ----- | ----------------------------- | -------------------------------------------- | ----------- |
| 0     | Specification v0.1            | Complete the specification set               | In Progress |
| 1     | Reference CLI Implementation  | First implementation of the specification    | Planned     |
| 2     | Local Dashboard               | Visual interface over the Workspace          | Planned     |
| 3     | SDK & Ecosystem               | Plugin, provider, and template SDKs          | Planned     |
| 4     | Enterprise                    | Organizations, teams, RBAC, policy, audit    | Future      |
| 5     | Platform Expansion            | Marketplace and additional surfaces          | Future      |

---

## Phase 0 — Specification v0.1

**Status: In Progress**

Goal: define the complete workspace standard before any implementation exists.

- Complete the full 80-document specification set across all eight sections (000–079).
- Finalize JSON schemas in [schemas/](schemas/) as the canonical contracts for core objects.
- Keep document, diagram, and example scaffolding consistent with the rules.
- Operate the RFC and ADR process live through [rfcs/](rfcs/) and [adr/](adr/).
- Stabilize Foundation (020–029) documents from Draft toward Stable.
- Keep Enterprise (060–069) and Future (070–079) ranges explicitly out of v0.1 scope until an ADR activates them.

Exit criteria: the specification set is internally consistent, schemas validate examples, and the overview reading order tells a coherent story end to end.

---

## Phase 1 — Reference CLI Implementation

**Status: Planned**

Goal: prove the specification with a working command-line tool.

- `workspace init` — scaffold a new workspace from a template.
- `workspace import` — detect an existing project and generate its manifest.
- `workspace validate` — check a manifest against canonical schemas.
- `workspace export` — emit a portable workspace bundle.
- Provider abstraction implementing DEVOS-SPEC-024 semantics.
- Secrets handling honoring DEVOS-SPEC-028 security requirements.
- Offline-first behavior as required by Rule 7.

Nothing ships here that is not already specified.

---

## Phase 2 — Local Dashboard

**Status: Planned**

Goal: give developers a visual surface over the same Workspace model.

- Local dashboard per DEVOS-SPEC-041, reading the same manifests as the CLI.
- Workspace health, lifecycle, and connection status views per DEVOS-SPEC-046.
- No cloud dependency; the dashboard runs fully offline.

---

## Phase 3 — SDK & Ecosystem

**Status: Planned**

Goal: let others build on DevOS without touching the core.

- Plugin SDK per DEVOS-SPEC-051 following the Plugin First rule.
- Provider SDK so new AI, cloud, and database providers are drop-in replaceable.
- Template SDK for shareable workspace patterns.
- Registries and distribution mechanisms defined through RFCs before any code.

---

## Phase 4 — Enterprise

**Status: Future**

Goal: extend the single-workspace model to organizations.

- Organizations and teams per DEVOS-SPEC-060 and DEVOS-SPEC-061.
- RBAC per DEVOS-SPEC-062 and policy enforcement per DEVOS-SPEC-063.
- Audit trails per DEVOS-SPEC-065.
- Cloud sync and sharing per DEVOS-SPEC-064 and DEVOS-SPEC-066.
- Activation of each capability requires an ADR and MUST NOT break the single-Workspace aggregate model.

---

## Phase 5 — Platform Expansion

**Status: Future**

Goal: carry workspaces to every surface developers use.

- Marketplace ecosystem per DEVOS-SPEC-070.
- Desktop, web, mobile, and cloud platforms per DEVOS-SPEC-073 to DEVOS-SPEC-076.
- Ecosystem governance per DEVOS-SPEC-077.

These remain forward-looking specifications until activated by ADR.

---

## Guiding Rule

> **Nothing ships before its specification exists.**
>
> Every phase above depends on [SPECIFICATION_RULES.md](SPECIFICATION_RULES.md), especially Rule 1 (Specification First).
> Implementation follows the specification; it never leads it.
