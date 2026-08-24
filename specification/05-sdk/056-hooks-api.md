# 056 – Hooks API

**Document ID:** DEVOS-SPEC-056

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
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-059 – Versioning Policy

**Referenced By:**

- DEVOS-SPEC-026 – Plugin Specification
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-051 – Plugin SDK
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-057 – Events API

---

# Abstract

This document defines the Hooks API, the Integration-tier contract for synchronous extension points embedded in platform operations.

A hook is a named interception point on a public operation path where an authorized subscriber runs inline and MAY veto the operation before it completes.

It defines hook point structure, registration duties, ordering rules, decision semantics, bounded-time obligations, failure handling, and the distinction from the asynchronous events surface defined in DEVOS-SPEC-057.

Hooks are the ONLY mechanism through which extensions can stop an operation; everything else observes after the fact.

---

# Purpose

This specification answers the following question:

> **How can authorized code inspect and veto consequential operations synchronously, without ever corrupting them?**

Hook handlers run inside the operation they intercept, so their contract is strict: bounded time, read-only context, one explicit decision, fail-closed behavior.

Veto is safety-critical power, so this document makes its grant, scope, and cost explicit.

---

# Goals

This specification aims to:

- Define the structure and naming of hook points.
- Define registration through declared plugin contributions.
- Define handler invocation context and its read-only discipline.
- Define decision semantics including veto and fail-closed behavior.
- Define deterministic ordering and short-circuit rules.
- Define bounded-time enforcement and timeout consequences.
- Provide a starter catalog of Version 0.1 hook points.

---

# Non Goals

This specification does not define:

- Event delivery or subscription mechanics, owned by DEVOS-SPEC-057
- Plugin isolation mechanics, owned by DEVOS-SPEC-032
- Sandbox implementation techniques
- Hook payload wire schemas
- Marketplace policy for hook-heavy plugins, deferred to DEVOS-SPEC-070
- Asynchronous follow-up work patterns, which belong to event subscribers

---

# Hook Point Model

A hook point is a named, typed position on one public operation path.

| Element      | Required | Description                                                            |
| ------------ | -------- | ---------------------------------------------------------------------- |
| name         | Yes      | Stable dotted identifier under `devos.hooks.<domain>.<operation>`.     |
| position     | Yes      | Before-commit stage of exactly one named public operation.              |
| context type | Yes      | Declared read-only view of the operation: actor, object refs, parameters. |
| decision set | Yes      | Exactly proceed or veto with a reason code.                             |

Model rules:

- Hook points exist only where their owning operation specifications declare them.
- A hook point MUST sit before durable commit so a veto prevents all effects.
- Context exposes identifiers, references, and parameter values; it MUST NEVER expose raw secret values, consistent with DEVOS-SPEC-028.
- Renaming or removing a published hook point is a breaking change under DEVOS-SPEC-059.

---

# Registration

Subscriptions are declared, never ambient.

Registration rules:

- Plugins declare intended hook subscriptions in their manifests and register nothing themselves; the Plugin Engine registers declared subscriptions at enable time per DEVOS-SPEC-032.
- A subscription naming a nonexistent hook point is rejected as unknown-interface, keeping the plugin from enabling, consistent with DEVOS-SPEC-032.
- Subscription requires an explicit grant following the permission grammar, such as `hooks:intercept:devos.hooks.workspace.*`, evaluated deny-by-default per DEVOS-SPEC-036.
- Revocation ends matching invocations for subsequent evaluations without reinstallation.
- Disabling the owning plugin withdraws its subscriptions atomically.

Unregistered components are never invoked; there are no global wildcard observers at hook depth.

---

# Invocation Semantics

When an operation reaches a registered hook point, the host invokes each subscribed handler inline.

Invocation contract:

- Handlers receive the declared read-only context plus the correlation identifier of the running operation.
- Handlers return exactly one decision: proceed, or veto carrying a stable reason code and human-readable reason.
- Handlers MUST NOT mutate shared state, emit blocking work, or call back into the intercepted operation.
- Handler faults count as vetoes; a throwing handler blocks the operation and the fault is recorded against the subscribing plugin per the isolation model of DEVOS-SPEC-032.

Fail-closed is absolute: any uncertainty resolves to veto, mirroring deny-by-default authorization.

## Ordering and Short-Circuit

- Execution order MUST be deterministic for identical registration state, and hosts MUST document the order rule they implement.
- The first veto short-circuits remaining handlers and aborts the operation with that reason.
- Handlers after a veto never run, and their non-execution is unobservable except through the emitted rejection record.

```mermaid
sequenceDiagram

    participant Op as Operation
    participant H as Host
    participant HA as Hook Subscriber A
    participant HB as Hook Subscriber B

    Op->>H: Reach registered hook point
    H->>HA: Invoke with read-only context
    HA-->>H: Proceed
    H->>HB: Invoke with read-only context
    HB-->>H: Veto (reasonCode, reason)
    H-->>Op: Abort before commit
    Note over H: Remaining handlers skipped; rejection recorded
```

On full consent the operation continues to commit exactly as if no hooks existed, because proceeding adds no effects.

---

# Bounded-Time Obligations

Inline execution makes time a correctness concern.

Rules:

- Every hook point declares a maximum handler budget; hosts enforce it.
- A handler exceeding its budget is treated as a veto carrying a timeout reason code, never silently continued.
- Budgets SHOULD be small enough that hooked operations stay interactive.
- Long-running reactions to an operation belong in event subscribers per DEVOS-SPEC-057, never inside hook handlers.

