# Changelog

All notable changes to the DevOS project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com), and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- Repository charter documents: Project Manifesto, Specification Rules, Governance, Contributing guide, Code of Conduct, and Roadmap.
- Specification v0.1 draft documents for the Overview section (000–010): governance, executive summary, vision, problem statement, design philosophy, guiding principles, terminology, scope, non goals, success metrics, glossary.
- Specification v0.1 draft documents for the Domain Model section (011–015): domain model, domain relationships, object lifecycle, state model, object ownership.
- Specification v0.1 draft documents for the Foundation section (020–029): workspace, project, profile, environment, provider, connection, plugin, template, secret, and workspace manifest.
- Specification v0.1 draft documents for the Core Architecture section (030–039): system architecture, workspace/plugin/provider/connection/template/security engines, event system, memory engine, AI router.
- Specification v0.1 draft documents for the Platform section (040–049): CLI, dashboard, project import and detection, workspace lifecycle, configuration, health, settings, update system, logging.
- Specification v0.1 draft documents for the SDK section (050–059): SDK overview, plugin/provider/template/workspace SDKs, API specification, hooks API, events API, CLI API, versioning policy.
- Forward-looking specification drafts for the Enterprise section (060–069) and Future section (070–079), excluded from v0.1 scope pending an approved ADR.
- JSON schemas for core objects in `schemas/`, including workspace, project, profile, environment, provider, connection, plugin, template, secret, settings, and manifest schemas.
- RFC process with directory lifecycle (`proposed`, `accepted`, `implemented`, `rejected`, `archived`) and an RFC template.
- ADR process with directory lifecycle (`proposed`, `accepted`, `superseded`, `deprecated`) and an ADR template.
- Document scaffolding under `templates/` for specifications, RFCs, ADRs, decisions, and meeting notes.
- Diagram scaffolding organized by type under `diagrams/`.
- Example workspace directories organized by category under `examples/`.

## [0.1.0]

### Added

- Initial public skeleton of the repository.
- Frozen top-level directory structure: `adr/`, `assets/`, `diagrams/`, `examples/`, `rfcs/`, `schemas/`, `specification/`, `templates/`, `tools/`.
- Project Manifesto stating the vision, beliefs, and commitments of DevOS.
- Specification Rules defining the mandatory rules for all contributions.

---

This changelog follows the Keep a Changelog format.
