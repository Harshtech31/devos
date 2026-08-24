# 075 – Mobile Platform

**Document ID:** DEVOS-SPEC-075

**Version:** 0.1

**Status:** Draft

**Category:** Future

**Depends On:**

- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-041 – Dashboard
- DEVOS-SPEC-046 – Health System
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-057 – Events API
- DEVOS-SPEC-058 – CLI API
- DEVOS-SPEC-062 – RBAC
- DEVOS-SPEC-074 – Web Platform

**Referenced By:**

- DEVOS-SPEC-073 – Desktop Platform
- DEVOS-SPEC-074 – Web Platform
- DEVOS-SPEC-079 – Future Vision

---

# Abstract

This document defines the Mobile Platform, the forward-looking companion form factor for DevOS focused on observation, approval, and light interaction rather than full workspace editing.

It defines the companion scope, approval-flow duties for enterprise governance, connectivity honesty, and parity boundaries against full surfaces.

The phone in your pocket is a control surface, not a second workstation.

This specification is forward-looking and activates only through an approved RFC and ADR.

---

# Purpose

This specification answers the following question:

> **What is a mobile client genuinely good for, and how does its narrowness become a strength instead of a limitation?**

Mobile excels at watching workspaces and answering requests quickly: approvals, status checks, notifications.

By scoping deliberately, it stays secure, fast, and honest about degraded connectivity.

---

# Goals

This specification aims to:

- Define the companion scope: observe, approve, notify, adjust.
- Define approval-flow integration with hooks and policies.
- Define connectivity-honest behavior on unreliable networks.
- Define authentication and device-bound session discipline.
- Preserve parity where mobile operations overlap other surfaces.

---

# Non Goals

This specification does not define:

- Full manifest authoring or heavy editing flows
- Device platform specifics such as store review requirements
- Wearable or embedded form factors
- Cloud commercial offerings, owned by DEVOS-SPEC-076

---

# Companion Scope

Mobile capability divides into four deliberate lanes.

| Lane      | Capabilities                                                   | Authority Path                             |
| --------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| Observe   | Health summaries, states, recent events.                          | Read-scoped SDK handles per DEVOS-SPEC-054.     |
| Approve   | Answer hook vetoes, policy escalations, agent requests.            | Hook and policy decision surfaces per 056/063.  |
| Notify    | Receive filtered event pushes.                                     | Subscriptions per DEVOS-SPEC-057 grants only.   |
| Adjust    | Narrow mutations such as toggling profiles or rotating secrets.     | Mutations through standard engine gates.        |

Anything outside these lanes belongs to desktop or web surfaces per DEVOS-SPEC-073 and DEVOS-SPEC-074.

---

# Approval Flows

Mobile makes enterprise governance responsive.

```mermaid

sequenceDiagram

    participant Op as Guarded Operation
    participant HN as Notification Path
    participant M as Mobile Client
    participant HV as Hook Veto Surface

    Op->>HN: Pending decision emitted as event
    HN->>M: Push notification within granted topics
    M->>M: Authenticate principal and re-evaluate grants
    alt Approved within window
        M->>HV: Submit approval decision
        HV-->>Op: Proceed with attribution
    else Expired or denied
        M-->>Op: Veto stands; operation aborts safely
    end
```

Rules:

- Decisions attribute to the approving principal and device session.
- Decision windows expire safely toward veto, honoring fail-closed defaults.
- Approval authority follows role bindings once RBAC activates per DEVOS-SPEC-062.

---

# Connectivity Honesty

Mobile networks fail constantly; the surface must tell the truth.

Rules:

- Stale data carries visible age markers rather than pretending freshness.
- Queued decisions persist durably and flush on reconnect without silent retries past expiry.
- Full functionality degrades to observation honestly, consistent with Offline First values even though mobile assumes connectivity.

---

# Device Session Discipline

Companion devices demand tighter session hygiene.

| Duty          | Requirement                                                            |
| ------------- | -------------------------------------------------------------------------- |
| Device binding | Sessions bind to specific devices with revocable identity.                  |
| Least scope   | Default scopes cover observation plus explicitly added approval rights.     |
| Timeout       | Idle sessions invalidate faster than desktop norms, configurable by policy. |
| Remote wipe   | Revocation renders cached sensitive views unreadable where custody allows.  |

Secret display follows identical prohibitions to web clients: raw values never reach device storage in any encoding.

---

# Relationship to Version 0.1

Version 0.1 defines no remote clients of any kind.

The Mobile Platform adds governed companionship atop hosted foundations laid by DEVOS-SPEC-074.

Activation requires an RFC covering scope and session model, an approved ADR preserving aggregate invariants, and conformance criteria before implementation ships.

Until activated, implementations MUST NOT ship partial mobile behavior under this document's name.

---

# Future Extension Invariants

The following invariants MUST hold when activated.

- Mobile never exceeds its declared lanes regardless of client capability.
- Approvals attribute fully and expire safely toward denial.
- Cached content obeys redaction absolutely.
- Parity holds wherever lanes overlap other surfaces.
- Degraded connectivity reports honestly everywhere.

These MUST NOT break the single Workspace aggregate model.

---

# Security Requirements

When activated, this extension enforces:

- Deny-by-default evaluation of every device-session grant per DEVOS-SPEC-036.
- Raw-secret absence from device storage and payloads per DEVOS-SPEC-028.
- Attribution of every decision and adjustment through audit direction per DEVOS-SPEC-065.

---

# Future Extensions

Future specifications may add support for:

- Biometric-gated approval classes under explicit ADR
- Watch-class ultra-companion surfaces limited to observe-and-approve
- Offline-first field kits syncing on reconnection via DEVOS-SPEC-064

These extensions require their own RFCs and ADRs and MUST preserve the invariants above.

---

# References

- DEVOS-SPEC-000 – Specification Governance
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope
- DEVOS-SPEC-011 – Domain Model
- SPECIFICATION_RULES.md – Repository rule set (Rule 7)
- DEVOS-SPEC-020 – Workspace Specification
- DEVOS-SPEC-028 – Secret Specification
- DEVOS-SPEC-030 – System Architecture
- DEVOS-SPEC-036 – Security Engine
- DEVOS-SPEC-046 – Health System
- DEVOS-SPEC-050 – SDK Overview
- DEVOS-SPEC-054 – Workspace SDK
- DEVOS-SPEC-055 – API Specification
- DEVOS-SPEC-056 – Hooks API
- DEVOS-SPEC-057 – Events API
- DEVOS-SPEC-058 – CLI API
- DEVOS-SPEC-062 – RBAC
- DEVOS-SPEC-063 – Policy Engine
- DEVOS-SPEC-065 – Audit System
- DEVOS-SPEC-073 – Desktop Platform
- DEVOS-SPEC-074 – Web Platform
- DEVOS-SPEC-076 – Cloud Platform
- DEVOS-SPEC-079 – Future Vision

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
