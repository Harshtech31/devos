# 008 – Non Goals

**Document ID:** DEVOS-SPEC-008

**Version:** 0.1

**Status:** Draft

**Category:** Overview

**Depends On:**

- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope

**Referenced By:**

All DevOS Specifications

---

# Abstract

This document records what DevOS is not.

Each entry states a deliberate exclusion, the reasoning behind it, the approach DevOS takes instead, and the conditions under which the decision may be revisited.

Non goals are permanent by default.

Changing one requires the full governance process defined in DEVOS-SPEC-000.

---

# Purpose

This document answers the following question:

> **Which capabilities does DevOS deliberately refuse to become?**

A specification is defined as much by its exclusions as by its features.

This document prevents scope drift and gives contributors a stable contract about what will never be built into DevOS.

Each entry states its statement, reasoning, alternative approach, and revisit conditions.

---

# Goals

This document aims to:

- Record every deliberate exclusion of the platform.
- Explain why each exclusion exists.
- State what DevOS does instead.
- Keep the core platform minimal.

---

# Non Goals

## Not an IDE or Code Editor

**Statement**

DevOS is not an IDE and not a code editor.

**Why Excluded**

Editors are a crowded, fast-moving space; building one would duplicate enormous existing effort.

**What We Do Instead**

DevOS manages Workspaces that editors consume.

Editors are modeled as replaceable Providers.

**Revisit Conditions**

An editing surface would require proof that Provider integration cannot express a required workflow.

## Not an AI Assistant or Chatbot

**Statement**

DevOS is not an AI assistant, coding agent, or chatbot.

**Why Excluded**

AI assistants evolve monthly; embedding one would hard-code today's models into tomorrow's platform.

Assistant behavior belongs to providers, not to the workspace layer.

**What We Do Instead**

AI capability is accessed through the Provider abstraction and routed by the AI Router.

Assistants are replaceable Providers; future autonomous behavior belongs to Agents.

**Revisit Conditions**

Only if the Provider abstraction proves unable to express a required AI capability.

## Not a Cloud Provider or Hosting Platform

**Statement**

DevOS is not a cloud provider and hosts no developer workloads.

**Why Excluded**

Operating infrastructure would create the exact dependency DevOS exists to remove.

It contradicts the cloud-agnostic and Offline First commitments.

**What We Do Instead**

Cloud systems connect through Connections and Providers.

Cloud services extend DevOS; they never define it.

**Revisit Conditions**

Only as optional hosting extensions that never become required for core workflows.

## Not a Container Runtime

**Statement**

DevOS is not a container runtime.

**Why Excluded**

Runtimes are mature external systems; reimplementing them adds risk without adding workspace value.

**What We Do Instead**

Containers are modeled as Resources managed through Providers.

DevOS expresses intent, not container mechanics.

**Revisit Conditions**

Only if the Resource and Provider abstractions prove insufficient for reproducible environments.

## Not a Database Manager

**Statement**

DevOS is not a database manager or database client.

**Why Excluded**

Database tooling is a specialized market; duplicating it would bloat the core platform.

**What We Do Instead**

Databases are external systems reached through Connections.

Their required state is described declaratively inside the Workspace.

**Revisit Conditions**

Only if Connection semantics prove unable to express common management tasks.

## Not a Deployment Platform

**Statement**

DevOS is not a deployment platform and does not ship releases itself.

**Why Excluded**

Deployment pipelines differ per organization; owning one would reintroduce the lock-in DevOS removes.

**What We Do Instead**

Deployments are expressed as Workflows whose steps invoke external systems through Providers.

**Revisit Conditions**

When Workflow and Provider semantics demonstrably fail to cover deployment scenarios.

## Not a Proprietary Ecosystem

**Statement**

DevOS is not a proprietary ecosystem or closed product family.

**Why Excluded**

The project aims to become an open workspace standard; proprietary control would betray its founding beliefs.

**What We Do Instead**

Specifications, schemas, and extension interfaces are public.

The Reference Implementation demonstrates the Specification; it does not own it.

