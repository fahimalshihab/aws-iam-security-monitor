# Complete Setup Guide

## Step 1: Create SNS Topic
1. Go to SNS Console
2. Create topic: `iam-security-alerts`
3. Subscribe your email
4. Confirm subscription via email

## Step 2: Create Lambda Function
1. Go to Lambda Console
2. Create function: `iam-security-monitor`
3. Runtime: Python 3.9
4. Upload the provided code
5. Update SNS_TOPIC_ARN in code

## Step 3: Set Permissions
Attach this policy to Lambda role:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:ListUsers",
                "iam:ListAccessKeys"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:*:*:iam-security-alerts"
        }
    ]
}

```
## Step 4: Schedule Scans
Add CloudWatch Events trigger

Schedule: rate(7 days)

Test the function

## Step 5: Verify
Check Lambda logs

Receive email report

Monitor CloudWatch metrics
