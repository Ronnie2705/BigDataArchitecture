# BigDataArchitecture (Beyond Price)


# For GKE Deployment
# Following are the steps involved in setting up the Gcloud environment and deployment over the Google Cloud Platform(using GKE)
# For reference: https://github.com/cu-csci-4253-datacenter/kubernetes-tutorial/tree/master/07-guestbook-on-gke

# Deployment setup:
create an account and project on gcp and save its projectid 
install gcloud sdk on local machine

# To create cluster on gcp, run following commands:

# Run once to make your ip address static, so that every time you deploy on gcp you get same ip address
gcloud compute addresses create global-ip --global

gcloud init- for authorization

gcloud config set compute/zone us-central1-b

gcloud container clusters create mykube --preemptible --release-channel None --zone us-central1-b (mykube is your cluster name)

gcloud container clusters get-credentials mykube 

kubectl get nodes

gcloud container clusters update mykube --update-addons=HttpLoadBalancing=ENABLED

gcloud components install gke-gcloud-auth-plugin

kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user $(gcloud config get-value account)

# deploy your ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml

# deploy all pods, services, and ingress

sh .\deploy-gke-dev.sh

kubectl get pods

# Once you've created the load-balancer, you can find the IP address using *e.g.*
```
kubectl get ingress frontend-ingress --output yaml

# delete your cluster
gcloud container clusters delete mykube

# To see external ip address in your angular pod
kubectl get svc

# Presentation for whole setup of this project
https://docs.google.com/presentation/d/1ER9J-tPlghq3FXPQrMDk_fNXqd8zatYyNM-LHwZ7_2c/edit#slide=id.g2148cd7d853_0_47

