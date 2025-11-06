"""
Part 1: AWS S3 & Sourcing Datasets
Syncs BLS time series data from https://download.bls.gov/pub/time.series/pr/ to S3
"""

import os
import hashlib
import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urljoin
import time
import json

# Configuration
BLS_BASE_URL = "https://download.bls.gov/pub/time.series/pr/"
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "yemi-data-quest")
S3_PREFIX = "bls/pr/"  # Prefix for organizing files in S3

# Initialize S3 client
s3_client = boto3.client('s3')

def get_file_list_from_bls():
    """
    Fetch the list of files from the BLS website.
    Uses proper headers to avoid 403 Forbidden errors.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; RearcDataQuest/1.0; +https://rearc.io)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(BLS_BASE_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        files = []
        
        # Parse directory listing for file links
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('?') and href != '../':
                # Filter out directory navigation links
                if not href.endswith('/'):
                    files.append(href)
        
        print(f"INFO: Found {len(files)} files on BLS website")
        return files
    
    except requests.RequestException as e:
        print(f"ERROR: Error fetching file list from BLS: {e}")
        raise

def calculate_md5(content):
    """Calculate MD5 hash of file content"""
    return hashlib.md5(content).hexdigest()

def get_s3_file_metadata(filename):
    """
    Get metadata for a file in S3, including MD5 hash.
    Returns None if file doesn't exist.
    """
    clean_filename = filename.lstrip('/')
    s3_key = f"{S3_PREFIX}{clean_filename}"
    try:
        response = s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        # S3 ETag is MD5 for non-multipart uploads
        etag = response['ETag'].strip('"')
        return {
            'etag': etag,
            'last_modified': response['LastModified'],
            'size': response['ContentLength']
        }
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return None
        raise

def download_file_from_bls(filename):
    """Download a file from BLS website"""
    url = urljoin(BLS_BASE_URL, filename)
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; RearcDataQuest/1.0; +https://rearc.io)',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"ERROR: Error downloading {filename}: {e}")
        raise

def upload_to_s3(filename, content):
    """Upload file content to S3"""
    # Clean filename to avoid double paths
    clean_filename = filename.lstrip('/')
    s3_key = f"{S3_PREFIX}{clean_filename}"
    
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=content,
            ContentType='text/plain'
        )
        print(f"INFO: Uploaded {filename} to s3://{S3_BUCKET_NAME}/{s3_key}")
        return True
    except ClientError as e:
        print(f"ERROR: Error uploading {filename} to S3: {e}")
        return False

def get_existing_s3_files():
    """Get list of files currently in S3 bucket with the prefix"""
    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=S3_PREFIX
        )
        
        if 'Contents' not in response:
            return set()
        
        # Extract just the filenames (remove prefix)
        files = set()
        for obj in response['Contents']:
            key = obj['Key']
            if key.startswith(S3_PREFIX):
                filename = key[len(S3_PREFIX):]
                if filename:  # Ignore the prefix itself if it's a "folder"
                    files.add(filename)
        
        return files
    except ClientError as e:
        print(f"ERROR: Error listing S3 files: {e}")
        return set()

def delete_from_s3(filename):
    """Delete a file from S3"""
    clean_filename = filename.lstrip('/')
    s3_key = f"{S3_PREFIX}{clean_filename}"
    
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        print(f"INFO: Deleted {filename} from S3 (no longer exists on source)")
        return True
    except ClientError as e:
        print(f"ERROR: Error deleting {filename} from S3: {e}")
        return False

def sync_bls_to_s3():
    """
    Main sync function:
    1. Get list of files from BLS website
    2. Get list of files in S3
    3. Upload new/updated files
    4. Delete files that no longer exist on source
    """
    print(f"INFO: Starting BLS data sync to s3://{S3_BUCKET_NAME}/{S3_PREFIX}")
    
    # Get source files
    source_files = get_file_list_from_bls()
    source_files_set = set(source_files)
    
    # Get existing S3 files
    s3_files = get_existing_s3_files()
    
    # Track statistics
    stats = {
        'uploaded': 0,
        'skipped': 0,
        'deleted': 0,
        'errors': 0
    }
    
    # Process each source file
    for filename in source_files:
        try:
            # Download file content
            content = download_file_from_bls(filename)
            content_md5 = calculate_md5(content)
            
            # Check if file exists in S3 and compare
            s3_metadata = get_s3_file_metadata(filename)
            
            if s3_metadata and s3_metadata['etag'] == content_md5:
                # File exists and is identical - skip
                print(f"INFO: Skipping {filename} (already up to date)")
                stats['skipped'] += 1
            else:
                # File is new or updated - upload
                if upload_to_s3(filename, content):
                    stats['uploaded'] += 1
                else:
                    stats['errors'] += 1
            
            # Small delay to be respectful to BLS servers
            time.sleep(0.1)
            
        except Exception as e:
            print(f"ERROR: Error processing {filename}: {e}")
            stats['errors'] += 1
    
    # Delete files that no longer exist on source
    files_to_delete = s3_files - source_files_set
    for filename in files_to_delete:
        if delete_from_s3(filename):
            stats['deleted'] += 1
        else:
            stats['errors'] += 1
    
    # Print summary
    print("\n" + "="*50)
    print("Sync Summary:")
    print(f"  Files uploaded: {stats['uploaded']}")
    print(f"  Files skipped (up to date): {stats['skipped']}")
    print(f"  Files deleted: {stats['deleted']}")
    print(f"  Errors: {stats['errors']}")
    print("="*50)
    
    return stats

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Triggers the BLS to S3 sync process.
    """
    try:
        # Ensure bucket name is set
        if not os.environ.get("S3_BUCKET_NAME"):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'S3_BUCKET_NAME environment variable not set'
                })
            }
        
        # Run the sync
        stats = sync_bls_to_s3()
        
        # Return success response with statistics
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'BLS data sync completed successfully',
                'statistics': stats
            })
        }
    
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Sync failed',
                'details': str(e)
            })
        }

if __name__ == "__main__":
    # Ensure bucket name is set
    if not os.environ.get("S3_BUCKET_NAME"):
        print("WARNING: S3_BUCKET_NAME not set, using default 'rearc-bls-data'")
        print("INFO: Set via: export S3_BUCKET_NAME=your-bucket-name")
    
    sync_bls_to_s3()
