pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/kengrary/shell.git', branch: '*/master')
        sh 'git rev-parse --short HEAD'
      }
    }
  }
}