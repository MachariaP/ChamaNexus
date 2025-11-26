# ChamaHub Backend - Django REST Framework API

## 📜 Table of Contents
* [1. Project Overview](#1-project-overview)
* [2. Team Roles and Responsibilities](#2-team-roles-and-responsibilities)
* [3. Technology Stack Overview](#3-technology-stack-overview)
* [4. Database Design Overview](#4-database-design-overview)
* [5. Feature Breakdown](#5-feature-breakdown)
* [6. API Security Overview](#6-api-security-overview)
* [7. CI/CD Pipeline Overview](#7-cicd-pipeline-overview)
* [8. Resources](#8-resources)
* [9. License](#9-license)
* [10. Created By](#10-created-by)

---

## 1. Project Overview

### Brief Description

The ChamaHub Backend is a production-grade REST API built with Django 5.1+ and Django REST Framework 3.16+. It serves as the core engine powering the ChamaHub fintech platform, providing secure endpoints for managing savings groups, financial transactions, governance, and investments.

The API is designed with scalability, security, and developer experience in mind. It implements RESTful best practices, comprehensive authentication with JWT tokens, role-based access control, and automatic API documentation via OpenAPI/Swagger. The backend handles complex financial operations including loan calculations, multi-signature approvals, and real-time balance tracking with ACID-compliant database transactions.

### Project Goals

* **Scalability**: Handle thousands of concurrent users with efficient database queries and Redis caching
* **Security First**: Implement bank-level security with KYC verification, audit trails, and multi-signature approvals
* **API Excellence**: Provide a well-documented, versioned API that frontend developers love to work with
* **Compliance Ready**: Support AML/KYC requirements, ODPC registration, and financial regulatory compliance
* **Real-Time Capabilities**: Enable live updates through Django Channels and WebSocket support
* **Background Processing**: Handle long-running tasks (emails, reports, payments) with Celery workers
* **Type-Safe Integration**: Generate OpenAPI schemas for automatic TypeScript type generation on the frontend

### Key Tech Stack

* **Framework**: Python 3.12+, Django 5.1+, Django REST Framework 3.16+
* **Database**: PostgreSQL 16 with optimized indexes
* **Caching**: Redis 7 for session storage and API response caching
* **Task Queue**: Celery 5.5+ with Redis as message broker
* **Real-Time**: Django Channels 4+ with WebSocket support
* **Authentication**: Simple JWT for token-based authentication
* **Documentation**: drf-spectacular for OpenAPI 3.0 schema generation
* **Production**: Gunicorn WSGI server, WhiteNoise static files, Sentry monitoring

---

## 2. Team Roles and Responsibilities

| Role | Key Responsibility |
|------|-------------------|
| **Backend Lead** | Architect API design, establish coding standards, review PRs, and mentor junior developers |
| **Backend Developer** | Implement API endpoints, write serializers, create viewsets, and handle business logic |
| **Database Engineer** | Design PostgreSQL schemas, optimize queries, create migrations, and manage database performance |
| **DevOps Engineer** | Configure Render/Railway deployments, set up environment variables, manage database backups |
| **Security Engineer** | Implement KYC/KYB workflows, audit logging, permission classes, and multi-signature approvals |
| **QA Engineer** | Write pytest test cases, integration tests, and ensure 80%+ code coverage |
| **Technical Writer** | Document API endpoints, create developer guides, and maintain OpenAPI schemas |

---

## 3. Technology Stack Overview

| Technology | Purpose in the Project |
|-----------|----------------------|
| **Python 3.12** | Primary programming language, chosen for readability, extensive libraries, and Django ecosystem support |
| **Django 5.1+** | Web framework providing ORM, migrations, authentication, admin interface, middleware, and security features |
| **Django REST Framework 3.16** | REST API toolkit with serializers, viewsets, routers, permissions, throttling, and content negotiation |
| **PostgreSQL 16** | Robust relational database with ACID compliance, JSON support, and advanced indexing for financial data |
| **Redis 7** | In-memory data store for caching API responses, storing sessions, and serving as Celery broker |
| **Celery 5.5** | Distributed task queue for background jobs like sending emails, generating reports, and processing payments |
| **Django Channels 4** | ASGI support for WebSockets, enabling real-time notifications and live data updates |
| **Simple JWT 5.5** | JWT authentication library with access/refresh token rotation and blacklisting |
| **drf-spectacular 0.29** | OpenAPI 3.0 schema generation with Swagger UI and ReDoc documentation |
| **django-filter 25** | Flexible queryset filtering for list endpoints with automatic filter generation |
| **django-cors-headers 4.9** | Cross-Origin Resource Sharing middleware for frontend communication |
| **django-auditlog 3.3** | Automatic model change tracking for audit trails and compliance |
| **Pillow 12** | Image processing for profile pictures, KYC documents, and receipt uploads |
| **psycopg2-binary 2.9** | PostgreSQL database adapter for Python with optimized binary protocol |
| **python-decouple 3.8** | Environment variable management for secure configuration |
| **Gunicorn 21** | Production-grade WSGI HTTP server for serving Django applications |
| **WhiteNoise 6.6** | Efficient static file serving for production without external CDN |
| **Sentry SDK 1.39** | Error tracking and performance monitoring in production |
| **pytest 9** | Testing framework with fixtures, parameterization, and coverage reporting |
| **pytest-django 4.11** | Django integration for pytest with database fixtures and client utilities |
| **factory-boy 3.3** | Test data generation with model factories for consistent test fixtures |
| **Faker 38** | Realistic fake data generation for seeding databases and testing |

---

## 4. Database Design Overview

### Key Entities

The backend manages 20+ database models organized into the following Django apps:

**accounts** - User management and authentication
* `User` - Custom user model with email authentication, KYC fields, credit score
* `MemberWallet` - Personal wallet tracking for each user

**groups** - Chama group management
* `ChamaGroup` - Savings/investment/welfare groups with KYB verification
* `GroupMembership` - User-group relationships with roles and status
* `GroupOfficial` - Elected officials with term tracking
* `GroupGoal` - Financial goals with progress tracking
* `GroupMessage` - In-group chat messages with attachments

**finance** - Financial operations
* `Contribution` - Member contributions with payment tracking
* `Loan` - Loan applications with interest calculation
* `LoanRepayment` - Loan repayment records
* `Expense` - Group expenses with approval workflow
* `DisbursementApproval` - Multi-signature approval tracking
* `ApprovalSignature` - Individual approver signatures

**governance** - Group governance and compliance
* `GroupConstitution` - Group rules and policies
* `Fine` - Member fines with payment tracking
* `Vote` - Digital voting records
* `VoteBallot` - Individual vote ballots
* `Document` - Group document storage
* `ComplianceRecord` - Regulatory compliance tracking

**investments** - Investment management
* `Investment` - Group investments (T-Bills, Fixed Deposits, etc.)
* `StockHolding` - Stock/share holdings
* `Portfolio` - Portfolio metrics and diversification
* `InvestmentTransaction` - Investment transactions

### Relationships

* **User → GroupMembership → ChamaGroup** (Many-to-Many through Membership)
  - A user can belong to multiple groups with different roles
  - Each membership tracks status, contributions, and join date

* **ChamaGroup → Contributions, Loans, Expenses** (One-to-Many)
  - All financial transactions are associated with a specific group
  - Enables group-level financial reporting and accountability

* **Loan → LoanRepayments** (One-to-Many)
  - Each loan tracks multiple repayment records
  - Outstanding balance calculated from repayment history

* **DisbursementApproval → ApprovalSignatures** (One-to-Many)
  - Multi-signature workflow requires multiple officials to sign
  - Tracks approval timestamp and comments

* **ChamaGroup → GroupConstitution** (One-to-One)
  - Each group has a single governing constitution
  - Constitution includes rules, fines, and policies

---

## 5. Feature Breakdown

### User Authentication & Management
* **Custom User Model**: Email-based authentication replacing Django's username field for better UX
* **JWT Authentication**: Access tokens (5 min) and refresh tokens (7 days) with automatic rotation
* **Token Blacklisting**: Revoke tokens on logout to prevent unauthorized access
* **Password Reset**: Email-based password reset with secure token generation
* **Profile Management**: Update profile picture, contact info, and personal details via API

### KYC/KYB Verification
* **Document Upload**: Secure file upload for ID documents, KRA PIN, registration certificates
* **Verification Status**: Track KYC status (pending, verified, rejected) with timestamp
* **Compliance Integration**: Support for ODPC registration and AML/KYC checks
* **File Validation**: Validate file types, sizes, and content before storage

### Group API Endpoints
* **CRUD Operations**: Create, read, update, delete groups with proper permissions
* **Member Management**: Add/remove members, update roles, approve membership requests
* **Official Elections**: Assign and track elected officials with term dates
* **Goal Tracking**: Set financial goals, track progress, mark as achieved
* **Group Messaging**: Real-time chat API with WebSocket support

### Financial Operations API
* **Contributions**:
  - Record contributions with payment method (M-Pesa, Bank, Cash)
  - Reconciliation workflow for treasurers
  - Filter by date, member, status, amount

* **Loans**:
  - Loan application with automatic interest calculation
  - Approval workflow (pending → approved → disbursed → active → completed)
  - Monthly payment calculation: `(principal × rate × months) / (100 × 12) + principal`
  - Outstanding balance tracking with repayment history

* **Expenses**:
  - Expense submission with category and receipt upload
  - Multi-signature approval before disbursement
  - Status tracking (pending → approved → disbursed)

* **Multi-Signature Approvals**:
  - Configurable approval threshold (default: 2 signatures)
  - Track individual signatures with timestamps
  - Automatic status update when threshold reached

### Governance API
* **Constitution Management**: Create and version group constitutions
* **Digital Voting**: 
  - Vote types: Simple Majority, Two-Thirds, Unanimous
  - Proxy voting support for absent members
  - Automatic result calculation
* **Fine Management**: Issue, track, and collect fines with reason documentation
* **Document Storage**: Upload and retrieve group documents with access control

### Investment API
* **Investment Tracking**: 
  - Support multiple types: Fixed Deposits, T-Bills, Money Market, Stocks, Bonds, Real Estate
  - Track principal, current value, expected returns
  - Calculate ROI and profit/loss

* **Stock Holdings**:
  - Track shares on NSE/USE exchanges
  - CDSC account integration
  - Real-time price updates

* **Portfolio Management**:
  - Aggregate portfolio metrics
  - Diversification percentages
  - Year-to-date return calculation

### Background Tasks (Celery)
* **Email Notifications**: Send contribution reminders, loan approvals, meeting invites
* **Report Generation**: Generate PDF financial statements asynchronously
* **Data Aggregation**: Calculate group statistics and update balances
* **Scheduled Tasks**: Daily/weekly/monthly automated jobs

### Real-Time Features (Django Channels)
* **Live Notifications**: Push notifications for new contributions, loan approvals
* **Group Chat**: Real-time messaging within groups
* **Online Presence**: Track which members are currently online
* **Balance Updates**: Live balance updates when transactions occur

---

## 6. API Security Overview

| Security Measure | Implementation | Why It's Crucial |
|-----------------|----------------|------------------|
| **JWT Authentication** | `djangorestframework-simplejwt` with 5-minute access tokens and 7-day refresh tokens | Stateless authentication scales horizontally; short-lived access tokens limit exposure window |
| **Token Rotation** | New refresh token issued on each refresh request | Prevents refresh token theft from granting permanent access |
| **Permission Classes** | `IsAuthenticated`, `IsGroupMember`, `IsGroupAdmin`, `IsGroupOfficial` | Role-based access control ensures users only access authorized resources |
| **Object-Level Permissions** | Check user membership before accessing group resources | Prevents cross-group data leakage |
| **Input Validation** | DRF serializers with field validators, regex patterns, and custom validators | Prevents SQL injection, XSS, and malformed data |
| **Rate Limiting** | `AnonRateThrottle` (100/day), `UserRateThrottle` (1000/day) | Prevents brute force attacks and API abuse |
| **CORS Whitelist** | `CORS_ALLOWED_ORIGINS` environment variable | Only trusted frontend domains can make API requests |
| **HTTPS Enforcement** | `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` in production | Encrypts all traffic, prevents man-in-the-middle attacks |
| **Password Security** | Django's PBKDF2 hashing with 720,000 iterations | Industry-standard password storage, resistant to rainbow table attacks |
| **Audit Logging** | `django-auditlog` on all models | Creates immutable audit trail for compliance and dispute resolution |
| **File Upload Security** | Validate content type, limit size, scan for malware | Prevents malicious file uploads |
| **SQL Injection Prevention** | Django ORM with parameterized queries | All database queries use parameterization, never raw SQL with user input |
| **XSS Prevention** | Django's auto-escaping templates, DRF JSON responses | API returns JSON, which is inherently XSS-safe |
| **CSRF Protection** | Django CSRF middleware for session-based views | Protects admin interface and any non-API views |
| **Secret Management** | `python-decouple` for environment variables | Secrets never committed to source code |
| **Error Monitoring** | Sentry integration with PII scrubbing | Detect attacks and errors without exposing sensitive data |

### API Authentication Flow

```
1. User submits email/password to /api/token/
2. Server validates credentials, returns access + refresh tokens
3. Client stores tokens securely (httpOnly cookie or secure storage)
4. Client includes access token in Authorization header: Bearer <token>
5. On 401 response, client sends refresh token to /api/token/refresh/
6. Server issues new access token (and optionally rotates refresh token)
7. On logout, client sends refresh token to /api/token/blacklist/
```

---

## 7. CI/CD Pipeline Overview

Continuous Integration and Continuous Deployment (CI/CD) automates the testing, building, and deployment of the backend API. This ensures code quality, reduces human error, and enables rapid iteration.

### Pipeline Stages

1. **Code Push**: Developer pushes code to GitHub repository
2. **Automated Testing**: 
   - Run `pytest` with coverage reporting
   - Lint code with `flake8` and `black`
   - Check types with `mypy` (optional)
3. **Build**: 
   - Install dependencies from `requirements.txt`
   - Run database migrations
   - Collect static files with `python manage.py collectstatic`
4. **Deploy**: 
   - Render automatically deploys on push to main branch
   - Environment variables configured in Render dashboard
5. **Health Check**: 
   - Verify `/api/health/` endpoint returns 200 OK
   - Sentry notifies on deployment

### Deployment Configuration

The `render.yaml` file configures the Render deployment:

```yaml
services:
  - type: web
    name: chamahub-api
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
    startCommand: gunicorn chamahub.wsgi:application
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: chamahub-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: chamahub-redis
          property: connectionString
```

### Testing Strategy

| Test Type | Tool | Coverage Target |
|-----------|------|-----------------|
| Unit Tests | pytest + pytest-django | 80%+ |
| Integration Tests | DRF APIClient | All endpoints |
| Model Tests | factory-boy for fixtures | All models |
| Security Tests | Custom test cases | Auth, permissions |

### Monitoring

* **Sentry**: Error tracking with stack traces and context
* **Render Logs**: Real-time log streaming for debugging
* **Database Metrics**: Connection pool, query performance via Render dashboard

---

## 8. Resources

### Official Documentation
* [Django Documentation](https://docs.djangoproject.com/en/5.1/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
* [drf-spectacular](https://drf-spectacular.readthedocs.io/)
* [Celery Documentation](https://docs.celeryq.dev/)
* [Django Channels](https://channels.readthedocs.io/)

### Project Documentation
* [API Reference](../API_README.md)
* [Fintech API Documentation](../FINTECH_API_DOCUMENTATION.md)
* [Finance API Guide](../FINANCE_API.md)
* [Render Deployment Guide](../docs/RENDER_DEPLOYMENT.md)
* [CORS Troubleshooting](../CORS_TROUBLESHOOTING.md)

### Learning Guides
* [Guide 1: Initial Setup](../docs/01-initial-setup.md)
* [Guide 4: Database Design](../docs/04-models-database.md)
* [Guide 5: Advanced DRF](../docs/05-advanced-drf.md)
* [Guide 6: Production Features](../docs/06-production-features.md)
* [PostgreSQL Deep Dive](../learn/09-postgresql-deep-dive.md)
* [Authentication Explained](../learn/10-authentication-explained.md)

### API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/token/` | POST | Obtain JWT access and refresh tokens |
| `/api/token/refresh/` | POST | Refresh access token |
| `/api/v1/users/` | GET, POST | List users, create user |
| `/api/v1/users/me/` | GET, PATCH | Current user profile |
| `/api/v1/groups/` | GET, POST | List/create chama groups |
| `/api/v1/groups/{id}/members/` | GET, POST | Group members |
| `/api/v1/contributions/` | GET, POST | List/create contributions |
| `/api/v1/loans/` | GET, POST | List/create loans |
| `/api/v1/expenses/` | GET, POST | List/create expenses |
| `/api/v1/votes/` | GET, POST | List/create votes |
| `/api/v1/investments/` | GET, POST | List/create investments |

---

## 9. License

This project is licensed under the **MIT License**.

Copyright (c) 2025 Phinehas Macharia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

---

## 10. Created By

**Phinehas Macharia**

* GitHub: [@MachariaP](https://github.com/MachariaP)
* Twitter: [@_M_Phinehas](https://twitter.com/_M_Phinehas)

---

*Last Updated: November 2025*

