#!/bin/bash

# AWS Lambda Deployment Script for DataUSA Sync Function
# This script packages the Lambda function with all dependencies

set -e

echo "🚀 Starting AWS Lambda deployment preparation..."

# Configuration
FUNCTION_NAME="datausa-sync-function"
PACKAGE_NAME="lambda-deployment.zip"
BUILD_DIR="build"
LAYER_DIR="python"

# Clean up previous builds
echo "🧹 Cleaning up previous builds..."
rm -rf $BUILD_DIR
rm -f $PACKAGE_NAME

# Create build directory structure
echo "📁 Creating build directory structure..."
mkdir -p $BUILD_DIR/$LAYER_DIR

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt -t $BUILD_DIR/$LAYER_DIR/

# Copy the Lambda function code
echo "📋 Copying Lambda function code..."
cp datausa_sync.py $BUILD_DIR/

# Create the deployment package
echo "📦 Creating deployment package..."
cd $BUILD_DIR
zip -r ../$PACKAGE_NAME . -x "*.pyc" "*/__pycache__/*" "*/test*" "*/tests/*"
cd ..

# Display package info
echo "📊 Package information:"
echo "Package size: $(du -h $PACKAGE_NAME | cut -f1)"
echo "Package location: $(pwd)/$PACKAGE_NAME"

echo "✅ Deployment package created successfully!"
echo ""
echo "Next steps:"
echo "1. Upload $PACKAGE_NAME to AWS Lambda"
echo "2. Set the handler to 'datausa_sync.lambda_handler'"
echo "3. Set the runtime to Python 3.9 or higher"
echo "4. Set timeout to 120 seconds (for API calls)"
echo "5. Set memory to 512 MB"
echo "6. Set environment variable S3_BUCKET_NAME to your bucket name"
echo "7. Configure appropriate IAM permissions for S3 access"
echo "8. IMPORTANT: Ensure Lambda has internet access (remove from VPC if needed)"
echo ""
echo "To deploy using AWS CLI:"
echo "aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$PACKAGE_NAME"
echo "aws lambda update-function-configuration --function-name $FUNCTION_NAME --timeout 120 --memory-size 512"
