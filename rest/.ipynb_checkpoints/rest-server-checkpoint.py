from flask import Flask, request, Response
import redis
import json
import platform
import pickle
import base64, requests
import os, io, glob
import sys
import jsonpickle
from minio import Minio
import random, string

redisHost= os.getenv("REDIS_HOST") or "localhost"
redisPort= os.getenv("REDIS_PORT") or 6379

minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPassword = os.getenv("MINIO_PASSWD") or "rootpass123"


queueBucketName= "queue"
outputBucketName="output"

workerQueue="toWorker"

print(f"Connecting to redis({redisHost}:{redisPort})")

redisClient = redis.StrictRedis(host=redisHost, port = redisPort, db=0)
minioClient = Minio(minioHost,access_key=minioUser,secret_key=minioPassword, secure=False)

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())

# Initialize the Flask application
app = Flask(__name__)
log_debug("Creating Rest front-end")


def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")


def getBucketObjectNames(bucket, recursive=False):
    try:
        log_debug(f"get contents of {bucket}")
        if minioClient.bucket_exists(bucket):
            contents= [_x.object_name for x in minioClient.list_objects(bucket, recursive=recursive)]
        else:
            contents=[]

    except Exception as exp:
        print(f"error in getBucketObjectNames({bucket})")
        contents = []
        log_info(f"error in getBucketObjectNames => exception {exp}")
    return contents

@app.route('/')
def root():
    return "<p>Music Separation as a Service!</p>"

@app.route('/apiv1/queue', methods=['GET'])
def queue():
    status=200
    contents = getBucketObjectNames(queueBucketName)
    log_debug(f"contents are {contents}")
    responce_pickled= jsonpickle.encode({"queue": contents})
    log_info(f"/queue => {responce_pickled}")
    return Response(response=responce_pickled, status=status, mimetype="application/json")

def removeSongHashRecursive(songHash):
    log_debug(f"removeSongHashRecursive({songHash})")

    if minioClient.bucket_exists(outputBucketName):
        contents= getBucketObjectNames(outputBucketName, recursive=True)
        log_debug(f"removeSongHashRecursive : contents are ({contents})")
        for content in contents:
            if content.startswith(songHash):
                log_debug(f"removeSongHashRecursive : Remove ({content}) from ({outputBucketName})")
                minioClient.remove_bucket(outputBucketName, content)


@app.route('/apiv1/remove/<string:songhash>/<string:track>', methods=['GET'])
def remove(songhash, track):
    status = 200

    if track not in ["bass","drums","vocal", "other"]:
        return Response(response=jsonpickle.encode({"response": f"Track type {track} unknown"}), status=400, mimetype="application/json")
    
    if not minioClient.bucket_exists(outputBucketName):
        log_debug(f"output bucket {outputBucketName} does not exist")
        status = 400
        response="Output bucket doesn't exist"

    else:
        objectName= f"{songhash}/{track}.mp3"
        log_debug(f"Remove {songhash}/{track}.mp3 from {outputBucketName}")
        try:
            minioClient.remove_bucket(outputBucketName, objectName)
            log_debug(f"Removed {songhash}/{track}.mp3 from {outputBucketName}")
            return Response(response=jsonpickle.encode({"response": f"Removed track {track} from {songhash}"}), status=400, mimetype="application/json")
        except Exception as exp:
            print(f"error in remove ({songhash}), ({track})")
            log_info(f"error in getBucketObjectNames => exception {exp}")


@app.route('/apiv1/remove/<string:songhash>/<string:track>', methods=['GET'])
def getTrack(songhash, track):
    log_debug(f"Retrieve track {track}.mp3 from {outputBucketName}")

    if track not in ["bass","drums","vocal", "other"]:
        return Response(response=jsonpickle.encode({"response": f"Track type {track} unknown"}), status=400, mimetype="application/json")
    
    if not minioClient.bucket_exists(outputBucketName):
        log_debug(f"output bucket {outputBucketName} does not exist")
        status = 400
        response="Output bucket doesn't exist"

    else:
        objectName= f"{songhash}/{track}.mp3"

        try:
            log_debug(f"Retrieve {objectName} from {outputBucketName}")
            try:
                resp= minioClient.get_object(outputBucketName,objectName)
                bytes= io.BytesIO(resp.data)
            finally:
                resp.close()
                resp.release_conn()
            log_debug(f"Send bytes as {songhash} - {track}.mp3")    
        except Exception as exp:
            print(f"error in retrieving ({songhash}), ({track})")
            log_info(f"error in getTrack => exception {exp}")


@app.route('/apiv1/separate', methods=['POST'])
def separateTracks():    
    songhash= ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    print(songhash)
    
    


def initialize():
    for mp3 in glob.glob("data/short*mp3"):
        print(f"Separate data/{mp3}")
        mkReq(requests.post, "apiv1/separate",
            data={
                "mp3": base64.b64encode( open(mp3, "rb").read() ).decode('utf-8'),
                "callback": {
                    "url": "http://localhost:5000",
                    "data": {"mp3": mp3, 
                            "data": "to be returned"}
                }
            },
            verbose=True
            )
        print(f"Cache from server is")
        mkReq(requests.get, "apiv1/queue", data=None)

def mkReq(reqmethod, endpoint, data, verbose=True):
    print(f"Response to http://{REST}/{endpoint} request is {type(data)}")
    jsonData = jsonpickle.encode(data)
    if verbose and data != None:
        print(f"Make request http://{REST}/{endpoint} with json {data.keys()}")
        print(f"mp3 is of type {type(data['mp3'])} and length {len(data['mp3'])} ")
    response = reqmethod(f"http://{REST}/{endpoint}", data=jsonData,
                         headers={'Content-type': 'application/json'})
    if response.status_code == 200:
        jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
        print(jsonResponse)
        return
    else:
        print(
            f"response code is {response.status_code}, raw response is {response.text}")
        return response.text

# start flask app
#app.run(host="0.0.0.0", port=5000)