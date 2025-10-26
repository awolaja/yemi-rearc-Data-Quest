# Rearc Data Quest - Setup Guide

## Quick Start

Follow these steps to get the project running:

### 1. Prerequisites Check

Before you begin, ensure you have:
- **Python 3.8+**: Check with `python3 --version`
- **pip**: Check with `pip --version`
- **git**: Check with `git --version`
- **Internet connection**: Required for API access

### 2. Clone the Repository

```bash
git clone https://github.com/awolaja/yemi-rearc-Data-Quest.git
cd yemi-rearc-Data-Quest
```

### 3. Set Up Virtual Environment (Recommended)

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected packages:
- `requests` - For API calls
- `pandas` - For data processing
- `boto3` - For AWS integration (optional)
- `python-dotenv` - For environment variables

### 5. Configure Environment (Optional)

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` to customize:
- BLS Series ID
- Date ranges
- API key (if you have one)

### 6. Run the Pipeline

**Option A: Use the automation script (Recommended)**
```bash
./run_pipeline.sh
```

**Option B: Run scripts individually**
```bash
# Step 1: Fetch data
python3 scripts/fetch_data.py

# Step 2: Process data
python3 scripts/process_data.py

# Step 3: Analyze data
python3 scripts/analyze_data.py
```

### 7. View Results

Check the `data/` directory for output files:
```bash
ls -lt data/
```

You should see:
- `bls_data_*.json` - Raw API data
- `bls_processed_*.csv` - Processed data
- `bls_analysis_*.json` - Analysis results

## Troubleshooting

### Problem: Python not found
**Solution:** Install Python 3.8 or higher from python.org

### Problem: pip install fails
**Solution:** 
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Problem: API request fails
**Possible causes:**
1. No internet connection
2. BLS API is down (check https://www.bls.gov/developers/)
3. Rate limit exceeded (wait 24 hours or get API key)

**Solution:**
- Check internet connection
- Try again later
- Register for API key at BLS website

### Problem: Permission denied on run_pipeline.sh
**Solution:**
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### Problem: Module not found errors
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running Tests

To run the test suite:
```bash
# Install test dependencies
pip install pytest

# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_fetch_data.py -v
```

## CI/CD Pipeline

This project includes a GitHub Actions workflow that:
1. Runs on every push to main
2. Runs on pull requests
3. Can be triggered manually
4. Runs daily at 2 AM UTC

View workflow runs at: `https://github.com/awolaja/yemi-rearc-Data-Quest/actions`

## Next Steps

After successful setup:
1. Review the generated data files in `data/`
2. Examine the analysis results
3. Modify scripts to fetch different BLS series
4. Explore additional BLS datasets
5. Add your own analysis logic

## Additional Resources

- [BLS API Documentation](https://www.bls.gov/developers/)
- [BLS Data Finder](https://beta.bls.gov/dataQuery/search)
- [Project Architecture](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)

## Getting Help

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Review error messages carefully
3. Check the GitHub Issues page
4. Consult BLS API documentation

## License

This project is part of the Rearc Data Quest challenge.
