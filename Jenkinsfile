pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        sh 'git rev-parse --short HEAD'
      }
    }
  }
}