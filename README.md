
# Week 5 Security Enhancement Project

## Project Overview

A secure Python Flask application designed to
demonstrate common security enhancements.

## Requirements

- Python 3.10 or later
- pip
- Flask
- SQLite

## Installation

1. Extract the project ZIP file.
2. Open a terminal in the project directory.
3. Create a virtual environment.

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

4. Install dependencies:

pip install -r requirements.txt

5. Configure the application secret.

Copy .env.example to .env.
Generate a secret with:

python -c "import secrets; print(secrets.token_hex(32))"

Set SECRET_KEY to the generated value.

Load environment variables before starting
the application, for example using python-dotenv
or your operating system's environment settings.

6. Start the application:

python -c "from app import initialize_database; initialize_database()"
python app.py

7. Open your browser:

http://127.0.0.1:5000

## Run Automated Tests

pytest -v

## Run Static Security Analysis

bandit -r app.py -ll

## Security Features

- Parameterized SQL queries
- Password hashing using scrypt
- CSRF protection
- Input validation
- Secure session cookies
- Safe error messages
- Environment-based secrets

## Important

This is an educational project.
Before production deployment, add login rate
limiting, HTTPS, security headers, production
logging controls, and backup procedures.
