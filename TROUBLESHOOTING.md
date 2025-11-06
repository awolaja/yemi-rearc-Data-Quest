# DataUSA Sync Lambda - Troubleshooting Guide

## Connection Timeout Issues

### Problem
Your Lambda function is getting connection timeouts when trying to reach `honolulu-api.datausa.io`.

### Solutions

#### 1. VPC Configuration (Most Common Issue)
If your Lambda is in a VPC, ensure it has internet access:

**Option A: Remove Lambda from VPC (Recommended)**
- Go to Lambda Console → Configuration → VPC
- Click "Edit" → "No VPC" → Save
- This gives Lambda direct internet access

**Option B: Configure VPC with Internet Access**
- Ensure your VPC has:
  - Internet Gateway attached
  - Public subnets with route to Internet Gateway (0.0.0.0/0)
  - NAT Gateway for private subnets
  - Security groups allowing outbound HTTPS (port 443)

#### 2. Lambda Configuration Updates
Update your Lambda settings:
- **Timeout**: 120 seconds (instead of 60)
- **Memory**: 512 MB (sufficient)
- **Runtime**: Python 3.9+

#### 3. Network Troubleshooting
Test connectivity from Lambda:
```python
# Add this test function to your Lambda
def test_connectivity():
    import socket
    try:
        socket.create_connection(("honolulu-api.datausa.io", 443), timeout=10)
        print("✅ Can reach DataUSA API")
        return True
    except Exception as e:
        print(f"❌ Cannot reach DataUSA API: {e}")
        return False
```

#### 4. Alternative API Endpoints
If the Honolulu API is down, try these alternatives:
- `https://api.datausa.io/tesseract/data.jsonrecords?...`
- `https://datausa.io/api/data?...`

### Deployment Commands

```bash
# Deploy with updated code
./deploy.sh

# Update Lambda function
aws lambda update-function-code \
  --function-name datausa-sync-function \
  --zip-file fileb://lambda-deployment.zip

# Update Lambda configuration
aws lambda update-function-configuration \
  --function-name datausa-sync-function \
  --timeout 120 \
  --memory-size 512
```

### Testing Steps

1. **Test locally first**:
   ```bash
   python datausa_sync.py
   ```

2. **Test in Lambda**:
   - Use the test event
   - Check CloudWatch logs for detailed error messages

3. **Monitor CloudWatch**:
   - Check for network errors
   - Verify timeout settings
   - Look for VPC-related errors

### Expected Success Response
```json
{
  "statusCode": 200,
  "body": "{\"message\": \"DataUSA API sync completed successfully\", \"summary\": {...}}"
}
```
