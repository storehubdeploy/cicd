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
sed -i 's#.env$##g' .dockerignore
black ">>> Apollo"
/data/ops/ci/libs/get_config.py --env ${env} --appid ${app} --cluster ${cluster} || die "ERROR : Fail to get .env file"

black ">>> Docker build"
image_name=${app}:${cluster}

green ">>> docker build --force-rm -t storehub/${image_name} ."
docker build --force-rm -t storehub/${image_name} . || die "ERROR"

black ">>> Docker push"
green ">>> docker push storehub/${image_name}"
docker push storehub/${image_name} &>/dev/null || die "ERROR : Failed to push to dockerhub"
