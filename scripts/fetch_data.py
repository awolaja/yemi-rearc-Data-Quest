#!/usr/bin/env python3
"""
Data Retrieval Script for Rearc Data Quest

This script retrieves data from the Bureau of Labor Statistics (BLS) API
and saves it to a local file for further processing.
"""

import os
import requests
import json
from datetime import datetime


def fetch_bls_data(series_id='CES0000000001', start_year='2020', end_year='2023'):
    """
    Fetch data from BLS API for a specific series.
    
    Args:
        series_id (str): BLS series ID to fetch
        start_year (str): Start year for data retrieval
        end_year (str): End year for data retrieval
    
    Returns:
        dict: JSON response from BLS API
    """
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    
    headers = {'Content-type': 'application/json'}
    
    data = json.dumps({
        "seriesid": [series_id],
        "startyear": start_year,
        "endyear": end_year
    })
    
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from BLS API: {e}")
        return None


def save_data(data, output_dir='data'):
    """
    Save the fetched data to a JSON file.
    
    Args:
        data (dict): Data to save
        output_dir (str): Directory to save the data
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/bls_data_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to {filename}")
    return filename


def main():
    """Main function to orchestrate data retrieval."""
    print("Starting BLS data retrieval...")
    
    # Fetch data from BLS API
    # Using CES0000000001 - All Employees, Total Nonfarm
    data = fetch_bls_data(series_id='CES0000000001', 
                         start_year='2020', 
                         end_year='2023')
    
    if data and data.get('status') == 'REQUEST_SUCCEEDED':
        print("Successfully fetched data from BLS API")
        filename = save_data(data)
        print(f"Data retrieval completed. File saved: {filename}")
        return filename
    else:
        print("Failed to fetch data from BLS API")
        if data:
            print(f"Status: {data.get('status')}")
            print(f"Message: {data.get('message', [])}")
        return None


if __name__ == '__main__':
    main()
