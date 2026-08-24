# 052 – Provider SDK

**Document ID:** DEVOS-SPEC-052

**Version:** 0.1

**Status:** Draft

**Category:** SDK

**Depends On:**

- DEVOS-SPEC-005 – Guiding Principles
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-033 – Provider Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-039 – AI Router
- DEVOS-SPEC-059 – Versioning Policy

**Referenced By:**

- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-033 – Provider Engine
- DEVOS-SPEC-039 – AI Router
- DEVOS-SPEC-055 – API Specification

---

# Abstract

This document defines the Provider SDK, the Extension-tier contract through which developers implement replaceable capability providers.

It specifies the adapter model, the credential contract, state reporting duties, streaming and quota signaling, registration paths, and configuration validation.

The SDK turns vendor-specific services into honest, interchangeable providers that behave correctly in every Workspace, preserving the Provider Agnostic principle (Rule 4).

---

# Purpose

This specification answers the following question:

> **How does one implement a replaceable capability provider that behaves correctly everywhere?**

An author implements declared capability interfaces behind one adapter, maps vendor payloads into normalized shapes, treats resolved credentials as transient parameters only, and reports states from the canonical set honestly.

Consumers then address capabilities, never vendors, exactly as DEVOS-SPEC-024 requires.

---

# Goals

This specification aims to:

- Define the adapter model over capability interfaces per provider family.
- Define normalized capability operations for the AI family as first-class.
- Define the credential contract governing resolved values.
- Define state reporting duties mapping vendor conditions to provider states.
- Define optional health probes, streaming semantics, and quota signaling.
- Recap registration paths and configuration validation for adapter authors.

---

# Non Goals

This specification does not define:

- Concrete vendor integrations, endpoints, or wire protocols
- Routing or selection algorithms, owned by DEVOS-SPEC-039
- Credential storage formats or resolution mechanics, owned by DEVOS-SPEC-036
- Pricing, quota, or billing models
- Language binding idioms or packaging formats

Vendor names appear nowhere in this document because none are needed.

---

# Adapter Model

A provider is implemented as an adapter: a unit implementing CAPABILITY INTERFACES for one family.

Families form the open category set defined in DEVOS-SPEC-024; the AI family is FIRST-CLASS and aligns to the normalization of DEVOS-SPEC-039.

An adapter declares exactly the operations it serves and rejects those it does not, per DEVOS-SPEC-024.

Adapters never address consumers directly; all traffic flows through the Provider Engine defined in DEVOS-SPEC-033 and, for AI capability, through the Router defined in DEVOS-SPEC-039.

## Capability Operations

The AI operations below are illustrative verbs from the open set of DEVOS-SPEC-039.

| Operation   | Request Fields (normalized)                          | Response Fields (normalized)                  |
| ----------- | ---------------------------------------------------- | --------------------------------------------- |
| generate    | capability, context references, options, constraints | content, usage, provider, warnings             |
| summarize   | capability, context references, options, constraints | content, usage, provider, warnings             |
| embed       | capability, input references, options                | content, usage, provider, warnings             |
| stream flag | streaming constraint on any operation above          | chunk sequence of partials plus final response |

Request fields follow the request model of DEVOS-SPEC-039; responses always carry usage metrics and the fulfilling provider identifier.

---

# Normalization Duty

Normalization is the defining duty of every adapter.

Vendor payloads are mapped behind adapters so that consumer-facing shapes stay stable regardless of vendor.

This specification does not duplicate the canonical tables of DEVOS-SPEC-039; adapters implement them.

Adapter faults MUST surface as provider failures, never as corrupted normalized responses, consistent with DEVOS-SPEC-039.

Adding or replacing an adapter MUST NOT change consumer APIs or Workspace structure.

---

# Credential Contract

This contract is the normative centerpiece of this document.

An adapter receives RESOLVED credential values as transient invocation parameters ONLY.

Resolved values cross the invocation boundary once, delivered by the Security Engine per DEVOS-SPEC-028 and DEVOS-SPEC-036, and cease to exist when the invocation ends.

An adapter MUST NOT persist, cache, log, echo, export, or otherwise retain resolved values beyond the invocation.

Credentials exist in configuration exclusively as Secret references; inline credential values are invalid per DEVOS-SPEC-024.

AuthRequired duty: an adapter MUST map authentication failures to AuthRequired state with a reason code instead of surfacing raw vendor errors.

The adapter MUST NOT attempt fallback credentials outside the resolution it was given.

---

# State Reporting Duties

Adapters report honest runtime states from the provider set defined in DEVOS-SPEC-014.

| Vendor Condition        | Reported Provider State |
| ----------------------- | ----------------------- |
| Healthy and usable      | Available               |
| Quota exceeded          | Degraded                |
| Vendor outage           | Unavailable             |
| Authentication failure  | AuthRequired            |
| Response parse failure  | Failed                  |
| Intentionally disabled  | Disabled                |

A provider MUST NOT report Available while a required Secret cannot resolve, per DEVOS-SPEC-024 and DEVOS-SPEC-033.

State changes are published through the Event System per DEVOS-SPEC-037 and consumed by the Health System defined in DEVOS-SPEC-046.

Silent degradation MUST NOT happen; every reduced-capability condition carries a visible signal.

---

# Health Probe

An adapter MAY implement a health probe: a cheap availability check with no side effects.

Probes are consumed by the evaluation cycle of DEVOS-SPEC-033 and by the Health System defined in DEVOS-SPEC-046.

A probe SHOULD complete locally where possible, preserving Offline First behavior.

Probe results inform evaluation but never override honest operation-time reporting.

---

# Streaming Contract

Streaming is a variant of any declared operation, enabled by the constraints field of a request.

