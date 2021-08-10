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

script_path=`readlink -f $(dirname $0)`
python_lib_path="$script_path/libs"

check_schemas() {
    python3 -c "import sys;sys.path.append('${python_lib_path}');from common import check_schemas; check_schemas()"
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
    --host)
            shift;
            host="$1";
            ;;
    --nvm)
            shift;
            nvm="$1";
            ;;
    --launch)
            shift;
            launch="$1";
            ;;
    --dry)
            dry=true;
            ;;
    --skip)
            skip=true;
            ;;
    esac
    shift
done

# Default Value
[ -z $cluster ]&&cluster='default'
[ -z $nvm ]&&nvm='system'
[ -z $launch ]&&launch='start.json'

black ">>> Params:"
black "  app     : $app"
black "  env     : $env"
black "  cluster : $cluster"
black "  host    : $host"
black "  nvm     : $nvm"

if [ -z "$skip" ];then
    black ">>> Apollo"
    /data/ops/ci/libs/get_config.py --env ${env} --appid ${app} --cluster ${cluster} || die "ERROR : Fail to get .env file"
    /data/ops/ci/libs/match.sh || die "ERROR : Fail to match .env"
fi
if [ $env = "pro" || $env = "uat" ];then
    # /data/ops/ci/script/check_schemas.sh || exit 1
    check_schemas || exit 1
    my_memory=1000
else
    my_memory=500
fi
if [ $env = "fat" ] && [ $cluster != "default" ];then
    /data/ops/tools/write_tester.py -e ${cluster} -u ${BUILD_USER_EMAIL}
fi
black ">>> Build"
green ">>> Build logs: https://share.shub.us/build_log/${JOB_NAME}/${BUILD_NUMBER}.txt"
mkdir -p /data/share/build_log/${JOB_NAME}
bash ${WORKSPACE}/.cd/build.sh --env ${env} &>/data/share/build_log/${JOB_NAME}/${BUILD_NUMBER}.txt
rc=$?
sed -i "s/^[\[[0-9]*m//g" /data/share/build_log/${JOB_NAME}/${BUILD_NUMBER}.txt # Remove Color Code
if [ `hostname` != "storehub-control-panel" ];then
    scp -P 6666 /data/share/build_log/${JOB_NAME}/${BUILD_NUMBER}.txt jenkins-master:/data/share/build_log/${JOB_NAME}/${BUILD_NUMBER}.txt
fi
if [ $rc = "1" ];then
    die "ERROR : Failed to run build \n"
fi

black ">>> Deploy"
black ">>>> Copy to ${host}:/data/apps/"
rsync -ar --delete --exclude=.git --exclude=.log $JENKINS_HOME/workspace/$JOB_NAME ${host}:/data/apps/ || die "ERROR : Failed to copy"
black ">>>> Run PM2"

ssh ${host} <<EOF
[ -e ~/nvm ] || git clone https://github.com/creationix/nvm.git
grep -rl 'nvm.sh' ~/.bashrc >/dev/null || echo "source nvm/nvm.sh" >> ~/.bashrc
source ~/.bashrc
nvm install ${nvm} >/dev/null
nvm use ${nvm}
cd /data/apps/$JOB_NAME
[ $app = "ecommerce-v1-consumer" ] && pm2 delete ecommerce-v1-consumer
pm2 startOrRestart .cd/$launch --env ${env} --max-memory-restart ${my_memory}M
EOF

# Notification
if [ -z "$dry" ];then
    if [ ${cluster} = "default" ];then
        /data/ops/ci/for_monitor/send.sh --app ${app} --env ${env}
    else
        /data/ops/ci/for_monitor/send.sh --app ${app} --env ${cluster}
    fi
fi

