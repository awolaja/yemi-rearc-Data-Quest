import json
import os
import boto3
import requests
import time
from datetime import datetime
from botocore.exceptions import ClientError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
# Using US Census Bureau API instead of deprecated DataUSA API
API_URL = "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=us:*"
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'yemi-data-quest')
S3_PREFIX = 'part2/'
OUTPUT_FILENAME = 'population_data.json'


def fetch_population_data():
    """
    Fetch population data from the US Census Bureau API with retry logic.
    
    Returns:
        dict: JSON response from the API
    
    Raises:
        Exception: If the API request fails after all retries
    """
    print(f"INFO: Fetching data from US Census Bureau API...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Wait time between retries: {backoff factor} * (2 ^ ({number of total retries} - 1))
        status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # HTTP methods to retry
    )
    
    # Create session with retry strategy
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        print(f"INFO: Attempting to connect to US Census Bureau API...")
        response = session.get(
            API_URL, 
            headers=headers, 
            timeout=(10, 30),  # (connect timeout, read timeout)
            verify=True
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Census API returns data as a list, convert to more structured format
        if isinstance(data, list) and len(data) > 1:
            headers = data[0]  # First row contains headers
            records = data[1:]  # Rest are data records
            
            # Convert to structured format
            structured_data = {
                'headers': headers,
                'data': records,
                'total_records': len(records),
                'api_source': 'US Census Bureau ACS 2022'
            }
            print(f"INFO: Successfully fetched {len(records)} records from US Census Bureau API")
            return structured_data
        else:
            print(f"INFO: Successfully fetched data from US Census Bureau API")
            return data
    
    except requests.exceptions.ConnectTimeout as e:
        print(f"ERROR: Connection timeout to US Census Bureau API: {str(e)}")
        raise Exception(f"Unable to connect to US Census Bureau API. This may be due to network issues or VPC configuration.")
    
    except requests.exceptions.ReadTimeout as e:
        print(f"ERROR: Read timeout from US Census Bureau API: {str(e)}")
        raise Exception(f"US Census Bureau API response timeout. The server may be slow or overloaded.")
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch data from API: {str(e)}")
        raise Exception(f"API request failed: {str(e)}")
    
    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        raise


def upload_json_to_s3(s3_client, bucket, data):
    """
    Upload JSON data to S3.
    
    Args:
        s3_client: Boto3 S3 client
        bucket (str): S3 bucket name
        data (dict): JSON data to upload
    
    Returns:
        str: S3 key where the file was uploaded
    """
    s3_key = f"{S3_PREFIX}{OUTPUT_FILENAME}"
    
    try:
        # Convert data to JSON string with pretty formatting
        json_content = json.dumps(data, indent=2)
        
        # Add metadata
        metadata = {
            'source': 'us-census-bureau-api',
            'fetch_timestamp': datetime.utcnow().isoformat(),
            'record_count': str(len(data) if isinstance(data, list) else len(data.get('data', [])))
        }
        
        # Upload to S3
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=json_content.encode('utf-8'),
            ContentType='application/json',
            Metadata=metadata
        )
        
        print(f"INFO: Successfully uploaded data to s3://{bucket}/{s3_key}")
        return s3_key
    
    except ClientError as e:
        print(f"ERROR: Failed to upload to S3: {str(e)}")
        raise


def sync_datausa_to_s3():
    """
    Main function to fetch US Census Bureau API data and save to S3.
    
    Returns:
        dict: Summary of the sync operation
    """
    print("INFO: Starting US Census Bureau API sync to S3...")
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Fetch data from API
    data = fetch_population_data()
    
    # Upload to S3
    s3_key = upload_json_to_s3(s3_client, S3_BUCKET_NAME, data)
    
    summary = {
        'bucket': S3_BUCKET_NAME,
        's3_key': s3_key,
        'record_count': len(data) if isinstance(data, list) else len(data.get('data', [])),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    print(f"INFO: Sync completed successfully")
    print(f"INFO: Summary: {json.dumps(summary, indent=2)}")
    
    return summary


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event object
        context: Lambda context object
    
    Returns:
        dict: Lambda response with statusCode and body
    """
    try:
        # Validate S3 bucket name
        if not S3_BUCKET_NAME:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'S3_BUCKET_NAME environment variable is not set'
                })
            }
        
        # Execute sync
        summary = sync_datausa_to_s3()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'US Census Bureau API sync completed successfully',
                'summary': summary
            })
        }
    
    except Exception as e:
        print(f"ERROR: Lambda execution failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Sync failed',
                'message': str(e)
            })
        }


# For local testing
if __name__ == "__main__":
    print("Running US Census Bureau API sync locally...")
    try:
        result = sync_datausa_to_s3()
        print(f"\nSync completed successfully!")
        print(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"\nSync failed: {str(e)}")
