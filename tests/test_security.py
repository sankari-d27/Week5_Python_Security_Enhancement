
import os
os.environ.setdefault("TESTING", "1")

import pytest
from app import app, initialize_database


@pytest.fixture
def client(tmp_path):
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        DATABASE=str(tmp_path / "test.db"),
        SECRET_KEY="test-secret"
    )

    initialize_database()

    with app.test_client() as client:
        yield client


def register_user(client, username="testuser",
                  password="StrongPassword123!"):
    return client.post(
        "/register",
        data={
            "username": username,
            "password": password
        },
        follow_redirects=True
    )


def login_user(client, username="testuser",
               password="StrongPassword123!"):
    return client.post(
        "/login",
        data={
            "username": username,
            "password": password
        },
        follow_redirects=True
    )


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_successful_registration(client):
    response = register_user(client)
    assert response.status_code == 200
    assert b"Registration successful" in response.data


def test_duplicate_registration(client):
    register_user(client)
    response = register_user(client)

    assert b"Unable to create account" in response.data


def test_weak_password_rejected(client):
    response = register_user(
        client,
        password="123"
    )

    assert b"Registration successful" not in response.data


def test_invalid_username_rejected(client):
    response = register_user(
        client,
        username="<script>alert(1)</script>"
    )

    assert b"Registration successful" not in response.data


def test_successful_login(client):
    register_user(client)
    response = login_user(client)

    assert response.status_code == 200
    assert b"Welcome back," in response.data
    assert b"testuser" in response.data


def test_invalid_login(client):
    response = login_user(
        client,
        password="WrongPassword123!"
    )

    assert b"Invalid username or password" in response.data


def test_sql_injection_input(client):
    register_user(client)

    response = login_user(
        client,
        username="' OR '1'='1"
    )

    assert b"Invalid username or password" in response.data
    assert b"Welcome, testuser" not in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.location


def test_logout(client):
    register_user(client)
    login_user(client)

    response = client.post("/logout")

    assert response.status_code == 302

    response = client.get("/dashboard")
    assert response.status_code == 302


def test_csrf_protection(client):
    app.config["WTF_CSRF_ENABLED"] = True

    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "StrongPassword123!"
        }
    )

    assert response.status_code == 400
