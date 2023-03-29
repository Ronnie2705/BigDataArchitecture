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
    
@app.route('/apiv1/subscribe/<string:name>', methods=['GET'])
def subscribe(name):
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


# # Finds all tracks by artist that has been queried before and is stored in our DB
# # and returns the result to the user if it exists, otherwise let's them know to do
# # a brand new voice query
# @app.route('/apiv1/artist/<string:name>', methods=['GET'])
# def findArtist(name):
#     try:
#         print("Searching for a pre-existing query of ", name)
#         ### SEARCH OUR DATABASE FOR ANY SONG ENTRIES THAT HAVE THAT ARTIST NAME???
#         mydb = mysql.connector.connect(
#         host=mySQLhost,
#         user="root",
#         password="password"
#         )

#         mycursor = mydb.cursor()
#         mycursor.execute("USE spotifydb")
#         query = "SELECT * FROM tracks WHERE artist='{}'".format(name)
#         mycursor.execute(query)
#         # results is a list of the track info: ENTRY ID | NAME | ARTIST | ALBUM | URL
#         results = mycursor.fetchall()
#         if results is None:
#             response = {
#             "No Records": "Nothing matching that query could be found..."
#             }
#         # finalData=[]
#         print("results:----", results)
#         # for idx, track in enumerate(results['tracks']['items']):
#         #     # print for server debugging
#         #     print(idx, track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify'])
#         #     # send back top 10 results to client: NAME | ARTIST NAME | ALBUM NAME | SPOTIFY TRACK URL
#         #     songData[idx] = [track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify']] # Returns the track object but we can access certain values from the dict
#         finalDict=[]
#         for idx in range(len(results)):  
#             dict={}
#             dict['TrackName']=results[idx][1]
#             dict['ArtistName']=results[idx][2] 
#             dict['AlbumName']=results[idx][3]
#             dict['Url']=results[idx][4]
#             finalDict.append(dict)
            
#         # This can be improved by looping over all of the results and returning all of them instead of just the first by indexing the 0th element as follows
#         info = "Songs found by " + name + ": Track Name: " + results[0][1] + ", Artist Name: " + results[0][2] + ", Album Name: " + results[0][3] + ", Spotify URL: " + results[0][4]
#         print(info)
#         # Later on this response could be improved if it were a list instead of a string so it can be worked with efficiently
#         response = {
#         "TrackRecords": finalDict
#         }

#     except Exception as exp:
#         log_debug("Exception in rest-server file:", exp)
#         print("Exception in rest-server file:", exp)
#         response = {}
#         resp_pickled = jsonpickle.encode(response)
#         return Response(response = resp_pickled, status = 404, mimetype = "application/json")

#     # Encoding our response dict into json and returning it
#     resp_pickled = jsonpickle.encode(response)
#     return Response(response = resp_pickled, status = 200, mimetype = "application/json")


# start flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)