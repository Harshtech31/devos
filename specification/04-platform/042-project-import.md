# 042 – Project Import

**Document ID:** DEVOS-SPEC-042

**Version:** 0.1

**Status:** Draft

**Category:** Platform

**Depends On:**

- DEVOS-SPEC-005 – Guiding Principles
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-013 – Object Lifecycle
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-021 – Project Specification
- DEVOS-SPEC-029 – Workspace Manifest
- DEVOS-SPEC-031 – Workspace Engine
- DEVOS-SPEC-043 – Project Detection
- DEVOS-SPEC-044 – Workspace Lifecycle

**Referenced By:**

- DEVOS-SPEC-040 – CLI
- DEVOS-SPEC-041 – Dashboard
- DEVOS-SPEC-076 – Cloud Platform

---

# Abstract

This document defines Project Import, the controlled path by which an existing UNMANAGED software project becomes a managed DevOS Workspace.

Import acquires the project from a declared source, analyzes it with Project Detection defined in DEVOS-SPEC-043, generates a DRAFT manifest, and submits every generated object to a mandatory HUMAN review gate.

Only after human approval and successful validation may the Workspace proceed toward activation through the lifecycle machinery of DEVOS-SPEC-044.

---

# Purpose

This specification answers the following question:

> **How does an existing software project become a managed DevOS Workspace without surprises?**

Import proposes instead of acting: it reads, suggests, and waits, every consequential decision belongs to a human, and every suggestion carries its evidence.

---

# Goals

This specification aims to:

- Define what it means to bring an unmanaged project under Workspace management.
- Catalog permitted import sources and acquisition rules.
- Define the mandatory pipeline from acquisition to activation eligibility.
- Define provenance, the human review gate, identity handling, and error classes.
- State normatively what import MUST NEVER do.

---

# Non Goals

This specification does not define:

- Detection algorithms or heuristics, owned by DEVOS-SPEC-043.
- Manifest syntax and validation stages, owned by DEVOS-SPEC-029.
- Activation guards, owned by DEVOS-SPEC-044.
- CLI commands or Dashboard layouts, owned by DEVOS-SPEC-040 and DEVOS-SPEC-041.
- Organization-scale import policy, deferred to DEVOS-SPEC-060.

---

# Definition

Import brings an UNMANAGED project under Workspace management.

The result of a successful import is a Workspace at the Created stage holding a DRAFT manifest, meaning ordinary manifest data per DEVOS-SPEC-029 that has NOT been validated into Active standing.

Import is NEVER silent normative action: nothing it proposes becomes binding until a HUMAN approves it and the activation gate of DEVOS-SPEC-044 is passed.

The imported Workspace MUST satisfy every ownership and aggregate invariant of DEVOS-SPEC-011, DEVOS-SPEC-015, and DEVOS-SPEC-020.

---

# Import Sources

Import accepts projects from exactly three source classes.

| Source                       | Acquisition                                                                                                   | Notes                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Local Directory              | In-place adoption of an existing project tree on the same machine.                                             | Fully offline; no copying or moving of project files.                            |
| Archive Bundle               | Reading a Workspace bundle produced by export per DEVOS-SPEC-020, or a zip-style archive treated conceptually. | Untrusted input; extraction MUST apply path traversal protection.                |
| Remote Repository Descriptor | Fetching from a declared git URL class descriptor.                                                             | Permitted ONLY with explicit user consent for that specific network operation.   |

Remote acquisition MUST NOT begin without consent scoped to the single declared descriptor, MUST NOT contact any other host, and forbids metadata lookups, telemetry, and registry queries.

Local directory and local bundle imports MUST function fully offline, while remote descriptors require connectivity by definition.

Detection during any import remains offline per DEVOS-SPEC-043, so Offline First from DEVOS-SPEC-005 holds everywhere except the consent-scoped fetch itself.

---

# Import Pipeline

Every import proceeds through the same ordered pipeline.

```mermaid
graph LR

Acquire[Acquire Source] --> Detect[Detect - 043]
Detect --> Generate[Draft Manifest Generation]
Generate --> Review[HUMAN REVIEW]
Review --> Validate[Validate - 031 Stages]
Validate --> Draft[Created Draft]
Draft --> Activate[Activate - 044 Gate]
```

