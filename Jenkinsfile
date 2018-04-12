pipeline {
  agent {
    node {
      label 'master'
    }
    
  }
  stages {
    stage('Checkout') {
      steps {
        sh 'git rev-parse --short HEAD'
      }
    }
    stage('Archive') {
      agent {
        node {
          label 'master'
        }
        
      }
      steps {
        sh "tar --exclude=\".git\" --exclude=\"Jenkinsfile\" -zcvf python-${GIT_COMMIT.substring(0,6)}.tgz ./*"
        archiveArtifacts '*.tgz'
      }
    }
  }
}