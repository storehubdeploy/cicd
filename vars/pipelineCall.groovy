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
                        nodejs('v12.22.7') {
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
                        nodejs('v12.22.7') {
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
                        nodejs('v12.22.7') {
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
                    sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline success' 'Ready_For_Test'"
                }
                failure {
                    echo "failed"
                    sh "python3.6 /data/tools/change_jira.py ${env.issue}  'CI pipeline failed' 'Not_ready'"
                }
            }
        }
    } else if (type == "gradle") {
        print(">>> else pipeline")
    }
}
