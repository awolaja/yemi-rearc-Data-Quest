# Yemi Rearc Data Quest

## Overview

This project is a complete solution for the Rearc Data Quest challenge. It demonstrates a data engineering pipeline that retrieves, processes, and analyzes employment data from the Bureau of Labor Statistics (BLS) Public Data API.

## Features

- **Data Retrieval**: Automated fetching of BLS employment data via public API
- **Data Processing**: Transformation of raw JSON data into structured CSV format
- **Data Analysis**: Statistical analysis and insights generation
- **Automation**: Complete pipeline script for end-to-end execution
- **Documentation**: Comprehensive documentation and usage instructions

## Project Structure

```
yemi-rearc-Data-Quest/
├── data/                   # Data directory (output files)
│   └── .gitkeep
├── scripts/                # Python scripts
│   ├── fetch_data.py      # Data retrieval from BLS API
│   ├── process_data.py    # Data processing and transformation
│   └── analyze_data.py    # Data analysis and reporting
├── docs/                   # Documentation
├── tests/                  # Test files
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── run_pipeline.sh        # Pipeline automation script
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API access)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/awolaja/yemi-rearc-Data-Quest.git
cd yemi-rearc-Data-Quest
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Complete Pipeline

The easiest way to run the entire pipeline is using the automation script:

```bash
./run_pipeline.sh
```

This script will:
1. Set up the virtual environment (if needed)
2. Install dependencies
3. Fetch data from the BLS API
4. Process the data into CSV format
5. Perform analysis and generate insights

### Running Individual Scripts

You can also run each step individually:

1. **Fetch Data**:
```bash
python3 scripts/fetch_data.py
```

2. **Process Data**:
```bash
python3 scripts/process_data.py
```

3. **Analyze Data**:
```bash
python3 scripts/analyze_data.py
```

## Data Source

This project uses the **Bureau of Labor Statistics (BLS) Public Data API**:
- API Documentation: https://www.bls.gov/developers/
- Series Used: CES0000000001 (All Employees, Total Nonfarm)
- No API key required for basic usage

## Output Files

The pipeline generates the following files in the `data/` directory:

1. **bls_data_YYYYMMDD_HHMMSS.json**: Raw data from BLS API
2. **bls_processed_YYYYMMDD_HHMMSS.csv**: Processed and structured data
3. **bls_analysis_YYYYMMDD_HHMMSS.json**: Analysis results and statistics

## Dependencies

- `requests`: HTTP library for API calls
- `pandas`: Data manipulation and analysis
- `boto3`: AWS SDK (for potential cloud integration)
- `python-dotenv`: Environment variable management

See `requirements.txt` for specific versions.

## Testing

Run tests using:
```bash
python3 -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is created as part of the Rearc Data Quest challenge.

## Contact

Project maintained by: Yemi Awolaja

## Acknowledgments

- Rearc for the Data Quest challenge
- Bureau of Labor Statistics for the public API