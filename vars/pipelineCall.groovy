#! groovy

/*
1. Map map变量中只包含获取apollo信息的相关配置，例如：env, cluster, namespace, appid等
2. props为apollo配置json数据，后续构建所有变量从props和环境变量（env）中获取

jenkins插件需求
- HTTP Request Plugin：使用httpRequest获取apollo配置
- Pipeline Utility Steps
*/

def configMap(env,appId,namespace,cluster){
    switch(env) {
        case ["fat"]:
            apolloBaseUrl = 'http://apollo-fat.shub.us'
            break
        case ["uat"]:
            apolloBaseUrl = 'http://apollo-uat.shub.us'
            break
        case ["pro"]:
            apolloBaseUrl = 'http://apollo-pro.shub.us'
            break
        default:
            sh "echo 'env error'"
    }

    def apolloUrl = "${apolloBaseUrl}/configfiles/json/${appId}/${cluster}/${namespace}"
    def getConfig = httpRequest(url: apolloUrl, contentType: 'APPLICATION_JSON')
    def config = readJSON text: getConfig.content

    return config
}

def call(Map map) {
    def props = configMap(map.ENV,map.APPID,map.NAMESPACE,map.CLUSTER)

    if (props.PROJECT == "rnpos") {
        timestamps {
            node('master'){
                buildSteps = props.STEPS.replaceAll(/^\"|\"$/,'').split(',')
                echo "-- These steps will be run: $buildSteps"

                def work_space = env.WORKSPACE
                def script_path = work_space.split("@")[0]
                def func_path = sh returnStdout: true, script: "set +x && find $script_path@libs -name functions.groovy"

                func = load func_path.trim()
            }

            func.initial(props)
            
            try{
                for(step in buildSteps){
                    stage(">>> ${step}"){
                        func."${step}"()
                    }
                }
            }catch(ex) {
                print(ex)
                func.afterDeployFailed()
            }
        }
    } else if (type == "gradle") {
        print(">>> else pipeline")
    }
}
