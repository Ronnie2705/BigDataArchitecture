from flask import Flask, request, Response
import redis
import platform
import os, io
import sys
import jsonpickle
import json
import base64
import pika

# import mysql.connector
from flask_cors import CORS

redisHost= os.getenv("REDIS_HOST") or "localhost"
redisPort= os.getenv("REDIS_PORT") or 6379
REST = os.getenv("REST") or "localhost:5000"

# clientKey = os.getenv("SPOTIFY_CLIENT_ID") or "e0562ed50444401b834de3180171af02"
# clientSecret = os.getenv("SPOTIFY_CLIENT_SECRET") or "146de64b5b3c4751ad14aef744415aa0"

print(f"Connecting to redis({redisHost}:{redisPort})")

redisClient = redis.StrictRedis(host=redisHost, port = redisPort, db=0)
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())

# Debugging functions
def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")

    
# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
log_debug("Creating Rest front-end")


# We need this default route since Google Kubernetes Engine checks for the health of our services(if we deploy to the cloud)
@app.route('/', methods=['GET'])
def hello():
    return '<h1> Welcome to Voice-based music search service</h1><p> Use a valid endpoint </p>'


@app.route('/apiv1/subscribe/<string:name>', methods=['GET'])
def subscribe(name):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toComputeEngine')
    print("got a request to subscribe for the api from user with name " + name)
    message = name
    rabbitMQChannel.basic_publish(exchange='',routing_key='toComputeEngine', body=message)
    rabbitMQChannel.close()
    rabbitMQ.close()
    result = {"action":"queued"}
    response_pickled = jsonpickle.encode(result)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
