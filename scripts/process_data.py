#!/usr/bin/env python3
"""
Data Processing Script for Rearc Data Quest

This script processes the raw BLS data and transforms it into
a more usable format (CSV).
"""

import json
import pandas as pd
import os
from datetime import datetime


def load_bls_data(filepath):
    """
    Load BLS data from JSON file.
    
    Args:
        filepath (str): Path to the JSON file
    
    Returns:
        dict: Loaded JSON data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def process_bls_data(data):
    """
    Process BLS JSON data and convert to a pandas DataFrame.
    
    Args:
        data (dict): Raw BLS API response
    
    Returns:
        pandas.DataFrame: Processed data
    """
    if data.get('status') != 'REQUEST_SUCCEEDED':
        print("Error: Data request was not successful")
        return None
    
    series_data = data['Results']['series'][0]['data']
    
    # Extract relevant fields
    processed_data = []
    for item in series_data:
        processed_data.append({
            'year': item['year'],
            'period': item['period'],
            'periodName': item['periodName'],
            'value': item['value'],
            'footnotes': ', '.join([f['text'] for f in item.get('footnotes', [])])
        })
    
    df = pd.DataFrame(processed_data)
    
    # Convert value to numeric
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Sort by year and period
    df = df.sort_values(['year', 'period'])
    
    return df


def save_processed_data(df, output_dir='data'):
    """
    Save processed DataFrame to CSV.
    
    Args:
        df (pandas.DataFrame): DataFrame to save
        output_dir (str): Directory to save the file
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/bls_processed_{timestamp}.csv'
    
    df.to_csv(filename, index=False)
    print(f"Processed data saved to {filename}")
    return filename


def get_latest_json_file(directory='data'):
    """
    Get the most recent JSON file from the data directory.
    
    Args:
        directory (str): Directory to search
    
    Returns:
        str: Path to the latest JSON file
    """
    json_files = [f for f in os.listdir(directory) if f.startswith('bls_data_') and f.endswith('.json')]
    
    if not json_files:
        return None
    
    # Sort by filename (which includes timestamp)
    json_files.sort(reverse=True)
    return os.path.join(directory, json_files[0])


def main():
    """Main function to orchestrate data processing."""
    print("Starting BLS data processing...")
    
    # Find the latest JSON file
    latest_file = get_latest_json_file()
    
    if not latest_file:
        print("No JSON data files found. Please run fetch_data.py first.")
        return
    
    print(f"Processing file: {latest_file}")
    
    # Load and process data
    data = load_bls_data(latest_file)
    df = process_bls_data(data)
    
    if df is not None:
        print(f"Processed {len(df)} records")
        print("\nData preview:")
        print(df.head())
        
        # Save to CSV
        output_file = save_processed_data(df)
        print(f"\nProcessing completed. Output: {output_file}")
    else:
        print("Failed to process data")


if __name__ == '__main__':
    main()
