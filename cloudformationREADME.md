# AWS Data Pipeline (BLS & Population Sync) with CloudFormation and CDK

This project implements an automated AWS data pipeline using **AWS Lambda**, **Amazon S3**, **Amazon EventBridge**, and **AWS CDK (Python)**.  
It synchronizes BLS datasets, fetches population data, and performs automated analytics daily.

---

## Architecture Overview



---

##  Project Architecture Overview

```
+---------------------+         +-----------------------------+
| EventBridge Schedule| ----->  | Lambda: bls_sync            |
| (Daily @ 00:00 UTC) |         | - Syncs BLS data to S3      |
+---------------------+         +-----------------------------+
                                     |
                                     |
                               +-----v------+
                               | S3 Bucket  |  (yemi-data-quest)
                               +------------+
                                     |
+---------------------+         +---v----------------------------+
| EventBridge Schedule| ----->  | Lambda: datausa_sync           |
| (Daily @ 00:00 UTC) |         | - Fetches population API       |
+---------------------+         | - Stores JSON to S3/API_DATA/  |
                                +--------------------------------+
                                          |
                                          v (on S3 PUT)
                                +----------------------+
                                | S3 Event Notification|
                                +----------------------+
                                          |
                                          v
                                    +------------+
                                    |   SQS Queue |
                                    +------------+
                                          |
                                          v
                              +--------------------------+
                              | Lambda: analytics         |
                              | - Processes new JSON file |
                              | - Logs computed reports   |
                              +--------------------------+
```

---

##  Breakdown by Part

###  Part 1: Sync BLS Dataset to S3


---

## Components

### Part 1 – BLS Sync Lambda (`bls_sync`)
- Downloads data from the [BLS public dataset](https://download.bls.gov/pub/time.series/pr/).  
- Syncs only new or updated files into `s3://yemi-data-quest/bls/`.  
- Runs daily at **00:00 UTC** using **Amazon EventBridge**.  
- Implemented as a **Python 3.9 Lambda**.

### Part 2 – Population Data Sync (`datausa_sync`)
- Fetches population data from the [DataUSA API](https://datausa.io/api/data?drilldowns=Nation&measures=Population).  
- Saves timestamped JSON results to `s3://yemi-data-quest/API_DATA/`.  
- Scheduled daily at **00:00 UTC** using **EventBridge**.

### Part 3 – Analytics Processor (`analytics`)
- Triggered by **S3 → SQS** notifications when new population data arrives.  
- For each file:
  - Loads BLS data (`pr.data.0.Current`) from S3.  
  - Loads the new population JSON file.  
  - Computes:
    - Mean and standard deviation of U.S. population (2013–2018).  
    - Best year by total value for each `series_id`.  
    - Join of `series_id = PRS30006032` and `period = Q01` with matching year’s population.  
  - Outputs logs to **CloudWatch Logs**.

### Part 4 – Infrastructure as Code (IaC)
Infrastructure is defined using **AWS CDK (Python)**:
- 3 Lambda functions  
- 1 S3 bucket (external or referenced)  
- 1 SQS queue  
- 2 EventBridge rules  
- 1 S3 notification trigger  
- IAM roles and permissions  

---

## CloudFormation Template (Standalone `bls_sync` Deployment)

The `template.yaml` file defines a minimal CloudFormation stack for the `bls_sync` Lambda function.

### Resources Created
- **AWS Lambda Function (`bls_sync`)**  
  Executes Python code from an S3-deployed ZIP file.
- **IAM Role (`lambda_exec_role`)**  
  Allows writing logs to CloudWatch.
- **EventBridge Rule (`daily-run`)**  
  Runs the Lambda daily at midnight UTC.
- **Lambda Permission (`AllowExecutionFromCloudWatch`)**  
  Grants EventBridge permission to invoke the Lambda.

### Prerequisites
1. Upload `lambda/bls_sync.zip` to an S3 bucket.  
2. Update `S3Bucket` and `S3Key` in `template.yaml` accordingly.

### Deployment
```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name bls-sync-stack \
  --capabilities CAPABILITY_IAM

---

## Getting Started

### 1. Install CDK and Dependencies
npm install -g aws-cdk
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**requirements.txt**
```txt
aws-cdk-lib>=2.0.0
constructs>=10.0.0
```

### 2. Bootstrap Environment
```bash
cdk bootstrap
```

### 3. Deploy the Stack
```bash
cdk deploy
```

---

##  Project Structure

```
.
├── lambda/
│   ├── bls_sync.py
│   ├── datausa_sync.py
│   └── analytics.py
├── data_pipeline_cdk/
│   ├── __init__.py
│   └── data_pipeline_stack.py
├── template.yaml
├── app.py
├── cdk.json
└── requirements.txt

```

---

##  Future Improvements

- Add IAM policies with least privilege
- Log results to S3 or a database instead of CloudWatch
- Extend analytics using AWS Glue or Athena
- Add retries and DLQ for failed SQS messages

---

##  Contact

Maintained by: Yemi Awolaja
