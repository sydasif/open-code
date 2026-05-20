---
name: adr-template
description: Create and manage Architectural Decision Records (ADRs) using MADR format. Use when making significant architectural decisions, evaluating technology choices, or documenting design rationale.
---

# ADR Template Skill

This skill guides the creation and management of Architectural Decision Records (ADRs) using the MADR (Markdown Architectural Decision Records) format.

## When to Create an ADR

Create an ADR when a decision:
- Affects system structure or component boundaries
- Involves technology selection (language, framework, database, etc.)
- Has long-term maintenance implications
- Requires significant trade-offs between competing concerns
- Could be difficult to reverse later
- Involves multiple teams or significant cost

## ADR Format (MADR 4.0)

```markdown
---
status: {proposed | accepted | rejected | deprecated | superseded}
date: YYYY-MM-DD
decision-makers: Name1, Name2
consulted: Expert1, Expert2
informed: Team1, Team2
---

# {Short title, representative of solved problem and found solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story.}

## Decision Drivers

* {decision driver 1, e.g., a force, facing concern, …}
* {decision driver 2, e.g., a force, facing concern, …}

## Considered Options

* {title of option 1}
* {title of option 2}
* {title of option 3}

## Decision Outcome

Chosen option: "{title of option}", because {justification. e.g., only option, which meets k.o. criterion | resolves force | comes out best}.

### Consequences

* Good, because {positive consequence}
* Bad, because {negative consequence}

### Confirmation

{How compliance will be confirmed: code review, ArchUnit tests, design review, etc.}

## Pros and Cons of the Options

### {Option 1 Title}

* Good, because {argument a}
* Good, because {argument b}
* Neutral, because {argument c}
* Bad, because {argument d}

### {Option 2 Title}

{...}

## More Information

{Additional evidence, team agreement, links to related decisions}
```

## ADR Location

Store ADRs in one of:
- `docs/decisions/` — Recommended for documentation-focused projects
- `adr/` — Alternative common name
- `docs/architecture/adrs/` — For larger projects

## Naming Convention

Use one of:
- `NNNN-title-with-dashes.md` (e.g., `0001-use-postgresql.md`)
- `YYYY-MM-DD-title.md` (e.g., `2026-05-20-use-postgresql.md`)

## ADR Workflow

### 1. Proposed
When the decision is being discussed but not yet decided.

### 2. Accepted
When the decision is made and work begins.

### 3. Rejected
When the decision is discussed but rejected. The ADR is kept for history to document why a path was not taken.

### 4. Deprecated
When the decision is no longer relevant but kept for history.

### 5. Superseded
When a new ADR replaces this one. Reference the new ADR.

## Example ADRs

### Example: Database Selection

```markdown
---
status: accepted
date: 2026-05-20
decision-makers: Architecture Team
---

# Use PostgreSQL as Primary Database

## Context and Problem Statement

Our application needs a primary database for storing user data and application state. We currently have no database, and need to select one that can handle our expected load of 10,000 concurrent users with ACID compliance.

## Decision Drivers

* ACID compliance required for financial transactions
* Need for complex queries and joins
* Team has PostgreSQL experience
* Budget constraints — need open source
* Expected scale: 10,000 concurrent users

## Considered Options

* PostgreSQL — Open source relational database
* MongoDB — Document database
* MySQL — Open source relational database

## Decision Outcome

Chosen option: "PostgreSQL", because it meets all our requirements: ACID compliance, team expertise, open source, and proven scalability to our expected load.

### Consequences

* Good, because team already knows PostgreSQL
* Good, because strong ACID guarantees
* Bad, because horizontal scaling requires more effort than MongoDB

### Confirmation

Performance test with 10,000 concurrent users passes with <200ms response time.

## Pros and Cons of the Options

### PostgreSQL

* Good, because ACID compliant out of the box
* Good, because team has experience
* Good, because excellent JSON support for semi-structured data
* Neutral, because more verbose than MongoDB
* Bad, because horizontal scaling requires sharding

### MongoDB

* Good, because easy horizontal scaling
* Good, because flexible schema
* Bad, because less mature than PostgreSQL for complex queries
* Bad, because team has less experience

### MySQL

* Good, because widely used
* Bad, because less feature-rich than PostgreSQL
* Bad, because team has less experience

## More Information

* PostgreSQL documentation: https://www.postgresql.org/docs/
```

## ADR Tools

### CLI Tools
- `adr` — Command-line tool for managing ADRs
- `adr-tools` — Shell scripts for ADR management

### VS Code Extension
- "ADR Manager" — Manage ADRs from VS Code

## References

- [ADR GitHub Organization](https://adr.github.io/)
- [MADR Project](https://github.com/adr/madr)
- [Michael Nygard's Original ADR Template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Y-Statements](https://medium.com/@docsoc/y-statements-10eb07b5a177)
