# Material Writer Wiki Schema

This file defines the conventions, templates, and workflows for the Material Writer Wiki.

---

## Document Templates

### PRD Template (Product Requirements Document)

```markdown
---
id: YYYY-MM-NNN-slug/prd
type: prd
title: [Feature Name] PRD
summary: One-paragraph description of the feature and its goals.
tags: [tag1, tag2]
status: draft|review|approved|deprecated
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related:
  - features/YYYY-MM-NNN-slug/plan.md
  - topics/topic-name.md
---

# [Feature Name] - Product Requirements Document

## Overview
What problem does this solve? Why is it important?

## Goals
- Primary goal 1
- Primary goal 2

## Non-Goals
What this feature is NOT trying to solve.

## Success Metrics
How do we measure success?

## User Stories
1. As a [user type], I want to [action] so that [outcome].
2. As a [user type], I want to [action] so that [outcome].

## Requirements

### Functional Requirements
- REQ-001: [Description]
- REQ-002: [Description]

### Non-Functional Requirements
- Performance: [Criteria]
- Security: [Criteria]
- Scalability: [Criteria]

## Dependencies
- [External system/API]
- [Team/ownership]

## Open Questions
- [Question 1]
- [Question 2]

## Appendix
Additional context, research, references.
```

---

### Architecture Document Template

```markdown
---
id: YYYY-MM-NNN-slug/arch
type: arch
title: [Feature Name] Architecture
summary: High-level architecture overview and design decisions.
tags: [architecture, backend, api]
status: draft|review|approved|deprecated
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related:
  - features/YYYY-MM-NNN-slug/prd.md
  - features/YYYY-MM-NNN-slug/plan.md
---

# [Feature Name] - Architecture Document

## Context
Problem statement and constraints.

## Architecture Overview
High-level diagram description.

## Component Design

### Component A
Purpose, responsibilities, interface.

### Component B
Purpose, responsibilities, interface.

## Data Model
Database schema, entity relationships.

## API Design
Endpoint specifications if applicable.

## Security Considerations
Authentication, authorization, data protection.

## Deployment Model
How this component is deployed and scaled.

## Alternatives Considered
Other approaches that were evaluated and why they were rejected.
```

---

### Plan Template (Implementation Plan)

```markdown
---
id: YYYY-MM-NNN-slug/plan
type: plan
title: [Feature Name] Implementation Plan
summary: Phased implementation approach with milestones.
tags: [planning, implementation]
status: draft|review|approved|deprecated
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related:
  - features/YYYY-MM-NNN-slug/prd.md
  - features/YYYY-MM-NNN-slug/arch.md
---

# [Feature Name] - Implementation Plan

## Overview
Brief description of the implementation approach.

## Phases

### Phase 1: [Name] (Target: Week X)
**Goals:**
- Goal 1
- Goal 2

**Deliverables:**
- [ ] Deliverable 1
- [ ] Deliverable 2

**Tasks:**
- [ ] Task 1
- [ ] Task 2

### Phase 2: [Name] (Target: Week Y)
...

## Resource Requirements
- Team size: X FTEs
- External dependencies: [List]

## Risk Mitigation
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | Low/Med/High | Low/Med/High | [Strategy] |

## Definition of Done
- [ ] Criterion 1
- [ ] Criterion 2
```

---

### Report Template (Validation Report)

```markdown
---
id: YYYY-MM-NNN-slug/report
type: report
title: [Feature Name] Validation Report
summary: Test results, validation evidence, and acceptance summary.
tags: [validation, testing, qa]
status: draft|review|approved|deprecated
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related:
  - features/YYYY-MM-NNN-slug/prd.md
  - features/YYYY-MM-NNN-slug/plan.md
---

# [Feature Name] - Validation Report

## Executive Summary
One-paragraph summary of validation results and recommendation.

## Test Results

### Unit Tests
| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| [TC-001] | [Result] | [Result] | Pass/Fail |

### Integration Tests
| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| [TC-101] | [Result] | [Result] | Pass/Fail |

### Performance Tests
- Throughput: [X] requests/second
- Latency P99: [Y]ms
- Error rate: [Z]%

## Defects
| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| [DEF-001] | Critical/Major/Minor | [Description] | Open/Resolved |

## Acceptance Criteria Checklist
- [ ] Criterion 1 verified
- [ ] Criterion 2 verified

## Sign-off
| Role | Name | Date | Signature |
|------|------|------|------------|
| Tech Lead | | | |
| Product Owner | | | |
| QA | | | |
```

---

### Notes Template (Research Notes / Decisions / Lessons)

