#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
  Author  : mingdez
  Dtae    : 201901
"""

import os, sys, json
import time,datetime
import ConfigParser
from optparse import OptionParser
try:
    import git
except :
    os.system('sudo pip install GitPython')
    import git
sys.path.append("/data/ops/ci/libs")
from common import default_cfg, print_color, run

# Globle parameter
config_file = default_cfg()

#jenkins
workspace   = os.getenv("WORKSPACE")
job_name    = os.getenv("JOB_NAME")
revision    = os.getenv("GIT_COMMIT")
backup_dir   = "/data/storehub/bak/docker/"
if job_name:
    backup_full  = os.path.join(backup_dir,job_name)

if __name__ == "__main__":
    usage='''
        python {0} --env ENV --app APP (--rolback revision)
        '''.format(sys.argv[0])
        
    parser = OptionParser(usage=usage)
    parser.add_option("--env"      , dest="env"      , default=None)
    parser.add_option("--app"      , dest="app"      , default=None)
    parser.add_option("--rollback" , dest="rollback" , default=None , help="rollback to specific revision")
    (options, args) = parser.parse_args()

    #config
    env      = options.env
    app      = options.app
    rollback = options.rollback

    cfg_key  = "web#%s#%s#" % (env,app)
    configs  = []
    for line in open(config_file):
        if cfg_key in line:
            info            = line.split('#')
            config          = {}
            config['cluster'    ] = info[3].strip('\n')
            config['count'      ] = info[4].strip('\n')
            config['extra_cmd'  ] = info[5].strip('\n')
            config['service'    ] = env+'-'+app
            config['definition' ] = env+'-'+app
            configs.append(config)
    
    # Git part
    repo = git.Repo(workspace)
    git  = repo.git
    os.chdir(workspace)
    print_color(31, "==> Current Revision %s" % revision)
    
    print_color(30, "==> Getting configurations")
    configs_color = json.dumps(configs,indent=4)
    if configs == []:
        print_color(31, "==> Can't get the configurations!")
        sys.exit(1)
    else:
        print configs_color
        
    if env == 'test' or env == 'perf':
        profile_key='fat'
    elif env == 'uat' or env == 'pro':
        profile_key='pro'
    else:
        print_color(31, "==> FATAL ERROR!!! Can't get the aws profile key!!!")
        sys.exit(1)
        
    # Working
    for config in configs:
        # get parameters
        cluster      = config['cluster'   ]
        service      = config['service'   ]
        definition   = config['definition']
        count        = config['count'     ]
        extra_cmd    = config['extra_cmd' ]
        docker_image = "storehub/" + app + ":" + env
        
        if rollback is None:
            print_color(31, "==> [  Deploy Mode  ]")
            # Detect gitmodules
            os.chdir(workspace)
            if os.path.exists(os.path.join(workspace,'.gitmodules')):
                print_color(30, "==> detect file .gitmodules : git submodule update --init")
                git.submodule('update','--init')
            # Docker Part
            print_color(30, "==> Step 1 : docker build --force-rm %s -t %s ." % (extra_cmd,docker_image))
            cmd = "docker build --force-rm %s -t %s ." % (extra_cmd,docker_image)
            run(cmd,ignore=True)

            print_color(30, "==> Step 2 : docker push %s" % docker_image)
            cmd = "docker push %s" % docker_image
            run(cmd)

            # AWS ECS Part
            print_color(30, "==> Step 3 : Getting latest definition")
            cmd = "aws --profile {0} ecs list-task-definitions --family-prefix {1} --sort DESC".format(profile_key, definition)
            definition_all  = run(cmd,show=False)
            definition_last = str(json.loads(definition_all.out)['taskDefinitionArns'][0].split(':')[-1])
            print_color(30, "==> Auto get latest definition : %s" % definition_last)

            print_color(30, "==> Step 4 : aws --profile {0} ecs update-service --cluster {1} --service {2} --task-definition {3} --deployment-configuration maximumPercent=200,minimumHealthyPercent=0 --desired-count {4} --force-new-deployment".format(profile_key,cluster,service,definition,count))
            cmd = "aws --profile {0} ecs update-service --cluster {1} --service {2} --task-definition {3} --deployment-configuration maximumPercent=200,minimumHealthyPercent=0 --desired-count {4} --force-new-deployment".format(profile_key,cluster,service,definition,count)
            run(cmd)
                
            cmd = "docker images|grep none|awk '{print $3}'|xargs docker rmi || exit 0"
            print "==> Delete images which TAG is <none> "
            run(cmd)
                
            ## 下面是回滚脚本
            # # # 研究一下ECS 调用旧的image
            # # # Backup Record
            # # print_color(30, "==> Step 5 : Save backup info to %s " % backup_full)
            # # if not os.path.exists(backup_full):
                # # os.mknod(backup_full)
                # # print_color(31, "==> Not exists, touch : %s" % backup_full)
            # # f = open(backup_full, 'a')
            # # f.write("[{0}]\ndefinition = {1}\ntimestamp = {2}".format(revision,definition_all,time.time()))
            # # f.close()
        # # else:
            # # print_color(31, "==> [ Rollback Mode ]")
            # # # Read configuration
            # # config     = ConfigParser.ConfigParser()
            # # config.readfp(open(backup_full))

            # # # Get parameters
            # # definition = config.get(rollback, "definition"  )
            # # timestamp  = config.get(rollback, "timestamp"   )
            # # print_color(30, "==> Select version %s" % time.strftime('%Y-%m-%d %H:%M', time.localtime(timestamp)))
            # # print_color(30, "==> rollback   : %s" % rollback)
            # # print_color(30, "==> definition : %s" % definition)
            
            
            
            # Useless API
            # docker build
            # import docker
            # client   = docker.APIClient(base_url='unix://var/run/docker.sock',version='auto',timeout=10)
            # try:
                # response = [line for line in client.build(path=workspace, rm=True, tag=docker_image, encoding='UTF-8', decode=True)]
            # except docker.errors.APIError, e:
                # print_color(31, "==> Failed")
            # print json.dumps(response,indent=4)
            
            
