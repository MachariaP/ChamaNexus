# ChamaHub - Full-Stack Fintech Platform

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

ChamaHub is a comprehensive full-stack fintech platform designed to modernize and digitize the management of savings groups (chamas) in Kenya and across Africa. The platform addresses the critical need for transparent, secure, and efficient management of community-based savings and credit associations, which are a cornerstone of financial inclusion in developing economies.

The solution combines a powerful Django REST Framework backend with a modern React/TypeScript frontend, enabling groups to track contributions, manage loans, handle expenses, facilitate democratic governance through digital voting, and grow wealth through investment tracking—all while maintaining bank-level security and compliance standards.

### Project Goals

* **Financial Inclusion**: Democratize access to financial management tools for savings groups of all sizes
* **Transparency**: Provide immutable audit trails and real-time financial tracking to build trust among members
* **Scalability**: Handle groups ranging from 5 members to thousands with consistent performance
* **Security**: Implement bank-grade security with KYC/KYB verification, AML compliance, and multi-signature approvals
* **Mobile-First**: Deliver a responsive, progressive web application optimized for mobile users in Africa
* **Integration-Ready**: Support M-Pesa and other mobile money platforms for seamless transactions
* **Automation**: Enable automated wealth management through treasury bill investments and dividend reinvestment

### Key Tech Stack

* **Backend**: Python 3.12+, Django 5.1+, Django REST Framework 3.16+
* **Frontend**: TypeScript 5+, React 19+, Vite 7+, Tailwind CSS
* **Database**: PostgreSQL 16
* **Caching & Queues**: Redis 7, Celery 5.5+
* **Real-Time**: Django Channels, WebSockets
* **Authentication**: JWT (Simple JWT)
* **Documentation**: drf-spectacular (OpenAPI/Swagger)

---

## 2. Team Roles and Responsibilities

| Role | Key Responsibility |
|------|-------------------|
| **Backend Developer** | Design and implement REST APIs, database models, authentication, and business logic using Django and DRF |
| **Frontend Developer** | Build responsive UI components, implement state management, integrate APIs using React/TypeScript |
| **Full-Stack Developer** | Bridge backend and frontend, ensure type-safe API integration, handle CORS and authentication flows |
| **Database Administrator** | Design and optimize PostgreSQL schemas, implement indexes, manage migrations and backups |
| **DevOps Engineer** | Set up CI/CD pipelines, manage deployments to Render/Railway, configure monitoring and logging |
| **QA Engineer** | Write and maintain unit, integration, and e2e tests using pytest and React Testing Library |
| **Security Engineer** | Implement KYC/KYB verification, audit trails, AML compliance, and multi-signature approvals |
| **Product Manager** | Define feature requirements, prioritize backlog, coordinate between stakeholders and development team |
| **Technical Writer** | Create API documentation, user guides, and maintain README files |
| **UI/UX Designer** | Design user interfaces, create wireframes, ensure accessibility and mobile responsiveness |

---

## 3. Technology Stack Overview

### Backend Technologies

| Technology | Purpose in the Project |
|-----------|----------------------|
| **Python 3.12** | Primary programming language for backend development, chosen for readability and extensive ecosystem |
| **Django 5.1+** | Web framework providing ORM, authentication, admin interface, and security features out of the box |
| **Django REST Framework** | Toolkit for building RESTful APIs with serializers, viewsets, permissions, and pagination |
| **PostgreSQL 16** | Primary relational database for storing all application data with ACID compliance |
| **Redis 7** | In-memory data store for caching, session management, and Celery message broker |
| **Celery 5.5** | Distributed task queue for background processing (emails, reports, scheduled jobs) |
| **Django Channels** | WebSocket support for real-time features (live updates, notifications, chat) |
| **Simple JWT** | JSON Web Token authentication for secure, stateless API authentication |
| **drf-spectacular** | OpenAPI 3.0 schema generation for automatic API documentation |
| **django-filter** | Flexible filtering for API querysets |
| **django-cors-headers** | CORS handling for frontend-backend communication |
| **django-auditlog** | Automatic audit trail logging for database changes |
| **Pillow** | Image processing for profile pictures and document uploads |
| **Gunicorn** | Production WSGI server for serving Django applications |
| **WhiteNoise** | Static file serving for production deployments |
| **Sentry** | Error monitoring and performance tracking in production |

### Frontend Technologies

