# 005 – Guiding Principles

**Document ID:** DEVOS-SPEC-005

**Version:** 0.1

**Status:** Draft

**Category:** Overview

**Depends On:**

- DEVOS-SPEC-004 – Design Philosophy

**Referenced By:**

- DEVOS-SPEC-011 – Domain Model
- All DevOS Specifications

---

# Abstract

This document is the canonical, normative statement of the DevOS guiding principles.

Each principle carries a MUST-style definition, a rationale, practical rules for implementations, and violation examples.

It defines precedence for resolving conflicts between principles and provides a compliance checklist for new specifications.

---

# Purpose

This specification exists to answer one question:

> **Which principles are binding on every DevOS implementation and specification?**

The ten principles below are binding.

---

# Goals

This document aims to:

- Formalize each principle as an enforceable obligation.
- Give reviewers a concrete compliance checklist.
- Define resolution when principles conflict.
- Provide stable vocabulary used by every other specification.

---

# Non Goals

This document does not restate the repository rule set verbatim; it formalizes principles for implementers.

It does not define architecture, schemas, or features, and it does not replace the Change Process defined in DEVOS-SPEC-000.

---

# Principles

Each principle below follows the same structure: Definition, Rationale, Practical Rules, and Violation Examples.

## Workspace First

### Definition

The Workspace is the unit of ownership and integration.

Every object, setting, and capability MUST belong to exactly one Workspace.

### Rationale

Ownership, permissions, synchronization, import/export, and lifecycle all simplify when exactly one root exists.

A second root would reintroduce the fragmentation DevOS removes.

### Practical Rules

- Implementations MUST scope all persistent data to a Workspace.
- Subsystems SHOULD integrate through the Workspace boundary.
- Features MUST NOT introduce owners above or beside the Workspace in Version 0.1.
- Tools MAY operate on Workspaces but MUST NOT become the primary abstraction themselves.

### Violation Examples

- Storing projects or credentials in a user-global store outside any Workspace.
- A command whose effects escape Workspace ownership.

## Provider Agnostic

### Definition

No vendor is required for any capability.

Providers implementing a capability MUST be interchangeable.

### Rationale

Providers evolve unevenly and disappear; lock-in destroys portability.

Interchangeability turns vendor changes into configuration edits instead of migrations.

### Practical Rules

- Capability interfaces MUST NOT leak vendor-specific concepts into core contracts.
- Swapping a provider SHOULD require only a configuration change.
- Implementations MUST NOT hard-code an irremovable default provider.
- New providers SHOULD be registrable without modifying the core platform.

### Violation Examples

- An export format only one cloud platform understands.
- AI calls bound to one model endpoint inside core logic.

## Plugin First

### Definition

Functionality that can be implemented as a plugin SHOULD be implemented as a plugin.

The core MUST remain as small as possible.

### Rationale

Small cores stay understandable, maintainable, and adaptable.

Plugins let the ecosystem grow without inflating the platform.

### Practical Rules

- The core MUST contain only domain, engines, and public contracts.
- Plugins MUST extend functionality through public interfaces.
- Plugins MUST NOT modify core behavior implicitly.
- New capabilities SHOULD justify inclusion in core before being accepted there.

### Violation Examples

- Niche workflows compiled permanently into the core.
- Core modules importing plugin code or reaching into engine internals.

## Offline First

### Definition

Core functionality MUST work without internet connectivity.

Cloud integrations are optional extensions, never requirements.

### Rationale

Connectivity is unreliable and sometimes untrusted.

Local control is a prerequisite for ownership and security.

### Practical Rules

- Creating, opening, editing, and exporting workspaces MUST work fully offline.
- Cloud services MAY enhance but MUST NOT gate core flows.
- Network failures SHOULD degrade gracefully with clear observable state.
- Offline operation SHOULD NOT require special setup.

### Violation Examples

- A login wall blocking access to local workspaces.
- Configuration requiring an online account to read.

## Configuration as Code

### Definition

All configuration MUST exist as human-readable, declarative files.

Configuration MUST be version-controllable, reviewable, portable, and reproducible.

### Rationale

Hidden configuration creates hidden problems.

Files enable review, diffing, backup, and reproduction across machines and teams.

### Practical Rules

- Configuration MUST be expressible entirely as files.
- Critical state MUST NOT exist only in hidden application storage.
- Configuration formats SHOULD live in version control.
- Formats MUST remain diffable and reviewable by humans.

### Violation Examples

- Settings saved exclusively to an internal database.
- Environment state mutated imperatively at runtime.

## Security by Default

### Definition