**Revisit Conditions**

Never.

Openness is identity, not strategy.

## Not a Replacement for Git, Package Managers, or CI Systems

**Statement**

DevOS does not replace Git, package managers, or CI systems.

It integrates with them.

**Why Excluded**

These tools solved their problems well; replacing them creates migration cost with no developer benefit.

**What We Do Instead**

They are treated as external systems connected through Connections and invoked through Workflows.

DevOS composes them; it does not absorb them.

**Revisit Conditions**

Only if successor standards emerge and the ecosystem demands unified semantics.

## No Hidden Configuration State

**Statement**

DevOS keeps no hidden configuration state.

**Why Excluded**

Hidden state breaks portability and reproducibility; hidden configuration creates hidden problems.

**What We Do Instead**

All persistent configuration lives in the declarative Workspace Manifest.

Everything else is derived and disposable.

**Revisit Conditions**

Never.

This is a core invariant of Configuration as Code.

## No Mandatory Cloud Dependency

**Statement**

No core DevOS function may require internet access or a hosted service.

**Why Excluded**

Developers must own their environments.

Availability must never depend on third-party infrastructure.

**What We Do Instead**

Core flows run locally.

Cloud services MAY extend DevOS; they can never define it.

**Revisit Conditions**

Only for capabilities that are physically impossible offline, and even then only as optional extensions.

## No Vendor Lock-In by Design

**Statement**

No vendor lock-in by design.

**Why Excluded**

Lock-in betrays developer trust; providers evolve, merge, and disappear.

**What We Do Instead**

Every provider category is replaceable.

Exports remain open; no format is proprietary.

**Revisit Conditions**

Never.

---

# Summary Table

| Non Goal                          | Reason                                  | Instead                                     | Revisit When                              |
| --------------------------------- | --------------------------------------- | ------------------------------------------- | ----------------------------------------- |
| Not an IDE or code editor         | Crowded space, duplicated effort        | Editors are replaceable Providers           | If Provider integration proves inadequate |
| Not an AI assistant or chatbot    | Models change too fast                  | AI Router plus Provider abstraction         | If abstraction cannot express a need      |
| Not a cloud provider              | Would recreate the problem DevOS solves | Clouds connect via Connections              | Optional hosting extensions only          |
| Not a container runtime           | Mature external systems exist           | Containers are Provider-managed Resources   | If Resource abstraction fails             |
| Not a database manager            | Specialized, well-served market         | Databases are Connections                   | If Connections prove insufficient         |
| Not a deployment platform         | Pipelines differ per organization       | Deployments are Workflows                   | If Workflow semantics fall short          |
| Not a proprietary ecosystem       | Openness is the identity                | Public specs, schemas, interfaces           | Never                                     |
| Not a Git/package/CI replacement  | Existing tools solved these problems    | Integration via Connections and Workflows   | Successor standards emerge                |
| No hidden configuration state     | Hidden state breaks reproducibility     | Declarative Workspace Manifest only         | Never                                     |
| No mandatory cloud dependency     | Offline First                           | Local-first core, optional cloud extensions | Physically impossible capabilities        |
| No vendor lock-in                 | Developer trust                         | Replaceable Providers, open exports         | Never                                     |

---

# Guardrails

The following rules MUST always hold.

- This document MUST be checked during every design review.
- Removing an entry MUST follow Rules 13 and 14 of DEVOS-SPEC-000 – Specification Governance.
- Adding any excluded capability back into DevOS requires BOTH an accepted RFC AND an accepted ADR.
- Silent scope growth MUST NOT occur.
- A non goal MUST NOT be bypassed through a plugin that requires core changes.

---

# Future Extensions

Future versions of this document MAY:

- add new entries with full rationale,
- retire entries after RFC and ADR acceptance,
- cross-reference specifications that demonstrate the "instead" approach.

Entries are never weakened silently.

---

# References

- DEVOS-SPEC-000 – Specification Governance
- DEVOS-SPEC-002 – Vision
- DEVOS-SPEC-005 – Guiding Principles
- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-007 – Scope

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
