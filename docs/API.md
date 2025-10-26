# API Documentation

## Bureau of Labor Statistics (BLS) API

### Overview
This project uses the BLS Public Data API v2 to retrieve employment statistics.

### API Details
- **Base URL**: `https://api.bls.gov/publicAPI/v2/timeseries/data/`
- **Method**: POST
- **Authentication**: None required (public API)
- **Rate Limits**: 
  - Without registration: 25 queries per day
  - With registration: 500 queries per day

### Request Format

```json
{
  "seriesid": ["CES0000000001"],
  "startyear": "2020",
  "endyear": "2023"
}
```

### Response Format

```json
{
  "status": "REQUEST_SUCCEEDED",
  "responseTime": 123,
  "message": [],
  "Results": {
    "series": [
      {
        "seriesID": "CES0000000001",
        "data": [
          {
            "year": "2023",
            "period": "M01",
            "periodName": "January",
            "value": "157000",
            "footnotes": [
              {
                "code": "P",
                "text": "Preliminary"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Series IDs Used

#### CES0000000001
- **Title**: All Employees, Total Nonfarm
- **Survey**: Current Employment Statistics
- **Measure**: Number of employees (in thousands)
- **Frequency**: Monthly
- **Seasonality**: Seasonally Adjusted

### Period Codes

- `M01` - `M12`: Monthly data (January - December)
- `Q01` - `Q04`: Quarterly data
- `A01`: Annual data

### Status Codes

- `REQUEST_SUCCEEDED`: Request was successful
- `REQUEST_FAILED`: Request failed
- `REQUEST_NOT_PROCESSED`: Request could not be processed

### Error Handling

Common errors and solutions:

1. **Too Many Requests**
   - Error: Rate limit exceeded
   - Solution: Wait 24 hours or register for API key

2. **Invalid Series ID**
   - Error: Series not found
   - Solution: Verify series ID at BLS website

3. **Invalid Date Range**
   - Error: Date range invalid
   - Solution: Check year format (YYYY) and valid range

### Additional Resources

- [BLS Developer Portal](https://www.bls.gov/developers/)
- [BLS Series ID Finder](https://www.bls.gov/help/hlpforma.htm)
- [Data Tool](https://beta.bls.gov/dataQuery/search)

## Script APIs

### fetch_data.py

```python
fetch_bls_data(series_id='CES0000000001', start_year='2020', end_year='2023')
```
**Parameters:**
- `series_id` (str): BLS series identifier
- `start_year` (str): Starting year (YYYY format)
- `end_year` (str): Ending year (YYYY format)

**Returns:** dict - JSON response from API

```python
save_data(data, output_dir='data')
```
**Parameters:**
- `data` (dict): Data to save
- `output_dir` (str): Output directory path

**Returns:** str - Path to saved file

### process_data.py

```python
process_bls_data(data)
```
**Parameters:**
- `data` (dict): Raw BLS API response

**Returns:** pandas.DataFrame - Processed data

```python
get_latest_json_file(directory='data')
```
**Parameters:**
- `directory` (str): Directory to search

**Returns:** str - Path to latest JSON file

### analyze_data.py

```python
analyze_data(df)
```
**Parameters:**
- `df` (pandas.DataFrame): Data to analyze

**Returns:** dict - Analysis results with statistics
