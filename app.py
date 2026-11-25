import os
import re
import sqlite3
import logging
from pathlib import Path
from functools import wraps

from dotenv import load_dotenv

load_dotenv()


from flask import (
    Flask, render_template, redirect, url_for,
    flash, session, g, abort
)
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Regexp
)
from werkzeug.security import generate_password_hash, check_password_hash


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

secret = os.environ.get("SECRET_KEY")
if not secret and os.environ.get("TESTING") != "1":
    raise RuntimeError("SECRET_KEY must be configured.")

app.config.update(
    SECRET_KEY=secret or "test-only-secret",
    DATABASE=os.environ.get(
        "DATABASE_PATH", str(INSTANCE_DIR / "users.db")
    ),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.environ.get("HTTPS_ONLY") == "1",
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_REFRESH_EACH_REQUEST=True,
    MAX_CONTENT_LENGTH=16 * 1024,
)

csrf = CSRFProtect(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------- DATABASE ----------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def initialize_database():
    with sqlite3.connect(app.config["DATABASE"]) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()


# ---------------- FORMS ----------------

class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-z0-9_]+$",
                message="Use letters, numbers, and underscores only."
            )
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=12, max=128)
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=30)]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(max=128)]
    )

    submit = SubmitField("Login")


# ---------------- AUTHENTICATION ----------------

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        password_hash = generate_password_hash(
            password,
            method="scrypt"
        )

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            db.commit()

            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Unable to create account with those details.")
        except sqlite3.Error:
            logger.exception("Database error during registration.")
            abort(500)

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        try:
            user = get_db().execute(
                "SELECT id, username, password_hash "
                "FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if user and check_password_hash(
                user["password_hash"], password
            ):
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]

                return redirect(url_for("dashboard"))

            flash("Invalid username or password.")

        except sqlite3.Error:
            logger.exception("Database error during login.")
            abort(500)

    return render_template("login.html", form=form)


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username")
    )


# ---------------- LOGOUT ----------------

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))


# ---------------- ERROR HANDLING ----------------

@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", message="Invalid request."), 400


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", message="Page not found."), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error("Internal server error.")
    return render_template(
        "error.html",
        message="An unexpected error occurred."
    ), 500


if __name__ == "__main__":
    initialize_database()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
