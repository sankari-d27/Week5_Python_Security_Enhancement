
# WEEK 5 SECURITY AUDIT REPORT

## Project Title
Security Enhancements in Python Applications

## Application
Secure User Management System

## 1. Introduction

The purpose of this project is to identify and
resolve common security vulnerabilities in a
Python web application.

The application uses Flask and SQLite to provide
user registration, authentication, and dashboard
functionality.

## 2. Initial Security Review

The following potential vulnerabilities were
examined:

1. SQL Injection
2. Plain-text password storage
3. Cross-Site Scripting (XSS)
4. Cross-Site Request Forgery (CSRF)
5. Weak session management
6. Improper error handling
7. Invalid user input
8. Information leakage

These are the security weaknesses assessed
during the review. The final implementation
uses defensive controls against them.

## 3. Vulnerability Analysis and Fixes

### 3.1 SQL Injection

Risk: High

Description:
SQL injection occurs when untrusted user input
is directly included in SQL statements.

Impact:
An attacker could manipulate database queries
and potentially access or modify unauthorized
records.

Security Fix:
Parameterized SQL queries were implemented.

Secure code:

db.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)

The database treats user input as data rather
than executable SQL.

### 3.2 Plain-Text Password Storage

Risk: High

Description:
Storing passwords in plain text exposes user
credentials if the database is compromised.

Impact:
Attackers could obtain passwords and attempt
to access other accounts.

Security Fix:
Werkzeug's scrypt password hashing was used.

password_hash = generate_password_hash(
    password,
    method="scrypt"
)

Passwords are verified using
check_password_hash().

### 3.3 Cross-Site Scripting (XSS)

Risk: High

Description:
XSS occurs when untrusted content is rendered
as executable browser code.

Impact:
An attacker may execute scripts in another
user's browser.

Security Fix:
Jinja2 automatic HTML escaping is retained.
User-provided content must not be marked safe
or inserted into templates as raw HTML.

### 3.4 Cross-Site Request Forgery (CSRF)

Risk: High

Description:
CSRF tricks an authenticated user's browser
into submitting an unwanted request.

Impact:
Unauthorized actions may be performed using
the user's active session.

Security Fix:
Flask-WTF CSRF protection is enabled.
Forms include CSRF tokens.

### 3.5 Weak Session Management

Risk: Medium

Description:
Improper session configuration can expose
authentication cookies.

Security Fix:
The application uses:
- HttpOnly cookies
- SameSite=Lax
- Secure cookies when HTTPS_ONLY=1
- Session clearing before login and logout

### 3.6 Improper Error Handling

Risk: Medium

Description:
Detailed technical errors can reveal database
structure, file paths, and internal information.

Security Fix:
Generic error messages are returned to users.
Technical exceptions are recorded in server logs.

### 3.7 Input Validation

Risk: Medium

Description:
Unvalidated input may cause unexpected
application behavior.

Security Fix:
- Username length: 3–30 characters
- Username character restrictions
- Password length: 12–128 characters
- Request size limit

## 4. Applied Security Measures

| Security measure | Implementation |
|---|---|
| SQL injection prevention | Parameterized queries |
| Password protection | Scrypt hashing |
| XSS mitigation | Template escaping |
| CSRF prevention | Flask-WTF |
| Session security | Secure cookie settings |
| Input validation | WTForms validators |
| Error handling | Generic messages |
| Secret management | Environment variables |
| Request limits | Maximum request size |

## 5. Testing Strategy

The application should be tested against:

1. Valid user registration.
2. Duplicate username registration.
3. Invalid username input.
4. Weak password submission.
5. Valid login.
6. Invalid login.
7. SQL injection-style input.
8. Missing CSRF token.
9. Unauthorized dashboard access.
10. Logout functionality.

## 6. Conclusion

The project demonstrates how secure coding
practices can reduce common application risks.

Parameterized queries, password hashing,
CSRF protection, input validation, and secure
session configuration improve application
security.

The application should undergo automated
testing and deployment security review before
being used in a production environment.
