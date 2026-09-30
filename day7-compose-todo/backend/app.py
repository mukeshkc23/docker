from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root123"),
        database=os.getenv("DB_NAME", "todo_db")
    )


def initialize_database():

    for attempt in range(10):

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    task VARCHAR(255) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE
                )
            """)

            connection.commit()

            cursor.close()
            connection.close()

            print("Database initialized successfully")
            return

        except Exception as e:

            print(f"Database not ready: {e}")
            time.sleep(3)

    raise Exception("Could not connect to database")


@app.route("/")
def home():
    return "Todo API V2 is running!"


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/todos", methods=["GET"])
def get_todos():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM todos")

    todos = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(todos)


@app.route("/todos", methods=["POST"])
def create_todo():

    data = request.get_json()

    task = data.get("task")

    if not task:
        return jsonify({
            "error": "task is required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO todos (task) VALUES (%s)",
        (task,)
    )

    connection.commit()

    todo_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "id": todo_id,
        "task": task,
        "completed": False
    }), 201


if __name__ == "__main__":

    initialize_database()

    app.run(
        host="0.0.0.0",
        port=5000
    )

