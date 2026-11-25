
# WEEK 5 – SECURITY TESTING REPORT

## Project
Secure User Management System

## 1. Application Testing

The Flask application was successfully started
using Python 3.11.

The SQLite database was initialized successfully.

Manual testing confirmed:
- User registration works.
- User login works.
- Dashboard access works after login.
- Invalid login credentials are rejected.

## 2. Automated Testing

Testing tool: Pytest

Command:
python -m pytest -v

Result:
11 tests passed.

## 3. Static Security Analysis

Tool: Bandit

Command:
python -m bandit -r app.py -ll

Results:

| Severity | Issues |
|---|---:|
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Undefined | 0 |

Confidence findings:
All categories reported zero issues.

Files skipped: 0

## 4. Security Measures Validated

- Parameterized SQL queries
- Scrypt password hashing
- Input validation
- CSRF protection
- Secure session configuration
- Safe error handling
- Environment-based secret management

## 5. Conclusion

The application successfully passed 11
automated tests.

Bandit reported zero security issues at the
selected severity and confidence levels.

Manual testing confirmed the main application
features.

The results demonstrate the practical use of
secure coding techniques in Python applications.