| Technology | Purpose in the Project |
|-----------|----------------------|
| **TypeScript 5.9** | Strongly-typed JavaScript for improved code quality and developer experience |
| **React 19** | UI library for building component-based user interfaces |
| **Vite 7** | Next-generation frontend build tool for fast development and optimized production builds |
| **Tailwind CSS 3.4** | Utility-first CSS framework for rapid UI development |
| **React Router 7** | Client-side routing for single-page application navigation |
| **React Query (TanStack)** | Server state management, caching, and data synchronization |
| **Zustand 5** | Lightweight state management for client-side state |
| **React Hook Form** | Performant form handling with validation |
| **Zod 4** | TypeScript-first schema validation for forms and API responses |
| **Framer Motion** | Animation library for smooth UI transitions and interactions |
| **Recharts 3** | Composable charting library for financial data visualization |
| **Lucide React** | Modern icon library with tree-shakeable icons |
| **Axios** | HTTP client for API communication |
| **Radix UI** | Unstyled, accessible component primitives |

---

## 4. Database Design Overview

### Key Entities

* **User** - Custom user model with email-based authentication, KYC fields, credit scoring, and profile information
* **MemberWallet** - Individual member wallet for tracking personal funds within groups
* **ChamaGroup** - Savings group entity with KYB documents, settings, and balance tracking
* **GroupMembership** - Junction table linking users to groups with roles and status
* **GroupOfficial** - Elected officials with term tracking (Chairperson, Treasurer, Secretary)
* **GroupGoal** - Financial goals with target amounts and progress tracking
* **GroupMessage** - Chat messages within groups with attachment support
* **Contribution** - Member contributions with payment method, status, and reconciliation
* **Loan** - Loan applications with interest calculation, approval workflow, and repayment tracking
* **LoanRepayment** - Individual loan repayment records
* **Expense** - Group expenses with approval workflow and receipt uploads
* **DisbursementApproval** - Multi-signature approval records for disbursements
* **ApprovalSignature** - Individual approver signatures
* **Vote** - Digital voting records with various voting types
* **VoteBallot** - Individual vote ballots with proxy voting support
* **GroupConstitution** - Group rules, policies, and fines
* **Fine** - Member fines with payment tracking
* **Document** - Group document storage with access control
* **ComplianceRecord** - Regulatory compliance tracking (ODPC, AML/KYC)
* **Investment** - Group investments (Fixed Deposits, T-Bills, Money Market, Stocks, Bonds)
* **StockHolding** - Stock/share holdings with real-time valuation
* **Portfolio** - Portfolio metrics and diversification tracking
* **InvestmentTransaction** - Investment buy/sell/dividend transactions

### Relationships

* **One User has many GroupMemberships** - A user can be a member of multiple chama groups, each with different roles (Member, Treasurer, Chairperson)
* **One ChamaGroup has many Contributions, Loans, and Expenses** - All financial transactions are associated with a specific group for accountability
* **One Loan has many LoanRepayments** - Each loan tracks its repayment history with multiple payments until completion
* **One DisbursementApproval has many ApprovalSignatures** - Multi-signature approvals require multiple officials to sign off before disbursement
* **One ChamaGroup has one GroupConstitution** - Each group has a single governing constitution document
* **One ChamaGroup has one Portfolio** - Investment portfolio metrics are tracked per group

---

## 5. Feature Breakdown

### User Management & Authentication
* **Email-based authentication**: Custom user model using email as the primary identifier instead of username
* **JWT token authentication**: Secure, stateless authentication with automatic token refresh and rotation
* **KYC verification**: Upload and verify ID documents, KRA PIN for regulatory compliance
* **Profile management**: Profile pictures, date of birth, address, and contact information
* **Credit scoring**: Internal credit score based on payment history within the platform

### Group Management
* **Chama creation**: Create savings, investment, welfare, or mixed-purpose groups with custom settings
* **KYB verification**: Upload registration certificates, KRA documents, and articles of association
* **Role-based membership**: Assign roles (Admin, Chairperson, Treasurer, Secretary, Member) with appropriate permissions
* **Member management**: Track membership status (Pending, Active, Suspended, Exited) and approval workflows
* **Group goals**: Set and track financial targets with progress visualization

### Financial Operations
* **Contribution tracking**: Record member contributions via M-Pesa, Bank Transfer, or Cash with reconciliation
* **Loan management**: Apply for loans with interest calculation, approval workflow, and repayment scheduling
* **Expense management**: Submit expenses with receipts, categorization, and multi-signature approval
* **Multi-signature approvals**: Require multiple officials to approve large disbursements
* **Real-time balance updates**: Track group and individual balances in real-time

### Governance & Compliance
* **Digital voting**: Create votes with simple majority, two-thirds, or unanimous requirements
* **Proxy voting**: Allow members to vote on behalf of absent members
* **Constitution management**: Digital storage of group constitution with versioning
* **Fine management**: Issue and track fines for rule violations (late contributions, missed meetings)
* **Compliance tracking**: Monitor ODPC registration, AML/KYC compliance, and security certifications
* **Audit trail**: Automatic logging of all data changes for transparency

