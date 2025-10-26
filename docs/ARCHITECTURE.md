# Architecture Overview

## System Design

The Rearc Data Quest solution follows a modular ETL (Extract, Transform, Load) pipeline architecture:

```
┌─────────────────┐
│   BLS API       │
│  (Data Source)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  fetch_data.py  │  ◄── Extract
│   (Retrieval)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ process_data.py │  ◄── Transform
│ (Processing)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ analyze_data.py │  ◄── Load/Analyze
│  (Analysis)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output Files   │
│  (JSON/CSV)     │
└─────────────────┘
```

## Components

### 1. Data Retrieval (fetch_data.py)
- **Purpose**: Fetch employment data from BLS Public API
- **Input**: None (uses hardcoded series ID and date range)
- **Output**: Raw JSON file with timestamp
- **API Endpoint**: https://api.bls.gov/publicAPI/v2/timeseries/data/
- **Series**: CES0000000001 (All Employees, Total Nonfarm)

### 2. Data Processing (process_data.py)
- **Purpose**: Transform raw JSON into structured CSV format
- **Input**: Latest JSON file from data directory
- **Output**: Processed CSV file with timestamp
- **Transformations**:
  - Extract relevant fields
  - Convert values to numeric
  - Sort by year and period
  - Handle footnotes

### 3. Data Analysis (analyze_data.py)
- **Purpose**: Generate statistical insights
- **Input**: Latest CSV file from data directory
- **Output**: Analysis JSON file with timestamp
- **Analytics**:
  - Descriptive statistics (mean, median, min, max, std dev)
  - Yearly averages
  - Date range summary

## Data Flow

1. **Extract Phase**:
   - HTTP POST request to BLS API
   - JSON response validation
   - Save raw data to `data/bls_data_TIMESTAMP.json`

2. **Transform Phase**:
   - Load latest JSON file
   - Parse nested JSON structure
   - Convert to pandas DataFrame
   - Apply data type conversions
   - Save to `data/bls_processed_TIMESTAMP.csv`

3. **Load/Analyze Phase**:
   - Load latest CSV file
   - Perform statistical calculations
   - Generate summary metrics
   - Save to `data/bls_analysis_TIMESTAMP.json`

## Error Handling

- API request failures are caught and logged
- File I/O errors are handled gracefully
- Missing data is managed with pandas error handling
- Pipeline continues on non-critical errors (in CI/CD)

## Automation

The `run_pipeline.sh` script orchestrates all three phases:
- Sets up Python virtual environment
- Installs dependencies
- Executes scripts in sequence
- Provides progress feedback

## Scalability Considerations

- **Modular Design**: Each component can be scaled independently
- **Time-stamped Files**: Allows historical tracking
- **Configurable Parameters**: Series ID and date ranges can be modified
- **Cloud Ready**: boto3 included for AWS integration
- **CI/CD Integration**: GitHub Actions workflow included

## Future Enhancements

1. **Database Integration**: Store processed data in PostgreSQL/MySQL
2. **Cloud Storage**: Upload to S3/Cloud Storage
3. **Visualization**: Add data visualization dashboards
4. **Alerting**: Email/Slack notifications on pipeline failures
5. **API Key Management**: Support for higher API rate limits
6. **Multiple Series**: Process multiple BLS series simultaneously
7. **Incremental Updates**: Only fetch new data since last run
