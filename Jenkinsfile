#!/usr/bin/env groovy
pipeline {
  agent {
    label 'linux'
  }
  stages {
    stage('Prepare') {
      steps {
        echo 'Prepare build env...'
	sh 'git submodule update --init'
	sh 'sudo ./scripts/pkgdep.sh'
      }
    }
    stage('Build') {
      steps {
        echo 'Building...'
        sh './configure --disable-debug --enable-werror --disable-coverage --disable-ubsan'
        sh 'make'
      }
    }
    stage('Test') {
      steps {
        echo 'Testing...'
        sh './unittest.sh'
      }
    }
  }
}
