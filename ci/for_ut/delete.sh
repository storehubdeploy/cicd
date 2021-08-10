#!/bin/sh
project=$1
docker rm -f $(docker ps|grep $project|awk '{print $1}'|sed ':t;N;s/\n/ /;b t')
docker volume prune -f