Acquire obtains the project from one declared source class.

Detect runs read-only analysis producing a detection report per DEVOS-SPEC-043, Draft Manifest Generation converts suggestions and user answers into manifest data, and HUMAN REVIEW then presents every generated object without being skippable.

Validate runs the approved draft through the stages of DEVOS-SPEC-031 and DEVOS-SPEC-029 before the Workspace records at Created per DEVOS-SPEC-013, leaving Activate to evaluate the gate of DEVOS-SPEC-044.

Each stage MUST complete before the next begins, and failure MUST stop the pipeline with the matching error class.

---

# Draft Generation and Human Review

The governing rule is: the generator proposes, the user disposes.

Every suggested Profile, Connection, Provider, Plugin, Template, and Secret reference MUST appear in review with provenance attached.

| Provenance Field | Meaning                                                                        |
| ---------------- | ------------------------------------------------------------------------------ |
| originDetector   | The detector that produced the suggestion, as reported by DEVOS-SPEC-043.       |
| confidence       | The reported High, Medium, or Low level from DEVOS-SPEC-043.                    |
| evidence         | Cited signals and file paths backing the suggestion.                            |
| disposition      | The reviewer outcome accepted, edited, or skipped.                              |

Example provenance wording: suggested by detector X, confidence High.

Generated names MUST be marked as proposals, never as facts inherited from the project.

Human review is MANDATORY and MUST NOT be bypassed by any interface.

The review view MUST list every generated object, including the single Project per DEVOS-SPEC-021, each Profile with its embedded Environment per DEVOS-SPEC-022 and DEVOS-SPEC-023, all optional owned objects, and Secret reference placeholders flagged for later binding per DEVOS-SPEC-028.

It MUST present a summary diff against the empty state, approval MUST be attributable to a recorded human decision, and rejection MUST discard the draft cleanly as review-rejected.

Interfaces MUST NOT offer a silent or zero-prompt import mode in Version 0.1.

Reviewers MAY select subsets of detected objects.

Unselected detections MUST be recorded as skipped-suggestions with provenance, creating no domain object, so future runs can remind the user what was declined; selection changes re-enter review before the draft is finalized.

---

# Identity, Conflicts, and Re-Import

Incoming identifiers follow the identity mapping rules of DEVOS-SPEC-029.

A collision with an identifier already used in the target environment MUST be resolved by remapping the incoming identifier, recording the mapping, and showing the remap in review before approval; overwriting an existing object is FORBIDDEN.

Re-importing the SAME project takes the update path.

That path compares the existing manifest against the new draft and proposes a minimal diff listing only differing objects, each approved individually, with destructive auto-merge excluded in Version 0.1.

If the existing Workspace is Active, the update path MUST NOT create a second Project inside it per DEVOS-SPEC-021 and operates only on metadata replacement proposals subject to review.

---

# What Import Never Does

The following prohibitions are NORMATIVE.

Import MUST NOT modify project source code.

Import MUST NOT run builds, tests, or any project-executed command.

Import MUST NOT make network calls beyond acquiring the declared source with consent.

Import MUST NOT read secret values, though it MAY create secret reference placeholders flagged for later binding per DEVOS-SPEC-028.

---

# Error Classes

Import failures MUST be reported using the following classes.

| Error Class            | Meaning                                                                     | Example Trigger                                        |
| ---------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------ |
| acquisition-failed     | The declared source could not be reached or read.                            | Missing local directory; unreadable bundle.             |
| unsupported-layout     | The acquired tree uses a layout the importer cannot represent conceptually.  | Empty tree; structure outside supported concepts.       |
| detection-inconclusive | Detection produced no confident suggestions.                                 | Low confidence across categories per DEVOS-SPEC-043.    |
| validation-blocked     | The approved draft failed a validation stage of DEVOS-SPEC-031.              | Manifest rejected at Domain or Relationship validation. |
| review-rejected        | The human reviewer declined the draft.                                       | Explicit rejection at the review gate.                  |

