pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        sh 'git rev-parse --short HEAD'
      }
    }
    stage('Archive') {
      steps {
        sh '''if [ -e python.tgz ]; then
   rm -f python.tgz
fi
tar --exclude=".git" --exclude="Jenkinsfile" -zcvf python.tgz ./*'''
      }
    }
  }
}