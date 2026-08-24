# DevOS

> Build once. Work anywhere. Own your development environment.

## What is DevOS?

DevOS is an open platform **specification** for portable, reproducible, AI-ready development workspaces.
It is not an IDE, not an AI assistant, and not a cloud platform.
It is the connective layer between them: a shared contract that lets projects define their entire development environment once and run it anywhere, across tools, providers, operating systems, and teams.

Read the [Executive Summary](specification/00-overview/001-executive-summary.md) or the [Project Manifesto](PROJECT_MANIFESTO.md) for the full story.

## Status

> **Specification v0.1 — Draft.**
> The specification set is actively developed and not yet stable.
> Per the first rule of [SPECIFICATION_RULES.md](SPECIFICATION_RULES.md), implementations come only after the specification stabilizes.
> Everything marked Enterprise (060–069) or Future (070–079) is forward-looking and requires an approved ADR to activate.

## Why DevOS Exists

Modern development setup is broken:

- Every project starts with hours or days of manual configuration across IDEs, assistants, clouds, databases, containers, secrets, and MCP servers.
- Every new laptop means rebuilding the same environment by hand.
- Every new teammate repeats the same onboarding.
- Every company reinvents the same internal tooling.
- Configuration ends up scattered across hidden application state tied to one machine, one editor, or one vendor.
- Vendors benefit from that lock-in; developers do not.

DevOS eliminates that friction by making the **Workspace** a portable unit owned by the project, described as code, and understood by any compliant tool.

See [DEVOS-SPEC-003 – Problem Statement](specification/00-overview/003-problem-statement.md) for the full analysis.

## Core Concepts

| Concept            | Meaning                                                                    | Canonical Spec                                                        |
| ------------------ | -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Workspace          | The root aggregate owning everything a development environment needs       | [DEVOS-SPEC-020](specification/02-foundation/020-workspace-specification.md) |
| Project            | The codebase a Workspace is built around                                   | [DEVOS-SPEC-021](specification/02-foundation/021-project-specification.md)   |
| Profile            | A named variant of a workspace owning exactly one Environment              | [DEVOS-SPEC-022](specification/02-foundation/022-profile-specification.md)   |
| Environment        | The concrete runtime a Profile materializes                                | [DEVOS-SPEC-023](specification/02-foundation/023-environment-specification.md) |
| Provider           | An interchangeable implementation of a capability (AI, cloud, database)    | [DEVOS-SPEC-024](specification/02-foundation/024-provider-specification.md)  |
| Connection         | A configured link to an external system                                    | [DEVOS-SPEC-025](specification/02-foundation/025-connection-specification.md) |
| Plugin             | An extension adding functionality without modifying the core               | [DEVOS-SPEC-026](specification/02-foundation/026-plugin-specification.md)    |
| Template           | A reusable workspace pattern                                               | [DEVOS-SPEC-027](specification/02-foundation/027-template-specification.md)  |
| Secret             | Sensitive material held securely and never exposed                         | [DEVOS-SPEC-028](specification/02-foundation/028-secret-specification.md)    |
| Workspace Manifest | The declarative, version-controlled description of a Workspace             | [DEVOS-SPEC-029](specification/02-foundation/029-workspace-manifest.md)      |

The domain behind these objects is defined in the [Domain Model](specification/01-domain-model/011-domain-model.md).

## Repository Layout

| Directory        | Contents                                                       |
| ---------------- | -------------------------------------------------------------- |
| [adr/](adr/)     | Architecture Decision Records (accepted, proposed, superseded) |
| [assets/](assets/) | Images and other static resources                            |
| [diagrams/](diagrams/) | Mermaid, C4, UML diagrams organized by type              |
| [examples/](examples/) | Example workspaces, plugins, providers, templates        |
| [rfcs/](rfcs/)   | Request for Comments documents driving feature design          |
| [schemas/](schemas/) | JSON schemas — the canonical contracts for core objects    |
| [specification/](specification/) | The numbered DEVOS-SPEC document set          |
| [templates/](templates/) | Templates for specifications, RFCs, ADRs, decisions    |
| [tools/](tools/) | Generators, validation scripts, and helper tooling             |

