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
        sh '''sudo su -
        cd /root
git clone https://github.com/storehubdeploy/cicd.git'''
      }
    }

  }
}
