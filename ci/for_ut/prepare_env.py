#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author  : mingdez
  Dtae    : 201903
"""

import os, sys, json, random, time
from optparse import OptionParser
from dotenv import load_dotenv
from pathlib import Path
sys.path.append("/data/ops/ci/libs")
from common import print_color, run

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--create" , dest="create" , default=False , action="store_true")
    parser.add_option("--delete" , dest="delete" , default=False , action="store_true")

    (options, args) = parser.parse_args()

    # config
    create = options.create
    delete = options.delete

    # Read configuration
    file_name=".env"
    if not os.path.exists(file_name):
        print('{} not exists'.format(file_name))
        sys.exit(1)

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    app = os.getenv("UT_APP")
    host = os.getenv("UT_HOST")
    mongo_port = os.getenv("UT_MONGO_PORT")
    es_port = os.getenv("UT_ES_PORT")
     
    lock_path = '/data/ops/ci/for_ut/ut_lock'
    app_lock=os.path.join(lock_path,app)

    if not os.path.exists(lock_path):
        os.mkdir(lock_path)

    if create:
        print('>>>Create')
        lock_time=0
        while True:
            if os.path.exists(app_lock):
                time.sleep(3)
                lock_time+=3
                print(lock_time)
            elif lock_time > 80:
                print(">>>Timeout")
                sys.exit(1)
            else:
                break
        os.mknod(app_lock)
        print(app_lock)
        print('-----------------')
        run('''ssh {0} docker exec -i redis redis-cli FLUSHALL'''.format(host))
        if mongo_port:
            run('''ssh {0} docker run -d --name {1}ut{2} -p {3}:27017 mongo:4.0.13 '''.format(host,app, random.random(), mongo_port))
        if es_port:
            run('''ssh {0} docker run -d --name {1}ut{2} -p {3}:9200 -p {4}:9300 --env-file /data/ops/ci/for_ut/elasticsearch.env elasticsearch:6.4.0 '''.format(host,app, random.random(), es_port,random.randint(10000,20000)))
            time.sleep(25)

    if delete:
        print('>>>Delete')
        os.remove(app_lock)
        run('''ssh {0} "/data/ops/ci/for_ut/delete.sh {1}" '''.format(host,app))