```markdown
---
id: YYYY-MM-NNN-slug/notes
type: notes
title: [Feature Name] - Research Notes
summary: Research findings, design decisions, and lessons learned.
tags: [research, decisions]
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related:
  - features/YYYY-MM-NNN-slug/prd.md
---

# [Feature Name] - Research Notes

## Research Summary
Key findings from research phase.

## Decisions

### DEC-001: [Decision Title]
**Date:** YYYY-MM-DD
**Context:** [Why this decision was needed]
**Decision:** [What was decided]
**Alternatives Considered:**
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]
**Consequences:**
- [Positive consequence]
- [Negative consequence]

## Lessons Learned

### What Went Well
- [Lesson 1]
- [Lesson 2]

### What Could Be Improved
- [Lesson 1]
- [Lesson 2]

### Action Items
- [ ] Action from lesson 1
- [ ] Action from lesson 2

## References
- [Link to PRD]
- [Link to external research]
- [Meeting notes]
```

---

### Topic Template (Cross-feature Concept)

```markdown
---
id: topics/[topic-name]
type: topic
title: [Concept Title]
summary: Overview of this cross-cutting concept.
tags: [concept, domain]
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
related:
  - features/YYYY-MM-NNN-slug/prd.md
  - features/YYYY-MM-PPP-slug/arch.md
---

# [Concept Title]

## Overview
What is this concept and why does it matter?

## Key Principles
1. Principle 1
2. Principle 2

## Usage in Features

### Authentication
[[../2026-07-001-auth/prd]]

### Payment
[[../2026-07-002-payment/payment-prd]]

## Best Practices
- Do: [Good practice]
- Don't: [Bad practice]

## Related Topics
- [Topic A](topics/topic-a.md)
- [Topic B](topics/topic-b.md)
```

---

## Ingest Workflow

When adding a new document to the wiki:

1. **Prepare the document**
   - Ensure filename follows convention: `YYYY-MM-DD-<type>-[short-name].md`
   - Add YAML frontmatter (use template above)
   - Include `related[]` links to any connected documents

2. **Determine feature folder**
   - Parse `YYYY-MM-NNN` from filename to get feature ID
   - Place in `wiki/features/<feature-id>/`

3. **Run wiki add**
   ```bash
   python .github/skills/material-writer-wiki/scripts/wiki.py add <file>
   ```
   This updates:
   - Feature-local `features/<feature-id>/index.json`
   - Master `wiki/index.json`
   - Appends to `wiki/log.md`

4. **Verify**
   - Check `wiki/index.json` contains the new entry
   - Run `wiki list` to confirm visibility

---

## Query Workflow

When searching for existing documentation:

1. **Search by topic**
   ```bash
   python .github/skills/material-writer-wiki/scripts/wiki.py search "<keyword>"
   ```

2. **List by type/tag/status**
   ```bash
   python .github/skills/material-writer-wiki/scripts/wiki.py list --type prd --tag auth
   ```

3. **Find related documents**
   ```bash
   python .github/skills/material-writer-wiki/scripts/wiki.py related <file>
   ```

4. **Check recent activity**
   ```bash
   grep "^## \[" wiki/log.md | tail -10
   ```

---

## Lint Workflow (Periodic Check)

Run periodically to maintain wiki health:

1. **Rebuild master index**
   ```bash
   python .github/skills/material-writer-wiki/scripts/wiki.py reindex
   ```

2. **Check for orphan documents**
   - Documents in feature folders but not in `index.json`

3. **Verify related links**
   - All paths in `related[]` should point to existing files

4. **Check for missing frontmatter**
   - All documents should have valid YAML frontmatter

---

## Tag Taxonomy

Use consistent tags across all documents:

| Tag | Use For |
|-----|---------|
| `auth` | Authentication, authorization, sessions, tokens |
| `security` | Security practices, vulnerability handling |
| `api` | API design, endpoints, versioning |
| `frontend` | UI components, UX patterns |
| `backend` | Server logic, database, services |
| `infra` | Deployment, infrastructure, DevOps |
| `docs` | Documentation, wikis |
| `testing` | Test strategies, coverage |
| `planning` | Plans, roadmaps, estimates |
| `research` | Research, discovery, exploration |
| `decisions` | ADRs, design decisions |
| `validation` | QA, testing, verification |

---

## Cross-Reference Patterns

### Wikilinks (Obsidian Graph Compatible)
```
[[../2026-07-002-payment/payment-prd]]
[[../../topics/authentication]]
```

### Markdown Links (Universal)
```
[payment-prd](../2026-07-002-payment/payment-prd.md)
[authentication](../../topics/authentication.md)
```

### When to Use Which
- Use **wikilinks** when working in Obsidian for graph view visualization
- Use **markdown links** for compatibility with other tools
- Always include both if the doc will be viewed in multiple contexts

---

## Status Values

| Status | Meaning |
|--------|---------|
| `draft` | Initial version, not reviewed |
| `review` | Under review by team |
| `approved` | Reviewed and approved |
| `deprecated` | Superseded by newer version |

---

## Feature ID Format

Format: `YYYY-MM-NNN-<slug>`

- `YYYY-MM`: Year and month of creation
- `NNN`: Sequential 3-digit number (001, 002, 003...)
- `slug`: Short kebab-case identifier (e.g., `auth`, `payment-gateway`)

Example: `2026-07-001-auth`
