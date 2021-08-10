#!/bin/bash

PROFILE=${1:-shbuild}
CLUSTER=${2:-feature-test-env-1}

echo "Using aws profile: $PROFILE"
echo "Using ECS cluster: $CLUSTER"

set -e

RUNNING_TASK=$(aws --profile $PROFILE ecs list-tasks --cluster $CLUSTER)

if [[ $RUNNING_TASK == *arn:aws:ecs* ]]
then
  echo "Found following task: $TASK"
  TASK=$(echo $RUNNING_TASK | tr '\n' ' ' | cut -d'"' -f 4)
  echo "Stopping task: $TASK"
  aws --profile $PROFILE ecs stop-task --cluster $CLUSTER --task $TASK
else
  echo "no task found in cluster"
  exit 1
fi



