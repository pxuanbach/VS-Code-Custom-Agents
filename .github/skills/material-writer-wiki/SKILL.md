---
name: material-writer-wiki
description: |
  LLM Wiki skill for Material Writer - organizes artifacts (PRD, Architecture, Plans, Reports) 
  into a team knowledge base with 3-layer structure (sources, wiki, schema). 
  
  USE WHEN:
  - User says "save doc to wiki", "organize artifacts into wiki", "add to wiki"
  - User asks "search doc related to X", "what do we have about Y", "query wiki"
  - Before writing a new doc, need to check for existing related docs (avoid duplicates)
  - material-writer.agent.md needs to register, search, or cross-link documents
  - User wants to browse, search, or maintain a project knowledge base
  
  Triggers: "write doc", "create PRD", "draft document", "save doc to wiki", 
  "organize artifacts", "query wiki", "add to wiki", "search wiki"
  
  This skill provides CLI tools (wiki init, wiki add, wiki list, wiki search, wiki related, wiki reindex)
  and conventions for maintaining a team wiki with YAML frontmatter, JSON indexes, and wikilinks.
version: 1.0
created_at: 2026-07-13
---

# Material Writer Wiki Skill

Wiki is a team knowledge base containing artifacts of multi-agent workflow + research notes + decisions + lessons learned.

---

## Wiki Directory Layout

```
wiki/
├── SCHEMA.md
├── index.json
├── log.md
├── features/
│   └── YYYY-MM-NNN-<slug>/
│       ├── index.json
│       ├── prd.md
│       ├── arch.md
│       ├── plan.md
│       ├── report.md
│       └── notes.md
└── topics/
    ├── index.json
    └── <topic>.md
```

---

## File Naming Convention

- Documents: `YYYY-MM-DD-<type>-[short-name].md` (e.g., `2026-07-13-prd-auth.md`)
- Features: `YYYY-MM-NNN-<slug>` (date-prefix + sequential 3-digit + slug)
- Topics: lowercase with hyphens, e.g., `authentication.md`, `api-design.md`

---

## YAML Frontmatter (Required for Every Document)

```yaml
---
id: 2026-07-001-auth/prd
type: prd
title: Authentication PRD
summary: Implement OAuth2 + JWT based authentication system with SSO support.
tags: [auth, security, sso]
status: approved
created_at: 2026-07-13
updated_at: 2026-07-13
related:
  - features/2026-07-001-auth/plan.md
  - topics/authentication.md
---
```

---

## Document Types

| Type | Description | Required Fields |
|------|-------------|-----------------|
| `prd` | Product Requirements Document | title, summary, tags, status |
| `arch` | Architecture Document | title, summary, tags, status |
| `plan` | Implementation Plan | title, summary, tags, status |
| `report` | Validation Report | title, summary, tags, status |
| `notes` | Research notes, decisions, lessons | title, tags |
| `topic` | Cross-feature concept page | title, tags |

---

## Cross-reference Conventions

**Wikilinks** (Obsidian graph view):
```
[[../2026-07-002-payment/payment-prd]]
[[../../topics/authentication]]
```

**Markdown links** (compatibility):
```
[payment-prd](../2026-07-002-payment/payment-prd.md)
[authentication](../../topics/authentication.md)
```

---

## CLI Commands

All commands are run via `python scripts/wiki.py <command>` from the project root.

### `wiki init`
Initialize wiki structure in current directory. Creates:
- `wiki/SCHEMA.md` (from references/)
- `wiki/index.json` (empty master index)
- `wiki/log.md` (empty log)
- `wiki/features/` and `wiki/topics/` directories

### `wiki add <file>`
Auto-detect doc type from path, extract metadata, update feature-local + master index.
- Detects doc type from filename: `*-prd.md` → `prd`, `*-plan.md` → `plan`, etc.
- If document has no YAML frontmatter → generates minimal frontmatter from filename + first heading
- Summary: first non-empty line after frontmatter, stripped of markdown, ≤200 chars
- Appends entry to `wiki/log.md`

### `wiki list [--type X] [--tag Y] [--status Z] [--feature NNN]`
Query master index with filters. Returns matching documents with paths and summaries.

### `wiki search <query>`
Substring match on title + summary + tags. Returns ranked results.

### `wiki related <path>`
Traverse `related[]` array in document's frontmatter, return related docs.

### `wiki reindex`
Rebuild master index from all feature-local indexes. Idempotent - safe to run after any changes.

---

## Material Writer Workflow

### Ingest Workflow (when adding new doc)

```
1. Receive doc type + content + output path from calling agent
2. Determine feature folder:
   - Parse YYYY-MM-NNN from output path
   - If feature folder doesn't exist → create new + generate notes.md skeleton
3. Write document with standard YAML frontmatter (templates in SCHEMA.md)
4. Run: wiki add <file> to update indexes
5. Append to log.md: ## [YYYY-MM-DD] ingest | <title>
6. Return path + index entry to calling agent
```

### Query Workflow (before writing new doc)

```
1. Run: wiki search <topic> to find existing related docs
2. If related docs found → read summaries, check for duplicates
3. List related docs in new doc's frontmatter (related field)
4. After writing → wiki add <file> to integrate into index
```

---

## Log Format

```
## [2026-07-13] ingest | Authentication PRD
## [2026-07-13] ingest | Authentication Plan
## [2026-07-14] query | authentication sso
## [2026-07-14] ingest | Payment PRD
```

Parseable via: `grep "^## \[" wiki/log.md | tail -5`

---

## Tag Taxonomy Guidelines

- **auth**: authentication, authorization, sessions, tokens
- **security**: security best practices, vulnerability handling
- **api**: API design, endpoints, versioning
- **frontend**: UI components, UX patterns
- **backend**: server logic, database, services
- **infra**: deployment, infrastructure, DevOps
- **docs**: documentation, wikis
- **testing**: test strategies, coverage

---

## Feature Folder Creation

When creating a new feature folder:

1. Parse date and sequence number from `YYYY-MM-NNN-<slug>`
2. Create folder at `wiki/features/YYYY-MM-NNN-<slug>/`
3. Create local `index.json` with feature metadata
4. Create skeleton `notes.md` with frontmatter

---

## Scheduled Maintenance

Run periodically (or when issues suspected):
- `wiki reindex` - rebuild master index from feature indexes
- Check for orphan docs (docs in folders but not in any index)
- Verify all `related[]` links point to existing files

---

## See Also

- `references/SCHEMA.md` - Full templates for each document type
- `references/json-schema.md` - Detailed JSON schema specifications
- `references/examples.md` - Complete example feature folders
