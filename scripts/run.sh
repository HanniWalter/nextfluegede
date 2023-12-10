#!/bin/bash

minikube status
if [ $? -ne 0 ]
then 
minikube start
fi



kubectl delete -k kubernetes/backend/
#kubectl delete -k kubernetes/test/


docker build services/provider_manager/ -t providermanager:latest
docker build services/hash_calculator/ -t hashcalculator:latest
docker build services/searcher_simulator2/ -t searchersimulator2:latest
docker build services/searcher_simulator3/ -t searchersimulator3:latest
docker build services/searcher_simulator/ -t searchersimulator:latest
docker build services/reprocessor/ -t reprocessor:latest
docker build services/flight_cache -t flightcache:latest
docker build services/pricer -t pricer:latest
docker build services/searchagent -t searchagent:latest
docker build services/searchagent_callback -t searchagentcallback:latest

docker build services/website -t website:latest



kubectl apply -k kubernetes/backend/
#kubectl apply -k kubernetes/test/
#kubectl port-forward providermanagerpod 81:81

minikube dashboard
