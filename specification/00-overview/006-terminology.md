# 006 – DevOS Terminology

**Document ID:** DEVOS-SPEC-006

**Version:** 0.1

**Status:** Draft

**Category:** Foundation

**Depends On:** 005 – Guiding Principles

**Required By:** All Specifications

---

# Purpose

This document defines the official terminology used throughout the DevOS Specification.

The purpose of this document is to ensure that every contributor, implementation, plugin, and integration uses the same language.

Each term defined here has exactly one meaning within the DevOS ecosystem.

If a future specification introduces a new concept, it must first be defined here.

---

# Terminology Rules

Every defined term must satisfy the following rules:

- Have one canonical definition.
- Have one primary purpose.
- Have one lifecycle.
- Have one owner.
- Be implementation independent.
- Be reusable across implementations.

Terms must never depend on:

- Programming languages
- Frameworks
- Operating systems
- Cloud providers
- AI providers
- Editors

---

# Core Domain Model

At the highest level DevOS is composed of the following concepts.

Workspace

↓

Project

↓

Profiles

↓

Connections

↓

Providers

↓

Resources

Every subsystem in DevOS is built around these concepts.

---

# Core Terms

---

## Workspace

### Definition

A Workspace is the primary organizational unit of DevOS.

It represents everything required to develop, test, deploy, document, and maintain one software project.

A Workspace is portable.

A Workspace is reproducible.

A Workspace is the central object of the DevOS Platform.

### Responsibilities

A Workspace owns:

- Project metadata
- Connections
- Profiles
- Providers
- Secrets
- Templates
- Plugins
- Automation
- Documentation
- AI configuration

### Lifetime

Created

↓

Configured

↓

Active

↓

Archived

↓

Deleted

### Examples

CloudSentinel

Assemble

Personal Website

---

## Project

### Definition

A Project is the software system being developed.

Projects exist independently of DevOS.

DevOS manages Workspaces.

Workspaces manage Projects.

### Examples

CloudSentinel AI

Inventory API

Research Platform

---

## Workspace Manifest

### Definition

The Workspace Manifest is the canonical configuration describing a Workspace.

It contains every configuration required to recreate the Workspace.

Examples include:

- Project
- Providers
- Connections
- Plugins
- Templates

The Workspace Manifest is portable.

---

## Workspace Package

### Definition

A Workspace Package is a distributable Workspace.

It contains all metadata required to recreate a development environment.

Workspace Packages are intended for:

- Team onboarding
- Open-source projects
- Internal company projects

---

## Profile

### Definition

A Profile represents one configurable environment inside a Workspace.

Examples include:

Development

Testing

Staging

Production

Research

Personal

Profiles allow one Workspace to support multiple environments.

---

## Environment

### Definition

An Environment represents the runtime configuration used by a Profile.

Examples include:

Environment variables

Feature flags

Runtime settings

Secrets

Configuration values

An Environment belongs to a Profile.

---

## Connection

### Definition

A Connection defines how DevOS communicates with an external system.

Connections are reusable.

Connections never contain business logic.

Examples

PostgreSQL

Redis

MongoDB

GitHub

AWS

Azure

GCP

---

## Provider

### Definition

A Provider is an implementation of a service category.

Providers are interchangeable.

Examples

Cloud

AWS

Azure

GCP

AI

OpenAI

Anthropic

Google

Ollama

Editor

VS Code

Cursor

Codex

Claude Code

---

## Resource

### Definition

A Resource represents something managed through a Provider.

Examples

Database

Bucket

Repository

Cluster

Container

Secret

---

## Plugin

### Definition

A Plugin extends DevOS functionality without modifying the core platform.

Plugins are independently versioned.

Plugins communicate through public APIs.

---

## Extension

### Definition

An Extension enhances an existing feature.

Unlike Plugins, Extensions cannot introduce new platform capabilities.

---

## Template

### Definition

A Template defines reusable project structures.

Templates may describe:

Backend services

Frontend applications

