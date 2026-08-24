# 029 – Workspace Manifest

**Document ID:** DEVOS-SPEC-029

**Version:** 0.1

**Status:** Draft

**Category:** Foundation

**Depends On:**

- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-012 – Domain Relationships
- DEVOS-SPEC-013 – Object Lifecycle
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-015 – Object Ownership
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-021 – Project Specification
- DEVOS-SPEC-022 – Profile Specification
- DEVOS-SPEC-023 – Environment Specification
- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-025 – Connection Specification
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-027 – Template Specification
- DEVOS-SPEC-028 – Secret Specification

**Referenced By:**

- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-031 – Workspace Engine
- DEVOS-SPEC-044 – Workspace Lifecycle
- DEVOS-SPEC-054 – Workspace SDK
- DEVOS-SPEC-064 – Cloud Sync

---

# Abstract

This document defines the Workspace Manifest, the canonical declarative form of a DevOS Workspace.

The manifest expresses the complete Workspace aggregate as configuration that can be version-controlled, reviewed, exported, imported, and validated.

It defines the manifest schema, its logical structure, identity and import semantics, the validation pipeline, and round-trip guarantees.

---

# Purpose

This specification answers the following question:

> **What is the canonical declarative form of a Workspace and what must validation guarantee?**

The manifest is a complete and portable representation of one Workspace.

Anything required to reconstruct and activate the Workspace must be derivable from it, except secret values, which never appear in any form.

---

# Goals

This specification aims to:

- Define the manifest as the canonical declarative form of a Workspace.
- Bind the manifest to its canonical schema.
- Define required and optional logical blocks.
- Define identity handling during import.
- Define the validation pipeline from syntax to activation eligibility.
- Guarantee export-import-export round trips.
- Define schema versioning and compatibility expectations.

---

# Non Goals

This specification does not define:

- On-disk file names or directory layout conventions
- CLI commands or editor tooling
- Bundle compression or transport formats
- Cloud synchronization protocol
- Database schemas
- User interface rendering

Transport and synchronization behavior belong to DEVOS-SPEC-064.

---

# Manifest Definition

A Workspace Manifest is the complete, declarative, portable representation of a Workspace.

The manifest implements Rule 5 of SPECIFICATION_RULES.md, Configuration as Code.

A manifest MUST be version controlled, reviewable, human readable, and portable across implementations.

Configuration MUST NOT exist only inside hidden application state.

The manifest describes the Workspace; it never executes.

---

# Manifest Schema

Every manifest MUST validate against `schemas/manifest.schema.json`.

That schema is expressed in JSON Schema under the reserved namespace `https://devos.dev/schemas/v0/`.

Schemas are canonical per Rule 17 of SPECIFICATION_RULES.md and the precedence rules of DEVOS-SPEC-000.

Schemas define the specification, documentation explains the schemas, and implementations validate against the schemas.

When this prose and the schema appear to conflict, the schema wins and the prose defect is fixed through the editorial process.

No other schema location is normative for manifests in Version 0.1.

---

# Encoding

The RECOMMENDED encoding is a human-readable YAML-style structure.

This encoding is recommended, not required.

Conformance statement: ANY format is conformant if it validates against the manifest schema and maps losslessly onto the logical model defined below.

Binary-only formats that cannot be reviewed as text violate the reviewability requirement above.

---

# Illustrative Example

The following snippet is ILLUSTRATIVE ONLY.

It demonstrates shape and vocabulary; it is not a normative format definition and it is not exhaustive.

```yaml
apiVersion: devos.dev/v0
kind: Workspace
metadata:
  id: ws-example
  name: Example Workspace
  schemaVersion: "0.1"
project:
  name: example-service
profiles:
  - name: development
    environment:
      variables:
        LOG_LEVEL: debug
connections:
  - name: local-database
providers:
  - name: ai-assistant
    credentialSecretRef: ai-provider-key
plugins:
  - name: git-integration
templates:
  - id: service-template
secrets:
  - id: ai-provider-key
    name: AI Provider Key
workflows:
  - name: verify-pipeline
    tasks:
      - lint
      - test
documentation:
  - path: docs/architecture.md
```

Note the secrets block: it carries identifiers and metadata only.

No field anywhere in this structure may hold a secret value, as mandated by DEVOS-SPEC-028.

---

# Logical Structure

A manifest is a mapping onto the domain objects defined in DEVOS-SPEC-011 and owned per DEVOS-SPEC-015.

Required blocks:

| Block       | Required | Contents                                                        |
| ----------- | -------- | --------------------------------------------------------------- |
| apiVersion  | Yes      | Schema generation identifier, for example `devos.dev/v0`.        |
| kind        | Yes      | Object kind; MUST be `Workspace` for a workspace manifest.       |
| metadata    | Yes      | `id`, `name`, and `schemaVersion`.                               |
| project     | Yes      | The single Project owned by the Workspace.                       |
| profiles    | Yes      | One or more Profiles, each embedding its Environment definition. |

Optional collections:

- connections
- providers
- plugins
- templates
- secrets (references only)
- workflows
- documentation

Optional collections map to Workspace-owned objects as defined in DEVOS-SPEC-020.

