# DevOS Specification Rules

**Version:** 1.0

**Status:** Active

---

# Purpose

This document defines the mandatory rules governing the DevOS Specification repository.

These rules ensure that DevOS remains consistent, scalable, maintainable, and implementation-independent.

Every contributor must follow these rules before proposing, modifying, or implementing any feature.

These rules apply to:

- Specifications
- RFCs
- ADRs
- Schemas
- Diagrams
- Examples
- Future implementation

---

# Core Philosophy

DevOS is designed as an **open platform specification**, not merely an application.

The specification always takes precedence over implementation.

Implementation follows the specification.

The specification never follows implementation.

---

# Rule 1 — Specification First

No feature may be implemented before it exists in the specification.

Required flow:

Idea

↓

RFC

↓

Discussion

↓

Specification

↓

ADR (if required)

↓

Implementation

↓

Release

Implementation without specification is not permitted.

---

# Rule 2 — Workspace First

Everything in DevOS belongs to a Workspace.

Not:

- User
- CLI
- Dashboard
- AI Provider

Workspace is the primary abstraction.

Every subsystem must integrate through the Workspace.

---

# Rule 3 — Open Specification

The specification must never depend on a single implementation.

The specification should be implementable by:

- DevOS CLI
- Desktop Dashboard
- Web Dashboard
- Third-party applications
- IDE plugins
- Community tools

---

# Rule 4 — Provider Agnostic

DevOS must never depend on a single vendor.

Supported providers are interchangeable.

Examples include:

AI

- OpenAI
- Anthropic
- Google
- Ollama
- OpenRouter

Cloud

- AWS
- Azure
- GCP
- Cloudflare
- DigitalOcean

Databases

- PostgreSQL
- MySQL
- MongoDB
- Redis

Changing providers should not require redesigning DevOS.

---

# Rule 5 — Configuration as Code

All project configuration must exist as human-readable files.

Configuration must be:

- Version controlled
- Reviewable
- Portable
- Reproducible

Configuration must never exist only inside hidden application state.

---

# Rule 6 — Plugin First

If functionality can be implemented as a plugin,
it should not become part of the core platform.

The core should remain as small as possible.

---

# Rule 7 — Offline First

Core functionality must work without internet connectivity.

Cloud integrations are optional extensions.

Offline development is a first-class use case.

---

# Rule 8 — Security by Default

Security must never be optional.

Secrets must:

- never be committed
- never appear in logs
- never be stored unencrypted

Least privilege should always be the default.

---

# Rule 9 — Simplicity Over Features

Every new feature increases complexity.

Features should only exist if they solve a real developer problem.

Avoid feature accumulation.

Prefer composability.

---

# Rule 10 — One Source of Truth

Every concept has one canonical document.

Examples:

Workspace

011-workspace-specification.md

Plugin

018-plugin-specification.md

Dashboard

037-dashboard.md

Never duplicate specifications.

---

# Rule 11 — Stable Document Numbers

Specification numbers are permanent.

Example:

023-workspace-engine.md

This number never changes.

Only the content evolves.

---

# Rule 12 — Stable Repository Structure

Top-level directories are frozen.

No contributor may introduce a new top-level folder without an approved ADR.

---

# Rule 13 — RFC Before Features

Every significant feature starts as an RFC.

RFC lifecycle:

Draft

↓

Proposed

↓

Discussion

↓

Accepted

↓

Implemented

↓

Archived

---

# Rule 14 — ADR for Architectural Decisions

Major architectural changes require an ADR.

Examples:

Changing configuration format

Changing plugin model

Changing workspace lifecycle

Changing storage architecture

---

# Rule 15 — Documentation Consistency

Every specification document must use the standard template.

Required sections:

Purpose

Background

Goals

Non Goals

Architecture

Components

Interfaces

Security

Performance

Examples

Future Work

References

Revision History

---

# Rule 16 — Diagrams are Required

Major specifications must include diagrams.

Preferred formats:

Mermaid

PlantUML

C4

UML

Component diagrams

Sequence diagrams

State diagrams

Deployment diagrams

---

# Rule 17 — Schemas are Canonical

Schemas define the specification.

Documentation explains the schemas.

Implementation validates against the schemas.

Schemas are the single source of truth.

---

# Rule 18 — Backward Compatibility

Breaking changes require:

RFC

ADR

Migration strategy

Version bump

Deprecation notice

---

# Rule 19 — Version Everything

Everything has versions.

Examples:

Specification

Workspace format

Plugin API

Schemas

CLI API

Dashboard API

---

# Rule 20 — Human First

DevOS exists to reduce cognitive load.

Developer experience is more important than adding another feature.

Every feature should answer one question:

"Does this make a developer's life easier?"

If not,

it probably does not belong.

---

# Repository Standards

Repository layout is frozen.

Top-level folders may not change without:

RFC

AND

Approved ADR

---

# Naming Standards

All specification files use:

NNN-name.md

Examples:

001-vision.md

023-workspace-engine.md

051-sdk-overview.md

Document numbers never change.

---

# Specification Lifecycle

Idea

↓

RFC

↓

Specification

↓

ADR

↓

Schema

↓

Implementation

↓

Testing

↓

Release

↓

Maintenance

---

# Contribution Principles

Every contribution should satisfy at least one of the following:

Improve developer experience

Improve portability

Improve interoperability

Improve security

Improve maintainability

Improve extensibility

Otherwise,

the contribution should be reconsidered.

---

# Long-Term Vision

DevOS should become:

- an open specification

- a reference implementation

- an ecosystem

- a community project

The goal is not merely to build another CLI.

The goal is to define the standard for AI-powered software development workspaces.

---

# Final Principle

Whenever uncertainty exists, choose the solution that is:

- simpler
- more portable
- easier to understand
- easier to extend
- easier to maintain
- implementation independent

These six principles take precedence over convenience.
