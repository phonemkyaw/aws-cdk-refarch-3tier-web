import os
from flask import Flask, request
from rediscluster import RedisCluster


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/api/')
def api():
    return "0.2"

@app.route('/api/redis', methods=["GET", "POST"])
def api_v1():
    host = os.environ.get("REDIS_ENDPOINT")
    client = RedisCluster(startup_nodes=[dict(host=host, port=6379)], decode_responses=True, skip_full_coverage_check=True)

    if request.method == "POST":
        client.set("data", request.json["data"])
        return "Successful"
    elif request.method == "GET":
        return client.get("data")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)