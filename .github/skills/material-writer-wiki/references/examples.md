# Wiki Examples

This document provides complete examples of feature folders and topic pages.

---

## Example 1: Authentication Feature (`2026-07-001-auth`)

### Folder Structure

```
features/2026-07-001-auth/
├── index.json
├── 2026-07-13-prd-auth.md
├── 2026-07-13-arch-auth.md
├── 2026-07-13-plan-auth.md
├── 2026-07-13-report-auth.md
└── 2026-07-13-notes-auth.md
```

### `features/2026-07-001-auth/index.json`

```json
{
  "feature": {
    "id": "2026-07-001-auth",
    "title": "Authentication System",
    "created_at": "2026-07-13",
    "updated_at": "2026-07-13"
  },
  "documents": [
    {
      "id": "2026-07-001-auth/prd",
      "path": "features/2026-07-001-auth/2026-07-13-prd-auth.md",
      "type": "prd",
      "title": "Authentication System PRD",
      "summary": "Implement OAuth2 + JWT based authentication system with SSO support for enterprise customers.",
      "tags": ["auth", "security", "sso"],
      "status": "approved",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-001-auth/2026-07-13-plan-auth.md",
        "topics/authentication.md"
      ]
    },
    {
      "id": "2026-07-001-auth/arch",
      "path": "features/2026-07-001-auth/2026-07-13-arch-auth.md",
      "type": "arch",
      "title": "Authentication System Architecture",
      "summary": "High-level architecture for OAuth2 + JWT authentication with SSO gateway.",
      "tags": ["architecture", "auth", "security"],
      "status": "approved",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-001-auth/2026-07-13-prd-auth.md",
        "features/2026-07-001-auth/2026-07-13-plan-auth.md"
      ]
    },
    {
      "id": "2026-07-001-auth/plan",
      "path": "features/2026-07-001-auth/2026-07-13-plan-auth.md",
      "type": "plan",
      "title": "Authentication Implementation Plan",
      "summary": "3-phase implementation: OAuth2 foundation → JWT integration → SSO deployment.",
      "tags": ["planning", "auth"],
      "status": "approved",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-001-auth/2026-07-13-prd-auth.md",
        "features/2026-07-001-auth/2026-07-13-arch-auth.md"
      ]
    },
    {
      "id": "2026-07-001-auth/report",
      "path": "features/2026-07-001-auth/2026-07-13-report-auth.md",
      "type": "report",
      "title": "Authentication System Validation Report",
      "summary": "All 47 test cases passed. Security audit completed. Production deployment approved.",
      "tags": ["validation", "testing", "auth"],
      "status": "approved",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-001-auth/2026-07-13-prd-auth.md",
        "features/2026-07-001-auth/2026-07-13-plan-auth.md"
      ]
    },
    {
      "id": "2026-07-001-auth/notes",
      "path": "features/2026-07-001-auth/2026-07-13-notes-auth.md",
      "type": "notes",
      "title": "Authentication Research Notes",
      "summary": "Research findings on OAuth2 providers, JWT best practices, and SSO patterns.",
      "tags": ["research", "decisions", "auth"],
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-001-auth/2026-07-13-prd-auth.md"
      ]
    }
  ]
}
```

### `features/2026-07-001-auth/2026-07-13-prd-auth.md`

```markdown
---
id: 2026-07-001-auth/prd
type: prd
title: Authentication System PRD
summary: Implement OAuth2 + JWT based authentication system with SSO support for enterprise customers.
tags: [auth, security, sso]
status: approved
created_at: 2026-07-13
updated_at: 2026-07-13
related:
  - features/2026-07-001-auth/2026-07-13-plan-auth.md
  - topics/authentication.md
---

# Authentication System - Product Requirements Document

## Overview
Enterprise customers require secure, single sign-on (SSO) access to our platform. This PRD defines an OAuth2 + JWT based authentication system that supports SAML 2.0 enterprise SSO while maintaining backwards compatibility with existing username/password authentication.

## Goals
- Enable enterprise customers to authenticate via their existing SAML 2.0 identity providers (Okta, Azure AD, Google Workspace)
- Provide JWT-based session management for API authentication
- Maintain existing username/password login for non-SSO users
- Achieve SOC 2 Type II compliance for authentication subsystem

## User Stories
1. As an enterprise IT admin, I want to configure SSO so my users can sign in with company credentials
2. As a developer, I want API authentication via JWT so I can build integrations
3. As an end user, I want to choose between SSO and password login so I can access the platform my way

## Requirements

### Functional Requirements
- REQ-001: Support SAML 2.0 SP-initiated SSO with major IdPs (Okta, Azure AD, Google)
- REQ-002: Issue JWTs with 1-hour expiry, refresh token rotation
- REQ-003: Fallback to username/password when SSO is unavailable
- REQ-004: Support multi-domain SSO configurations

### Non-Functional Requirements
- Performance: Authentication response < 200ms p95
- Security: All auth endpoints require TLS 1.3
- Scalability: Support 10,000 concurrent auth sessions

## Dependencies
- Identity Provider configurations (customer-managed)
- JWT library (PyJWT)
- SSO gateway service

## Open Questions
- Should we support OIDC in addition to SAML 2.0?
- What's the session timeout policy for SSO users?
```

---

## Example 2: Payment Feature (`2026-07-002-payment`)

### Folder Structure

```
features/2026-07-002-payment/
├── index.json
├── 2026-07-13-prd-payment.md
├── 2026-07-13-plan-payment.md
└── 2026-07-13-notes-payment.md
```

### `features/2026-07-002-payment/index.json`

