# lambda-CICD Daily Costs notification to Slack channel

[![CI-CD-Lambda-Day-Costs](https://github.com/Vitalikys/Lambda_Slack_Daily_Cost/actions/workflows/to-lambda.yml/badge.svg)](https://github.com/Vitalikys/Lambda_Slack_Daily_Cost/actions/workflows/to-lambda.yml)


- application to send notification to Slack channel.
- crontab is disabled (No EventBridge)


### Branch - "Stage-ci-cd" is for Jenkins CI-CD

#### Using scripts files for Pipeline

need to install AWS-cli on Jenkins-Master EC2 Server

```shell
sudo apt install awscli
aws configure # add credentials
```