The secrets collection carries references and metadata only, per DEVOS-SPEC-028.

Each Profile embeds exactly one Environment, and ownership encoded in the manifest MUST match DEVOS-SPEC-015.

---

# Identity and Import

Import MAY remap identifiers when they conflict with objects already present in the target environment.

Every remap MUST be recorded as an identity mapping together with the imported Workspace so internal references stay consistent.

Import MUST revalidate the entire aggregate before the Workspace can become Active, as required by DEVOS-SPEC-020.

Import MUST NOT skip relationship validation because identifiers changed.

Unresolved Secret references after import follow DEVOS-SPEC-028 binding behavior.

---

# Round-Trip Guarantee

Export followed by import followed by export MUST produce an equivalent manifest.

Equivalence means identical semantics, modulo identifiers remapped by import and insignificant formatting differences.

The round trip MUST preserve:

- Project and Profile definitions including embedded Environments.
- all owned object definitions.
- all references between owned objects.
- identity mappings introduced by import.

If two conformant implementations produce semantically different results for the same bundle, one of them is defective; round-trip equivalence is a testable conformance requirement.

---

# Validation Pipeline

Manifest validation proceeds through ordered stages.

```mermaid
graph LR

Syntax[Parsing and Syntax] --> Schema[Schema Validation]
Schema --> Domain[Domain Validation]
Domain --> Relationship[Relationship Validation]
Relationship --> Eligible[Workspace Activation Eligibility]
```

Stage meaning:

- Parsing and Syntax confirms the input is well formed.
- Schema Validation checks the input against `schemas/manifest.schema.json`.
- Domain Validation checks object-specific rules from DEVOS-SPEC-020 through DEVOS-SPEC-028.
- Relationship Validation checks references, ownership, and DEVOS-SPEC-012 constraints.
- Workspace Activation Eligibility marks the manifest ready for activation decisions by lifecycle machinery such as DEVOS-SPEC-044.

Each stage MUST pass completely before the next begins.

Failure at any stage MUST stop the pipeline and report reason codes without exposing secret values.

Passing the pipeline establishes eligibility only; activation itself remains governed by DEVOS-SPEC-013 and DEVOS-SPEC-020.

---

# Validation Requirements

Manifest validation MUST verify:

- apiVersion exists and is recognized.
- kind is Workspace.
- metadata contains id, name, and schemaVersion.
- exactly one project block exists.
- at least one profile exists.
- every profile embeds exactly one Environment.
- every reference resolves within the manifest or is explicitly marked external.
- no child object has multiple owners.
- ownership matches DEVOS-SPEC-015.
- the secrets collection contains no values, only references and metadata.
- the whole input conforms to `schemas/manifest.schema.json`.
- validation output contains no secret values.

---

# Versioning and Compatibility

The manifest declares its schema contract through metadata schemaVersion.

schemaVersion values follow the Versioning Policy defined in DEVOS-SPEC-059.

Backward compatibility follows Rule 18 of SPECIFICATION_RULES.md.

Breaking changes require an RFC, an ADR, a migration strategy, a version bump, and a deprecation notice.

Additive changes that keep older manifests valid are MINOR changes.

Deprecated fields MUST remain readable during their migration window and MUST point to their replacement.

---

# Manifest Invariants

The following invariants MUST always hold.

- A manifest describes exactly one Workspace.
- The manifest is declarative data and MUST NOT execute.
- Every manifest element maps to a domain object defined in DEVOS-SPEC-011.
- A manifest MUST validate against the canonical schema before activation eligibility.
- A manifest MUST NOT contain secret values in any field or encoding.
- Export, import, and round-trip operations preserve ownership relationships.

---

# Security Requirements

The manifest is a primary leak surface because it travels widely.

A manifest MUST NOT contain secret values, consistent with DEVOS-SPEC-028.

Validation and import tooling MUST treat manifests as untrusted input.

Import MUST revalidate the full aggregate rather than trusting exporter claims.

Audit systems SHOULD record manifest-level lifecycle events as specified in DEVOS-SPEC-065.

---

# Future Extensions

Future specifications may add support for:

- Signed and encrypted bundles
- Partial manifests for sub-aggregates
- Multi-Workspace composition formats
- Cloud synchronization deltas
- Marketplace-installed content blocks

These extensions MUST preserve the canonical schema precedence of this document.

They MUST NOT break the single Workspace aggregate model without an approved ADR.

---

# References

- DEVOS-SPEC-000 – Specification Governance
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-012 – Domain Relationships
- DEVOS-SPEC-013 – Object Lifecycle
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-015 – Object Ownership
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-021 – Project Specification
- DEVOS-SPEC-022 – Profile Specification
- DEVOS-SPEC-023 – Environment Specification
- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-025 – Connection Specification
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-027 – Template Specification
- DEVOS-SPEC-028 – Secret Specification
- SPECIFICATION_RULES.md – Repository rule set (Rules 5, 17, 18)
- DEVOS-SPEC-031 – Workspace Engine
- DEVOS-SPEC-044 – Workspace Lifecycle
- DEVOS-SPEC-059 – Versioning Policy

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
