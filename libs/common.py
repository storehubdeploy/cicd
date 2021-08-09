#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
  Author  : mingdez
  Dtae    : 201901
"""
import os
import sys
import time
import hashlib
try:
    import paramiko
except :
    os.system('sudo pip install paramiko')
    import paramiko
try:
    import requests
except :
    os.system('sudo pip install requests')
    import requests
import shutil
import tarfile

# Globle parameter
def default_cfg():
    config_file = "/data/storehub/deploy.csv" 
    return config_file

# output
def print_color(color,text):
    '''
    30:黑                don't like it
    31:红    for stderr
    32:绿                don't like it
    33:棕                don't like it
    34:蓝    for stdout
    35:紫红  for title
    36:青                just so so
    37:灰                can't see it
    '''
    print("\033[1;{0}m{1}\033[0m".format(color,text))

# # # md5
# # def md5sum(file):
    # # rb = open(file,'rb')
    # # rb_md5 = hashlib.md5()
    # # rb_md5.update(rb.read())
    # # return rb_md5.hexdigest()

# # # ssh 
# # class SSH(object):    
    # # def __init__(self,host):
        # # self.host    = host
        # # self.user    = 'web'
        # # self.pk_path = '/home/web/.ssh/id_rsa'
        # # self.port    = 22
        # # self.connect()
        
    # # def connect(self):
        # # key = paramiko.RSAKey.from_private_key_file(self.pk_path)
        # # self.ssh = paramiko.SSHClient()
        # # self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # # self.ssh.load_system_host_keys() 
        # # try:
            # # self.ssh.connect( self.host, port = self.port, username = self.user, pkey = key )
        # # except:
            # # print_color(31, "==> Can't reach %s" % self.host)
            # # sys.exit(25)
    
    # # def close(self):
        # # self.ssh.close()
        
    # # def run(self,command,out=True,result=False):
        # # print_color(30, '==> ssh {0} "{1}"'.format(self.host,command)) 
        # # stdin, stdout, stderr = self.ssh.exec_command(command)
        # # rc = len(stderr.readlines())
        # # if out:
            # # if result:
                # # if rc > 0:
                    # # return stderr.read().strip()
                # # else:
                    # # return stdout.read().strip()
            # # else:
                # # if rc > 0:
                    # # print_color(30, "==> %-15s Result :" % self.host)
                    # # print_color(34, stdout.read())
                    # # print_color(31, stderr.read())
                # # else:
                    # # print_color(30, "==> %-15s Result :" % self.host)
                    # # print_color(34, stdout.read())
    
    # # def remote_md5(self,file):
        # # stdin, stdout, stderr = self.ssh.exec_command("md5sum %s" % file)
        # # return stdout.read().split(' ')[0]
        
    # # def check_md5(self,local_file,remote_file):
        # # local_md5   = md5sum(local_file)
        # # remote_md5  = self.remote_md5(remote_file)
        # # if local_md5 == remote_md5 :
            # # print_color(34, "==> File received     --> %s : %s" % (self.host,remote_file))
        # # else:
            # # print_color(31, "==> File not received --> %s : %s" % (self.host,remote_file))

    # # def put(self,local_file,dest_path,exclude=[]):
        # # filename = os.path.split(os.path.realpath(local_file))[1]
        # # remote_file = os.path.join(dest_path,filename)
        # # if os.path.isfile(local_file):                  # for file
            # # self.ssh.exec_command("mkdir -p %s" % dest_path)
            # # self.sftp = self.ssh.open_sftp()
            # # self.sftp.put(local_file, remote_file)
            # # self.check_md5(local_file,remote_file)
            # # self.sftp.close()
        # # if os.path.isdir(local_file):                   # for dir
            # # if not exclude:
                # # rsync_cmd = 'rsync -av {0} {1}:{2}'.format(local_file,self.host,dest_path)
            # # else:
                # # exclude_files = ''
                # # for i in exclude:
                    # # exclude_files+='--exclude={0} '.format(i)
                # # rsync_cmd = 'rsync -av {0} {1} {2}:{3}'.format(exclude_files,local_file,self.host,dest_path)
            # # rsync_result = call(rsync_cmd)
            # # if rsync_result.code == 0:
                # # received_files = rsync_result.out.split('\n')[1:-3]
                # # for received_file in received_files:
                    # # print_color(34, "==> File received     --> %s : %s" % (self.host,received_file))
            # # else:
                # # print_color(31, "==> File not received --> %s : %s" % (self.host,remote_file))
    
    # def rm_file(self,file):
        # self.sftp = self.ssh.open_sftp()
        # self.sftp.remove(file)
        # self.sftp.close()
    
    # def rm_path(self,path):
        # self.sftp = self.ssh.open_sftp()
        # self.sftp.rmdir(path)
        # self.sftp.close()
    
    # def dir_exists(self,path):
        # stdin,stdout,stderr = self.ssh.exec_command('ls {0}'.format(path))
        # if stdout.readline() != '':
            # return True
        # else:
            # return None
            
    # def symlink(self,src,des)
        # self.sftp = self.ssh.open_sftp()
        # sftp.symlink(src, des)
        # self.sftp.close()
        
    
# # find file in path
# def find_file(path,filename,suffix=None):
    # if not os.path.exists(path): 
        # print_color(31, "==> Path is not found\n")
        # return None
    # if os.path.isfile(path): 
        # print_color(31, "==> Path is not found\n")
        # return None
    # my_file = None
    # if suffix is None:
        # for root, dirs, files in os.walk(path):
            # if filename in files: 
                # return os.path.join(root, filename)
            # if filename in dirs:
                # return os.path.join(root, filename)
    # else:
        # for root, dirs, files in os.walk(path):
            # for file in files:
                # if file.endswith(filename):
                    # my_file = os.path.join(root, file)
                    # return my_file
    # if my_file is None:
        # print_color(31, "==> %s is not found\n" % filename)
        # raise Exception



# copy
def copy_file(old, new):
    if os.path.exists(old):
        if os.path.isfile(old):
            shutil.copyfile(old, new) 
        if os.path.isdir(old):
            shutil.copytree(old, new)
    else:
        print_color(31, "==> %s not exits!" % old)

# # kill pid contains name
# def kill_task(keyword):
    # from subprocess import check_output
    # import signal
    
    # pid_dict={}
    # for pid in check_output(['ps','-aux']).split('\n'):
        # if keyword in pid and 'python' not in pid:
            # pid_no         = pid.split()[1]
            # pid_name       = ' '.join(pid.split()[10:])
            # pid_dict[pid_no] = pid_name
    
    # if pid_dict:
        # print_color(30, "    %-5s : %s" % ('PID','COMMAND'))
        # for k,v in pid_dict.items():
            # print_color(34, "    %-5s : %s" % (k,v))
        # # do the kill
        # for key in pid_dict.keys():
            # this_pid = int(key)
            # try:
                # rc = os.kill(this_pid, signal.SIGKILL)
                # print_color(34, '==> Already killed %-5s' % this_pid)
            # except OSError, e:
                # print_color(31, '==> Process [ %s ] disappeared' % this_pid)
    # else:
        # print_color(31, "==> No such process [ %s ]" % keyword)
    
# call
def call(cmd):
    from subprocess import Popen, PIPE, STDOUT
    import tempfile
    
    class CallResult(object):
        def __init__(self, out, err, returncode):
            self.out = out
            self.err = err
            self.code = returncode
    
    temp_file_stdout = tempfile.TemporaryFile()
    temp_file_stderr = tempfile.TemporaryFile()
    result = Popen(cmd, shell=True, stdin=PIPE, \
        stdout=temp_file_stdout.fileno(), stderr=temp_file_stderr.fileno(), close_fds=False)
    result.wait()

    temp_file_stdout.seek(0)
    out = temp_file_stdout.read().strip()
    temp_file_stdout.close()
    temp_file_stderr.seek(0)
    err = temp_file_stderr.read().strip()
    temp_file_stderr.close()

    return CallResult(out, err, result.returncode)

def run(cmd, show=True,ignore=False):
    from subprocess import Popen, PIPE, STDOUT
    
    class CallResult(object):
        def __init__(self, out, returncode):
            self.out = out
            self.code = returncode
    
    print_color(30, ">>> %s" % cmd)
    result = Popen(cmd ,shell=True , stdout=PIPE, stderr=STDOUT)
    lines = []
    for line in iter(result.stdout.readline, b''):
        line = line.rstrip()
        if show:
            print('>>>  {}'.format(line))
        lines.append(str(line))
    out="\n".join(lines)
    result.wait()
    if result.returncode == 0:
        pass
    else:
        print(result.returncode)
        if not ignore:
            print_color(31, result.stderr)
            print_color(31, ">>> Failed\n")
            sys.exit(1)
    return CallResult(out, result.returncode)
            
    

# tar and untar
def tar_xf( scr, file , des=sys.path[0]):
    if file.endswith('.tar'):
        file_path = os.path.join(scr,file)
    else:
        file_path = os.path.join(scr,file+".tar")
    with tarfile.open(file_path, "r") as tar:
        for file in tar:
            tar.extract(file,des)

def tar_cf( scr , file, des=sys.path[0] , exclude=[]):
    if file.endswith('.tar'):
        file_path = os.path.join(des,file)
    else:
        file_path = os.path.join(des,file+".tar")
    with tarfile.open(file_path, "w:gz") as tar:
        if exclude:
            tar.add(scr, arcname=os.path.basename(scr) , filter = lambda x: None if x.name in exclude else x)
        else:
            tar.add(scr, arcname=os.path.basename(scr))
        
#delete
def rm(file):
    if os.path.isfile(file):
        os.remove(file)
    if os.path.isdir(file):
        shutil.rmtree(file)
    print_color(31, '==> delete %s' % file)
