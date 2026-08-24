# Diagram Guidelines

This directory stores diagram sources for the DevOS specification.

Diagrams are part of the normative documentation set, not decoration.

They follow the same rules as every other contribution in [SPECIFICATION_RULES.md](../SPECIFICATION_RULES.md).

---

## Purpose

Rule 16 requires major specifications to include diagrams.

A diagram makes structure, lifecycle, and interaction visible at a glance, and it keeps prose honest: if the picture and the text disagree, one of them is wrong.

Every major specification should be understandable from its diagrams plus its tables.

---

## Formats

Mermaid is preferred.

Mermaid code blocks are embedded directly inside specification markdown so they render in place and evolve with the text.

PlantUML, C4 model sources, and UML remain acceptable when their expressiveness is needed.

Such non-Mermaid sources are committed here as files, never only as exported images.

---

## Directory Taxonomy

| Folder          | What belongs here                                            | Example                       |
| --------------- | ------------------------------------------------------------ | ----------------------------- |
| `activity/`     | Step-by-step activities with decisions and branches           | `044-workspace-activation.mmd` |
| `architecture/` | High-level system and layer views                             | `030-system-layers.mmd`        |
| `c4/`           | C4 context, container, and component models                   | `030-c4-context.mmd`           |
| `class/`        | Structural class diagrams of domain objects                   | `011-domain-classes.mmd`       |
| `component/`    | Engines and services shown with their interfaces              | `036-security-engine-parts.mmd`|
| `deployment/`   | Nodes, environments, and cloud-agnostic topology              | `020-workspace-deployment.mmd` |
| `domain/`       | Ownership and relationship maps across the aggregate          | `015-ownership-map.mmd`        |
| `er/`           | Entity-relationship views of schemas                          | `029-manifest-entities.mmd`    |
| `sequence/`     | Interactions between actors, engines, and services            | `034-connection-testing.mmd`   |
| `state/`        | Lifecycle and state machines                                  | `013-object-lifecycle.mmd`     |
| `ui/`           | Conceptual screen and navigation flows for CLI and Dashboard  | `041-dashboard-navigation.mmd` |
| `workflow/`     | Workflow and Task orchestration graphs                        | `044-task-execution.mmd`       |

---

## Naming Convention

Diagram source files are named `NNN-topic.mmd`.

- `NNN` matches the DEVOS-SPEC number the diagram illustrates, for example `020-workspace-composition.mmd` illustrates DEVOS-SPEC-020.
- `topic` is lowercase and hyphenated.
- One topic per file.
- A diagram shared by several documents takes the lowest relevant specification number.

---

## Embedding Rule

Major specifications embed their diagrams inline as Mermaid code blocks.

When a diagram cannot be expressed in Mermaid — PlantUML, C4, UML — the specification references the rendered form and the source file is dropped here, linked from the specification.

Never duplicate the same diagram in two specifications; reference the owning document instead (Rule 10).

---

## Style Rules

- Use object names exactly as defined in DEVOS-SPEC-006 Terminology: Workspace, Project, Profile, Environment, Connection, Provider, Plugin, Template, Secret, Workflow, Task, Documentation.
- Label everything in English.
- Keep labels short and consistent across all diagrams.
- Do not commit screenshots or images of text-based diagrams; commit the source so diagrams stay diffable and editable.

---

## Previewing Mermaid

GitHub renders Mermaid code blocks in markdown automatically.

In editors such as VS Code, any Mermaid preview extension can render `.mmd` files and code blocks side by side.

Command-line renderers work equally well for local checks.

Verify that a diagram renders correctly before opening a pull request.
