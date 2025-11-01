
---

## 🐍 File 2: `src/lambda_function.py`

```python
"""
AWS IAM Security Monitor
Automatically scans IAM for security risks and sends alerts.
Author: Your Name
Date: 2024
"""

import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    """
    Main Lambda function to scan IAM security issues
    
    Args:
        event: Lambda event object
        context: Lambda context object
    
    Returns:
        dict: Execution results
    """
    print("🚀 Starting IAM security scan...")
    
    # Initialize AWS clients
    iam = boto3.client('iam')
    sns = boto3.client('sns')
    
    # Configuration - Update with your SNS Topic ARN
    SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN_HERE"  # Replace with your actual ARN
    
    security_issues = []
    scanned_users = 0
    
    try:
        # Get IAM users
        print("📋 Step 1: Listing IAM users...")
        users_response = iam.list_users(MaxItems=50)
        users = users_response['Users']
        scanned_users = len(users)
        
        print(f"🔍 Scanning {scanned_users} IAM users...")
        
        # Check each user for security issues
        for user in users:
            username = user['UserName']
            print(f"   👤 Checking user: {username}")
            
            # Check for old access keys
            try:
                keys_response = iam.list_access_keys(UserName=username)
                
                for key in keys_response['AccessKeyMetadata']:
                    key_id_short = key['AccessKeyId'][-4:]  # Last 4 chars for security
                    create_date = key['CreateDate']
                    
                    # Calculate key age in days
                    now = datetime.now(create_date.tzinfo)
                    key_age_days = (now - create_date).days
                    
                    print(f"      🔑 Key ...{key_id_short}: {key_age_days} days old")
                    
                    # Check if key is too old
                    if key_age_days > 90:
                        issue_msg = f"🚨 OLD ACCESS KEY: User '{username}' has {key_age_days}-day-old key"
                        security_issues.append(issue_msg)
                        print(f"      ⚠️  {issue_msg}")
                    else:
                        print(f"      ✅ Key is within compliance ({key_age_days} days)")
                        
            except Exception as e:
                error_msg = f"⚠️ ERROR: Failed to check user '{username}': {str(e)}"
                security_issues.append(error_msg)
                print(f"      ❌ {error_msg}")
        
        # Generate security report
        report = generate_security_report(security_issues, scanned_users)
        
        print("📧 Sending SNS notification...")
        # Send notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=report['message'],
            Subject=report['subject']
        )
        
        print("✅ Security scan completed successfully!")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Security scan completed',
                'users_scanned': scanned_users,
                'issues_found': len(security_issues),
                'scan_time': datetime.utcnow().isoformat()
            })
        }
        
    except Exception as e:
        error_message = f"❌ SCAN FAILED: {str(e)}"
        print(error_message)
        
        # Send failure notification
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"IAM Security Scan Failed:\n{error_message}",
                Subject='🔒 IAM Security Scan - FAILED'
            )
        except Exception as sns_error:
            print(f"❌ Failed to send error notification: {sns_error}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def generate_security_report(issues, user_count):
    """
    Generate formatted security report
    
    Args:
        issues (list): List of security issues found
        user_count (int): Number of users scanned
    
    Returns:
        dict: Contains message and subject for notification
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if issues:
        message = "🔒 IAM SECURITY SCAN REPORT\n\n"
        message += "🚨 SECURITY ISSUES FOUND:\n"
        message += "\n".join(issues)
        message += f"\n\n📊 SCAN SUMMARY:\n"
        message += f"• Users Scanned: {user_count}\n"
        message += f"• Issues Found: {len(issues)}\n"
        message += f"• Scan Time: {timestamp}\n"
        message += "\n⚠️  Recommended Actions:\n"
        message += "• Rotate access keys older than 90 days\n"
        message += "• Review IAM user permissions regularly"
        subject = "🚨 IAM Security Issues Found"
    else:
        message = "🔒 IAM SECURITY SCAN REPORT\n\n"
        message += "✅ ALL CLEAR! No security issues detected.\n\n"
        message += f"📊 SCAN SUMMARY:\n"
        message += f"• Users Scanned: {user_count}\n"
        message += f"• Issues Found: 0\n"
        message += f"• Scan Time: {timestamp}\n"
        message += "\n🎉 Excellent security hygiene!"
        subject = "✅ IAM Security Scan - All Clear"
    
    return {'message': message, 'subject': subject}


# Example test event for local testing
if __name__ == "__main__":
    """
    For local testing without AWS Lambda
    """
    class MockContext:
        def get_remaining_time_in_millis(self):
            return 30000
    
    # Test the function
    test_event = {}
    test_context = MockContext()
    
    result = lambda_handler(test_event, test_context)
    print("\n--- TEST RESULTS ---")
    print(json.dumps(result, indent=2))