Infrastructure

Research papers

Documentation

Templates are implementation independent.

---

## Engine

### Definition

An Engine is a core subsystem responsible for managing one domain.

Examples

Workspace Engine

Plugin Engine

Connection Engine

Dashboard Engine

---

## Module

### Definition

A Module is a logical implementation unit inside an Engine.

Modules are internal implementation concepts.

Modules are not exposed to users.

---

## Service

### Definition

A Service performs one well-defined responsibility inside DevOS.

Examples

Validation Service

Logging Service

Discovery Service

Update Service

---

## Agent

### Definition

An Agent performs autonomous work on behalf of the user.

Agents may execute:

Automation

Analysis

Generation

Monitoring

Future AI capabilities should be implemented as Agents.

---

## Task

### Definition

A Task represents one executable unit of work.

Tasks are:

Atomic

Repeatable

Observable

---

## Workflow

### Definition

A Workflow is an ordered collection of Tasks.

Workflows may be:

Manual

Automatic

Scheduled

Event-driven

---

## Event

### Definition

An Event represents something that occurred inside DevOS.

Examples

Workspace Created

Plugin Installed

Connection Updated

Workspace Imported

Events may trigger Workflows.

---

## Hook

### Definition

A Hook is a user-defined extension point.

Hooks execute custom logic when specific Events occur.

---

## Secret

### Definition

A Secret is confidential information required by a Workspace.

Examples

API Keys

Passwords

Access Tokens

Certificates

Private Keys

Secrets must never appear in logs.

---

## Registry

### Definition

A Registry is a collection of reusable objects.

Examples

Workspace Registry

Template Registry

Plugin Registry

Connection Registry

---

## Dashboard

### Definition

The Dashboard is the graphical interface for interacting with DevOS.

The Dashboard is one implementation.

It is not the platform itself.

---

## CLI

### Definition

The Command Line Interface provides terminal access to DevOS.

The CLI and Dashboard expose the same capabilities.

Neither owns platform logic.

---

## SDK

### Definition

The Software Development Kit enables third parties to extend DevOS.

The SDK exposes stable public interfaces.

---

## API

### Definition

An API defines the contract between DevOS components.

APIs are versioned.

Breaking API changes require a major version.

---

## Schema

### Definition

A Schema defines the structure of DevOS configuration files.

Schemas are implementation independent.

Schemas are considered canonical.

---

## Specification

### Definition

The Specification defines how DevOS should behave.

It is implementation independent.

The Specification always takes precedence over code.

---

## Reference Implementation

### Definition

The Reference Implementation is the official DevOS implementation.

Its purpose is to demonstrate the Specification.

It does not define the Specification.

---

# Relationships

Workspace

├── Project

├── Profiles

│ └── Environment

├── Connections

├── Providers

├── Plugins

├── Templates

├── Secrets

├── Workflows

├── Tasks

└── Documentation

---

# Reserved Terms

The following words have reserved meanings inside DevOS.

Workspace

Project

Provider

Connection

Profile

Plugin

Engine

Registry

Template

Manifest

Package

Agent

Workflow

Task

Schema

Specification

These terms must not be redefined elsewhere.

---

# Naming Guidelines

Terminology should satisfy the following rules:

Use singular nouns.

Use descriptive names.

Avoid abbreviations.

Avoid vendor-specific terminology.

Avoid implementation-specific names.

Prefer conceptual names over technical names.

---

# Future Extensions

Future versions of this document may define additional concepts including:

Workspace Federation

Workspace Marketplace

Organization

Team

Policy

Cloud Sync

AI Agent

Knowledge Graph

Workspace Analytics

Remote Execution

These concepts are intentionally excluded from Version 0.1.

---

# References

005 – Guiding Principles

011 – Workspace Specification

021 – System Architecture

---

# Revision History

| Version | Date | Author             | Notes         |
| ------- | ---- | ------------------ | ------------- |
| 0.1     | TBD  | DevOS Contributors | Initial Draft |
