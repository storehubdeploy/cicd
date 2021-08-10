#!/bin/bash

die() {
    echo -e "\033[1;31m>>> $@ \033[0m"
    exit 1
}

cd ${WORKSPACE}
branch=`cat /home/web/.jenkins/jobs/${fail_name}/builds/${fail_number}/log | grep "Merging Revision " | sed -e s#\).*##g -e s#.*/##g`

if [ `echo ${branch}|wc -c` -eq 0 ];then
    die "ERROR : No branch found, exiting..."
fi
    
git checkout ${branch}

if  [ ${branch} = "release" ];then
cat >> ${WORKSPACE}/.git/config <<EOF
[branch "release"]
        remote = origin
        merge = refs/heads/development
[branch "development"]
        remote = origin
        merge = refs/heads/development
EOF
elif [ ${branch} = "master" ];then
cat >> ${WORKSPACE}/.git/config <<EOF
[branch "master"]
        remote = origin
        merge = refs/heads/release
[branch "release"]
        remote = origin
        merge = refs/heads/release
EOF

else
    echo "branch=${branch}"
    die "ERROR : Does not support such branch, exiting..."
fi




cd ${WORKSPACE}
git pull-request --no-fork --no-rebase --title "Jenkins: Found Conflicts" -m "## Jenkins: Found Conflicts"
