from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask API is running!"

@app.route("/db")
def database():
    try:
        connection = mysql.connector.connect(
            host="mysql-day4",
            user="root",
            password="root123",
            database="company"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return f"MySQL connection successful: {result}"

    except Exception as e:
        return f"MySQL connection failed: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
