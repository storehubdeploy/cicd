#!/bin/bash

black() {
    echo -e "\033[1;30m>>> $@ \033[0m"
}

red() {
    echo -e "\033[1;31m>>> $@ NOT FOUND \033[0m"
}

die() {
    echo -e "\033[1;31m>>> $@ NOT FOUND \033[0m"
    exit 1
}

# Default Value
[ -z $WORKSPACE ] && WORKSPACE="./"
github=".env.example"
apollo=".env"
rc=0

cd ${WORKSPACE}

if [ ! -e ${github} ];then
    die "FILE .env.example"
fi

if [ ! -e ${apollo} ];then
    die "FILE ${apollo}"
fi

black "Matching ${github} and ${apollo}"
list_g=$(cat ${github} |grep -vE "^#|^$"|sed s#=.*##g)
list_a=$(cat ${apollo} |sed s#=.*##g)
echo ${list_a}|grep -w "PORT" >/dev/null || list_a+=" PORT"

for i in ${list_g}
do
if ! echo ${list_a}|grep -w $i >/dev/null; then
    red "'$i'"
    rc=1
fi
done
exit $rc
