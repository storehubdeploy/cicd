#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
  Author  : zyjiang
  Dtae    : 202005
"""

import os, sys, json
import requests
from optparse import OptionParser
sys.path.append("/data/ops/ci/libs")
from common import print_color

if __name__ == "__main__":
    usage='''
        python {0} --env ENV --app APP (--rolback revision)
        '''.format(sys.argv[0])
        
    parser = OptionParser(usage=usage)
    parser.add_option("-e","--env"      , dest="env"        , default=None)
    parser.add_option("-a","--appid"    , dest="appid"      , default=None)
    parser.add_option("-c","--category" , dest="category"   , default='properties')
    parser.add_option("-o","--out"      , dest="out"        , default='application')
    parser.add_option("-n","--namespace", dest="namespaces" , default=['application'], action="append")
    parser.add_option("-g","--cluster"  , dest="cluster"    , default='default')
    (options, args) = parser.parse_args()

    #config
    env        = options.env
    appid      = options.appid
    category   = options.category
    out        = options.out
    namespaces = options.namespaces
    cluster    = options.cluster
    
    # Get meta Url
    dev_meta ='http://apollo-dev.shub.us'
    fat_meta ='http://apollo-fat.shub.us'
    uat_meta ='http://apollo-uat.shub.us'
    pro_meta ='http://apollo-pro.shub.us'
 
    if env == 'test' or env== 'perf' or env=='fat':
        url = fat_meta
    elif env == 'dev':
        url = dev_meta
    elif env == 'uat':
        url = uat_meta
    elif env == 'pro':
        url = pro_meta
    else:
        print_color(31, "==> Can't get the Apollo Meta")
        sys.exit(1)
        
    if category == 'properties':
        aname = "web.{}".format(appid)
        namespaces = [aname, 'secret']
        for namespace in namespaces:
            r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url,appid,cluster,namespace))
            if r.status_code == 200:
                with open('.env', 'a') as f:
                    for k,v in r.json().iteritems():
                        f.write("{0}={1}\n".format(k,v))
            else:
                print_color(31, "==> Can't connect to %s" % url)
                sys.exit(1)
    else:
        r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url,appid,cluster,out+'.'+category))
        if r.status_code == 200:
            with open(out+'.'+category, 'a') as f:
                for k,v in r.json().iteritems():
                    f.write(v+'\n')
        else:
            print_color(31, "==> Can't connect to %s" % url)
            sys.exit(1)
