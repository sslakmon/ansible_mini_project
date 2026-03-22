import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

"""
we use the os in order to read the environment variable 
These values are injected by docker-compose 
"""
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "usersdb")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")


def get_connection():
    """
    Creates and returns a new PostgreSQL connection.
    A new connection is opened for each request.
    """
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    """
    Creates the 'users' table if it does not already exist.
    This ensures the application can run even on a fresh database.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/users", methods=["GET"])
def get_users():
    """
    Returns all users from the database.
    Only id, username, and email are returned (password is excluded).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [
        {"id": r[0], "username": r[1], "email": r[2]}
        for r in rows
    ]
    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    """
    Creates a new user.
    Expects JSON body with: username, email, password.
    Example:
    {
        "username": "shlomo",
        "email": "shlomo@example.com",
        "password": "1234"
    }
    """
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate required fields
    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id;",
        (username, email, password)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "username": username, "email": email}), 201


@app.route("/", methods=["GET"])
def health():
    """
    Simple health-check endpoint to verify the app is running.
    """
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Initialize the database table when running locally
    init_db()
    app.run(host="0.0.0.0", port=5000)
