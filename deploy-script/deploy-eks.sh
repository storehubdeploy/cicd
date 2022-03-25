#!/bin/bash
#nicktest
# Load
script_path=`readlink -f $(dirname $0)`
. ${script_path}/libsqa/common.inc

while [ "$1" ]; do
    case "$1" in
    deploy)
            action=deploy;
            ;;
    rollback)
            action=rollback;
            ;;
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
    esac
    shift
done

actions=(build rollback)
#echo "${actions[@]}" | grep -wq "$action" || die ">>> [ERROR] UNSUPPORTED ACTION"

# Default
[ -z $cluster ]&&cluster='default'

git_tag="`git rev-parse --short HEAD`"
image_tag_json=`curl -s -u "admin:${HELM_PSW}" -X GET "https://harbor.mymyhub.com/api/repositories/${env}%2F${app}/tags" -H "accept: application/json"`
current_image_tag=`echo ${image_tag_json} | grep -Po 'name[" :]+\K[^"]+'`
echo ${git_tag}
echo ${current_image_tag}

# def 
main_init() {
    [ -e "${WORKSPACE}/.gitmodules" ] && git submodule update --init
    # check_schemas
}

docker_part() {
    blue ">>> Docker Login"
    # docker login ${DOCKER_REG} -u ${DOCKER_USR} -p ${DOCKER_PSW} || die ">>> Login Harbor Failed"
    echo "${DOCKER_PSW}" | docker login ${DOCKER_REG} -u ${DOCKER_USR} --password-stdin 2>/dev/null || die ">>> Login Harbor Failed"
    blue ">>> Docker build"
    if [ $app = "beep-v1-web" ] || [ $app = "ist-v1-web" ];then
        /data/ops/ci/libs/get_config-shared.py --env ${env} --appid ${app} --cluster ${cluster}
    fi
    if [ $app = "alertservice" ]; then
        docker build -f Dockerfile.alertservice -t ${DOCKER_REG}/${env}/${app}:${git_tag} . || die ">>> Docker Build Failed"
    else
        docker build -t ${DOCKER_REG}/${env}/${app}:${git_tag} . || die ">>> Docker Build Failed"
    fi
    #rm -f ${WORKSPACE}/.env
    blue ">>> Docker push"
    docker push ${DOCKER_REG}/${env}/${app}:${git_tag} || die ">>> Docker Push Failed"
    #docker images|grep none|awk '{print $3}'|xargs docker rmi -f || die ">>> Docker delete failed"
}

helm_repo() {
    blue ">>> Helm Add Repo"
    green "helm repo add --username=${HELM_USR} --password=****** ${env} ${HELM_REPO}/${env}"
    # helm repo list | awk -F " " '{if (NR>1){print $2}}' | grep "${HELM_REPO}/${env}" > /dev/null || helm repo add --username=${HELM_USR} --password=${HELM_PSW} ${env} ${HELM_REPO}/${env}
    helm repo add --username=${HELM_USR} --password=${HELM_PSW} ${env} ${HELM_REPO}/${env}
}

helm_pack() {
    blue ">>> Helm Pack"
    helm pull ${env}/${app}
    tar -xf ${app}*.tgz
    rm -f ${app}*.tgz
    python3 ${script_path}/shared_yaml.py -a ${app}  -e ${env} -c ${cluster} || die ">>> Helm Generate Yaml Failed"
    helm package ./${app} || die ">>> Helm Pack Failed"
}

helm_push() {
    blue ">>> Helm Push"
    helm plugin list | grep push &>/dev/null || helm plugin install https://github.com/chartmuseum/helm-push
    helm push ${app}*.tgz ${env} || die ">>> Helm Push Failed"
}

helm_backup() {
    blue ">>> Backup Current Version"
    ssh root@192.167.0.125 <<EOF
    date "+%y%m%d%H%M%S"
    helm list -n test16 | awk '{if(NR>1)print \$1, \$9}' > /data/backup/`date "+%y_%m_%d_%H_%M_%S"`.txt
EOF
} 

helm_deploy() {
    blue ">>> Helm Deploy"
#helm repo add --username=${HELM_USR} --password=${HELM_PSW} ${env} ${HELM_REPO}/${env}
    new_version="`cat ${WORKSPACE}/next_version`"
    ssh root@192.167.0.125 <<EOF
helm repo add --username=admin --password=${HELM_PSW} fat https://harbor.mymyhub.com/chartrepo/fat
helm repo update
if [ ${env} == fat ];then
  if [ ${cluster} == test18 ];then
    helm upgrade ${app} --version ${new_version} ${env}/${app} --namespace=${cluster}
  else
    helm uninstall ${app} --namespace=${cluster}
    sleep 3
    helm install ${app} ${env}/${app} --namespace=${cluster}
  fi
else
    #helm install ${env}/${app} --version ${new_version} --namespace=${cluster} --name=${app}
    helm install ${app} ${env}/${app} --namespace=${cluster}
fi
EOF
}

main() {
main_init
if echo ${current_image_tag} | grep -w ${git_tag} &>/dev/null;
then
    if [ ${app} == ist-v1-web ];then
      docker_part
    else
      echo "go got next...."
    fi
    echo "tag version exist,so don't package"
else
    echo "tag version not exist.Packaging.........."
    docker_part
fi
#docker_part
helm_repo
helm_pack
helm_push
helm_backup
helm_deploy
}

main
