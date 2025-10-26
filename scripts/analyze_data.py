#!/usr/bin/env python3
"""
Data Analytics Script for Rearc Data Quest

This script performs basic analytics on the processed BLS data.
"""

import pandas as pd
import os
import json
from datetime import datetime


def get_latest_csv_file(directory='data'):
    """
    Get the most recent CSV file from the data directory.
    
    Args:
        directory (str): Directory to search
    
    Returns:
        str: Path to the latest CSV file
    """
    csv_files = [f for f in os.listdir(directory) if f.startswith('bls_processed_') and f.endswith('.csv')]
    
    if not csv_files:
        return None
    
    csv_files.sort(reverse=True)
    return os.path.join(directory, csv_files[0])


def analyze_data(df):
    """
    Perform basic analytics on the DataFrame.
    
    Args:
        df (pandas.DataFrame): Data to analyze
    
    Returns:
        dict: Analysis results
    """
    analysis = {
        'total_records': len(df),
        'date_range': {
            'start': f"{df['year'].min()}-{df['period'].min()}",
            'end': f"{df['year'].max()}-{df['period'].max()}"
        },
        'statistics': {
            'mean_value': float(df['value'].mean()),
            'median_value': float(df['value'].median()),
            'min_value': float(df['value'].min()),
            'max_value': float(df['value'].max()),
            'std_dev': float(df['value'].std())
        },
        'yearly_average': df.groupby('year')['value'].mean().to_dict()
    }
    
    return analysis


def save_analysis(analysis, output_dir='data'):
    """
    Save analysis results to a JSON file.
    
    Args:
        analysis (dict): Analysis results
        output_dir (str): Directory to save the file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/bls_analysis_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Analysis saved to {filename}")
    return filename


def main():
    """Main function to orchestrate data analysis."""
    print("Starting BLS data analysis...")
    
    # Find the latest CSV file
    latest_file = get_latest_csv_file()
    
    if not latest_file:
        print("No CSV data files found. Please run process_data.py first.")
        return
    
    print(f"Analyzing file: {latest_file}")
    
    # Load data
    df = pd.read_csv(latest_file)
    
    # Perform analysis
    analysis = analyze_data(df)
    
    print("\n=== Analysis Results ===")
    print(f"Total Records: {analysis['total_records']}")
    print(f"Date Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
    print(f"\nStatistics:")
    print(f"  Mean Value: {analysis['statistics']['mean_value']:.2f}")
    print(f"  Median Value: {analysis['statistics']['median_value']:.2f}")
    print(f"  Min Value: {analysis['statistics']['min_value']:.2f}")
    print(f"  Max Value: {analysis['statistics']['max_value']:.2f}")
    print(f"  Standard Deviation: {analysis['statistics']['std_dev']:.2f}")
    
    print(f"\nYearly Averages:")
    for year, avg in sorted(analysis['yearly_average'].items()):
        print(f"  {year}: {avg:.2f}")
    
    # Save analysis
    output_file = save_analysis(analysis)
    print(f"\nAnalysis completed. Output: {output_file}")


if __name__ == '__main__':
    main()
