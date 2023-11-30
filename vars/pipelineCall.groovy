#! groovy

def send_message(status,s3,versionCode,versionNum,time_start){
    time_end=getTime()
    echo "${time_start} ==> ${time_end}"
    sh "python3.6 /data/tools/jira_issue_new.py " +
            "--status ${status} " +
            "--repo ${env.repo} " +
            "--pr_branch ${env.GIT_BRANCH} " +
            "--pgy_url ${env.pgy_url} " +
            "--report_url ${env.report_url} " +
            "--app ${env.app} " +
            "--build_url ${env.BUILD_URL} " +
            "--recipient_default ${env.channel_default} " +
            "--recipient ${env.channel} " +
            "--versionNum ${versionNum} " +
            "--versionCode ${versionCode} " +
            "--s3 ${s3} " +
            "--start \"${time_start}\" " +
            "--end \"${time_end}\" " +
            "--pr_link ${env.PR_LINK} "
}


def String get_s3(){
    if (action == "android_qaui_action") {
        node("master") {
            def dataObject = readJSON file: '/data/share/android__package/apk-rnpos-fat/output-metadata.json'
    
            s3=dataObject.S3_URL
            versionCode=dataObject.elements[0].versionCode
            versionNum=dataObject.elements[0].versionName
        }
    }else {
        s3="https://fat-rnpos-ipa.s3-ap-southeast-1.amazonaws.com/rnpos-test.ipa"
        versionCode="null"
        versionNum="null"
    }

    return [s3,versionCode,versionNum]
}


def String build_info(){
    node("master") {
        int num=readFile file: '/data/share/android__package/apk-rnpos-fat/build_nu.txt'
        echo "${num}"
        num=num+1
        echo "${num}"
        writeFile file: '/data/share/android__package/apk-rnpos-fat/build_nu.txt', text: "${num}"
    
        choose=num % 2
    
        if(choose == 1){
            action="ios_qaui_action"
        } else {
            action="android_qaui_action"
        }
    
        return action
    }
}


def getTime(){
    date_End = sh returnStdout: true, script: "date '+%Y-%m-%d %H:%M:%S'"
    return date_End.trim()
}

