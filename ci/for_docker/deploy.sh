#!/bin/bash

die() {
    echo -e "\033[1;31m>>> $@ \033[0m"
    exit 1
}

black() {
    echo -e "\033[1;30m$@ \033[0m"
}

green() {
    echo -e "\033[1;32m$@ \033[0m"
}

while [ "$1" ]; do
    case "$1" in
    --app)
            shift;
            app="$1";
            ;;
    --env)
            shift;
            env="$1";
            ;;
    --cluster)
            shift;
            cluster="$1";
            ;;
    --skip)
            skip=true;
            ;;
    esac
    shift
done

# Default Value
[ -z $cluster ]&&cluster='default'

black ">>> Params:"
black "  app     : $app"
black "  env     : $env"
black "  cluster : $cluster"

black ">>> Prepare"
mkdir .log
echo ".log" >> .dockerignore
sed -i 's#.env$##g' .dockerignore
if [ -z "$skip" ];then
    black ">>> Apollo"
    /data/ops/ci/libs/get_config.py --env ${env} --appid ${app} --cluster ${cluster} || die "ERROR : Fail to get .env file"
    /data/ops/ci/libs/match.sh || die "ERROR : Fail to match .env"
fi
if [ $env = "pro" ];then
    #/data/ops/ci/script/check_schemas.sh || exit 1
 echo
fi
black ">>> Docker build"
if [[ $cluster =~ "test" ]];then
    image_name=${app}:${cluster}
elif [ $env = "pro" ];then
    image_name=${app}:production
else
    image_name=${app}:${env}
fi
green ">>> docker build --force-rm -t storehub/${image_name} ."
docker build --force-rm -t storehub/${image_name} . &>./.log/docker || die "ERROR : Failed to run docker build\n>>> Build logs: ${JOB_URL}/ws/.log/docker/*view*/"
sed -i "s/\[[0-9]*m//g" ./.log/docker # Remove Color Code

green ">>> Build logs: ${JOB_URL}/ws/.log/docker/*view*/"

black ">>> Docker push"
green ">>> docker push storehub/${image_name}"
docker push storehub/${image_name} &>/dev/null || die "ERROR : Failed to push to dockerhub"
black ">>> AWS ECS"
if [ $env = "fat" ];then
    PROFILE="fat"
    CLUSTER="fat-env"
    SERVICE="${cluster}-${app}"
    TASK="${cluster}-${app}"
    MINI="0"
elif [ $env = "uat" ];then
    PROFILE="pro"
    CLUSTER="uat-env"
    SERVICE="${env}-${app}"
    TASK="${env}-${app}"
    MINI="0"
elif [ $env = "pro" ];then
    PROFILE="pro"
    CLUSTER="marketplace-ecs-cluster"
    if [ ${app} = "marketplace" ];then
        SERVICE="marketplace-svc"
    else
        SERVICE="${app}"
    fi
    TASK="${app}"
    MINI="100"
fi
green ">>> aws --profile $PROFILE ecs update-service --cluster ${CLUSTER} --service ${SERVICE} --task-definition ${TASK} --deployment-configuration maximumPercent=200,minimumHealthyPercent=${MINI} --desired-count 1 --force-new-deployment"
aws --profile $PROFILE ecs update-service --cluster ${CLUSTER} --service ${SERVICE} --task-definition ${TASK} --deployment-configuration maximumPercent=200,minimumHealthyPercent=${MINI} --desired-count 1 --force-new-deployment>>.aws.log || die "ERROR : Failed to Run AWS ECS"
if [ $env = "pro" ];then
    cat .aws.log | jq '.service.clusterArn,.service.deployments[0].taskDefinition,.service.serviceArn'
else
    cat .aws.log | jq '.service.clusterArn,.service.taskDefinition,.service.serviceArn'
fi

# Notification
if [ ${cluster} = "default" ];then
    /data/ops/ci/for_monitor/send.sh --app ${app} --env ${env}
else
    /data/ops/ci/for_monitor/send.sh --app ${app} --env ${cluster}
fi
