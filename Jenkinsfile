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
        sh '''if [ -e python.tgz ]; then
   rm -f python.tgz
fi
tar --exclude=".git" --exclude="Jenkinsfile" -zcvf python-(${GIT_COMMIT}).substring(0,6).tgz ./*'''
      }
    }
  }
}