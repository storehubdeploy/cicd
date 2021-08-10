#!/bin/bash

PROFILE=${1:-shbuild}
CLUSTER=${2:-feature-test-env-1}
DEFINITION=${3:-0}
COUNT=${4:-1}
SERVICE=${5:-test}
MIN=${6:-0}

echo "Using aws profile: $PROFILE"
echo "Using ECS cluster: $CLUSTER"
echo "Using definition: $DEFINITION"
echo "Number of task: $COUNT"
echo "Using service: $SERVICE"
echo "Using min: $MIN"

set -e

echo "aws --profile $PROFILE ecs update-service --cluster $CLUSTER --service $SERVICE --task-definition $DEFINITION --deployment-configuration maximumPercent=200,minimumHealthyPercent=$MIN --desired-count $COUNT --force-new-deployment"
aws --profile $PROFILE ecs update-service --cluster $CLUSTER --service $SERVICE --task-definition $DEFINITION --deployment-configuration maximumPercent=200,minimumHealthyPercent=$MIN --desired-count $COUNT --force-new-deployment
