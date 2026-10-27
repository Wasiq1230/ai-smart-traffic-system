# Security & Access Control

## Authentication & Authorization
- **Password Hashing**: Bcrypt with adaptive work factor.
- **Tokens**: Signed JWT (JSON Web Tokens) with configurable expiry.
- **Role-Based Access Control (RBAC)**:
  - `ADMIN`: Full administrative control, user management, and system configuration.
  - `OPERATOR`: Traffic monitoring, manual signal optimization, and incident resolution.
  - `AUTHORITY`: Emergency preemption access and violation oversight.
  - `VIEWER`: Read-only dashboard access.
- **Input Validation**: Strict Pydantic schemas on all request payloads.
- **Secrets Management**: Loaded exclusively via `.env` environment variables.