```json
{
  "feature": {
    "id": "2026-07-002-payment",
    "title": "Payment Gateway Integration",
    "created_at": "2026-07-13",
    "updated_at": "2026-07-13"
  },
  "documents": [
    {
      "id": "2026-07-002-payment/prd",
      "path": "features/2026-07-002-payment/2026-07-13-prd-payment.md",
      "type": "prd",
      "title": "Payment Gateway PRD",
      "summary": "Integrate Stripe payment gateway to support credit card processing and subscription billing.",
      "tags": ["payments", "stripe", "billing"],
      "status": "draft",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-002-payment/2026-07-13-plan-payment.md",
        "topics/payments.md"
      ]
    },
    {
      "id": "2026-07-002-payment/plan",
      "path": "features/2026-07-002-payment/2026-07-13-plan-payment.md",
      "type": "plan",
      "title": "Payment Gateway Implementation Plan",
      "summary": "Phase 1: Basic checkout. Phase 2: Subscriptions. Phase 3: Refunds and disputes.",
      "tags": ["planning", "payments"],
      "status": "draft",
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-002-payment/2026-07-13-prd-payment.md"
      ]
    },
    {
      "id": "2026-07-002-payment/notes",
      "path": "features/2026-07-002-payment/2026-07-13-notes-payment.md",
      "type": "notes",
      "title": "Payment Gateway Research Notes",
      "summary": "Comparing Stripe vs Square vs Braintree. PCI compliance requirements. Webhook handling patterns.",
      "tags": ["research", "decisions", "payments"],
      "created_at": "2026-07-13",
      "updated_at": "2026-07-13",
      "related": [
        "features/2026-07-002-payment/2026-07-13-prd-payment.md"
      ]
    }
  ]
}
```

---

## Example 3: Topic Page (`topics/authentication.md`)

### `topics/authentication.md`

```markdown
---
id: topics/authentication
type: topic
title: Authentication
summary: Cross-cutting concepts for authentication, authorization, and session management across all features.
tags: [auth, security, concept]
created_at: 2026-07-13
updated_at: 2026-07-13
related:
  - features/2026-07-001-auth/prd.md
---

# Authentication

## Overview
Authentication (authn) is the process of verifying identity. This topic covers authentication patterns, protocols, and best practices used across the platform.

## Key Principles

1. **Never store passwords** - Use OAuth2/SAML/federated identity
2. **Short-lived tokens** - JWTs should expire within hours, not days
3. **Refresh token rotation** - Each use generates a new refresh token
4. **Defense in depth** - Multiple auth factors for sensitive operations

## Authentication Methods

### OAuth2 + JWT
Used by: [[../2026-07-001-auth/prd]]

OAuth2 provides the authorization framework; JWTs provide stateless session tokens.

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│   App   │────▶│   API   │
└─────────┘     └────┬────┘     └─────────┘
                     │ JWT validation
                     ▼
                ┌─────────┐
                │  Auth   │
                │ Service │
                └─────────┘
```

### SAML 2.0 SSO
Used for enterprise SSO with identity providers like Okta, Azure AD.

## Session Management

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| JWT | API auth | Stateless, scalable | Can't revoke easily |
| Session cookie | Web apps | Easy revocation | Server state |
| Refresh token | Long-lived | Better UX | Complexity |

## Security Considerations

- All auth endpoints must use TLS 1.3
- Implement rate limiting on login attempts
- Log auth events for audit trail
- Support for MFA on sensitive operations

## Related Topics

- [Authorization](authorization.md) - Permissions and access control
- [Session Management](session-management.md) - Token lifecycle
- [Security](security.md) - Security best practices
```

---

## Example: Log File

### `wiki/log.md`

```markdown
# Wiki Log

Append-only chronological log of wiki operations.

Format: `## [YYYY-MM-DD] <action> | <title>`

## [2026-07-13] ingest | Authentication System PRD
## [2026-07-13] ingest | Authentication System Architecture
## [2026-07-13] ingest | Authentication Implementation Plan
## [2026-07-13] ingest | Authentication System Validation Report
## [2026-07-13] ingest | Authentication Research Notes
## [2026-07-13] ingest | Payment Gateway PRD
## [2026-07-13] ingest | Payment Gateway Implementation Plan
## [2026-07-13] ingest | Payment Gateway Research Notes
## [2026-07-13] query | authentication sso
## [2026-07-13] query | payment stripe
## [2026-07-14] ingest | Topic: Authentication
```

---

## CLI Usage Examples

### Initialize Wiki

```bash
python .github/skills/material-writer-wiki/scripts/wiki.py init
```

### Add Document

```bash
python .github/skills/material-writer-wiki/scripts/wiki.py add wiki/features/2026-07-001-auth/2026-07-13-prd-auth.md
```

### List Documents

```bash
# List all PRDs
python .github/skills/material-writer-wiki/scripts/wiki.py list --type prd

# List all auth-related docs
python .github/skills/material-writer-wiki/scripts/wiki.py list --tag auth

# List approved docs for feature 2026-07-001
python .github/skills/material-writer-wiki/scripts/wiki.py list --feature 2026-07-001 --status approved
```

### Search

```bash
python .github/skills/material-writer-wiki/scripts/wiki.py search "authentication"
python .github/skills/material-writer-wiki/scripts/wiki.py search "sso oauth2"
```

### Find Related Documents

```bash
python .github/skills/material-writer-wiki/scripts/wiki.py related wiki/features/2026-07-001-auth/2026-07-13-prd-auth.md
```

### Reindex

```bash
python .github/skills/material-writer-wiki/scripts/wiki.py reindex
```
