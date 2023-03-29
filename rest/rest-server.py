from flask import Flask, request, Response
import redis
import platform
import os, io
import sys
import jsonpickle
import json
import base64
import pika
import pickle

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


# We need this default route since Google Kubernetes Engine checks for the health of our services(if we deploy to the cloud)
@app.route('/', methods=['GET'])
def hello():
    return '<h1> Welcome to Voice-based music search service</h1><p> Use a valid endpoint </p>'



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
        else:               
            log_debug("Data is not present in redis:", {redis_data})
            print("Data is not present in redis:", {redis_data})

            # Pass the parameters to worker using rabbitmq
            input_data = curr_key
            subscribeToRMQ(input_data)
        
    except Exception as exp:
        log_debug("Exception raised in log loop:", {str(exp)})
        print(f"Exception raised in log loop: {str(exp)}")
     
    # Fetch the top 5 records based on sentiment score from redis and declaring the key
    products_with_sentiment_score= "TopFiveProducts"
    log_debug("Fetching the data from redis, based on sentiment score")

    list_of_sorted_products=redisClient.blpop(products_with_sentiment_score, timeout=0)
    
    value= list_of_sorted_products[1].decode()
    
    topFiveProducts=json.loads(value)
    log_debug(f"topFiveProducts: ({topFiveProducts})")

    # result = {"action":"Fetching the Data"}
    response_pickled = str(jsonpickle.encode(topFiveProducts))
    return Response(response=response_pickled, status=200, mimetype="application/json")

# # This route does a voice search for songs and returns it to the user
# # then adds the query data to our database and uploads any query related
# # images and thumbnails to our bucket in GCP
# @app.route('/apiv1/voice', methods=['POST'])
# def voice_search():
#     print("Welcome to voice api")

#     # Request should contain the voice data in a .wav or similar format
#     try:
#         # data = request.get_json()
#         # d=str(data)
#         data = request.headers['FileName']
#         print("data 1:", data)
#         # print("data 2 :", request.data)
#         # print("request.get_json() :",request.get_json())
#         # print("d:",d.split("=",1)[1])
#         # formattedString=d.split("base64,",1)[1]
#         # p=formattedString.split("'",1)[0]
#         # print("p:",p)
#         # decoded_song = base64.decodebytes(p.encode('utf-8'))
#         # print("data:", type(decoded_song))
#         # print("decoded_song:", (decoded_song))
#         # decoded_song = base64.b64decode(data)
#         # file_name = io.BytesIO(decoded_song)

#         # rec is our speech recognizer
#         recog = sr.Recognizer()
#         audio_file = sr.AudioFile(io.BytesIO(request.data))
#         with audio_file as source:
#             audio = recog.record(source)

#         sentence = recog.recognize_google(audio)
#         log_debug("sentence:", sentence)
       
#         print("The user's query turned into text:", sentence)
        
#         ### SPOTIFY API CALL TO MAKE A SEARCH FOR KEYWORDS IN THAT SENTENCE STRING ###
#         songData = {}
#         sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientKey,
#                                                            client_secret=clientSecret))
#         print("sp object:", sp)

#         results = sp.search(q=sentence, limit=10, type='track')
 
#         ### SPOTIFY API CALL, INCLUDING LOADING THE QUERY RESPONSE DATA INTO OUR MYSQL DB TABLE(S)
#         for idx, track in enumerate(results['tracks']['items']):
#             # print for server debugging
#             print(idx, track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify'])
#             # send back top 10 results to client: NAME | ARTIST NAME | ALBUM NAME | SPOTIFY TRACK URL
#             songData[idx] = [track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify']] # Returns the track object but we can access certain values from the dict
   
#         #Sending song data to redis
#         redisClient.lpush(songWorker,json.dumps(songData))
#         log_debug("Adding sentence to redis")

#     except Exception as exp:
#         log_debug("Exception in rest-server file:", exp)
#         print("Exception in rest-server file:", exp)
#         response = {}
#         resp_pickled = jsonpickle.encode(response)
#         return Response(response = resp_pickled, status = 404, mimetype = "application/json")


#     # Encoding our response dict into json and returning it
#     resp_pickled = jsonpickle.encode(songData)
#     return Response(response = resp_pickled, status = 200, mimetype = "application/json")

# start flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
