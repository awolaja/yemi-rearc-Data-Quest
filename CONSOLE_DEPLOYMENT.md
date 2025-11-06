# AWS Lambda Console Deployment Guide

## Method 1: Using Lambda Layers (Recommended)

### Step 1: Create the Dependencies Layer

#### Option A: Using the Script
```bash
# Run the layer creation script
chmod +x create-layer.sh
./create-layer.sh
```

#### Option B: Manual Creation
1. Create a folder called `python`
2. Install dependencies:
   ```bash
   pip install requests==2.31.0 beautifulsoup4==4.12.2 -t python/
   ```
3. Zip the `python` folder: `zip -r bls-sync-layer.zip python/`

### Step 2: Upload Layer in AWS Console
1. Go to **AWS Lambda Console** → **Layers**
2. Click **"Create layer"**
3. **Layer name**: `bls-sync-dependencies`
4. **Upload**: Select `bls-sync-layer.zip`
5. **Compatible runtimes**: Select Python 3.9, 3.10, 3.11
6. Click **"Create"**

### Step 3: Create/Update Lambda Function
1. Go to **AWS Lambda Console** → **Functions**
2. Click **"Create function"** or select existing function
3. **Function name**: `bls-sync-function`
4. **Runtime**: Python 3.9 (or higher)
5. **Handler**: `lambda_function.lambda_handler`

### Step 4: Upload Function Code
1. In your function, go to **Code** tab
2. Click **"Upload from"** → **".zip file"**
3. Upload `lambda_function.py` (or use the simple package from `create-function-only.sh`)

### Step 5: Add the Layer
1. In your function, scroll down to **Layers** section
2. Click **"Add a layer"**
3. Select **"Custom layers"**
4. Choose `bls-sync-dependencies` layer
5. Select the latest version
6. Click **"Add"**

### Step 6: Configure Environment Variables
1. Go to **Configuration** → **Environment variables**
2. Click **"Edit"**
3. Add: `S3_BUCKET_NAME` = `your-bucket-name`
4. Click **"Save"**

### Step 7: Configure Function Settings
1. Go to **Configuration** → **General configuration**
2. Click **"Edit"**
3. **Timeout**: 5 minutes (300 seconds)
4. **Memory**: 1024 MB
5. Click **"Save"**

---

## Method 2: Complete Package Upload

### Step 1: Create Complete Package
```bash
# Run the complete deployment script
chmod +x deploy.sh
./deploy.sh
```

### Step 2: Upload to Lambda Console
1. Go to **AWS Lambda Console** → **Functions**
2. Select your function
3. Go to **Code** tab
4. Click **"Upload from"** → **".zip file"**
5. Upload `lambda-deployment.zip`

---

## Method 3: Manual Console Upload

### Step 1: Prepare Dependencies
```bash
# Create build directory
mkdir lambda-package
cd lambda-package

# Install dependencies
pip install requests beautifulsoup4 -t .

# Copy function code
cp ../lambda_function.py .

# Create zip package
zip -r ../lambda-complete.zip .
cd ..
```

### Step 2: Upload in Console
1. Go to **AWS Lambda Console** → **Functions**
2. Select your function
3. Go to **Code** tab
4. Click **"Upload from"** → **".zip file"**
5. Upload `lambda-complete.zip`

---

## Troubleshooting Console Issues

### Common Problems:
1. **"No module named 'requests'"**
   - Solution: Use Method 1 (Layers) or Method 2 (Complete package)

2. **Package too large**
   - Solution: Use Method 1 (Layers) - keeps function code separate

3. **Timeout errors**
   - Solution: Increase timeout to 5 minutes in Configuration

4. **Memory errors**
   - Solution: Increase memory to 1024 MB in Configuration

### Testing Your Function:
1. Go to **Test** tab
2. Create test event:
   ```json
   {
     "test": "event"
   }
   ```
3. Click **"Test"**
4. Check **Execution result** for success

### Monitoring:
1. Go to **Monitor** tab
2. Check **CloudWatch Logs** for detailed logs
3. Look for any error messages

---

## IAM Permissions Required

Your Lambda execution role needs:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
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

---

## Quick Start Commands

```bash
# Create layer (Method 1 - Recommended)
chmod +x create-layer.sh
./create-layer.sh

# Create function package
chmod +x create-function-only.sh
./create-function-only.sh

# Or create complete package (Method 2)
chmod +x deploy.sh
./deploy.sh
```

Then follow the console steps above!
