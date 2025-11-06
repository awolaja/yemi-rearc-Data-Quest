# AWS Data Pipeline with Terraform

This Terraform project sets up an end-to-end serverless data pipeline on AWS. It automates data ingestion, processing, and basic analytics reporting using Lambda, S3, SQS, and EventBridge.

---

##  Features Overview

###  Part 1: BLS Data Sync
- **Lambda Function:** `bls_sync`
- Fetches BLS time series data and syncs it to `s3://yemi-data-quest/bls/`
- Scheduled to run daily via CloudWatch Event (EventBridge)

###  Part 2: Population Data from API
- **Lambda Function:** `datausa_sync`
- Calls the [DataUSA API](https://datausa.io/api/data?drilldowns=Nation&measures=Population)
- Stores the result as JSON in `s3://yemi-data-quest/API_DATA/`
- Also scheduled via EventBridge

###  Part 3: Analytics Processor
- **Lambda Function:** `analytics`
- Triggered whenever a new population JSON file is added to the S3 `API_DATA/` folder
- S3 event triggers SQS → which triggers the analytics Lambda
- Currently logs processing results to CloudWatch

###  Part 4: Infrastructure-as-Code
- Uses Terraform to provision:
  - Lambda functions
  - IAM roles
  - S3 bucket (reference only — ensure it exists)
  - SQS queue
  - CloudWatch Event rules
  - Lambda event source mapping (SQS → Lambda)

---

##  Project Structure

```
terraform_data_pipeline/
├── lambda/
│   ├── bls_sync.py
│   ├── datausa_sync.py
│   └── analytics.py
├── main.tf
└── README.md
```

---

##  Getting Started

### Prerequisites

- [Terraform CLI](https://developer.hashicorp.com/terraform/downloads)
- AWS CLI with credentials configured
- Python 3.9 for Lambda runtimes

---

### 1. Initialize Terraform

```bash
terraform init
```

### 2. Preview the Plan

```bash
terraform plan
```

### 3. Deploy the Stack

```bash
terraform apply
```

---

##  Notes

- The `s3://yemi-data-quest` bucket **must exist already** or be created manually.
- Make sure your Lambda IAM role has permission to:
  - Read/write to S3
  - Log to CloudWatch
  - Send/receive messages from SQS

You may extend the IAM roles or use custom policies as needed.

---

##  Maintainer

Yemi Awolaja 

