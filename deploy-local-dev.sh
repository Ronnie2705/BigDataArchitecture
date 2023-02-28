#!/bin/sh
#
# You can use this script to launch Redis and minio on Kubernetes
# and forward their connections to your local computer. That means
# you can then work on your worker-server.py and rest-server.py
# on your local computer rather than pushing to Kubernetes with each change.
#
# To kill the port-forward processes us e.g. "ps augxww | grep port-forward"
# to identify the processes ids
#
kubectl create namespace bigdata
kubectl config set-context --current --namespace=bigdata

kubectl -n bigdata apply -f redis/redis-deployment.yaml
kubectl -n bigdata apply -f redis/redis-service.yaml

kubectl -n bigdata apply -f rest/rest-deployment.yaml
kubectl -n bigdata apply -f rest/rest-service.yaml
kubectl -n bigdata apply -f rest/rest-ingress.yaml

kubectl -n bigdata apply -f logs/logs-deployment.yaml

kubectl -n bigdata apply -f worker/worker-deployment.yaml

kubectl -n bigdata apply -f mongodb/mongodb-secrets.yaml
kubectl -n bigdata create configmap mongodb-config-file --from-file=conf=mongodb/mongodb.conf
kubectl -n bigdata apply -f mongodb/mongodb-pvc.yaml
kubectl -n bigdata apply -f mongodb/mongodb-service.yaml
kubectl -n bigdata apply -f mongodb/mongodb-deployment.yaml

kubectl port-forward --address 0.0.0.0 service/mongodb 27017:27017

kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
kubectl port-forward --address 0.0.0.0 service/mongodb 27017:27017 &