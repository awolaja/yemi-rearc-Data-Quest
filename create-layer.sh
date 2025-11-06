#!/bin/bash

# Create Lambda Layer for BLS Sync Dependencies
# This creates a reusable layer that can be attached to multiple Lambda functions

set -e

echo "🚀 Creating Lambda Layer for BLS Sync dependencies..."

# Configuration
LAYER_NAME="bls-sync-dependencies"
PACKAGE_NAME="bls-sync-layer.zip"
BUILD_DIR="layer-build"
LAYER_DIR="python"

# Clean up previous builds
echo "🧹 Cleaning up previous builds..."
rm -rf $BUILD_DIR
rm -f $PACKAGE_NAME

# Create build directory structure
echo "📁 Creating layer directory structure..."
mkdir -p $BUILD_DIR/$LAYER_DIR

# Install dependencies to the layer directory
echo "📦 Installing Python dependencies to layer..."
pip install requests==2.31.0 beautifulsoup4==4.12.2 -t $BUILD_DIR/$LAYER_DIR/

# Create the layer package
echo "📦 Creating layer package..."
cd $BUILD_DIR
zip -r ../$PACKAGE_NAME . -x "*.pyc" "*/__pycache__/*" "*/test*" "*/tests/*"
cd ..

# Display package info
echo "📊 Layer package information:"
echo "Package size: $(du -h $PACKAGE_NAME | cut -f1)"
echo "Package location: $(pwd)/$PACKAGE_NAME"

echo "✅ Lambda Layer package created successfully!"
echo ""
echo "Next steps for AWS Console:"
echo "1. Go to AWS Lambda Console > Layers"
echo "2. Click 'Create layer'"
echo "3. Upload $PACKAGE_NAME"
echo "4. Set compatible runtimes to Python 3.9, 3.10, 3.11"
echo "5. Attach this layer to your Lambda function"
echo ""
echo "To create layer via AWS CLI:"
echo "aws lambda publish-layer-version \\"
echo "    --layer-name $LAYER_NAME \\"
echo "    --zip-file fileb://$PACKAGE_NAME \\"
echo "    --compatible-runtimes python3.9 python3.10 python3.11"
