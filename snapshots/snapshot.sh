#!/bin/bash
set -x 

#get snapshotid
snap=`curl --user "$key:$secret" --digest      --include      --request GET "https://cloud.mongodb.com/api/atlas/v1.0/groups/5b4db5610bd66b4ef8f3f810/clusters/v2021/backup/snapshots?pretty=true"| grep id | grep -v AWS | awk -F '"' '{print $4}' | head -n 1`

echo $snap

#get create-time
time=`curl --user "$key:$secret" --digest      --include      --request GET "https://cloud.mongodb.com/api/atlas/v1.0/groups/5b4db5610bd66b4ef8f3f810/clusters/v2021/backup/snapshots?pretty=true" | grep createdAt | awk -F '"' '{print $4}'| head -n 1`

echo $time

#generate download-link
gen=`curl --user "$key:$secret" --digest --include \
     --header "Accept: application/json" \
     --header "Content-Type: application/json" \
     --request POST "https://cloud.mongodb.com/api/atlas/v1.0/groups/5b4db5610bd66b4ef8f3f810/clusters/v2021/backup/restoreJobs" \
     --data '{
         "snapshotId" : "'$snap'",
         "deliveryType" : "download"
       }' | grep id | awk -F '"' '{print $16}' `
echo $gen 

sleep 5m

#get download-link
link=`curl --user "$key:$secret" --digest --include \
     --header "Accept: application/json" \
     --header "Content-Type: application/json" \
     --request GET "https://cloud.mongodb.com/api/atlas/v1.0/groups/5b4db5610bd66b4ef8f3f810/clusters/v2021/backup/restoreJobs/$gen?pretty=true" | grep deliveryUrl | awk -F '"' '{print $4}'`

echo $link

name=`echo $link | awk -F '/' '{print$5}'`

wget $link


#sleep 7h

#check=`cat wget-log | grep saved`

sleep 20

#if [[ $check == *"saved" ]]; then
  mv $name "$time".tar.gz
#fi

sleep 20

aws s3 cp *.tar.gz s3://shmongo-snapshots

rm -f *.tar.gz

sleep 5

sh s3.sh
