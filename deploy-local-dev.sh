#!/bin/sh
#
# You can use this script to launch Redis and minio on Kubernetes
# and forward their connections to your local computer. That means
# you can then work on your worker-server.py and rest-server.py
# on your local computer rather than pushing to Kubernetes with each change.
#
# To kill the port-forward processes us e.g. "ps augxww | grep port-forward"
# to identify the processes ids

# Creating a namespace to upload all pods
kubectl create namespace bigdata
kubectl config set-context --current --namespace=bigdata

# redis
kubectl -n bigdata apply -f redis/redis-deployment.yaml
kubectl -n bigdata apply -f redis/redis-service.yaml

#angular
kubectl -n bigdata apply -f BeyondPrice-app/angular-deployment.yaml
kubectl -n bigdata apply -f BeyondPrice-app/angular-service.yaml

# rabbitMq
kubectl -n bigdata apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl -n bigdata apply -f rabbitmq/rabbitmq-service.yaml

# rest
kubectl -n bigdata apply -f rest/rest-deployment.yaml
kubectl -n bigdata apply -f rest/rest-service.yaml
kubectl -n bigdata apply -f rest/rest-ingress.yaml

# logs
kubectl -n bigdata apply -f logs/logs-deployment.yaml

# worker
kubectl -n bigdata apply -f worker/worker-deployment.yaml

# mongodb
# kubectl -n bigdata apply -f mongodb/mongodb-secrets.yaml
# kubectl -n bigdata create configmap mongodb-config-file --from-file=conf=mongodb/mongodb.conf
# kubectl -n bigdata apply -f mongodb/mongodb-pvc.yaml
# kubectl -n bigdata apply -f mongodb/mongodb-service.yaml
# kubectl -n bigdata apply -f mongodb/mongodb-deployment.yaml

# portforwarding 
kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
# kubectl port-forward --address 0.0.0.0 service/mongodb 27017:27017 &
kubectl port-forward service/angular-service 80:90