# DevOS Governance

This document defines how the DevOS project makes decisions, who holds which responsibilities, and how conflicts are resolved.

It applies to the specification, schemas, RFCs, ADRs, diagrams, examples, and tooling in this repository.

---

# Principles

- **Openness.** Specifications, schemas, and processes are public. Anyone may read, implement, and build on DevOS.
- **Transparency.** Decisions happen in the open: issues, RFCs, and ADRs are the record. Nothing important happens off the record.
- **Merit.** Influence grows from consistent, high-quality contributions, not from titles or affiliations.
- **Long-term thinking.** We optimize for a standard that will still be sound in ten years, not for short-term convenience.

---

# Roles

| Role             | Responsibilities                                                                                         | How Appointed                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Contributor      | Files issues, submits pull requests, participates in discussions                                         | Anyone; no appointment required                                      |
| Reviewer         | Reviews specifications, schemas, diagrams, and examples for correctness and consistency                   | Recognized by maintainers after sustained quality contributions      |
| Maintainer       | Owns a specification section or area, merges changes, mentors reviewers, enforces the rules               | Invited by existing maintainers with Steering Council awareness      |
| Steering Council | Sets direction, arbitrates disputes, approves ADRs that alter structure or scope, guards the project charter | Founding members initially; later seats added by Council consensus  |

All roles are open to anyone regardless of employer or affiliation.

---

# Decision Making

Decisions follow an escalating ladder:

1. **Lazy consensus (default).** Small edits — wording fixes, table alignment, example additions — merge when no reviewer objects within a reasonable time.
2. **RFC.** Significant features and any new normative behavior require an accepted RFC before work begins (Rule 13).
3. **ADR.** Architectural decisions — configuration format, plugin model, workspace lifecycle, storage architecture, repository structure — require an approved ADR (Rule 14).
4. **Steering Council tie-break.** When discussion deadlocks, the Council decides and records the rationale.

**Breaking changes** to schemas or established specifications require supermajority approval of maintainers plus an RFC, ADR, migration strategy, version bump, and deprecation notice.

---

# Specification Change Flow

Specification numbers are frozen forever; only content evolves.

Document statuses:

| Status    | Meaning                                                                 |
| --------- | ----------------------------------------------------------------------- |
| Draft     | Under active development; content may change without migration promises |
| Stable    | Committed for backward compatibility; changes follow Rule 18            |
| Deprecated| Retained for reference; superseded by another document                  |

A document moves from Draft to Stable only through review by its area maintainer and at least one additional maintainer.

Deprecation requires naming the replacement document or recording that no successor exists.

---

# Area Ownership

Maintainers may own a specification section — for example, Foundation (020–029) or Core Architecture (030–039).

Ownership means:

- Triaging issues and reviewing pull requests touching that area.
- Keeping documents, schemas, and diagrams in that area consistent.
- Proposing status transitions for documents in the area.

Ownership does not mean unilateral control.
All normative changes still flow through the decision ladder above.

---

# Conflict Resolution

1. Disagreements are first resolved through direct discussion on the issue or pull request.
2. If unresolved, any participant may request review by the area maintainer.
3. If still unresolved, the Steering Council arbitrates and records the decision and rationale.

Participants are expected to disagree constructively and assume good faith, as described in the [Project Manifesto](PROJECT_MANIFESTO.md).

Persistent bad-faith behavior is handled under the [Code of Conduct](CODE_OF_CONDUCT.md), not this document.

---

# Code of Conduct Enforcement

The [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) applies to all project spaces.
The maintainer team enforces it proportionally using the enforcement guidelines defined there.
Conduct decisions are independent of technical merit: excellent technical work does not exempt anyone from the rules.

---

# Modifying This Document

Changes to this governance document require:

1. Consensus of the Steering Council.
2. A pull request that records the change and its rationale.
3. An entry in [CHANGELOG.md](CHANGELOG.md).

If governance and other documents conflict, this document prevails until amended.
