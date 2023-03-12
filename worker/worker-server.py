import pickle
import platform
import io
import os
import sys
import pika
import redis
import hashlib
import json
import requests
import time
import datetime
import smtplib
import logging
import queue
import threading
import time

hostname = platform.node()

redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())

def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()
rabbitMQChannel.queue_declare(queue='toComputeEngine')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toComputeEngine', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()

    
# log_debug(f"Connecting to redis({redisHost} : {redisPort})")    
# redisClient = redis.StrictRedis(host='redis', port=redisPort, db=0)
# while True:
#     try:
#         print(f"Enter the try block")
        
#     except Exception as exp:
#         log_debug("Exception raised in log loop:", {str(exp)})
#         print(f"Exception raised in log loop: {str(exp)}")
#     sys.stdout.flush()
#     sys.stderr.flush()