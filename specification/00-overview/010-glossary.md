# 010 – Glossary

**Document ID:** DEVOS-SPEC-010

**Version:** 0.1

**Status:** Draft

**Category:** Overview

**Depends On:**

- DEVOS-SPEC-006 – Terminology

**Referenced By:**

All DevOS Specifications

---

# Abstract

This document provides a quick index of DevOS terminology.

It summarizes each term in one line and points to the document that defines it canonically.

This document defines nothing.

---

# Purpose

This document answers the following question:

> **Where does a term mean what it means?**

The canonical definitions of every DevOS term live in DEVOS-SPEC-006 – Terminology.

This glossary exists only for fast lookup while reading and reviewing the specification set.

If any summary here appears to conflict with DEVOS-SPEC-006, DEVOS-SPEC-006 wins.

---

# Goals

This document aims to:

- Give readers a one-line reminder for every core term.
- Point each term to its canonical document.
- Index lifecycle stages, runtime states, and relationship types.
- Expand abbreviations used across the specification set.

---

# Non Goals

This document does not:

- define any term,
- override DEVOS-SPEC-006,
- introduce new concepts,
- replace reading the canonical documents.

---

# Usage Rules

The following rules MUST hold:

- This document MUST NOT be cited as a source of definitions.
- Authors MUST cite DEVOS-SPEC-006 when defining or reusing a term.
- Summaries in this index are reminders, never specifications.
- New terms MUST be added to DEVOS-SPEC-006 first, then indexed here.

---

# Term Index

Alphabetical quick index of core terms.

| Term                     | One-Line Meaning                                                    | Canonical Doc   |
| ------------------------ | ------------------------------------------------------------------- | --------------- |
| Actor                    | Human or system that owns a Workspace from outside the domain aggregate | DEVOS-SPEC-015 |
| Agent                    | Performs autonomous work on behalf of the user                       | DEVOS-SPEC-006 |
| API                      | Versioned contract between DevOS components                          | DEVOS-SPEC-006 |
| CLI                      | Terminal access to DevOS; equivalent in capability to the Dashboard  | DEVOS-SPEC-006 |
| Connection               | Defines how DevOS communicates with an external system               | DEVOS-SPEC-006 |
| Dashboard                | The graphical interface implementation; not the platform itself      | DEVOS-SPEC-006 |
| Engine                   | Core subsystem responsible for managing one domain                   | DEVOS-SPEC-006 |
| Environment              | Runtime configuration owned by exactly one Profile                   | DEVOS-SPEC-006 |
| Event                    | Something that occurred inside DevOS; may trigger Workflows          | DEVOS-SPEC-006 |
| Extension                | Enhances an existing feature; cannot introduce new capabilities      | DEVOS-SPEC-006 |
| Hook                     | User-defined extension point executed when Events occur              | DEVOS-SPEC-006 |
| Module                   | Internal implementation unit inside an Engine; not exposed to users  | DEVOS-SPEC-006 |
| Plugin                   | Extends DevOS functionality without modifying the core platform      | DEVOS-SPEC-006 |
| Profile                  | One configurable environment inside a Workspace                      | DEVOS-SPEC-006 |
| Project                  | The software system being developed; managed by its Workspace        | DEVOS-SPEC-006 |
| Provider                 | Interchangeable implementation of a service category                 | DEVOS-SPEC-006 |
| Reference Implementation | Official implementation demonstrating the Specification              | DEVOS-SPEC-006 |
| Registry                 | Collection of reusable objects                                       | DEVOS-SPEC-006 |
| Resource                 | Something managed through a Provider                                 | DEVOS-SPEC-006 |
| SDK                      | Enables third parties to extend DevOS through stable public interfaces | DEVOS-SPEC-006 |
| Schema                   | Structure of DevOS configuration files; canonical and implementation independent | DEVOS-SPEC-006 |
| Secret                   | Confidential information required by a Workspace; never logged       | DEVOS-SPEC-006 |
| Service                  | Performs one well-defined responsibility inside DevOS                | DEVOS-SPEC-006 |
| Specification            | Defines how DevOS behaves; takes precedence over code                | DEVOS-SPEC-006 |
| Task                     | One atomic, repeatable, observable unit of work                      | DEVOS-SPEC-006 |
| Template                 | Reusable project structure that accelerates Workspace creation       | DEVOS-SPEC-006 |
| Workflow                 | Ordered collection of Tasks                                          | DEVOS-SPEC-006 |
| Workspace                | Primary organizational unit and the single Aggregate Root of DevOS   | DEVOS-SPEC-006 |
| Workspace Manifest       | Canonical portable configuration describing a Workspace              | DEVOS-SPEC-006 |
| Workspace Package        | Distributable Workspace carrying all metadata to recreate it         | DEVOS-SPEC-006 |