Security MUST never be optional.

Secrets MUST be protected and least privilege MUST hold by default.

### Rationale

Ad-hoc secrets handling leaks credentials through shells, logs, and dotfiles.

Trust is a precondition for a tool that manages development environments.

### Practical Rules

- Secrets MUST NOT be committed to version control.
- Secrets MUST NOT appear in logs or error messages.
- Secrets MUST NOT be stored unencrypted at rest.
- Access SHOULD follow least privilege unless explicitly widened.
- Dangerous operations MUST require explicit consent.

### Violation Examples

- Tokens echoed into console output.
- Plaintext credential files created automatically for convenience.

## Open Specification

### Definition

The specification MUST be public and implementable by anyone.

Normative behavior MUST NOT depend on any single implementation or vendor.

### Rationale

Open standards win because anyone can adopt them without permission.

An open contract invites an ecosystem; a closed one forbids it.

### Practical Rules

- Specifications and schemas MUST be publicly readable.
- Conformance MUST be achievable without proprietary components.
- Extensions SHOULD flow back through the standard change process.
- Vendors MAY compete on implementations but MUST NOT own the format.

### Violation Examples

- Required undocumented endpoints for basic conformance.
- Format decisions made unilaterally outside the change process.

## Simplicity Over Features

### Definition

Features exist only to solve real developer problems.

Added complexity MUST be justified by that problem.

### Rationale

Complexity is the enemy of productivity.

Composability delivers more value than accumulation.

### Practical Rules

- Proposals MUST name the developer problem being solved.
- Existing capabilities SHOULD be composed before new ones are added.
- Redundant mechanisms MUST NOT be introduced alongside existing ones.
- Removal SHOULD be evaluated when usage no longer justifies cost.

### Violation Examples

- Parallel configuration systems for the same concern.
- Options nobody requested increasing cognitive load.

## Human First

### Definition

DevOS exists to reduce cognitive load.

Developer experience outweighs feature count in every decision.

### Rationale

Tools serve developers, not the reverse.

A powerful tool that requires memorization fails its purpose.

### Practical Rules

- Common flows SHOULD be understandable without reading manuals.
- Error messages MUST be actionable and specific.
- Every feature SHOULD answer: does this make a developer's life easier?
- Terminology MUST match DEVOS-SPEC-006 – Terminology consistently.

### Violation Examples

- Internal jargon exposed in user-facing output.
- Diagnostics pointing at internals instead of causes.

## One Source of Truth

### Definition

Every concept has exactly one canonical document or schema.

All other documents MUST reference canonical definitions instead of duplicating them.

### Rationale

Duplicated definitions drift apart silently.

Single sources keep the specification set auditable and consistent.

### Practical Rules

- Concepts MUST be defined canonically exactly once.
- Other documents SHOULD link rather than restate normative text.
- Conflicts MUST be resolved using the precedence rules of DEVOS-SPEC-000.
- Corrections MUST land in the canonical document first.

### Violation Examples

- Two documents defining the lifecycle differently.
- Copy-pasted tables drifting apart across revisions.

---

# Principle Precedence

When principles conflict during a decision, apply this order:

| Conflict                | Resolution      |
| ----------------------- | --------------- |
| Security vs Convenience | Security wins   |
| Simplicity vs Features  | Simplicity wins |
| Openness vs Lock-in     | Openness wins   |

Resolutions not covered by this table REQUIRE an ADR documenting the conflict, the options considered, and the chosen outcome; silent precedence choices MUST NOT ship.

---

# Compliance Checklist for New Specifications

New specifications and significant changes SHOULD be reviewed against every item.

- [ ] Does it preserve the Workspace as the only Aggregate Root?
- [ ] Are providers replaceable without domain changes?
- [ ] Could this functionality live in a plugin instead of the core?
- [ ] Does core functionality work fully offline?
- [ ] Is all configuration declarative, human-readable, and version-controllable?
- [ ] Are secrets protected and never logged?
- [ ] Does it depend on any single vendor anywhere?
- [ ] Is the added complexity justified by a named developer problem?
- [ ] Are failure paths transparent and actionable?
- [ ] Does it duplicate an existing canonical definition?
- [ ] Are document numbers, versions, and cross-references correct?

An unchecked item MUST be either resolved or explicitly waived through an ADR.

---

# References

- DEVOS-SPEC-000 – Specification Governance
- DEVOS-SPEC-002 – Vision
- DEVOS-SPEC-003 – Problem Statement
- DEVOS-SPEC-004 – Design Philosophy
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- SPECIFICATION_RULES.md – Repository rule set (root document)

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
