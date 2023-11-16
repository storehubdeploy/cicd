import os, sys, json
import argparse
import requests
from ruamel.yaml import YAML

def call(cmd, silent=False):
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
    out = temp_file_stdout.read().decode().strip()
    temp_file_stdout.close()
    temp_file_stderr.seek(0)
    err = temp_file_stderr.read().decode().strip()
    temp_file_stderr.close()

    return CallResult(out, err, result.returncode)

# Global Params
git_rev = call('git rev-parse  HEAD').out[0:8]

def print_color(color, text):
    print("\033[1;{0}m{1}\033[0m".format(color, text))


def die(text):
    print_color(31, text)
    sys.exit(1)


def match_env(file_1=".env.example", file_2=".env", extra=["PORT"]):
    if not os.path.exists(file_2):
        die(">>> dotenv files not exists")

    class Properties(object):
        def __init__(self, file):
            self.properties = {}
            with open(file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.find('=') > 0 and not line.startswith('#'):
                        strs = line.split('=')
                        self.properties[strs[0].strip()] = strs[1].strip()

        def get_keys(self):
            return self.properties

        def get_value(self, key, default_value=''):
            if key in self.properties:
                return self.properties[key]
            return default_value

    arr1 = Properties(file_1).get_keys()
    arr2 = Properties(file_2).get_keys()
    set_extra = ()
    set_1 = ()
    set_2 = ()

    set_extra = set(extra)
    set_1 = set(arr1) - set_extra
    set_2 = set(arr2) - set_extra

    set_more1 = ()
    set_more2 = ()

    set_1_2 = set_1 & set_2
    set_more1 = set_1 - set_1_2
    #set_more2 = set_2 - set_1_2
    if len(set_more1) > 0:
        die('>>>{} NOT FOUND in {}'.format(set_more1, file_2))
   

def generate_yaml(app, env, cluster):
    yaml = YAML(typ='safe')
    with open('./{}/values.yaml'.format(app)) as f:
        data = yaml.load(f)

    app_name = app
    name_config = '{0}-config'.format(app_name)
    data['image']['tag'] = git_rev
    data['image']['configMapref'] = name_config
    # Generate Config
    content = '''apiVersion: v1
kind: ConfigMap
metadata:
  name: {0}
data:
'''.format(name_config)
    if app.startswith("backoffice-v1-web"):
        with open("./web.backoffice-v1-web", 'r') as f:
            for line in f:
                key = line.split("=")[0]
                value = '='.join(line.split("=")[1:]).strip()
    #            if key.startswith('SH') and key.endswith('API_URL'):
    #                value = "{}-{}-{}".format(1,2,3)
                content += '  {0}: "{1}"\n'.format(key, value)
    else:
        with open("./web.{0}".format(app), 'r') as f:
            for line in f:
                key = line.split("=")[0]
                value = '='.join(line.split("=")[1:]).strip()
    #            if key.startswith('SH') and key.endswith('API_URL'):
    #                value = "{}-{}-{}".format(1,2,3)
                content += '  {0}: "{1}"\n'.format(key, value)

    with open('./{}/templates/config.yaml'.format(app), 'w') as f:
        f.write(content)

    if os.path.exists('./secret'):
        name_secret = '{0}-secret'.format(app_name)
        data['image']['secretref'] = name_secret
        # Generate Secret
        content = '''apiVersion: v1
kind: Secret
metadata:
  name: {}
type: Opaque
data:
'''.format(name_secret)

        with open('./secret', 'r') as f:
            for line in f:
                key = line.split("=")[0]
                value = '='.join(line.split("=")[1:]).strip()
                content += '  {0}: "{1}"\n'.format(key, value)
        with open('./{}/templates/secret.yaml'.format(app), 'w') as f:
            f.write(content)

    # values.yaml
    with open('./{}/values.yaml'.format(app), 'w') as file:
        yaml.dump(data, file)

    with open('./{}/Chart.yaml'.format(app)) as f:
        data_chart = yaml.load(f)

#issue gor "git": https://github.com/helm/helm/issues/6849 [if the hash code only have one char"e" will have issue like the link]
    data_chart['appVersion'] = "git"+ git_rev
    next_version = str(int(data_chart['version']) + 1)
    data_chart['version'] = next_version
    with open('./next_version', 'w') as f:
        f.write(next_version)
   
    with open('./{}/Chart.yaml'.format(app), 'w') as file:
        yaml.dump(data_chart, file)

def clean_cache():
    if app.startswith("backoffice-v1-web"):
        aname = "web.backoffice-v1-web"
    else:
        aname = "web.{}".format(app)
    for file in [aname, './secret', '.env', '.env.example']:
        if os.path.isfile(file):
            os.remove(file)


def get_yaml(app, env, cluster):
    if app.startswith("backoffice-v1-web"):
        aname = "web.backoffice-v1-web"
    else:
        aname = "web.{}".format(app)
    namespaces = [aname, 'secret']
    # Get meta Url
    if env in ['fat', 'dev', 'uat', 'pro']:
        url = 'http://apollo-{env}.shub.us'.format(env=env)
    else:
        die(">>> Can't reach Apollo")

    for namespace in namespaces:
        if app.startswith("backoffice-v1-web"):
            r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url,"backoffice-v1-web" , cluster, namespace))
        else:
            link = "{0}/configfiles/json/{1}/{2}/{3}".format(url, app, cluster, namespace)
            print(link)
            r = requests.get(link)
            print(r.status_code)
        if r.status_code == 200:
            for i in [".env", namespace]:
                with open(i, 'a') as f:
                    for k, v in r.json().items():
                        f.write("{0}={1}\n".format(k, v))
        else:
            die(">>> Config not exists")

    if app != "beep-v1-web" and app != "alertservice" and app!= "fe-logservice" and app != "puppeteerservice" and not app.startswith("core-event-consumer"): 
        print_color(32, ">>> match env check")
        match_env()

    print_color(32, ">>> Generate Yaml")
    generate_yaml(app, env, cluster)

    clean_cache()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-a", action='store', dest='app', required=True)
    parser.add_argument("-e", action='store', dest='env', required=True)
    parser.add_argument("-c", action='store', dest='cluster', default="default")

    # Params
    param = parser.parse_args()
    app = param.app
    env = param.env
    cluster = param.cluster

    # Main
    get_yaml(app, env, cluster)
