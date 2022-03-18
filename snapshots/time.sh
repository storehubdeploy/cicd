#!/bin/bash
aweekago=`date -d "7 days ago" +%s`
for f in $(ls)
do
stat -c %Y ${f}
aa=`stat -c %Y "${f}"`
echo "${f} createtime is ${aa}"
if [ ${aweekago} -lt ${aa} ];then
echo "yes"
fi
done
