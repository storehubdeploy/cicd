#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
  Author  : mingdez
  Date    : 20190330
  Function: Generate Configuration.h for POS
"""

import os, sys, json
import requests
from optparse import OptionParser

def print_color(color,text):
    '''
    30:黑
    31:红
    32:绿
    33:棕
    34:蓝
    35:紫红
    36:青
    37:灰
    '''
    print("\033[1;{0}m{1}\033[0m".format(color,text))

def apollo_get(url,app,cluster="dafault",namespace="application"):
    configs=""
    r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url,app,cluster,namespace))
    if r.status_code == 200:
        for k,v in r.json().iteritems():
            if v=="YES" or v=="NO":
                configs+='#define {}{}\n'.format(k.ljust(24),v)
            else:               
                configs+='#define {}@{}\n'.format(k.ljust(24),v)
        return configs[:-1] # Remove last \n
    else:
        print_color(31, ">>> Error,Can't connect to %s" % url)
        sys.exit(1)
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--app",dest="app",default="pos")
    parser.add_option("--cluster",dest="cluster", default='default')
    (options, args) = parser.parse_args()
    app = options.app
    cluster = options.cluster

    # Get meta Url
    dev_meta ='http://apollo-dev.shub.us'
    fat_meta ='http://apollo-fat.shub.us'
    uat_meta ='http://apollo-uat.shub.us'
    pro_meta ='http://apollo-pro.shub.us'

    # Template
    print_color(30, ">>> Generating 'Configuration.h'. Please wait.")
    Configuration='''//
//  Configuration.h
//  POS
//
//  Created by Congyu on 13-5-2.
//  Copyright (c) 2013年 RiseHub. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface Configuration : NSObject

#ifdef DEVELOPMENT
{}
#elif defined(TESTING)
{}
#elif defined(STAGING)
{}
#elif defined(PRODUCTION)
{}
#else 
#define SERVER_BASE_URL         @""
#define BOOST_AUTH_URL          @""
#define BOOST_PAYMENT_URL       @""
#define FORWARD_SERVER_BASE_URL @""
#define SSTOP_BASE_URL          @""
#endif

@end
'''.format(apollo_get(dev_meta,app),apollo_get(fat_meta,app,cluster),apollo_get(uat_meta,app),apollo_get(pro_meta,app))
    if os.path.exists(os.path.join(os.path.dirname(__file__),'fastlane')):
        with open('Configuration.h', 'w') as f:
            f.write(Configuration)
        print_color(30, ">>> Done")
    else:
        print_color(31, ">>> Error,Please run me where you need 'Configuration.h' ")
