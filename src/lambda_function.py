import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    print("Starting IAM security scan...")
    
    # Initialize clients
    iam = boto3.client('iam')
    sns = boto3.client('sns')
    
    # ⚠️ UPDATE THIS WITH YOUR SNS TOPIC ARN!
    SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:YOUR_CODE:iam-security-alerts"

    
    security_issues = []
    
    try:
        print("Step 1: Listing IAM users...")
        # Get only the first page of users (for testing)
        users_response = iam.list_users(MaxItems=10)
        users = users_response['Users']
        
        print(f"Found {len(users)} users to check")
        
        for user in users:
            username = user['UserName']
            print(f"Checking user: {username}")
            
            # Skip if this is taking too long
            if context.get_remaining_time_in_millis() < 10000:  # 10 seconds left
                security_issues.append("⏰ Scan incomplete due to time constraints")
                break
            
            try:
                # Check access keys
                keys_response = iam.list_access_keys(UserName=username, MaxItems=5)
                
                for key in keys_response['AccessKeyMetadata']:
                    key_id = key['AccessKeyId'][-4:]  # Last 4 chars for security
                    create_date = key['CreateDate']
                    
                    # Calculate age in days
                    now = datetime.now(create_date.tzinfo)
                    key_age_days = (now - create_date).days
                    
                    if key_age_days > 90:
                        security_issues.append(f"🚨 OLD KEY: {username} has {key_age_days}-day-old key (ID: ...{key_id})")
                    else:
                        print(f"✅ {username}: {key_age_days} days - OK")
                        
            except Exception as e:
                print(f"Error checking {username}: {str(e)}")
                security_issues.append(f"⚠️ Error checking {username}")
        
        # Create report message
        if security_issues:
            message = "🔒 IAM SECURITY SCAN RESULTS\n\n"
            message += "ISSUES:\n" + "\n".join(security_issues)
        else:
            message = "🔒 IAM SECURITY SCAN RESULTS\n\n"
            message += "✅ No security issues found!\n"
            message += f"Scanned {len(users)} users successfully."
        
        print("Sending SNS notification...")
        # Send notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject='IAM Security Scan - SUCCESS'
        )
        
        print("Scan completed successfully!")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Security scan completed',
                'users_checked': len(users),
                'issues_found': len(security_issues)
            })
        }
        
    except Exception as e:
        error_msg = f"❌ SCAN FAILED: {str(e)}"
        print(error_msg)
        
        # Send error notification
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"IAM Security Scan FAILED:\n{error_msg}",
                Subject='IAM Security Scan - FAILED'
            )
        except:
            pass  # If even SNS fails, just return error
            
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
