# Music Separation Worker

The steps you need to take:

+ Develop a Python program that listens to the `toWorkers` redis key exchange, receives a message and retrieves the MP3 song to separate.

## Creating a worker-server.py
In this file, we will fetch the song data from redis queue continously for every request made by user.
We will create a function that handles mysql database and table creation and store the data into it.

## Program to do Music Source Separation

You'll need a single Redis list data type to send data to the worker & another for logging. Redis uses numerical database numbers and number 0 is the default database. Each database is a "key-value" store meaning you can specify different keys for the worker queue (`toWorker` is a good key) and logging (`logging`).

You can use whatever method you like to get data from the REST API to the worker; my solution just sends JSON strings through the Redis queue.

Rather than send the large MP3 files through Redis, I suggest using the Min.io object storage system (or other object store) to store the song contents; see the [nodes in the overall README](../README.md).

If the `toWorker` request indicates that a *webhook callback* should be used, you should issue an HTTP POST request passing in the payload portion of the callback. You [can use the Python requests library](https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request) to make that request. You don't need to do anything if the request fails, but you should be aware the request may fail.


## Debugging Support

At each step of your processing, you should log debug information using the logging infrastructure documented in [the logging directory](../logs/README).

When installing the `redis` library used to communicate with `redis`, you should use the `pip` or `pip3` command to install the packages.
```
sudo pip3 install --upgrade minio redis requests
```

## Suggested Development Steps

When you actually run the text classifier, the existing 2.5GByte model will be downloaded from Germany. If you do this in a container or pod, this model will be repeatedly downloaded. This takes a while and it slows down your debug-edit cycle. If you do this on your laptop instead of in a container the downloaded model will be saved in your home directory.

Thus, we recommend that:
* Deploy Redis and Min.io and the use the `kubectl port-forward` mechanism listed in the [corresponding README.md](../redis/README.md) file to expose those services on your local machine. We've [provided a script `deploy-local-dev.sh`](../deploy-local-dev.sh) for that purpose.
* Now that you are port-forwarding during development, you can run `worker-server.py` on your laptop and it will find the Redis/Minio ports on the localhost. 
* But, when you deploy your solution in Kubernetes, you'll need to tell `worker-server.py` what hosts to use when deployed; this should be done using environment variables in the deployment specification.
* Use the provided `log_info` and `log_debug` routines that write to the `logs` topic to simplify your development. You won't be able to figure out what is going on without logs. We've provided template code for that.

Lastly, you should construct a program to send a sample request to your worker. We've [included one in send-request.py](./send-request.py) that uses the message format that my solution uses.

Following this process, you can debug the use of the `demucs` library and the interface to redis and minio. Once you have a functioning `worker-server.py` you can set it up in Kubernetes using a deployment.
