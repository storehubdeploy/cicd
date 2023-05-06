//=====================================init==============================================
def initial(props){
    myProps=props
}

// ===================================steps==============================================
def beforeBuild(){
    node(myProps.BUILD_SERVER){
        sh 'node -v'
        start_time = getTime()
        checkBranch()

        downloadSourceCode()
    }
}

def sonarCheck(){
    node(myProps.BUILD_SERVER){
        dir(myProps.BUILD_DIR){
//            unitTest()
//            sonarQube()
            echo "$myProps.BUILD_SERVER,$myProps.BUILD_DIR,$myProps.NODE_VERSION"
            print("This is sonarCheck.")
        }
    }
}

def linkCheck(){
    node(myProps.BUILD_SERVER){
        dir(myProps.BUILD_DIR){
//            unitTest()
//            lintTest()
            print("This is lintCheck.")
        }
    }
}

def appBuild(){ // 修改为appBuild
    node(myProps.BUILD_SERVER) {
        dir(myProps.BUILD_DIR) {
//            getApolloConfig()

            nodejs(myProps.NODE_VERSION) {
                print("This is appBuild.")
            }
        }
    }
}

def deployService(){
    print("This is deployService")
}

def afterDeployFailed(){
    node("master") {
        print(">>> Pipeline Run Failed. Please Check.")
        sendMsg()
        end_time=getTime()
    }
}


// =================================utils==============================================
def getTime(){
    date_End = sh returnStdout: true, script: "date '+%Y-%m-%d %H:%M:%S'"
    return date_End.trim()
}

def checkBranch(){
    jira_ticket = "Trunk-1.0.0"
    if(env.CHANGE_BRANCH == jira_ticket){
        print("Branch is OK.")
    }else{
        print("Branch is Error.")
    }
}

def unitTest(){
    nodejs(myProps.NODE_VERSION) {
        sh 'yarn install'
        sh 'yarn run compile'

        sh 'yarn run test:coverage'
    }
}

def lintTest(){
    nodejs(myProps.NODE_VERSION) {
        sh 'yarn lint'
    }
}

def sonarQube(){
    withSonarQubeEnv('SonarQube') {
        sh 'echo "sonar.branch.name=$GIT_BRANCH" >> sonar-project.properties'
        sh 'echo "sonar.projectVersion=$(date +"%y.%m")" >> sonar-project.properties'

        sh '/usr/local/sonar-scanner/bin/sonar-scanner'
    }
    script {
        timeout(20) {
            def qg = waitForQualityGate()
            if (qg.status != 'OK') {
                error "Pipeline failed due to Sonarqube Quality Gates! failure: ${qg.status}"
                sh 'exit 1'
            }
        }
    }
}

def downloadSourceCode(){
    cleanWs()
    git branch: env.CHANGE_BRANCH, credentialsId: myProps.CREDENTIALS_ID, url: myProps.GIT_URL
}

def sendMsg(){
    stage(">>> Send Message..."){
        print("Send Success.")
    }
}

return this;
