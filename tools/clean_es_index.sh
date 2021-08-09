#!/bin/sh
# auto delete logs before a month
savedays=${1:-150}
echo $savedays
delete_log="/data/logs/elasticsearch/clean_index.log"
index_prefix="apm-6.5.0-transaction-"

format_day='%Y%m%d'

echo "==> clean time $(date +%Y-%m-%d)" >>${delete_log}

index=`curl -u elastic:7552525 -s -XGET 'http://localhost:9200/_cat/indices/*?v'|awk '{print $3}'|sed '1d'|grep ${index_prefix}|sort|head -n -${savedays}`

for i in ${index}
do
    curl -u elastic:7552525 -XDELETE "http://localhost:9200/$i" &>/dev/null && echo $i >> ${delete_log}
done

