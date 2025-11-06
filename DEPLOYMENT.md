# AWS Lambda Deployment Instructions for BLS Sync Function

## Problem Solved
The error `"No module named 'requests'"` occurs because AWS Lambda doesn't include third-party Python packages like `requests` and `beautifulsoup4` by default. This guide shows you how to package these dependencies with your Lambda function.

## Files Created
- `requirements.txt` - Lists all required Python packages
- `deploy.sh` - Automated deployment script for Unix/Linux/macOS
- `lambda_function.py` - Your Lambda function code (already exists)

## Method 1: Using the Deployment Script (Recommended)

### For macOS/Linux:
```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### For Windows:
```cmd
# Install dependencies
pip install -r requirements.txt -t build/python/

# Copy Lambda function
copy lambda_function.py build\

# Create deployment package
cd build
powershell Compress-Archive -Path * -DestinationPath ..\lambda-deployment.zip
cd ..
```

## Method 2: Manual Deployment

### Step 1: Install Dependencies
```bash
# Create a build directory
mkdir build
cd build

# Install packages to the build directory
pip install -r ../requirements.txt -t .
```

### Step 2: Copy Your Function
```bash
# Copy your Lambda function code
cp ../lambda_function.py .
```

### Step 3: Create Deployment Package
```bash
# Create the zip file
zip -r ../lambda-deployment.zip . -x "*.pyc" "*/__pycache__/*"
cd ..
```

## Method 3: Using AWS CLI

### Step 1: Package the Function
```bash
# Install dependencies
pip install requests beautifulsoup4 boto3 -t ./package/

# Copy function code
cp lambda_function.py ./package/

# Create deployment package
cd package
zip -r ../lambda-deployment.zip .
cd ..
```

### Step 2: Deploy to AWS Lambda
```bash
# Update existing function
aws lambda update-function-code \
    --function-name bls-event \
    --zip-file fileb://lambda-deployment.zip

# Or create new function
aws lambda create-function \
    --function-name bls-sync-function \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda-deployment.zip \
    --timeout 300 \
    --memory-size 1024
```

## AWS Lambda Configuration

### Required Settings:
- **Runtime**: Python 3.9 or higher
- **Handler**: `lambda_function.lambda_handler`
- **Timeout**: 300 seconds (5 minutes) - BLS sync can take time
- **Memory**: 1024 MB (recommended)

### Environment Variables:
- `S3_BUCKET_NAME`: Your S3 bucket name (e.g., "yemi-data-quest")

### IAM Permissions:
Your Lambda execution role needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

## Testing Your Deployment

### Test Event:
```json
{
    "test": "event"
}
```

### Expected Response:
```json
{
    "statusCode": 200,
    "body": "{\"message\": \"BLS data sync completed successfully\", \"statistics\": {...}}"
}
```

## Troubleshooting

### Common Issues:
1. **Import errors**: Make sure all dependencies are packaged
2. **Timeout errors**: Increase Lambda timeout to 5 minutes
3. **Permission errors**: Check IAM role has S3 permissions
4. **Memory errors**: Increase Lambda memory to 1024 MB

### Debugging:
- Check CloudWatch logs for detailed error messages
- Test locally first: `python lambda_function.py`
- Verify S3 bucket exists and is accessible

## Package Size Considerations

The deployment package will be larger due to dependencies:
- `requests`: ~1.5 MB
- `beautifulsoup4`: ~0.5 MB
- `boto3`: ~50 MB (but already available in Lambda)

Total package size: ~2-3 MB

## Next Steps

1. Run the deployment script: `./deploy.sh`
2. Upload `lambda-deployment.zip` to AWS Lambda
3. Configure environment variables
4. Test the function
5. Set up CloudWatch Events for scheduling (optional)

## Alternative: Lambda Layers

For reusable dependencies, consider creating a Lambda Layer:
```bash
# Create layer package
mkdir layer
pip install requests beautifulsoup4 -t layer/python/
cd layer
zip -r ../requests-layer.zip .
cd ..

# Upload as layer
aws lambda publish-layer-version \
    --layer-name requests-layer \
    --zip-file fileb://requests-layer.zip \
    --compatible-runtimes python3.9
```
