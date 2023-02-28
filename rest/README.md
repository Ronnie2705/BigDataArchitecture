# REST API and interface

You must create a rest-server deployment, service and ingress that makes the specified REST api externally available.

You must provide a `rest-server.py` that implements a Flask server that responds to the routes below. 
We have provided example REST API queries implemented in Python in `rest-client.py` `. Use the short data during development.

The REST routes are:
+ /apiv1/voice[POST] - accept the wav file as an input.
Use speech recognition class to convert audio into sentence and then use Spotify api to make search for keywords present in the sentence.
After obtaining the song data, pass it to redis queue to be used by worker.

+ /apiv1/artist/<string:name>[GET] - retrieve the song data based on the imput(either song name or artist name) provided by user from front-end. After fetching the records from mysql database, pass the json response to front-end table to be shown.


Sample queries using the Python `requests` API are in `rest-client.py`. Refer to those examples for input format.


### Development Steps
You'll need a single Redis list data type to send data to the worker & another for logging. Redis uses numerical database numbers and number 0 is the default database. Each database is a "key-value" store meaning you can specify different keys for the worker queue (`toWorker` is a good key) and logging (`logging`).

You should use the `pip` or `pip3` command to install the packages in your container. The solution code uses the following packages:
```
sudo pip3 install --upgrade redis jsonpickle requests flask
```

## Deploying an ingress

You'll need to expose your REST service using an ingress.

### Deploy an `ingress` to publish our web server

Although an ingress is a standard Kubernetes network component, the specific implementation depends on the Kubernetes system you're using.  Once you've developed your service, you should deploy it on Google Container Engine (GKE). The steps to create a "ingress" on GKE are slightly different than the steps for the stand-alone Kubernetes development environment [discussed in the Kubernetes tutorial](https://github.com/cu-csci-4253-datacenter/kubernetes-tutorial/tree/master/05-guestbook). In that example, you [install an ingress extension based on nginx](https://kubernetes.github.io/ingress-nginx/deploy/#docker-for-mac) and then configure the ingress to forward from the host IP address to the specific service you want to access. 

Because we are sending large data through the REST API you will need to add an ["annotation" to the ingress](https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md) to configure it to accept large request:
```
nginx.ingress.kubernetes.io/proxy-body-size: 16m
```

See the [Kubernetes tutorial README](https://github.com/cu-csci-4253-datacenter/kubernetes-tutorial) for details on deploying to GKE.

### Using a GKE load balancer

For GKE, you [can use a "load balancer" as the ingress as described in this tutorial](https://cloud.google.com/kubernetes-engine/docs/how-to/load-balance-ingress#gcloud). In general, Google's load balancer can accept connections across multiple datacenters and direct them to your Kubernetes cluster. You first need to enable the load balancer functionality (assuming your cluster is named `mykube`) using:
```
gcloud container clusters update mykube --update-addons=HttpLoadBalancing=ENABLED
```

You can then use [create an ingress that directs web connections to your rest-service using the example from the tutorial](https://cloud.google.com/kubernetes-engine/docs/how-to/load-balance-ingress#creating_an_ingress). The main difference is that you need to specify:
```
  annotations:
    kubernetes.io/ingress.class: "gce"
```

The GKE load balancer [needs your service to use a specific kind of service called a `NodePort`](https://cloud.google.com/kubernetes-engine/docs/how-to/load-balance-ingress#creating_a_service). You can add that to your service spec by putting
```
spec:
  type: NodePort
```
in the service YAML file and restarting your service.

In addition, the GKE load balancer checks for the "health" of your service -- this means that you need to respond to requests to `/` with a positive response. I added the following route:
```
@app.route('/', methods=['GET'])
def hello():
    return '<h1>Welcome to Voice-based music search service</h1><p> Use a valid endpoint </p>'
```

Once you've created the load-balancer, you can find the IP address using *e.g.*
```
kubectl get ingress rest-ingress --output yaml
```
and then access the endpoint using the IP address at the end of the output. It should look like:
```
....
status:
  loadBalancer:
    ingress:
    - ip: 34.120.45.70
```
You can check if things are working by sending requests and looking at the output of your `logs` pod or the response you get.

If you have trouble getting your service to work, use
```
kubectl describe ingress rest-ingress
```
and you'll see error messages and diagnostics like this:
```
> kubectl describe ingress rest-ingress
Name:             rest-ingress
Namespace:        default
Address:          34.120.45.70
Default backend:  default-http-backend:80 (10.0.0.9:8080)
Rules:
  Host        Path  Backends
  ----        ----  --------
  *           
              /hello   hello-world:60000 (10.0.0.10:50000,10.0.1.7:50000,10.0.2.7:50000)
              /*       rest-service:5000 (10.0.2.15:5000)
Annotations:  ingress.kubernetes.io/backends:
                {"k8s-be-30496--28fa4eee16792bba":"HEALTHY","k8s-be-30815--28fa4eee16792bba":"HEALTHY","k8s-be-30914--28fa4eee16792bba":"HEALTHY"}
              ingress.kubernetes.io/forwarding-rule: k8s2-fr-pxfi3hd8-default-rest-ingress-zo9uwq5a
              ingress.kubernetes.io/target-proxy: k8s2-tp-pxfi3hd8-default-rest-ingress-zo9uwq5a
              ingress.kubernetes.io/url-map: k8s2-um-pxfi3hd8-default-rest-ingress-zo9uwq5a
              kubernetes.io/ingress.class: gce
Events:
  Type    Reason  Age   From                     Message
  ----    ------  ----  ----                     -------
  Normal  ADD     46m   loadbalancer-controller  default/rest-ingress
  Normal  CREATE  45m   loadbalancer-controller  ip: 34.120.45.70
```
It can take a while for the status of the connections to switch from "Unknown" to "HEALTHY". If that isn't happening, check that you've added the `/` route to your Flask server and try connecting to the IP address.

If you can't get this to work, just use your local Kubernetes setup during your grading interview.