Hosts MAY suspend misbehaving subscribers according to plugin isolation policy after repeated timeouts, consistent with DEVOS-SPEC-032.

---

# Starter Catalog

The following catalog seeds Version 0.1 with coverage over consequential operations.

Each entry declares the operation it guards; positions are uniformly before commit.

| Hook Point                              | Guarded Operation                       | Typical Veto Purpose                        |
| --------------------------------------- | --------------------------------------- | ------------------------------------------- |
| devos.hooks.workspace.activate          | Workspace Activate per DEVOS-SPEC-044.  | Policy gates beyond the built-in gate.       |
| devos.hooks.workspace.delete            | Workspace Delete per DEVOS-SPEC-044.    | Retention holds before destructive cascades. |
| devos.hooks.secret.rotate               | Secret rotation per DEVOS-SPEC-028.     | Change-control windows on sensitive material.|
| devos.hooks.plugin.enable               | Plugin Enable per DEVOS-SPEC-032.       | Supply-chain review of new extensions.       |
| devos.hooks.template.instantiate        | Template instantiation per DEVOS-SPEC-035. | Constrain creation into managed scopes.   |
| devos.hooks.workflow.run                | Workflow start per Workflow contracts.  | Approval flows before automation executes.   |

Catalog entries are additions-only in MINOR releases; removals or renames are breaking changes per DEVOS-SPEC-059.

Operations without listed hook points offer no interception in Version 0.1.

---

# Hooks versus Events

This section restates the canonical distinction fixed by DEVOS-SPEC-037 and binds it to surfaces.

| Aspect          | Hooks (this document)                 | Events (DEVOS-SPEC-057)                   |
| --------------- | --------------------------------------- | ------------------------------------------------ |
| Execution model | Synchronous lifecycle callback          | Asynchronous notification                        |
| Veto power      | May veto and abort the operation        | Cannot veto anything                             |
| Timing          | Runs inline during the intercepted step | Runs after the fact, at delivery time            |
| Coupling        | Tight coupling between caller and hook  | No coupling between emitter and subscriber       |
| Failure effect  | Blocks the operation, fail-closed       | Isolated; never affects the emitter              |

Choosing wrongly is a design defect: approval needs hooks, awareness needs events.

---

# Conformance Checklist

A binding claiming "DevOS SDK compatible v0" Hooks conformance MUST satisfy every item below.

- [ ] Invokes only declared, granted, enabled subscribers at declared hook points.
- [ ] Provides read-only context that cannot expose raw secret values.
- [ ] Accepts exactly proceed or veto decisions and treats faults as vetoes.
- [ ] Enforces declared time budgets and converts overruns into timeout vetoes.
- [ ] Guarantees deterministic order for identical registration state and documents the rule.
- [ ] Short-circuits on first veto and skips remaining handlers.
- [ ] Records every veto with subscriber identity, reason code, and correlation identifier.

---

# Hooks API Invariants

The following invariants MUST always hold.

- Veto power exists exclusively through registered hooks; no other path stops an operation.
- Unregistered, ungranted, or disabled subscribers never execute.
- Handler context is read-only and secret-free.
- Any fault, overrun, or uncertainty resolves to veto, never to silent continuation.
- Hook execution adds no observable effect to operations that proceed.
- Published hook points are stable identifiers governed by DEVOS-SPEC-059.

---

# Security Requirements

The following obligations are numbered and normative.

1. Subscription MUST be an explicitly granted capability evaluated deny-by-default per DEVOS-SPEC-036; absence of a grant equals absence of the handler.
2. Handler context MUST pass the Redaction Service of DEVOS-SPEC-036 wherever it becomes observable, including diagnostics and audit records.
3. Vetoes MUST be recorded with acting identity so responsibility for blocked operations is always attributable.
4. A handler MUST NOT gain authority over objects by virtue of interception; it decides, it never acts.
5. Repeated malicious vetoes SHOULD be containable through suspension per DEVOS-SPEC-032 without affecting unrelated plugins.

---

# Performance Requirements

- Inline budgets SHOULD keep hooked operations within interactive latency targets.
- Subscription lookup SHOULD scale with granted subscribers, not installed plugins.
- Hosts SHOULD evaluate hook registrations at enable time so runtime dispatch costs remain flat.
- Rejection recording SHOULD be asynchronous relative to the aborted caller once the veto returns.

---

# Future Extensions

Future Hooks API specifications may add support for:

- Mutation proposals letting handlers adjust parameters under strict schemas
- Asynchronous two-phase approvals with suspended operations
- Additional guarded operations across engine catalogs
- Policy-driven automatic subscription management through DEVOS-SPEC-063

These extensions MUST preserve fail-closed semantics, bounded time, and read-only default contexts unless an approved ADR changes them.

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
- SPECIFICATION_RULES.md – Repository rule set (Rule 6)
- DEVOS-SPEC-032 – Plugin Engine
- DEVOS-SPEC-035 – Template Engine
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-037 – Event System
- DEVOS-SPEC-044 – Workspace Lifecycle
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-051 – Plugin SDK
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-057 – Events API
- DEVOS-SPEC-059 – Versioning Policy
- DEVOS-SPEC-063 – Policy Engine
- DEVOS-SPEC-070 – Marketplace

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