---

# Lifecycle Stage Index

Canonical source: DEVOS-SPEC-013 – Object Lifecycle.

Stages proceed in order; Active MAY transition directly to Deleted.

Deleted is terminal.

| Stage      | One-Line Meaning                                    | Canonical Doc   |
| ---------- | --------------------------------------------------- | --------------- |
| Created    | Object exists but carries no configuration yet      | DEVOS-SPEC-013 |
| Configured | Configuration supplied but not yet validated        | DEVOS-SPEC-013 |
| Validated  | Configuration has passed validation                 | DEVOS-SPEC-013 |
| Active     | Object operates normally                            | DEVOS-SPEC-013 |
| Archived   | Object retained but inactive                        | DEVOS-SPEC-013 |
| Deleted    | Terminal stage; object no longer exists             | DEVOS-SPEC-013 |

---

# Runtime State Index

Canonical source: DEVOS-SPEC-014 – State Model.

These are the global runtime states shared across objects.

Object-specific state sets are defined in DEVOS-SPEC-014.

| State     | One-Line Meaning                              | Canonical Doc   |
| --------- | --------------------------------------------- | --------------- |
| Unknown   | State cannot be determined yet                | DEVOS-SPEC-014 |
| Ready     | Operating normally and available              | DEVOS-SPEC-014 |
| Busy      | Operational and currently processing work     | DEVOS-SPEC-014 |
| Degraded  | Operational with reduced capability           | DEVOS-SPEC-014 |
| Failed    | Not operational                               | DEVOS-SPEC-014 |
| Disabled  | Intentionally deactivated                     | DEVOS-SPEC-014 |

---

# Relationship Type Index

Canonical source: DEVOS-SPEC-012 – Domain Relationships.

| Relationship | One-Line Meaning                                        | Canonical Doc   |
| ------------ | ------------------------------------------------------- | --------------- |
| Owns         | Parent controls the existence and lifecycle of the child | DEVOS-SPEC-012 |
| Contains     | Parent holds the child inside its boundary               | DEVOS-SPEC-012 |
| Uses         | Object consumes a capability of another object           | DEVOS-SPEC-012 |
| References   | Object points to another object without owning it        | DEVOS-SPEC-012 |
| Registers    | Object makes another object discoverable in a Registry   | DEVOS-SPEC-012 |

---

# Abbreviations

| Abbreviation | Meaning                                                        |
| ------------ | -------------------------------------------------------------- |
| DevOS        | The open platform specification for AI-powered development workspaces |
| RFC          | Request For Comments                                            |
| ADR          | Architecture Decision Record                                    |
| RBAC         | Role-Based Access Control                                       |
| SDK          | Software Development Kit                                        |
| CLI          | Command Line Interface                                          |
| API          | Application Programming Interface                               |
| MCP          | Model Context Protocol                                          |

---

# Future Extensions

Future versions of this document MAY:

- append new terms after their introduction in DEVOS-SPEC-006,
- extend the lifecycle, state, and relationship indexes when canonical documents grow,
- add further abbreviation entries used by new specifications.

Entries are always added in sorted order and never redefined.

---

# References

- DEVOS-SPEC-006 – Terminology
- DEVOS-SPEC-011 – Domain Model
- DEVOS-SPEC-012 – Domain Relationships
- DEVOS-SPEC-013 – Object Lifecycle
- DEVOS-SPEC-014 – State Model
- DEVOS-SPEC-015 – Object Ownership

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
