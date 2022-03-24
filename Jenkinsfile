pipeline {
  agent any
  stages {
    stage('') {
      agent {
        node {
          label 'master'
        }

      }
      steps {
        sh '''cd /root
git clone https://github.com/storehubdeploy/cicd.git'''
      }
    }

  }
}