from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "application": "Production Docker App",
        "status": "running"
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/info")
def info():
    return {
        "environment": os.getenv("APP_ENV", "development"),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
