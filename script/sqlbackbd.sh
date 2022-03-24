#!/bin/bash 
user='apollo_user'
passwd='apollo_pwd'
mysqldump -u "$user" -h 192.168.0.50 -p"$passwd" --all-databases > /data/apollo/backdb.sql
