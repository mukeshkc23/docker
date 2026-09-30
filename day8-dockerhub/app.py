from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from Docker Hub - version 2!"


@app.route("/version")
def version():
    return {
        "application": "Docker Hub Demo",
        "version": "1.0"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
