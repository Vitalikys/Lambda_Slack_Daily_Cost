#!/bin/bash

echo "----- Start CD part, Push Zip Packages to S3 ------"

# Copy ZIP package to S3
aws s3 cp cost_notif_$BUILD_NUMBER.zip s3://aws-packages-vit

# Update Lambda Function
aws lambda update-function-code \
    --function-name  cost-notification \
    --s3-bucket aws-packages-vit \
    --s3-key cost_notif_$BUILD_NUMBER.zip \
    --region us-east-1


echo '------------------  END CD commands ------------------'