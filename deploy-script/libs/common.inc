# MY_DIR="$(pwd)"
# MY="`basename $(pwd)`"
script_path=`readlink -f $(dirname $0)`
python_lib_path="$script_path/libs"

DOCKER_REG=${DOCKER_REG:-harbor.shub.us}
DOCKER_USR=${DOCKER_USR:-admin}
DOCKER_PSW=${DOCKER_PSW:-storehub@#098}

HELM_REPO=${HELM_REPO:-https://harbor.shub.us/chartrepo}
HELM_USR=${HELM_USR:-admin}
HELM_PSW=${HELM_PSW:-storehub@#098}

die() {
    echo -e "\033[1;31m$@ \033[0m"
    exit 1
}

black() {
    echo -e "\033[1;30m$@ \033[0m"
}

green() {
    echo -e "\033[1;32m$@ \033[0m"
}

blue() {
    echo -e "\033[1;34m$@ \033[0m"
}

red() {
    echo -e "\033[1;31m$@ \033[0m"
}

send_notification() {
    app=$1
    env=$2
    cluster=$3
    black ">>> Notification"
    if [ $env = "pro" ];then
        recipient="t_1698967193551892"
    else
        recipient="t_2222121407839972"
    fi
    if [ ${cluster} = "default" ];then
        word=$env
    else
        word=$cluster
    fi
    /data/ops/ci/for_monitor/post.py --app $app --env $word -t $recipient
}

check_schemas() {
    python3 -c "import sys;sys.path.append('${python_lib_path}');from common import check_schemas; check_schemas()"
}

