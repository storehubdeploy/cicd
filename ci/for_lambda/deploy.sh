#!/bin/bash

die() {
    echo -e "\033[1;31m>>> $@ \033[0m"
    exit 1
}

check_commit() {
    git log -1 --pretty=format:" >>> Commit:%s"|grep "${app}" || die "ERROR : Cannot find '\[$app\]'"
}

black() {
    echo -e "\033[1;30m $@ \033[0m"
}

if [ $# -ne 4 ]&&[ $# -ne 6 ]&&[ $# -ne 8 ];then
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
    --bucket)
            shift;
            bucket="$1";
            ;;
    --region)
            shift;
            region="$1";
            ;;
    esac
    shift
done

# Default Value
[ -z $bucket ]&&bucket='fat-lambda-function'
[ -z $region ]&&region='ap-southeast-1'

black ">>> Params:"
black "	app    : $app"
black "	env    : $env"
black "	bucket : $bucket"
black "	region : $region"

black ">>> Check"
check_commit

black ">>> Npm"
cd ${WORKSPACE}/${app}
npm install || die "ERROR : Fail to npm install"

black ">>> Zip"
cd ${WORKSPACE}/${app} && zip -FS -q -r ${WORKSPACE}/dist/${app}.zip * || die "ERROR : Fail to zip"

black ">>> S3"
cd ${WORKSPACE}/dist/
aws --profile ${env} s3 cp --no-progress ${WORKSPACE}/dist/${app}.zip s3://${bucket}/ || die "ERROR : Fail to Upload to S3"
aws --profile ${env} s3 ls s3://${bucket}

black ">>> Deploy"
aws --profile ${env} lambda update-function-code --function-name ${app} --s3-bucket ${bucket} --s3-key ${app}.zip --publish --region ${region} || die "ERROR : Fail to Deploy"

# Notification
#/data/ops/ci/for_monitor/send.sh --app ${app} --env ${env}
