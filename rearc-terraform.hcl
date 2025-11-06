terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-east-1"
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}

# Attach basic Lambda logging policy
resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "bls_sync" {
  function_name = "bls_sync"
  handler       = "bls_sync.handler"
  runtime       = "python3.9"

  s3_bucket = "your-artifact-bucket"     # <-- Replace with your bucket
  s3_key    = "lambda/bls_sync.zip"

  role = aws_iam_role.lambda_exec.arn
  description = "BLS sync Lambda function"

  depends_on = [aws_iam_role_policy_attachment.lambda_logging]
}

# EventBridge (CloudWatch) Rule - runs daily at midnight UTC
resource "aws_cloudwatch_event_rule" "daily" {
  name                = "daily-run"
  schedule_expression = "cron(0 0 * * ? *)"
}

# Event Target to invoke Lambda
resource "aws_cloudwatch_event_target" "bls_target" {
  rule      = aws_cloudwatch_event_rule.daily.name
  target_id = "bls_lambda"
  arn       = aws_lambda_function.bls_sync.arn
}

# Lambda permission to allow EventBridge to invoke it
resource "aws_lambda_permission" "allow_events" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bls_sync.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily.arn
}