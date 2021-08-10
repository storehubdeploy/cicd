#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import os, sys, json, random, time



if __name__ == '__main__':
    app='marketplace-api'
    lock_path = '/data/ops/ci/for_ut/ut_lock'
    app_lock=os.path.join(lock_path,app)
    #os.mknod(app_lock)
    os.remove(app_lock)
    
