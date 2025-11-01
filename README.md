# 🔒 AWS IAM Security Monitor

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Serverless](https://img.shields.io/badge/Serverless-%23FD5750.svg?style=for-the-badge&logo=serverless&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A production-ready serverless security solution that automatically scans AWS IAM for security risks and sends real-time email alerts. Built with AWS Lambda, SNS, and CloudWatch Events.

## 🛡️ What It Solves

- **🔍 Automated Security Scanning** - Continuously monitors IAM for compliance issues
- **🚨 Old Access Key Detection** - Flags access keys older than 90 days (AWS best practice)
- **📧 Real-time Alerts** - Instant email notifications via Amazon SNS
- **⏰ Scheduled Monitoring** - Runs automatically on a configurable schedule
- **💰 Cost Effective** - 100% serverless with minimal operational costs

## 📊 System Architecture

<img width="521" height="271" alt="Untitled Diagram drawio (13)" src="https://github.com/user-attachments/assets/e0beb578-7d0c-4519-95e0-2c7184e5c45f" />



## 🚀 Quick Start

### Prerequisites
- AWS Account with appropriate permissions
- Basic knowledge of AWS Console
- Email address for notifications

### ⚡ 5-Minute Deployment

#### 1. Create SNS Topic for Notifications
```bash
# Create SNS topic
aws sns create-topic --name iam-security-alerts

# Subscribe your email
aws sns subscribe \
    --topic-arn arn:aws:sns:your-region:your-account-id:iam-security-alerts \
    --protocol email \
    --notification-endpoint your-email@example.com
```

#### 2. Deploy Lambda Function
1. **Create Lambda Function** in AWS Console
   - Runtime: Python 3.9
   - Name: `iam-security-monitor`
2. **Upload code** from `src/lambda_function.py`
3. **Update SNS Topic ARN** in the code
4. **Set configuration**:
   - Memory: 256 MB
   - Timeout: 30 seconds

#### 3. Schedule Automatic Scans
- Add **CloudWatch Events trigger** to Lambda
- Use schedule expression: `rate(7 days)`
- Enable the trigger

## 🛠️ Detailed Setup

For complete step-by-step instructions with screenshots, see [SETUP.md](docs/SETUP.md).

### IAM Permissions Required
The Lambda function needs this minimal policy:

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

## 📈 Features

### 🔍 Security Checks
- ✅ **Access Key Age Analysis** - Flags keys >90 days old
- ✅ **IAM User Inventory** - Complete visibility of all IAM users
- ✅ **Compliance Monitoring** - Ensures adherence to security best practices

### 🚀 Operational Excellence
- ✅ **Serverless Architecture** - No servers to manage
- ✅ **Automatic Scaling** - Handles any number of IAM users
- ✅ **Cost Optimization** - Only runs when needed, minimal resource usage

### 📊 Monitoring & Alerting
- ✅ **Real-time Notifications** - Immediate email alerts for issues
- ✅ **Detailed Reports** - Comprehensive security summary
- ✅ **Audit Trail** - Complete logging via CloudWatch

## 📨 Sample Output

### Clean Security Report
```
🔒 IAM SECURITY SCAN REPORT

✅ ALL CLEAR! No security issues detected.

📊 SCAN SUMMARY:
• Users Scanned: 8
• Access Keys Checked: 12  
• Issues Found: 0
• Scan Time: 2024-01-15 14:30:00 UTC

🎉 Excellent security hygiene! All access keys are within compliance.
```

### Issues Detected Report
```
🔒 IAM SECURITY SCAN REPORT

🚨 SECURITY ISSUES FOUND:

🚨 OLD ACCESS KEY: User 'jenkins-ci' has 145-day-old access key
🚨 OLD ACCESS KEY: User 'deploy-user' has 92-day-old access key

📊 SCAN SUMMARY:
• Users Scanned: 8
• Access Keys Checked: 12
• Issues Found: 2
• Scan Time: 2024-01-15 14:30:00 UTC

⚠️ RECOMMENDED ACTIONS:
• Rotate access keys older than 90 days immediately
• Review key rotation policies
• Consider using temporary credentials where possible
```

## 🛠️ Customization

### Modify Security Thresholds
Edit `MAX_KEY_AGE_DAYS` in the Lambda function:
```python
MAX_KEY_AGE_DAYS = 90  # Change to 60 for stricter compliance
```

### Adjust Scan Frequency
Update CloudWatch Events schedule:
- Daily: `rate(1 day)`
- Weekly: `rate(7 days)` 
- Custom: `cron(0 9 ? * MON *)` (Every Monday at 9 AM)

### Add Additional Checks
Extend the Lambda function to check for:
- Users without MFA
- Overly permissive policies
- Unused IAM roles
- Root account activity

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Lambda timeout | Increase timeout to 60 seconds |
| No email received | Check SNS subscription is confirmed |
| Permission errors | Verify IAM policy is attached to Lambda role |
| No IAM users found | Normal for new accounts - indicates clean state |

### Monitoring & Logs
- **CloudWatch Logs**: `/aws/lambda/iam-security-monitor`
- **SNS Delivery Status**: Check SNS console for notification metrics
- **Lambda Metrics**: Monitor invocation count and duration

## 📊 Cost Analysis

| Service | Cost (Monthly) | Free Tier |
|---------|----------------|-----------|
| AWS Lambda | ~$0.05 (100 invocations) | 1M requests free |
| CloudWatch Events | ~$0.00 | Minimal usage |
| SNS Notifications | ~$0.10 (100 emails) | 1000 emails free |
| **Total** | **~$0.15** | **Mostly free** |

## 🏗️ Project Structure

```
aws-iam-security-monitor/
├── 📄 README.md                 # Project documentation
├── 📁 src/
│   └── lambda_function.py       # Main Lambda function code
├── 📁 docs/
│   └── SETUP.md                 # Detailed setup guide
├── 📁 images/                   # Architecture diagrams
└── 📄 LICENSE                   # MIT License
```

## 🛡️ Security Best Practices

This project implements several AWS security best practices:

- **Principle of Least Privilege**: Lambda function has minimal required permissions
- **Secure Credentials**: No hardcoded secrets - uses IAM roles
- **Encryption**: All data in transit encrypted via HTTPS
- **Audit Trail**: Comprehensive CloudWatch logging
- **Regular Scanning**: Continuous compliance monitoring

