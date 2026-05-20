---
name: security-hardening
description: Apply security hardening techniques using OWASP standards. Use when reviewing code for vulnerabilities, implementing authentication, handling sensitive data, or adding new dependencies.
---

# Security Hardening Skill

This skill provides comprehensive security guidance based on OWASP standards and agentic AI security best practices.

## Quick Reference

### OWASP Top 10 for Agentic Applications (2026)

| ID | Risk | Quick Check |
|----|------|-------------|
| ASI01 | Goal Hijack | Does code process untrusted content from external sources? |
| ASI02 | Tool Misuse | Are tool permissions scoped to minimum required? |
| ASI03 | Identity Abuse | Are credentials properly scoped and short-lived? |
| ASI04 | Supply Chain | Are dependencies pinned and verified? |
| ASI05 | Code Execution | Is generated code executed without validation? |
| ASI06 | Memory Poisoning | Is RAG/chroma data filtered before ingestion? |
| ASI07 | Inter-Agent Comm | Are messages authenticated and encrypted? |
| ASI08 | Cascading Failures | Do failures properly isolate and not propagate? |
| ASI09 | Trust Exploitation | Does output contain persuasive language for sensitive actions? |
| ASI10 | Rogue Agents | Is there a kill switch for compromised agents? |

## Language-Specific Patterns

### Python Security

```python
# GOOD: Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# BAD: String interpolation (SQL injection)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# GOOD: Input validation with pydantic v2
from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    email: EmailStr
    age: int

# Alternative: Custom regex validation (less robust)
# from pydantic import BaseModel, field_validator
# import re
# EMAIL_PATTERN = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
# class UserInput(BaseModel):
#     email: str
#     age: int
#     @field_validator('email')
#     @classmethod
#     def validate_email(cls, v: str) -> str:
#         if not EMAIL_PATTERN.match(v):
#             raise ValueError('Invalid email')
#         return v

# BAD: No input validation
def process_user(data):
    return data['email']  # KeyError if missing
```

### TypeScript Security

```typescript
// GOOD: Type-safe input handling
interface UserInput {
  email: string;
  age: number;
}

function validateInput(input: unknown): UserInput {
  if (!input || typeof input !== 'object') {
    throw new Error('Invalid input');
  }
  const { email, age } = input as Record<string, unknown>;
  if (typeof email !== 'string' || !email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (typeof age !== 'number' || age < 0) {
    throw new Error('Invalid age');
  }
  return { email, age };
}

// BAD: No type checking or validation
function processUser(data: any) {
  return data.email; // Could be undefined
}
```

## Common Vulnerability Fixes

### Command Injection

```python
# BAD
os.system(f"ls {directory}")

# GOOD
subprocess.run(["ls", directory], shell=False)
```

### Path Traversal

```python
# BAD
with open(f"uploads/{filename}") as f:

# GOOD
from pathlib import Path
base = Path("uploads").resolve()
file_path = (base / filename).resolve()
if not file_path.is_relative_to(base):
    raise ValueError("Invalid path")
```

### YAML Deserialization

```python
# BAD - Unsafe
yaml.unsafe_load(user_input)

# GOOD - Safe
yaml.safe_load(user_input)
```

### Hardcoded Secrets

```python
# BAD
API_KEY = "sk-1234567890abcdef"

# GOOD - Use environment variables
import os
API_KEY = os.environ.get("API_KEY")
```

## Security Checklist

Before any code change:

- [ ] Input validation on all user-provided data
- [ ] Parameterized queries (no string interpolation)
- [ ] No hardcoded secrets (use env vars)
- [ ] Proper error handling (no stack traces in production)
- [ ] Authentication/authorization properly implemented
- [ ] Least privilege for file/network access
- [ ] Logging doesn't capture sensitive data
- [ ] Dependencies are up-to-date and scanned
- [ ] No eval() or exec() with user input
- [ ] CSP headers set for web apps

## MCP Server Security

When adding new MCP servers:

1. **Verify Source** — Official providers only
2. **Scope Permissions** — Minimum required access
3. **Network Isolation** — Don't allow unrestricted egress
4. **Monitor Usage** — Log all tool calls
5. **Pin Versions** — Don't use floating versions

## References

- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/)
- [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [MITRE ATLAS](https://atlas.mitre.org/)
