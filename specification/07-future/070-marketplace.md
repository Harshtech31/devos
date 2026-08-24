# 070 – Marketplace

**Document ID:** DEVOS-SPEC-070

**Version:** 0.1

**Status:** Draft

**Category:** Future

**Depends On:**

- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-027 – Template Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-059 – Versioning Policy
- DEVOS-SPEC-065 – Audit System
- DEVOS-SPEC-067 – License Management

**Referenced By:**

- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-033 – Provider Engine
- DEVOS-SPEC-051 – Plugin SDK
- DEVOS-SPEC-052 – Provider SDK
- DEVOS-SPEC-053 – Template SDK
- DEVOS-SPEC-066 – Workspace Sharing
- DEVOS-SPEC-077 – Ecosystem
- DEVOS-SPEC-078 – V2 Roadmap

---

# Abstract

This document defines the Marketplace, the forward-looking distribution channel through which plugins, providers, templates, and agent packages reach users beyond local and manual installation.

It defines listing contracts, provenance and attestation duties, install-time integration with existing engines, and the trust model that keeps marketplace content untrusted until verified.

The Marketplace is a delivery mechanism, never an authority: it changes where packages come from, not what they may do.

This specification is forward-looking and activates only through an approved RFC and ADR.

---

# Purpose

This specification answers the following question:

> **How can the ecosystem distribute extensions safely at scale without weakening local-first trust boundaries?**

Every installed artifact already passes compatibility, validation, and permission evaluation.

The Marketplace adds discovery, attestation, and update channels upstream of those unchanged gates.

Offline installation remains fully supported; the marketplace is optional enhancement.

---

# Goals

This specification aims to:

- Define listing metadata for distributable artifact classes.
- Define provenance and attestation records bound to packages.
- Define discovery and resolution flows feeding existing engine paths.
- Define update channel semantics aligned with DEVOS-SPEC-048.
- Preserve local-first installation as a first-class equal.

---

# Non Goals

This specification does not define:

- Hosting infrastructure, search ranking algorithms, or storefront design
- Payment processing, deferred to DEVOS-SPEC-067 activation
- Review board composition or curation policy
- Package internals, owned by their SDK specifications
- Cross-workspace federation of runtime behavior

---

# Listing Model

A Listing binds one publishable artifact to its distribution metadata.

| Field         | Required | Description                                                      |
| ------------- | -------- | ------------------------------------------------------------------ |
| artifact ref  | Yes      | Immutable package identity plus version per DEVOS-SPEC-059.         |
| class         | Yes      | Plugin, provider adapter, template, or agent package.               |
| publisher     | Yes      | Attested publishing identity.                                       |
| attestations  | Yes      | Verification claims carried with every distributed copy.             |
| compatibility | Yes      | Declared platform range evaluated unchanged at install time.         |

```mermaid
graph LR

    P["Publisher"] --> L["Listing"]
    L -->|"attested package"| M["Marketplace Channel"]
    M -->|"discovery"| U["User Workspace"]
    U --> E["Existing Engine Gates Unchanged"]
```

Attestation travels with the package; it informs decisions but never bypasses them.

---

# Install Integration

Marketplace installs terminate in the same gates as every other source.

Rules:

- Discovery results carry complete provenance; the engine refuses candidates lacking it per DEVOS-SPEC-032.
- Install re-executes compatibility checking, manifest validation, and permission evaluation exactly as for local sources.
- Signed packages verify before staging once signature enforcement activates through the deferred roadmap; absence of signatures degrades to explicit warning states, never silent acceptance.
- Template listings enter the shared pool under identical rules via DEVOS-SPEC-053 contribution discipline.

---

# Updates

Update flows respect user consent and versioning policy.

Rules:

- The Update System surfaces marketplace versions through declared channels per DEVOS-SPEC-048 without downloading or applying anything behind consent gates.
- Compatibility matrix evaluation precedes every offer per DEVOS-SPEC-059.
- Rollback restores prior immutable versions on failed updates per DEVOS-SPEC-032 semantics.

---

# Trust Posture

The marketplace inherits the platform's standing distrust of extension content.

| Content Condition        | Platform Behavior                                        |
| ------------------------ | ---------------------------------------------------------- |
| Attested and compatible  | Installs through normal gates after verification.           |
| Missing attestation      | Warns explicitly; proceeds only through informed consent flows. |
| Incompatible range       | Rejected with incompatible-version reporting.               |
| Policy violation claim   | Withheld from resolution pending publisher remedy.          |

No listing status ever widens permissions; grants remain deny-by-default through DEVOS-SPEC-036 regardless of reputation.

---

# Relationship to Version 0.1

Version 0.1 installs exclusively from local-first sources, as fixed by DEVOS-SPEC-032.

The Marketplace layers distribution onto that foundation.

Activation requires an RFC covering channel mechanics and attestation formats, an approved ADR preserving aggregate invariants, and schema additions beside existing canonical schemas.

Until activated, implementations MUST NOT ship partial marketplace behavior.

---

# Future Extension Invariants

The following invariants MUST hold when activated.

- Marketplace origin confers no authority; all gates stay unchanged.
- Provenance is present on every distributed artifact or it is refused.
- Local and manual installation remain equally capable forever.
- Consent gates govern every download and apply.
- Licensing integrates through DEVOS-SPEC-067 rather than private enforcement.
- Distribution events remain auditable through the direction of DEVOS-SPEC-065.

These MUST NOT break the single Workspace aggregate model.

---

# Security Requirements

When activated, this extension enforces:

- Publisher identity attestation evaluated deny-by-default per DEVOS-SPEC-036.
- Integrity verification over every staged package as roadmap maturity allows, strengthening without weakening current behavior.
- Full attribution of publication and installation events per DEVOS-SPEC-065.
- No secret material inside any listing or package per DEVOS-SPEC-028.

---

# Future Extensions

Future specifications may add support for:

- Decentralized mirrors with verifiable transparency logs
- Curated collections under organizational policy control per DEVOS-SPEC-063
- Automated compatibility certification pipelines
- Reputation signals derived solely from auditable events

These extensions require their own RFCs and ADRs and MUST preserve the invariants above.

---

# References

- DEVOS-SPEC-000 – Specification Governance
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope
- DEVOS-SPEC-011 – Domain Model
- SPECIFICATION_RULES.md – Repository rule set (Rule 7)
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-027 – Template Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-033 – Provider Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-048 – Update System
- DEVOS-SPEC-051 – Plugin SDK
- DEVOS-SPEC-052 – Provider SDK
- DEVOS-SPEC-053 – Template SDK
- DEVOS-SPEC-059 – Versioning Policy
- DEVOS-SPEC-063 – Policy Engine
- DEVOS-SPEC-065 – Audit System
- DEVOS-SPEC-066 – Workspace Sharing
- DEVOS-SPEC-067 – License Management
- DEVOS-SPEC-077 – Ecosystem
- DEVOS-SPEC-078 – V2 Roadmap

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