def call(String type,Map map) {
    if (type == "web") {
        pipeline {
            agent {
                label 'slave-03'
            }

            options {
                timeout(time: 2, unit: 'HOURS')   // timeout on whole pipeline job
            }

            environment {
                app = "backoffice-v2-webapp"
                repo = 'storehubnet/backoffice-v2-webapp'
                pr_branch = "${env.GIT_BRANCH}"
                PR_LINK = "https://github.com/${env.repo}/pull/${env.CHANGE_ID}"
                issue = """${sh(
                        returnStdout: true,
                        script: "python3.6 /data/tools/get_issue.py ${repo} ${pr_branch}"
                ).trim()}"""
                channel = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py backoffice-pipeline fat channel ${repo} ${pr_branch}"
                ).trim()}"""
                channel_default = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py backoffice-pipeline fat channel_default ${repo} ${pr_branch}"
                ).trim()}"""
                qaui_action = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py backoffice-pipeline fat qaui_action ${repo} ${pr_branch}"
                ).trim()}"""
                qaui_branch = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py backoffice-pipeline fat qaui_branch ${repo} ${pr_branch}"
                ).trim()}"""
                report_url = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py backoffice-pipeline fat report_url ${repo} ${pr_branch}"
                ).trim()}"""
            }
            stages {
                stage('Prepare env') {
                    steps {
                        nodejs('v16.20.0') {
                            script {
                                try{
                                    time_start=getTime()
                                    sh 'yarn install'
                                }
                                catch (exc) {
                                    status='"Prepare env run failed"'
                                    send_message(status,"null","null","null", time_start)
                                    sh 'exit 1'
                                }
                            }
                        }
                    }
                }
                stage('Static Code Detection') {
                    steps {
                        nodejs('v16.20.0') {
                            script {
                                try {
                                    sh 'yarn lint'
                                }
                                catch (exc) {
                                    status='"Static Code Detection failed"'
                                    send_message(status,"null","null","null",time_start)
                                    sh 'exit 1'
                                }
                            }
                        }
                    }
                }
                stage('Unit Test') {
                    steps {
                        nodejs('v16.20.0') {
                            script {
                                try {
                                    sh 'yarn test:coverage'
                                }
                                catch (exc) {
                                    status='"Unit Test run failed"'
                                    send_message(status,"null","null","null",time_start)
                                    sh 'exit 1'
                                }
                            }
                        }
                    }
                } 
//                stage('Deploy Service To Test23') {
//                    options {
//                        timeout(time: 1, unit: 'HOURS')  // timeout on this stage
//                    }
//                    steps {
//                        script{
//                            def jobBuild = build job: "02-test/test23/web-backoffice-v2-webapp-test23", parameters: [gitParameter(name: 'branch', value: "${env.issue}"), booleanParam(name: 'disallowIncomplete', value: false), string(name: 'snapshotType', value: 'formal')], propagate: false
//                            def jobResult = jobBuild.getResult()
//                            def jobURL = jobBuild.absoluteUrl
//                            echo "Build app result: ${jobResult}:${jobURL}"
//        
//                            if (jobResult != 'SUCCESS') {
//                                status='"Deploy Failed"'
//                                send_message(status,"null","null","null",time_start)
//                                sh 'exit 1'
//                            }
//                        }
//                    }
//                }
//                stage('UI Test') {
//                    steps {
//                        script {
//                            def jobBuild = build job: '00-QA/qa_automation_UI-test-web', parameters: [gitParameter(name: 'branch', value: "${env.qaui_branch}"), string(name: 'actiontags', value: "${env.qaui_action}")], propagate: false
//                            def jobResult = jobBuild.getResult()
//                            echo "Build of 'qaui_test' result: ${jobResult}"
//        
//                            if (jobResult != 'SUCCESS') {
//                                status='"UI Test Failed"'
//                                send_message(status,"null","null","null",time_start)
//                                sh 'exit 1'
//                            }
//                        }
//                    }
//                }
            }

            post {
                always {
                    cleanWs()
                    echo 'jira sendbuildinfo1'
                }
                success {
                    echo "success"
                    send_message('success',"null","null","null",time_start)
//                     sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline success' 'Ready_For_Test'"
                }
                failure {
                    echo "failed"
//                     sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline failed' 'Not_ready'"
                }
            }
        }
    } else if (type == "rnpos") {
        pipeline {
            agent {
                // label 'master'
                label 'slave-03'
            }

            options {
                timeout(time: 1, unit: 'HOURS')   // timeout on whole pipeline job
            }

            environment {
                action = build_info()
                app = "'RN POS'"
                repo = 'storehubnet/pos-v3-mobile'
                site = 'storehub.atlassian.net'
                pr_branch = "${env.GIT_BRANCH}"
                PR_LINK = "https://github.com/${env.repo}/pull/${env.CHANGE_ID}"
                jira_status = """${sh(
                        returnStdout: true,
                        script: "python3.6 /data/tools/get_jira_status.py ${env.CHANGE_BRANCH}"
                ).trim()}"""
                issue = """${sh(
                        returnStdout: true,
                        script: "python3.6 /data/tools/get_issue.py ${repo} ${pr_branch}"
                ).trim()}"""
                channel = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat channel ${repo} ${pr_branch}"
                ).trim()}"""
                qaapi_action = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat qaapi_action ${repo} ${pr_branch}"
                ).trim()}"""
                channel_default = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat channel_default ${repo} ${pr_branch}"
                ).trim()}"""
                pgy_url = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat pgy_url ${repo} ${pr_branch}"
                ).trim()}"""
                report_url = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat report_url ${repo} ${pr_branch}"
                ).trim()}"""
            }
            stages {
                stage('Prepare env') {
                    steps {
                        dir(path: 'pos-app') {
                            nodejs('v16.20.2') {
                                script {
                                    try{
                                        time_start=getTime()
                                        sh 'yarn install'
//                                         sh 'yarn run compile'
                                        sh 'echo "sonar.branch.name=$GIT_BRANCH" >> sonar-project.properties'
                                        sh 'echo "sonar.projectVersion=$(date +"%y.%m")" >> sonar-project.properties'
                                    }
                                    catch (exc) {
                                        status='"Prepare env run failed"'
                                        send_message(status,"null","null","null", time_start)
                                        sh 'exit 1'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Unit Test') {
                    steps {
                        dir(path: 'pos-app') {
                            nodejs('v16.20.2') {
                                script {
                                    try {
                                        sh 'yarn run test'

                                        echo ">>> Yarn Lint"
                                        sh 'yarn lint'
                                    }
                                    catch (exc) {
                                        status='"Unit Test Or Lint run failed"'
                                        send_message(status,"null","null","null",time_start)
                                        sh 'exit 1'
                                    }
                                }
                            }
                        }
                    }
                }
//        stage('SonarQube') {
//            steps {
//                dir(path: 'pos-app') {
//                    withSonarQubeEnv('SonarQube') {
//                        sh '/usr/local/sonar-scanner/bin/sonar-scanner'
//                    }
//                }
//                script {
//                    timeout(40) {
//                        def qg = waitForQualityGate()
//                        if (qg.status != 'OK') {
//                            error "Pipeline failed due to Sonarqube Quality Gates! failure: ${qg.status}"
//                            status='"SonarQube run failed"'
//                            send_message(status,"null","null","null",time_start)
//                            sh 'exit 1'
//                        }
//                    }
//                }
//            }
//        }
                stage('trigger test deploy') {
                    options {
                        timeout(time: 1, unit: 'HOURS')  // timeout on this stage
                    }
                    steps {
                        script{
                            if (env.jira_status == 'Ready for Release' || env.jira_status == 'Done'){
                                echo ">>> Skip."
                            } else {
                                if (action == "android_qaui_action") {
                                    jenkins_job='mobile/Android/apk-rnpos-fat-node16.20.2'
                                } else {
                                    jenkins_job='mobile/iOS/ios-rnpos-fat-node16.20.2'
                                }

                                def jobBuild = build job: "${jenkins_job}", parameters: [gitParameter(name: 'branch', value: "${env.issue}")], propagate: false
                                def jobResult = jobBuild.getResult()
                                echo "Build app result: ${jobResult}"

                                if (jobResult != 'SUCCESS') {
                                    status='"Packaging failed"'
                                    send_message(status,"null","null","null",time_start)
                                    sh 'exit 1'
                                }
                                (s3,versionCode,versionNum)=get_s3()
                            }
                        }
                    }
                }
                stage('trigger qaapi_test') {
                    steps {
                        script {
                            if (env.jira_status == 'Ready for Release' || env.jira_status == 'Done'){
                                echo ">>> Skip."
                            } else {
                                def jobBuild = build job: '00-QA/qa_automation_API-test', parameters: [gitParameter(name: 'branch', value: 'master'), string(name: 'action', value: "${env.qaapi_action}")], propagate: false
                                def jobResult = jobBuild.getResult()
                                echo "Build of 'qaapi_test' result: ${jobResult}"

                                if (jobResult != 'SUCCESS') {
                                    status='"API test failed"'
                                    send_message(status,s3,versionCode,versionNum,time_start)
                                    sh 'exit 1'
                                }
                            }
                        }
                    }
                }
                stage('trigger qaui_test') {
                    steps {
                        script {
                            // if (env.jira_status == 'Ready for Release' || env.jira_status == 'Done'){
                            if (env.jira_status != ''){
                                echo ">>> Skip."
                                s3 = "skip build and QA test"
                                versionCode = 0
                                versionNum = 0
                            } else {
                                qaui_action = """${sh(
                                        returnStdout: true,
                                        script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat ${action} ${repo} ${pr_branch}"
                                ).trim()}"""

                                if (action == "android_qaui_action") {
                                    uitest_branch="""${sh(
                                            returnStdout: true,
                                            script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat android_uitest_branch ${repo} ${pr_branch}"
                                    ).trim()}"""
                                } else {
                                    uitest_branch="""${sh(
                                            returnStdout: true,
                                            script: "/data/ops/ci/libs/get_config_return.py rnpos-pipeline fat ios_uitest_branch ${repo} ${pr_branch}"
                                    ).trim()}"""
                                }

                                def jobBuild = build job: '00-QA/qa_automation_UI-test-web_MY_MacMini', parameters: [gitParameter(name: 'branch', value: "${uitest_branch}"), string(name: 'actiontags', value: "${qaui_action}")], propagate: false
                                def jobResult = jobBuild.getResult()
                                echo "Build of 'qaui_test' result: ${jobResult}"

                                if (jobResult != 'SUCCESS') {
                                    status='"UI test failed"'
                                    send_message(status,s3,versionCode,versionNum,time_start)
                                    sh 'exit 1'
                                }
                            }
                        }
                    }
                }
            }

            post {
                always {
                    cleanWs()
                    echo 'jira sendbuildinfo1'
                    sh "rm -rf /data/share/android__package/apk-rnpos-fat/output-metadata.json"
                    // jiraSendBuildInfo branch: "${env.issue}", site: "${env.site}"
                    // jiraSendDeploymentInfo site: "${env.site}", environmentId: 'ap-southeast-1', environmentName: 'fat', environmentType: 'testing'
                }
                success {
                    echo "success"
                    send_message('success',s3,versionCode,versionNum,time_start)
//                    sh "python3.6 /data/tools/jira_issue.py success ${env.issue} ${env.repo} ${env.GIT_BRANCH} ${env.GIT_COMMIT} ${env.pgy_url} ${env.report_url} ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.BUILD_URL} ${env.channel_default} ${env.channel}"
//                    sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline success' 'Ready_For_Test'"
                }
                failure {
                    echo "failed"
//                    sh "python3.6 /data/tools/jira_issue.py failed ${env.issue} ${env.repo} ${env.GIT_BRANCH} ${env.GIT_COMMIT} ${env.pgy_url} ${env.report_url} ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.BUILD_URL} ${env.channel_default} ${env.channel}"
//                    sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline failed' 'Not_ready'"
                }
            }
        }
    } else if (type == "beepweb") {
        pipeline {
            agent {
                label 'slave-03'
            }

            options {
                timeout(time: 2, unit: 'HOURS')   // timeout on whole pipeline job
            }

            environment {
                app = "beep-v1-web"
                repo = 'storehubnet/beep-v1-web'
                pr_branch = "${env.GIT_BRANCH}"
                PR_LINK = "https://github.com/${env.repo}/pull/${env.CHANGE_ID}"
                issue = """${sh(
                        returnStdout: true,
                        script: "python3.6 /data/tools/get_issue.py ${repo} ${pr_branch}"
                ).trim()}"""
                channel = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py beep-pipeline fat channel ${repo} ${pr_branch}"
                ).trim()}"""
                channel_default = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py beep-pipeline fat channel_default ${repo} ${pr_branch}"
                ).trim()}"""
                qaui_action = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py beep-pipeline fat qaui_action ${repo} ${pr_branch}"
                ).trim()}"""
                qaui_branch = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py beep-pipeline fat qaui_branch ${repo} ${pr_branch}"
                ).trim()}"""
                report_url = """${sh(
                        returnStdout: true,
                        script: "/data/ops/ci/libs/get_config_return.py beep-pipeline fat report_url ${repo} ${pr_branch}"
                ).trim()}"""
            }
            stages {
                stage('Prepare env') {
                    steps {
                        nodejs('v12.16.1') {
                            dir("frontend") {
                                script {
                                    try{
                                        time_start=getTime()
                                        sh 'yarn install'
                                    }
                                    catch (exc) {
                                        status='"Prepare env run failed"'
                                        send_message(status,"null","null","null", time_start)
                                        sh 'exit 1'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Static Code Detection') {
                    steps {
                        nodejs('v12.16.1') {
                            dir("frontend") {
                                script {
                                    try {
                                        sh 'yarn lint'
                                    }
                                    catch (exc) {
                                        status='"Static Code Detection failed"'
                                        send_message(status,"null","null","null",time_start)
                                        sh 'exit 1'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Unit Test') {
                    steps {
                        nodejs('v12.16.1') {
                            dir("frontend") {
                                script {
                                    try {
                                        sh 'yarn test:coverage'
                                    }
                                    catch (exc) {
                                        status='"Unit Test run failed"'
                                        send_message(status,"null","null","null",time_start)
                                        sh 'exit 1'
                                    }
                                }
                            }
                        }
                    }
                } 
//                stage('Deploy Service To Test23') {
//                    options {
//                        timeout(time: 1, unit: 'HOURS')  // timeout on this stage
//                    }
//                    steps {
//                        script{
//                            def jobBuild = build job: "02-test/test23/web-backoffice-v2-webapp-test23", parameters: [gitParameter(name: 'branch', value: "${env.issue}"), booleanParam(name: 'disallowIncomplete', value: false), string(name: 'snapshotType', value: 'formal')], propagate: false
//                            def jobResult = jobBuild.getResult()
//                            def jobURL = jobBuild.absoluteUrl
//                            echo "Build app result: ${jobResult}:${jobURL}"
//        
//                            if (jobResult != 'SUCCESS') {
//                                status='"Deploy Failed"'
//                                send_message(status,"null","null","null",time_start)
//                                sh 'exit 1'
//                            }
//                        }
//                    }
//                }
//                stage('UI Test') {
//                    steps {
//                        script {
//                            def jobBuild = build job: '00-QA/qa_automation_UI-test-web', parameters: [gitParameter(name: 'branch', value: "${env.qaui_branch}"), string(name: 'actiontags', value: "${env.qaui_action}")], propagate: false
//                            def jobResult = jobBuild.getResult()
//                            echo "Build of 'qaui_test' result: ${jobResult}"
//        
//                            if (jobResult != 'SUCCESS') {
//                                status='"UI Test Failed"'
//                                send_message(status,"null","null","null",time_start)
//                                sh 'exit 1'
//                            }
//                        }
//                    }
//                }
            }

            post {
                always {
                    cleanWs()
                    echo 'jira sendbuildinfo1'
                }
                success {
                    echo "success"
                    send_message('success',"null","null","null",time_start)
//                     sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline success' 'Ready_For_Test'"
                }
                failure {
                    echo "failed"
//                     sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline failed' 'Not_ready'"
                }
            }
        }
    }
}