detection-inconclusive MUST still leave manual import available, meaning the user supplies Project and Profile definitions and enters review with them.

Error messages MUST identify the failing stage, the failing object where applicable, and a suggested next action, mapped per interface consistent with DEVOS-SPEC-044.

---

# Interaction Sequence

```mermaid
sequenceDiagram
    actor User
    participant UI as Interface (CLI 040 / Dashboard 041)
    participant Imp as Import Service (042)
    participant Det as Detector (043)
    participant Eng as Workspace Engine (031)

    User ->> UI: start import, declare source
    UI ->> Imp: acquire declared source
    Imp ->> Det: analyze acquired tree read-only
    Det -->> Imp: detection report with suggestions
    Imp ->> Imp: generate draft manifest with provenance
    Imp -->> UI: review summary listing every generated object
    User ->> UI: accept, edit, or skip suggestions
    UI ->> Eng: validate approved draft
    Eng -->> UI: stage-by-stage validation outcome

    alt validation passed
        Eng -->> UI: Workspace persisted at Created draft
        UI -->> User: import complete; activate via lifecycle to continue
    else validation failed
        UI -->> User: validation-blocked with attributed findings
    end
```

---

# Import Invariants

The following invariants MUST always hold.

- Human review is mandatory; there is no silent import.
- Import never mutates the acquired project source.
- Provenance is recorded for every suggestion accepted, edited, or skipped.
- Import produces a Created draft, never an Active Workspace.
- Identifier collisions resolve by recorded remapping per DEVOS-SPEC-029, never by overwriting.
- Re-import proposes minimal diffs; destructive auto-merge is forbidden in v0.1.
- Secret values never enter the draft manifest in any encoding.
- Skipped detections persist as skipped-suggestions and never become objects implicitly.

---

# Security Requirements

Archive extraction MUST apply path traversal protection against entries escaping the intended destination root.

Acquired code MUST NOT execute during import in any form, following the declarative stance of DEVOS-SPEC-027 and the DEVOS-SPEC-029 invariant that configuration describes but never executes.

All acquired input MUST be treated as untrusted, consistent with DEVOS-SPEC-021.

Secret placeholders MUST carry no resolvable value until bound through DEVOS-SPEC-028 behavior.

Approvals and import decisions SHOULD feed the audit trail of DEVOS-SPEC-065, with redaction owned by DEVOS-SPEC-036.

---

# Performance Requirements

Detection within import MUST respect the bounded time budget stated in DEVOS-SPEC-043 so latency stays predictable on large repositories.

Streaming acquisition SHOULD be supported for bundles and remote descriptors so memory use does not scale with total size.

Import MUST remain cancellable at every stage without corrupting the target environment or leaving partial objects behind, and large repositories MUST degrade to bounded detection plus manual completion rather than unbounded scanning.

---

# Future Extensions

Future specifications may extend Project Import with:

- watch-mode continuous import policies re-running detection on declared trees.
- organization-scale bulk import governed by DEVOS-SPEC-060.
- signed bundle verification prior to review.
- cloud-coordinated import flows through DEVOS-SPEC-076.

These extensions require an RFC and an ADR, MUST NOT break the single-Workspace aggregate model of DEVOS-SPEC-011, and MUST NOT weaken the mandatory human review gate.

---

# References

- DEVOS-SPEC-005 – Guiding Principles
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-013 – Object Lifecycle
- DEVOS-SPEC-015 – Object Ownership
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-021 – Project Specification
- DEVOS-SPEC-022 – Profile Specification
- DEVOS-SPEC-023 – Environment Specification
- DEVOS-SPEC-027 – Template Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-029 – Workspace Manifest
- DEVOS-SPEC-031 – Workspace Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-040 – CLI
- DEVOS-SPEC-041 – Dashboard
- DEVOS-SPEC-043 – Project Detection
- DEVOS-SPEC-044 – Workspace Lifecycle
- DEVOS-SPEC-060 – Organizations
- DEVOS-SPEC-065 – Audit System
- DEVOS-SPEC-076 – Cloud Platform

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
