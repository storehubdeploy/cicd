#!/bin/bash
set -x

t=`date -d "14 days ago" +%Y-%m-%d`

echo $t


snap=`aws s3 ls  s3://shmongo-snapshots | awk '$1 < "'$t'" {print $4}' | sort -n`

for i in $snap
do
echo $i
aws s3 rm s3://shmongo-snapshots/$i
done


