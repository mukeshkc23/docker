from flask import Flask, jsonify
import mysql.connector
import redis
import json

app = Flask(__name__)

# MySQL configuration
db_config = {
    "host": "day5-mysql",
    "user": "root",
    "password": "root123",
    "database": "company"
}

# Redis connection
cache = redis.Redis(
    host="day5-redis",
    port=6379,
    decode_responses=True
)


@app.route("/")
def home():
    return "Flask + MySQL + Redis is running!"


@app.route("/employees")
def employees():

    # Check Redis first
    cached_data = cache.get("employees")

    if cached_data:
        print("CACHE HIT")
        return jsonify({
            "source": "redis",
            "data": json.loads(cached_data)
        })

    print("CACHE MISS")

    # Connect to MySQL
    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    # Store result in Redis
    cache.setex(
        "employees",
        60,
        json.dumps(result)
    )

    return jsonify({
        "source": "mysql",
        "data": result
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
