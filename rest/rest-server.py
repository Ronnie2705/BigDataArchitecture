from flask import Flask, request, Response, jsonify
from pymongo import MongoClient # you may need to install pymongo
from fake_useragent import UserAgent
import redis
import platform
import os, io
import sys
import jsonpickle
import json
import requests
import pika
from bs4 import BeautifulSoup
import time


# import mysql.connector
from flask_cors import CORS

redisHost= os.getenv("REDIS_HOST") or "localhost"
redisPort= os.getenv("REDIS_PORT") or 6379
REST = os.getenv("REST") or "localhost:5000"



print(f"Connecting to redis({redisHost}:{redisPort})")

redisClient = redis.StrictRedis(host=redisHost, port = redisPort, db=0, decode_responses=True)
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

@app.route('/apiv1/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.users.find_one({'email': email, 'password': password})
    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/apiv1/signup', methods = ['POST'])
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
        result = {"Please fill all the details!"}
        response_pickled = str(jsonpickle.encode(result))
        return Response(response=response_pickled, status=200, mimetype="application/json")

    # Store email and password in MongoDB
    users_collection.insert_one({'email': email, 'password': password, 'firstname':firstname, 'lastname':lastname, 'phoneNumber':phoneNumber})

    result = {"SignUp is complete!"}
    response_pickled = str(jsonpickle.encode(result))
    return Response(response=response_pickled, status=200, mimetype="application/json")
    

def subscribeToRMQ(input_data):
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

    # price_values= priceRange.split('-')

    # #To get price without dollar sign
    # lowPrice = price_values[0][1:]
    # highPrice = price_values[1][1:]

    curr_key= category + " " + lowPrice + " " + highPrice
    log_debug("redis_curr_key:", {curr_key})

    # Check if data exists in redis    
    try:
        log_debug("Fetching the data from redis")            
        redis_data = redisClient.exists(curr_key)

        if(redis_data):
            log_debug("Data is present in redis:", {redis_data})
            print("Data is present in redis:", {redis_data})

            list_of_sorted_products=redisClient.get(curr_key) 
            value = list_of_sorted_products
            
            topFiveProducts=json.loads(value)
            response_pickled = str(jsonpickle.encode(topFiveProducts))
            return Response(response=response_pickled, status=200, mimetype="application/json")
        else:               
            log_debug("Data is not present in redis:", {redis_data})
            print("Data is not present in redis:", {redis_data})

            # Pass the parameters to worker using rabbitmq
            input_data = curr_key
            subscribeToRMQ(input_data)
            time.sleep(5)
        
    except Exception as exp:
        log_debug("Exception raised in log loop:", {str(exp)})
        print(f"Exception raised in log loop: {str(exp)}")
     
    # Fetch the top 5 records based on sentiment score from redis and declaring the key
    # products_with_sentiment_score= "TopFiveProducts"
    log_debug("Fetching the data from redis, based on sentiment score")

    list_of_sorted_products=redisClient.get(curr_key)
    log_debug(f"list_of_sorted_products: ({list_of_sorted_products})")
    value= list_of_sorted_products
    topFiveProducts=json.loads(value)
    log_debug(f"topFiveProducts: ({topFiveProducts})")

    # result = {"action":"Fetching the Data"}
    response_pickled = str(jsonpickle.encode(topFiveProducts))
    return Response(response=response_pickled, status=200, mimetype="application/json")


# Compare the product - Amazon vs Ebay
def helper(amazonLink, ebayLink):
    log_debug("We are in compare function")
    ua=UserAgent()
    hdr = {'User-Agent': ua.random,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    html_amz = requests.get(amazonLink, headers=hdr)
    soup_amz = BeautifulSoup(html_amz.content, 'html.parser')
    a_price = soup_amz.find_all('span', class_ ="a-offscreen")[0]
    amazon_price = a_price.text
    #print('Price: ', amazon_price)

    html_eb = requests.get(ebayLink, headers=hdr)
    soup_eb = BeautifulSoup(html_eb.content, 'html.parser')
    msg = soup_eb.find('span', class_ ="ux-textspans ux-textspans--BOLD")
    if msg.text == 'Seller information':
        ebay_price = soup_eb.find('span', {'itemprop':"price"}).text.strip()[3:]
    else:
        ebay_price = 'The item is no longer available'
    #print('Price: ', ebay_price)
    log_debug(f"Amazon Price: ({amazon_price})")
    log_debug(f"Ebay Price: ({ebay_price})")

    return amazon_price, ebay_price

@app.route('/apiv1/compareProducts', methods=['GET'])
def compareProducts():
    log_debug("We are in test function")
    amazonLink = "https://www.amazon.com/adidas-Ultraboost-Sneaker-White-Black/dp/B07S5K8QDN/ref=sr_1_8?crid=3K2HRUYTZ5VRK&keywords=mens%2Bshoes&qid=1677624404&refinements=p_89%3Aadidas&rnid=2528832011&s=apparel&sprefix=men%2Caps%2C144&sr=1-8&th=1"
    ebayLink = "https://www.ebay.com/itm/354346339494?hash=item5280b00ca6:g:7T8AAOSw9l5jUfrH&amdata=enc%3AAQAHAAAA8ID3w%2BdGpJcT%2BdFSejUG3yokyblYkJSSGkAVbyQeIdqBd8VOHrN%2F4n8jdlkib0yizJwOXOEC5etq0ikY6dGgJ9qWjpV4yaUZTU4gpkEjktEt6UENzvAtqae%2Fa65z0Z2WnieStkJfs4W2SYO182ZcyjH%2F7jpt0P8s5aOBBuRxLBTXFfTkxcuG1aCVFrym%2FEpxuyWCM0r6N0HrPDTs1RGSvzvrSWJugEq5ul0sRAYKGYZrzBm7DNE8sNcC2h%2FkwYS0EDR%2Fz5Lg2AC%2FVsq7TFI%2Bott%2BhltlGeAeYczQXyuumnqaX2g0gHjVhE6KaKGYlw6j3w%3D%3D%7Ctkp%3ABk9SR97yrKPTYQ"
    amazon_price, ebay_price = helper(amazonLink, ebayLink)
    finalPrices= [amazon_price, ebay_price]
    log_debug(f"result: ({finalPrices})")
    response_pickled = str(jsonpickle.encode(finalPrices))
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)