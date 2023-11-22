#!/bin/bash

minikube status
if [ $? -ne 0 ]
then 
minikube start
fi
eval $(minikube docker-env) 


kubectl delete -k kubernetes/backend/



docker build services/provider_manager/ -t providermanager:latest
docker build services/hash_calculator/ -t hashcalculator:latest
docker build services/searcher_simulator/ -t searchersimulator:latest
docker build services/reprocessor/ -t reprocessor:latest
docker build services/flight_cache -t flightcache:latest
docker build services/pricer -t pricer:latest

kubectl apply -k kubernetes/backend/
kubectl port-forward providermanagerpod 81:81

minikube dashboard