Chunks deliver progressively, and each partial result is clearly marked as partial.

Partial results MUST be distinguishable from the final response, which carries complete usage and warnings.

Cancellation propagates downstream and stops further chunks.

Partial-failure semantics follow DEVOS-SPEC-039: a failed stream reports failure through normal failover rules rather than pretending completeness.

---

# Rate and Quota Signaling

Adapters SHOULD emit structured rate and quota hints when vendors expose them.

Hints are machine-readable signals attached to responses and state reports, never free-form text.

Router policies defined in DEVOS-SPEC-039 consume hints for budget guards and downgrade decisions.

Exhausted budgets force explicit denial or downgrade signals upstream; adapters MUST NOT throttle silently on their own authority.

---

# Registration Paths

Providers enter a Workspace through two paths, both recapitulated from DEVOS-SPEC-033.

Static path: manifest-declared provider blocks listing adapter descriptors under providers[].

Dynamic path: plugin contributions registered at enable time through the Plugin Engine.

Both paths record provenance: manifest location for declared providers, contributing plugin id and version for contributed ones.

Withdrawing a contributing plugin removes its contributions atomically.

Duplicate identities inside a Workspace are rejected.

---

# Configuration Validation

Provider configuration MUST validate against provider.schema.json under the reserved namespace https://devos.dev/schemas/v0/, following the schema discipline of Rule 17.

Validation MUST verify identity, name, category recognition, category-contract conformance, declared operations, Secret-reference-only credentials, and absence of inline values.

Invalid configurations keep the provider in Failed or Unknown state, never Available.

Validation output MUST NOT contain credential values, consistent with DEVOS-SPEC-028.

---

# Illustrative Sketch

The following sketch is illustrative neutral pseudocode and non-normative.

```text
adapter ExampleAIAdapter implements ai-family:
  capabilities: [generate, embed]

  generate(request, credentials):
    # credentials arrive resolved and transient across the invocation boundary.
    vendorRequest = mapToVendorGenerate(request)
    raw = vendorCall(vendorRequest, credentials.apiKey)
    if raw.status == AUTH_REJECTED:
      report(AuthRequired, "auth.invalid-credential")
      return
    if raw.status == QUOTA_EXCEEDED:
      report(Degraded, "quota.exceeded")
      return
    return normalize(raw.body)     # content, usage, provider, warnings only

  embed(request, credentials):
    raw = vendorCall(mapToVendorEmbed(request), credentials.apiKey)
    if raw.status == AUTH_REJECTED:
      report(AuthRequired, "auth.invalid-credential")
      return
    return normalize(raw.body)

  probe():
    return cheapLocalCheck()       # optional availability signal
```

---

# Invocation Flow

One diagram shows a normalized AI invocation end to end.

```mermaid
sequenceDiagram

    participant R as AI Router
    participant PE as Provider Engine
    participant SE as Security Engine
    participant A as Adapter
    participant V as Vendor Endpoint

    R->>PE: Resolve candidates for requested capability
    PE-->>R: Selected adapter handle
    R->>PE: Invoke declared operation
    PE->>SE: Authorize consumer and resolve Secret references at use time
    SE-->>A: Deliver resolved values once, transiently
    A->>V: Vendor request mapped behind the adapter
    V-->>A: Vendor payload
    A->>A: Normalize shapes; drop all credential material
    A-->>PE: Normalized result, usage, and state hint
    PE-->>R: Content, usage, provider, warnings
```

---

# Conformance Checklist

An adapter claiming "DevOS SDK compatible v0" provider conformance MUST satisfy every item below.

- [ ] Implements every operation it declares and rejects undeclared ones per DEVOS-SPEC-024.
- [ ] Maps vendor payloads into the normalized request and response shapes of DEVOS-SPEC-039 without leaking dialects upward.
- [ ] Treats resolved credentials as transient invocation parameters and never persists, caches, or logs them.
- [ ] Reports authentication failures as AuthRequired with a reason code, never as raw vendor errors.
- [ ] Emits honest states from the DEVOS-SPEC-014 provider set for every detectable vendor condition.
- [ ] Marks partial results clearly and terminates streams with final or failed status per DEVOS-SPEC-039.
- [ ] Supplies structured rate and quota hints for router policies when available.
- [ ] Validates configuration against provider.schema.json before declaring readiness.
- [ ] Records and preserves provenance for its registration path per DEVOS-SPEC-033.

---

# Provider SDK Invariants

The following invariants MUST always hold.

- Consumers address capabilities, never vendors; adapters confine all vendor knowledge.
- Resolved credential values exist only across the invocation boundary.
- An adapter MUST NOT report Available while a required Secret cannot resolve.
- Replacing an adapter never requires changes to Workspace structure, Profiles, or Projects, restating Rule 4 normatively.
- Partial results are always distinguishable from complete ones.
- Degradation is always signaled explicitly; silence is a defect.
- Provenance is known for every registration path.

---

# Future Extensions

Future Provider SDK specifications may add support for:

- Usage metering feeds per provider and capability
- Cost telemetry for budget-aware routing decisions
- Negotiated capability discovery between providers and consumers
- Cross-Workspace provider federation through DEVOS-SPEC-070

These extensions MUST preserve capability addressing and vendor neutrality without an approved ADR.

---

# References

- DEVOS-SPEC-005 – Guiding Principles
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-024 – Provider Specification
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-033 – Provider Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-039 – AI Router
- DEVOS-SPEC-046 – Health System
- DEVOS-SPEC-050 – SDK Overview
- SPECIFICATION_RULES.md – Repository rule set (Rules 4, 7, 17)
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-059 – Versioning Policy
- https://devos.dev/schemas/v0/ – Reserved schema namespace

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
