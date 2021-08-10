#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
  Author  : mingdez
  Dtae    : 201903
"""

import os,sys,json
from optparse import OptionParser

def generate_new(json_path,**kw):
    with open(json_path, 'rb') as f:
        json_data=json.load(f)
        for k,v in kw.items():
            json_data['parameters'][k]['defaultValue']['value'] = v
        configs = json.dumps(json_data,indent=4)
        print configs
    f.close()
    return json_data

def write_new(json_path,json_data):
    with open(json_path, 'w') as f:
        json.dump(json_data,f)
    f.close()
 
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--key"   , dest="keys"     , default=[] , action="append")
    parser.add_option("--value" , dest="values"   , default=[] , action="append")
    parser.add_option("--file"  , dest="json_path", default='./remote_config.json')
    
    (options, args) = parser.parse_args()

    # config
    keys      = options.keys
    values    = options.values
    json_path = options.json_path

    # Main
    if not os.path.exists(json_path):
        print('{0} not exists'.format(json_path))
        sys.exit(1)

    data_dict=dict(zip(keys,values))
    json_data = generate_new(json_path,**data_dict)	
    write_new(json_path,json_data)




