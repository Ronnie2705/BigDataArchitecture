from flask import Flask, request, Response, jsonify
from pymongo import MongoClient # you may need to install pymongo
from bson.json_util import dumps
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

# Connect with Pymongo​
client = MongoClient('mongodb+srv://SwapnilSethi:La6r8Stu9AGqJbr@mongodbclusterforbdapro.4re5jyl.mongodb.net/test')
db = client["BeyondPrice"]
users_collection = db["UserData"]

# We need this default route since Google Kubernetes Engine checks for the health of our services(if we deploy to the cloud)
@app.route('/', methods=['GET'])
def hello():
    return '<h1> Welcome to Voice-based music search service</h1><p> Use a valid endpoint </p>'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.users.find_one({'username': username, 'password': password})
    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/apiv1/signin', methods = ['POST'])
def signup():
      data = request.json
      print(data)
      firstname =data['firstName']
      lastname =data['lastName']
      email = data['email']
      phoneNumber = data['phoneNumber']
      password = data['password']

      # Validate email and password
      if not email or not password or not firstname or not lastname or not phoneNumber:
        return {'message': 'Email and password are required'}, 400

      # Store email and password in MongoDB
      users_collection.insert_one({'email': email, 'password': password, 'firstname':firstname, 'lastname':lastname, 'phoneNumber':phoneNumber})
 
      return {'message': 'Signup successful'}, 201
    
#@app.route('/apiv1/subscribe/<string:name>', methods=['GET'])
def subscribe(input_data):
    log_debug("Input Data:", {input_data})
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='FetchData')
    print("got a request to subscribe for the api from user with data " + input_data)
    message = input_data
    rabbitMQChannel.basic_publish(exchange='',routing_key='FetchData', body=message)
    log_debug("Status:", "Process is in RabbitMQ")
    rabbitMQChannel.close()
    rabbitMQ.close()
    # result = {"action":"queued"}
    # response_pickled = jsonpickle.encode(result)
    # return Response(response=response_pickled, status=200, mimetype="application/json")

# Fetch top 10 products based upon user choice and price range
@app.route('/apiv1/fetchData/<string:category>/<string:lowPrice>/<string:highPrice>', methods=['GET'])
def fetchData(category, lowPrice, highPrice):
    redis_curr_key= category + " " + lowPrice + " " + highPrice
    log_debug("redis_curr_key:", {redis_curr_key})

    # Check if data exists in redis    
    try:
        log_debug("Fetching the data from redis")            
        redis_data = redisClient.exists(redis_curr_key)
        if(redis_data):
            log_debug("Data is present in redis:", {redis_data})
            print("Data is present in redis:", {redis_data})
        else:               
            log_debug("Data is not present in redis:", {redis_data})
            print("Data is not present in redis:", {redis_data})

            # Pass the parameters to worker using rabbitmq
            input_data = redis_curr_key
            subscribe(input_data)

        
    except Exception as exp:
        log_debug("Exception raised in log loop:", {str(exp)})
        print(f"Exception raised in log loop: {str(exp)}")


    

    

    # Fetch the top 10 records from redis

    
    result = {"action":"Fetching the Data"}
    response_pickled = jsonpickle.encode(result)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)