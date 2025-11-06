#!/bin/bash

# Create Simple Lambda Function Package (without dependencies)
# This creates a lightweight package with just your function code

set -e

echo "🚀 Creating simple Lambda function package..."

# Configuration
FUNCTION_NAME="bls-sync-function"
PACKAGE_NAME="lambda-function-only.zip"

# Clean up previous builds
echo "🧹 Cleaning up previous builds..."
rm -f $PACKAGE_NAME

# Create the function package (just the code)
echo "📦 Creating function package..."
zip $PACKAGE_NAME lambda_function.py

# Display package info
echo "📊 Function package information:"
echo "Package size: $(du -h $PACKAGE_NAME | cut -f1)"
echo "Package location: $(pwd)/$PACKAGE_NAME"

echo "✅ Lambda function package created successfully!"
echo ""
echo "This package contains only your function code."
echo "Make sure to attach the dependencies layer in AWS Console."
