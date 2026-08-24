# 057 – Events API

**Document ID:** DEVOS-SPEC-057

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
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-055 – API Specification

**Referenced By:**

- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-051 – Plugin SDK
- DEVOS-SPEC-054 – Workspace SDK
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-065 – Audit System

---

# Abstract

This document defines the Events API, the Integration-tier contract through which authorized code subscribes to and publishes on public event topics.

It specifies the subscription surface with topic patterns, the publication surface for authorized producers, handler obligations under at-least-once delivery, authorization grammar, workspace scoping, and error reporting.

The API packages the backbone guarantees of the Event System defined in DEVOS-SPEC-037 into a callable surface.

Events inform; they never veto anything.

---

# Purpose

This specification answers the following question:

> **How do external consumers and producers use events programmatically without weakening the guarantees of the bus?**

Consumers subscribe with granted topic patterns and receive complete envelopes through isolated handlers.

Producers publish well-formed envelopes to topics they are authorized for.

Neither side gains coupling to the other beyond the shared topic contract.

---

# Goals

This specification aims to:

- Define the subscription surface including pattern semantics.
- Define the publication surface and its validation duties.
- Define handler obligations under delivery tiers.
- Define authorization for subscriptions and publications.
- Define workspace scoping and boundary isolation for callers.
- Define error classes visible through this surface.
- Provide the conformance checklist for bindings claiming this tier.

---

# Non Goals

This specification does not define:

- Bus internals, transport, or routing mechanics, owned by DEVOS-SPEC-037
- Envelope field definitions beyond recapitulation, canonical in DEVOS-SPEC-037
- Hook interception or veto semantics, owned by DEVOS-SPEC-056
- Enterprise audit retention and queryability, deferred to DEVOS-SPEC-065
- Replay from history, excluded in Version 0.1 per DEVOS-SPEC-037 Future Extensions
- Language binding idioms

---

# Subscription Surface

A subscription binds one consumer to one topic pattern inside exactly one Workspace.

| Element        | Required | Description                                                            |
| -------------- | -------- | ------------------------------------------------------------------------ |
| topics pattern | Yes      | Dotted pattern over published topics, such as `devos.connection.*`.      |
| consumer       | Yes      | Registered identity receiving deliveries, such as a plugin or tool.       |
| scope          | Yes      | Exactly one Workspace; cross-Workspace delivery is structurally absent.   |

Subscription rules recapitulated from DEVOS-SPEC-037:

- A consumer MAY hold multiple subscriptions with distinct patterns.
- Authorization is deny-by-default per topic before every delivery, evaluated consistently with the Security Engine defined in DEVOS-SPEC-036.
- Subscribing to an ungranted topic is rejected as unauthorized-topic rather than silently ignored.
- Revocation of a grant ends matching deliveries for subsequent evaluations without unsubscription storms.
- An event published in one Workspace MUST NEVER reach a subscription held in another.

Pattern semantics follow the lowercase dotted convention of DEVOS-SPEC-037, where a trailing segment wildcard matches any single trailing segment sequence within one domain subtree.

---

# Publication Surface

Authorized producers publish envelopes onto public topics.

Publication rules:

- The publisher names one existing public topic and supplies payload data by reference.
- The surface validates structural envelope completeness at publish time and rejects malformed input as malformed-envelope, consistent with DEVOS-SPEC-037.
- Publishing requires an explicit grant following the permission grammar, such as `events:publish:devos.memory.*`, evaluated deny-by-default per DEVOS-SPEC-036.
- Envelopes and payloads MUST NOT contain secret values, consistent with DEVOS-SPEC-028.
- Publication is non-blocking with respect to subscribers regardless of subscriber count, preserving the performance stance of DEVOS-SPEC-037.

Publishers never learn subscriber identities or outcomes; delivery failures are recorded by the bus against consumers, never reported back as publication errors.

---

# Handler Obligations

Delivery follows the tier classification fixed by DEVOS-SPEC-037.

| Tier | Classification    | Handler Obligation                                        |
| ---- | ------------------- | ----------------------------------------------------------- |
| A    | Durable audit-grade | Treat as at-least-once; handling SHOULD be durable-aware.   |
| B    | Operational         | Treat as at-least-once with idempotent processing.          |
| C    | Ephemeral UI        | Treat as best-effort; never build correctness upon Tier C.  |

Handler rules:

- Handlers run in isolation; one failing handler affects neither emitters, the bus, nor sibling subscribers, consistent with DEVOS-SPEC-037.
- Handlers SHOULD be bounded in time so slow processing degrades into buffering or shedding per tier instead of stalling delivery.
- Repeated failures MAY suspend that subscriber's deliveries pending remediation, local to one consumer only.
- Handlers MUST be idempotent because at-least-once delivery permits redelivery.
- Handlers observing an envelope reconstruct context through correlationId and payloadReference rather than ambient state.

Suspension and resumption are observable through the surface as typed status changes on the affected subscription.

---

# Authorization Grammar

Topic access uses scoped permission strings following the grammar of DEVOS-SPEC-051.

| Example String                        | Meaning                                                  |
| -------------------------------------- | -------------------------------------------------------- |
| events:subscribe:devos.workspace.*     | Subscribe to Workspace-domain lifecycle topics.          |
| events:subscribe:devos.connection.state.changed | Subscribe to exactly one topic.                 |
| events:publish:devos.plugin.custom     | Publish on one plugin-owned public topic.                |

