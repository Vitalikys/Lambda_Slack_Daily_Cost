#!/bin/bash

echo "----- Start CD part, Push Zip Packages to S3 ------"

# Copy ZIP package to S3
aws s3 cp cost_notif_$BUILD_NUMBER.zip s3://aws-packages-vit

# Update Lambda Function
aws lambda update-function-code \
    --function-name  cost-notification \
    --zip-file fileb://cost_notif_$BUILD_NUMBER.zip


echo '------------------  END CD commands ------------------'