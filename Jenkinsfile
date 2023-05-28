pipeline{
    agent any
    stages {

        stage('Install packages, create ZIP'){
            steps {
                sh '''
                chmod +x scripts/ci_zip_part.sh
                ./scripts/ci_zip_part.sh
                '''}
            }

        stage('Push to S3 Bucket, update Lambda'){
            steps {
                sh '''
                chmod +x scripts/cd_aws.sh
                ./scripts/cd_aws.sh
                '''}
            }

    }
}