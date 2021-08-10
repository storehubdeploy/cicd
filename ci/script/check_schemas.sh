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
[ -z ${WORKSPACE} ] && WORKSPACE="`pwd`"
[ -e ${WORKSPACE}/.gitmodules ] || exit 0

[ ! -e /data/tools/schemas ] && die "tools disappeared"
cd /data/tools/schemas 
git pull
rev_short=`git log -1 --pretty='%h'`

cd ${WORKSPACE}
grep -rl 'schemas.git' .gitmodules &>/dev/null || exit 0
path=`grep -C 1 -r 'schemas.git' .gitmodules |grep path|awk -F '= ' '{print $2}'`
cd ${WORKSPACE}/$path
git branch|grep "*"|grep "${rev_short}" &>/dev/null || die "Schemas not master branch(* HEAD at ${rev_short})"
black "Schemas * (HEAD master at ${rev_short})"
