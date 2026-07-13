# JSON Schema Specification

This document describes the JSON schemas used by the Material Writer Wiki.

---

## Master Index Schema (`wiki/index.json`)

The master index is the entry point for all wiki queries.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "generated_at", "features", "topics", "documents"],
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+$",
      "description": "Schema version, currently 1.0"
    },
    "generated_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when index was last generated"
    },
    "features": {
      "type": "array",
      "description": "List of all features in the wiki",
      "items": {
        "$ref": "#/definitions/featureSummary"
      }
    },
    "topics": {
      "type": "array",
      "description": "List of all topic pages",
      "items": {
        "$ref": "#/definitions/topicSummary"
      }
    },
    "documents": {
      "type": "array",
      "description": "Flat list of all documents",
      "items": {
        "$ref": "#/definitions/documentEntry"
      }
    }
  },
  "definitions": {
    "featureSummary": {
      "type": "object",
      "required": ["id", "title", "path", "created_at", "updated_at", "documents"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^\\d{4}-\\d{2}-\\d{3}-[\\w-]+$",
          "description": "Feature ID, e.g. 2026-07-001-auth"
        },
        "title": {
          "type": "string",
          "description": "Human-readable feature title"
        },
        "path": {
          "type": "string",
          "description": "Relative path from wiki root, e.g. features/2026-07-001-auth"
        },
        "created_at": {
          "type": "string",
          "format": "date",
          "description": "Creation date YYYY-MM-DD"
        },
        "updated_at": {
          "type": "string",
          "format": "date",
          "description": "Last update date YYYY-MM-DD"
        },
        "documents": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of document filenames in this feature"
        }
      }
    },
    "topicSummary": {
      "type": "object",
      "required": ["id", "title", "path", "created_at", "updated_at", "tags"],
      "properties": {
        "id": {
          "type": "string",
          "description": "Topic identifier, e.g. authentication"
        },
        "title": {
          "type": "string",
          "description": "Human-readable topic title"
        },
        "path": {
          "type": "string",
          "description": "Relative path from wiki root, e.g. topics/authentication.md"
        },
        "created_at": {
          "type": "string",
          "format": "date"
        },
        "updated_at": {
          "type": "string",
          "format": "date"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "related": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Paths to related features or topics"
        }
      }
    },
    "documentEntry": {
      "type": "object",
      "required": ["id", "path", "type", "title", "summary", "tags", "status", "created_at", "updated_at", "related"],
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique document ID in format feature-id/doc-type, e.g. 2026-07-001-auth/prd"
        },
        "path": {
          "type": "string",
          "description": "Relative path from wiki root, e.g. features/2026-07-001-auth/prd.md"
        },
        "type": {
          "type": "string",
          "enum": ["prd", "arch", "plan", "report", "notes", "topic"],
          "description": "Document type"
        },
        "title": {
          "type": "string",
          "description": "Document title"
        },
        "summary": {
          "type": "string",
          "maxLength": 500,
          "description": "Brief summary (recommended ≤200 chars)"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Tags for categorization"
        },
        "status": {
          "type": "string",
          "enum": ["draft", "review", "approved", "deprecated"],
          "description": "Document lifecycle status"
        },
        "created_at": {
          "type": "string",
          "format": "date"
        },
        "updated_at": {
          "type": "string",
          "format": "date"
        },
        "related": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Paths to related documents"
        }
      }
    }
  }
}
```

---

## Feature Index Schema (`features/<feature-id>/index.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["feature", "documents"],
  "properties": {
    "feature": {
      "type": "object",
      "required": ["id", "title", "created_at", "updated_at"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^\\d{4}-\\d{2}-\\d{3}-[\\w-]+$"
        },
        "title": {
          "type": "string"
        },
        "created_at": {
          "type": "string",
          "format": "date"
        },
        "updated_at": {
          "type": "string",
          "format": "date"
        }
      }
    },
    "documents": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/documentEntry"
      }
    }
  },
  "definitions": {
    "documentEntry": {
      "type": "object",
      "required": ["id", "path", "type", "title", "summary", "status", "created_at", "updated_at", "related"],
      "properties": {
        "id": {
          "type": "string"
        },
        "path": {
          "type": "string"
        },
        "type": {
          "type": "string",
          "enum": ["prd", "arch", "plan", "report", "notes", "topic"]
        },
        "title": {
          "type": "string"
        },
        "summary": {
          "type": "string"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "status": {
          "type": "string",
          "enum": ["draft", "review", "approved", "deprecated"]
        },
        "created_at": {
          "type": "string",
          "format": "date"
        },
        "updated_at": {
          "type": "string",
          "format": "date"
        },
        "related": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

---

## Example: Complete Master Index

```json
{
  "version": "1.0",
  "generated_at": "2026-07-13T10:00:00Z",
  "features": [
    {
      "id": "2026-07-001-auth",
      "title": "Authentication System",
      "path": "features/2026-07-001-auth",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "documents": ["prd.md", "arch.md", "plan.md", "report.md", "notes.md"]
    },
    {
      "id": "2026-07-002-payment",
      "title": "Payment Gateway Integration",
      "path": "features/2026-07-002-payment",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "documents": ["prd.md", "plan.md", "notes.md"]
    }
  ],
  "topics": [
    {
      "id": "authentication",
      "title": "Authentication",
      "path": "topics/authentication.md",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "tags": ["security", "auth"],
      "related": ["2026-07-001-auth"]
    }
  ],
  "documents": [
    {
      "id": "2026-07-001-auth/prd",
      "path": "features/2026-07-001-auth/prd.md",
      "type": "prd",
      "title": "Authentication PRD",
      "summary": "Implement OAuth2 + JWT based authentication system with SSO support for enterprise customers.",
      "tags": ["auth", "security", "sso"],
      "status": "approved",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-001-auth/plan.md",
        "topics/authentication.md"
      ]
    }
  ]
}
```

---

## Field Constraints

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | string | Unique within wiki; format: `feature-id/doc-type` or `topic-name` |
| `path` | string | Relative path from wiki root; use forward slashes |
| `type` | enum | One of: `prd`, `arch`, `plan`, `report`, `notes`, `topic` |
| `title` | string | Max 200 characters |
| `summary` | string | Max 500 characters, recommended ≤200 |
| `tags` | array | Strings, lowercase, no spaces (use hyphens) |
| `status` | enum | One of: `draft`, `review`, `approved`, `deprecated` |
| `created_at` | date | Format: `YYYY-MM-DD` |
| `updated_at` | date | Format: `YYYY-MM-DD` |
| `related` | array | Paths relative to wiki root, or absolute paths |
| `version` | string | Semantic versioning `X.Y` |
| `generated_at` | datetime | ISO 8601 format |