### Investment Management
* **Portfolio tracking**: Monitor diversified investments across multiple asset classes
* **Stock holdings**: Track shares on NSE/USE with real-time valuation and CDSC integration
* **Investment types**: Support for Fixed Deposits, Treasury Bills, Money Market Funds, Bonds, and Real Estate
* **Transaction history**: Record buy/sell/dividend/interest/maturity transactions
* **ROI calculation**: Automatic return on investment and profit/loss calculations

### Communication
* **Group messaging**: Real-time chat within groups with file attachments
* **Document sharing**: Upload and share meeting minutes, financial statements, and reports
* **Notifications**: Email and in-app notifications for important events

---

## 6. API Security Overview

| Security Measure | Implementation | Why It's Crucial |
|-----------------|----------------|------------------|
| **JWT Authentication** | Simple JWT with access/refresh token rotation | Provides stateless authentication that scales horizontally and prevents session hijacking through token expiration |
| **CORS Configuration** | django-cors-headers with whitelist | Prevents cross-origin attacks by only allowing requests from trusted frontend domains |
| **Input Validation** | DRF serializers with Zod on frontend | Prevents SQL injection, XSS, and malformed data from reaching the database |
| **Permission Classes** | Custom DRF permissions (IsAuthenticated, IsGroupMember, IsGroupAdmin) | Ensures users can only access resources they're authorized to view or modify |
| **Rate Limiting** | DRF throttling (AnonRateThrottle, UserRateThrottle) | Prevents brute force attacks and API abuse |
| **Password Hashing** | Django's PBKDF2 algorithm | Secures user credentials even if database is compromised |
| **KYC/KYB Verification** | Document upload and manual verification | Ensures regulatory compliance and prevents fraud |
| **Multi-Signature Approvals** | Required approvals count before disbursement | Prevents unauthorized fund transfers and embezzlement |
| **Audit Logging** | django-auditlog for all model changes | Provides accountability and evidence for disputes or audits |
| **HTTPS Enforcement** | SECURE_SSL_REDIRECT in production | Encrypts all data in transit to prevent eavesdropping |
| **Environment Variables** | python-decouple for secrets | Keeps sensitive configuration out of source code |
| **Error Monitoring** | Sentry integration | Detects and alerts on security-related errors in production |

---

## 7. CI/CD Pipeline Overview

Continuous Integration and Continuous Deployment (CI/CD) is a software development practice that automates the process of testing, building, and deploying code changes. For ChamaHub, CI/CD ensures that every code change is automatically validated before being deployed to production, reducing the risk of introducing bugs and security vulnerabilities.

The project is configured for deployment on **Render** (recommended for beginners) with the following pipeline:

1. **Code Push**: Developers push code to GitHub repository
2. **Automated Testing**: On each push, automated tests run to validate code quality
3. **Build Process**: Backend builds with `pip install` and migrations; Frontend builds with `npm run build`
4. **Deployment**: Render automatically deploys changes from the main branch
5. **Health Checks**: Post-deployment health checks ensure the application is running correctly

**Tools Used**:
* **GitHub**: Source code repository and version control
* **Render**: Platform-as-a-Service for hosting backend, frontend, PostgreSQL, and Redis
* **Docker** (optional): Containerization for consistent development and production environments
* **pytest**: Backend testing framework with coverage reporting
* **ESLint/TypeScript**: Frontend code quality and type checking

**Benefits**:
* Faster feedback on code changes
* Reduced manual deployment errors
* Consistent testing across all changes
* Easy rollback capabilities
* Automatic environment configuration

---

## 8. Resources

### Official Documentation
* [Django Documentation](https://docs.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [React Documentation](https://react.dev/)
* [TypeScript Handbook](https://www.typescriptlang.org/docs/)
* [Tailwind CSS](https://tailwindcss.com/docs)

### Deployment Guides
* [Render Deployment Guide](./docs/RENDER_DEPLOYMENT.md)
* [CORS Troubleshooting](./CORS_TROUBLESHOOTING.md)
* [Dashboard Troubleshooting](./DASHBOARD_TROUBLESHOOTING.md)

### API Documentation
* [API Reference](./API_README.md)
* [Fintech API Documentation](./FINTECH_API_DOCUMENTATION.md)
* [Finance API Guide](./FINANCE_API.md)

### Learning Resources
* [PostgreSQL Deep Dive](./learn/09-postgresql-deep-dive.md)
* [Authentication Explained](./learn/10-authentication-explained.md)
* [Serializers Explained](./learn/11-serializers-explained.md)

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

