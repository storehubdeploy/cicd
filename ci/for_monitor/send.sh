#!/bin/bash

die() {
    echo -e "\033[1;31m>>> $@ \033[0m"
    exit 1
}

black() {
    echo -e "\033[1;30m $@ \033[0m"
}

if [ $# -ne 4 ];then
    die "ERROR : $#, please check the parameters"
fi

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
    esac
    shift
done

black ">>> Notification"
if [ $env = "pro" ];then
    recipient="t_1698967193551892"
else
    recipient="t_2222121407839972"
fi
/data/ops/ci/for_monitor/post.py --app $app --env $env -t $recipient