Top-level directories are frozen; changes require an approved ADR (Rule 12).

## Specification Map

| Section                                              | Range   | Theme             | Focus                                                              |
| ---------------------------------------------------- | ------- | ----------------- | ------------------------------------------------------------------ |
| [00-overview](specification/00-overview/)            | 000–010 | Overview          | Governance, story, vision, problem, philosophy, principles, terminology |
| [01-domain-model](specification/01-domain-model/)    | 011–015 | Domain Model      | Objects, relationships, lifecycle, states, ownership                |
| [02-foundation](specification/02-foundation/)        | 020–029 | Foundation        | Workspace, Project, Profile, Environment, Provider, Connection, Plugin, Template, Secret, Manifest |
| [03-core-architecture](specification/03-core-architecture/) | 030–039 | Core Architecture | Engines, event system, memory, AI router                     |
| [04-platform](specification/04-platform/)            | 040–049 | Platform          | CLI, dashboard, import, detection, lifecycle, operations            |
| [05-sdk](specification/05-sdk/)                      | 050–059 | SDK               | SDKs, APIs, hooks, events, versioning policy                        |
| [06-enterprise](specification/06-enterprise/)        | 060–069 | Enterprise        | Organizations, teams, RBAC, policy, sync, audit, remote agents      |
| [07-future](specification/07-future/)                | 070–079 | Future            | Marketplace, agents, extra platforms, ecosystem, roadmap            |

Enterprise and Future ranges are intentionally excluded from v0.1 scope and activate only through an ADR.

## Reading Order

New readers should stop after step 5 on a first pass.

1. [Executive Summary](specification/00-overview/001-executive-summary.md) — what DevOS is in one page.
2. [Terminology](specification/00-overview/006-terminology.md) — the shared vocabulary.
3. Domain Model ([011](specification/01-domain-model/011-domain-model.md)–[015](specification/01-domain-model/015-object-ownership.md)) — objects, relationships, lifecycle, states, ownership.
4. Foundation ([020](specification/02-foundation/020-workspace-specification.md)–[029](specification/02-foundation/029-workspace-manifest.md)) — each core object and the manifest.
5. Core Architecture ([030](specification/03-core-architecture/030-system-architecture.md)–[039](specification/03-core-architecture/039-ai-router.md)) — engines, events, AI router.
6. Platform ([040](specification/04-platform/040-cli.md)–[049](specification/04-platform/049-logging.md)) — CLI, dashboard, operational systems.
7. SDK ([050](specification/05-sdk/050-sdk-overview.md)–[059](specification/05-sdk/059-versioning-policy.md)) — programmatic surfaces.
8. Enterprise ([060](specification/06-enterprise/060-organizations.md)–[069](specification/06-enterprise/069-enterprise-roadmap.md)) — optional, beyond v0.1.
9. Future ([070](specification/07-future/070-marketplace.md)–[079](specification/07-future/079-future-vision.md)) — optional, beyond v0.1.

## Documentation & Process

- [PROJECT_MANIFESTO.md](PROJECT_MANIFESTO.md) — why DevOS exists and what we believe.
- [SPECIFICATION_RULES.md](SPECIFICATION_RULES.md) — the twenty rules every contribution must follow.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to propose, write, and review specifications.
- [GOVERNANCE.md](GOVERNANCE.md) — roles, decision making, and ownership.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — how we treat each other.
- [ROADMAP.md](ROADMAP.md) — phases from specification to ecosystem.
- [CHANGELOG.md](CHANGELOG.md) — what changed and when.

## License

The authoritative license text lives in the [LICENSE](LICENSE) file at the repository root.
DevOS is committed to keeping its specifications, schemas, and documentation openly available so that anyone can read, implement, fork, and build on them.
Until the license entry is finalized, contributions are governed by the terms stated there and by [GOVERNANCE.md](GOVERNANCE.md).
