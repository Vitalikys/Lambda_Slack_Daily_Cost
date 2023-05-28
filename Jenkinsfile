pipeline{
    agent any
    stages {

        stage('Install packages, create ZIP'){
            steps {
                sh '''
                chmod +x ci_zip_part.sh
                ./zip_part.sh
                '''}
            }

        stage('Push to S3 Bucket, update Lambda'){
            steps {
                sh '''
                chmod +x cd_aws.sh
                ./cd_aws.sh
                '''}
            }

    }
}