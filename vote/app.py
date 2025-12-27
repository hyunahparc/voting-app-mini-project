from flask import Flask, render_template, request, make_response
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(Flask, 'redis'):
        redis_host = os.environ.get("REDIS_HOST", "redis")  # localhost -> redis
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        
        redis_password = None
        password_file = os.environ.get("REDIS_PASSWORD_FILE")

        if password_file and os.path.exists(password_file):
            with open(password_file) as f:
                redis_password = f.read().strip()

        Flask.redis = Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=0,
            socket_timeout=5
        )
    return Flask.redis

@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