Rules:

- Grants name patterns or exact topics; broader grants imply their narrower matches.
- Absent, ambiguous, or expired grants resolve to denial, consistent with deny-by-default evaluation in DEVOS-SPEC-036.
- Security-relevant topics such as `devos.secret.rotated` and `devos.access.denied` remain subscribable only where policy grants them, feeding audit tooling aligned with DEVOS-SPEC-065.

---

# Error Classes

The surface reports the following classes to callers.

| Error Class         | Trigger                                          | Required Behavior                                       |
| ------------------- | ------------------------------------------------ | ------------------------------------------------------- |
| malformed-envelope  | Published envelope fails structural validation.   | Reject at publish time and report a reason code.         |
| unauthorized-topic  | Subscription or publication names an ungranted topic. | Deny the call with a typed error per DEVOS-SPEC-055. |
| unknown-topic       | Publication targets a nonexistent public topic.   | Reject the publication; suggest nearest valid namespace. |
| subscription-suspended | Consumer exceeded its failure threshold.       | Report suspended status and remediation guidance.        |
| delivery-backlog    | Consumer buffer pressure reached tier limits.     | Report honestly; apply tier shedding per DEVOS-SPEC-037. |

Errors carry reasonCode values from owned families plus correlation identifiers per the unified model of DEVOS-SPEC-055.

---

# Interaction Flow

One diagram shows subscribe, publish, and isolated delivery end to end.

```mermaid
sequenceDiagram

    participant P as Producer
    participant S as Events Surface
    participant B as Event Bus (037)
    participant SA as Subscriber A
    participant SB as Subscriber B

    SA->>S: Subscribe devos.template.*
    S->>B: Register authorized subscription
    P->>S: Publish devos.template.instantiated
    S->>S: Validate envelope and grants
    S->>B: Accept envelope
    B->>SA: Deliver envelope (Tier B)
    B->>SB: Deliver envelope
    SB--xB: Handler fault raised
    Note over B: Failure isolated to Subscriber B; A unaffected
    S-->>P: Accepted (no subscriber knowledge)
```

---

# Conformance Checklist

A binding claiming "DevOS SDK compatible v0" Events-tier conformance MUST satisfy every item below.

- [ ] Rejects subscriptions and publications on ungranted topics with typed denial per DEVOS-SPEC-055.
- [ ] Validates envelope completeness at publish time before accepting any event.
- [ ] Delivers only inside one Workspace and never crosses aggregate boundaries.
- [ ] Isolates handler failures from emitters, the bus, and sibling subscribers.
- [ ] Honors tier semantics including best-effort behavior for Tier C.
- [ ] Reports suspension and backlog states honestly on affected subscriptions.
- [ ] Never returns secret values from any envelope, payload, or diagnostic.

---

# Events API Invariants

The following invariants MUST always hold.

- Consumers receive only what they are authorized and subscribed to see.
- No subscription or publication escapes its Workspace scope.
- Events never veto, delay, or steer the operations that produced them.
- Malformed envelopes never enter delivery.
- Handler failures never propagate upward to publishers.
- At-least-once tiers behave identically across conformant implementations.
- Secret values never appear in any delivered or published content.

---

# Security Requirements

The following obligations are numbered and normative.

1. Topic access MUST be granted explicitly and evaluated deny-by-default per DEVOS-SPEC-036 on every subscription, publication, and delivery.
2. Event content MUST pass the Redaction Service of DEVOS-SPEC-036 wherever it becomes observable through this surface.
3. Security-grade topics MUST remain protected by narrower grants than operational topics, preserving least privilege.
4. Denials MUST be auditable through emitted security events per DEVOS-SPEC-037 without disclosing whether unrelated topics exist.
5. Bindings MUST NOT offer bulk export modes that bypass per-topic grants or tier retention rules.

---

# Performance Requirements

- Subscription registration SHOULD complete without network round trips where the addressed Workspace is local, preserving Offline First behavior.
- Delivery dispatch SHOULD scale linearly with active subscriptions, consistent with DEVOS-SPEC-037.
- Slow consumers SHOULD absorb pressure through buffering and tier-based shedding rather than stalling producers.
- Pattern matching SHOULD compile once per subscription rather than reevaluating per event.

---

# Future Extensions

Future Events API specifications may add support for:

- Replay windows over recorded history with grant-aware filtering
- Cursor-based historical queries aligned with audit tooling
- Federation bridges carrying events across instances under explicit policy
- Dead-letter inspection surfaces for undeliverable events

These extensions MUST preserve the envelope contract, deny-by-default topic authorization, and the no-veto rule without an approved ADR.

They MUST NOT break the single Workspace aggregate model.

---

# References

- DEVOS-SPEC-005 – Guiding Principles
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-030 – System Architecture
- SPECIFICATION_RULES.md – Repository rule set (Rule 7)
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-049 – Logging
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-051 – Plugin SDK
- DEVOS-SPEC-054 – Workspace SDK
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-056 – Hooks API
- DEVOS-SPEC-058 – CLI API
- DEVOS-SPEC-059 – Versioning Policy
- DEVOS-SPEC-065 – Audit System

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
