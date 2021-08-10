#!/usr/bin/env python3
# coding:utf-8
import os
import sys    
import git
import configparser
from optparse import OptionParser
import requests, json
from poeditor import POEditorAPI
sys.path.append("/data/ops/ci/libs")
from common import print_color

class POE(object):
    def __init__(self,app):
        config_ini = os.path.join("/data/ops/ci/for_translate/config.ini")
        config     = configparser.ConfigParser()
        config.readfp(open(config_ini))
        self.project_id = config.get(app,"app_id")
        if os.getenv("WORKSPACE"):
            self.file_path = os.path.join(os.getenv("WORKSPACE"),config.get(app,"path"))
        else:
            self.file_path = os.path.join('./',config.get(app,"path"))
        self.client     = POEditorAPI(api_token="bd608c0b2debdc1205e03ee20e2f46e6")

    def upload(self):
        file_name = os.path.join(self.file_path,'en.json')
        if os.path.exists(file_name):
           # self.client.update_terms(self.project_id, file_name, sync_terms=True)
            self.client.update_terms_translations(self.project_id, file_name, sync_terms=True,language_code='en')
        else:
            print_color(31,">>> Cannot find en.json")
            sys.exit(1)

    def view(self):
        return self.client.view_project_details(self.project_id)

    def show(self):
        return self.client.list_project_languages(self.project_id)

    def percent(self):
        for i in self.show():
            if i['percentage'] == 100:
                pass
            else:
                raise ValueError
        return True
    
    def export(self):
        for i in self.show(): 
            code = i['code']
            file_name = os.path.join(self.file_path,code+'.json') 
            self.client.export(project_id=self.project_id, language_code=code, file_type='key_value_json',local_file=file_name)

def check_progress(app):
    try:
        print_color(30,">>> Checking progress")
        POE(app).percent()
    except ValueError:
        print_color(31,">>> Skip, translation not complete")
        sys.exit(1)
    else:
        print_color(30,">>> Translation complete")

if __name__ == "__main__":
    usage='''
        python {0} --app APP (--upload) (--download)
        upload   -> will import en.json
        download -> check_progress
                    export
        '''.format(sys.argv[0])
    parser = OptionParser(usage=usage)
    parser.add_option("--app"      , dest="app"      , default=None)
    parser.add_option("--upload"   , dest="upload"   , default=False , action="store_true" )
    parser.add_option("--download" , dest="download" , default=False , action="store_true" )
    (options, args) = parser.parse_args()

    if options.app == None and os.getenv('JOB_NAME') == None:
        print_color(31,usage)
        sys.exit(1)

    if options.upload and options.download:
        print_color(31,usage)
        sys.exit(1)

    # General
    if options.app:
        app=options.app
    else:
        app=os.getenv('JOB_NAME').split('-')[1]
    print_color(30,">>> app = {}".format(app))
    app_lock=os.path.join('/data/ops/ci/for_translate/poe_lock',app)
    main = POE(app)

    if options.upload:
        repo = git.Repo(os.getenv("WORKSPACE"))
        git  = repo.git
        commit_auth=git.log('-1','--pretty=format:"%an"').replace('"','')
        if commit_auth == 'genchsusu':
            print_color(31,">>> Auth = devops, Skip")
            sys.exit(1)
        print_color(32,">>> Upload Terms")
        main.upload()
        if not os.path.exists(app_lock):
            os.mknod(app_lock)

    if options.download:
        if not os.path.exists(app_lock):
            print_color(31,">>> Skip, doesn't need to do download ")
            sys.exit(1)
        #check_progress(app)
        try:
            main.export()
        except Exception as e:
            print_color(31,">>> Export Failed") 
        else:
            print_color(30,">>> Done, push to github")
            repo = git.Repo(os.getenv("WORKSPACE"))
            git  = repo.git
            git.add('-A')
            git.commit('-m','add locales json files')
            os.system('git log -2')
            os.system('git push {}'.format(os.getenv('branch')))
            #git.push()
            os.remove(app_lock)
