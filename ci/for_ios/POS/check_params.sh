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
from="Configuration.h.old"
dest="Configuration.h"
rc=0

black "Matching ${from} and ${dest}"
list_g=$(cat ${from} |grep "#define"|awk '{print $2}'|sort -u)
list_a=$(cat ${dest} |grep "#define"|awk '{print $2}'|sort -u)

for i in ${list_g}
do
if ! echo ${list_a}|grep -w $i >/dev/null; then
    red "'$i'"
    rc=1
fi
done
exit $rc

