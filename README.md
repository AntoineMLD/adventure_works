# Adventure Works Data Pipeline

This repository contains a collection of scripts that form a data pipeline for processing and analyzing Adventure Works data. The pipeline handles various data operations including database extraction, Azure blob storage operations, and file format conversions.

## Pipeline Overview

The main pipeline consists of several components that are orchestrated by the `run_pipeline.sh` script:

1. **SAS Token Generation** (`generate_sas.py`):
   - Generates Shared Access Signature (SAS) tokens for Azure Blob Storage access
   - Saves the generated SAS URL to a file for subsequent operations

2. **Database Extraction** (`extract_data_from_bdd_to_csv.py`):
   - Connects to a SQL Server database using environment variables
   - Extracts data from specific schemas (Person, Production, Sales)
   - Saves the extracted data as CSV files in the `staging/bdd_files` directory

3. **Blob Download** (`download_blobs.py`):
   - Downloads files from Azure Blob Storage using the generated SAS token
   - Maintains the original folder structure during download
   - Provides a hierarchical view of the blob container contents

4. **Data Processing Scripts**:
   - `convert_multiple_parquet.sh`: Converts multiple Parquet files to CSV format
   - `convert_parquet_to_csv.py`: Handles individual Parquet to CSV conversion
   - `save_images_from_csv.py`: Extracts and saves images from CSV files with metadata
   - `unzip_folder.sh`: Handles decompression of downloaded ZIP files and organizes review data

## Prerequisites

- Python 3.x
- Required Python packages:
  - azure-storage-blob
  - pandas
  - pyodbc
  - python-dotenv
  - Pillow
  - pyarrow (for Parquet operations)
- ODBC Driver 18 for SQL Server
- Bash shell environment

## Environment Setup

1. Create a `.env` file in the root directory with the following variables:
   ```
   SERVER=your_server_name
   DATABASE=your_database_name
   USERNAME=your_username
   PASSWORD=your_password
   AZURE_STORAGE_CONTAINER_NAME=your_container_name
   STORAGE_CONNECTION_STRING=your_storage_connection_string
   ```

## Usage

1. Make sure all shell scripts are executable:
   ```bash
   chmod +x *.sh
   ```

2. Run the complete pipeline:
   ```bash
   ./run_pipeline.sh
   ```

   This will:
   - Generate a new SAS token
   - Extract data from the database
   - Download required blobs from Azure Storage
   - Process and organize the data in the staging directory

3. For individual component execution:
   - Convert Parquet files: `./convert_multiple_parquet.sh`
   - Process ZIP files: `./unzip_folder.sh`

## Output Directory Structure

```
staging/
├── bdd_files/          # Database extracted CSV files
├── machine_learning/   # Processed review data
└── nlp_data/          # Natural language processing data

downloaded_blobs/      # Raw downloaded files from Azure
```

## Error Handling

- All scripts include error handling and logging
- The main pipeline script (`run_pipeline.sh`) uses `set -euo pipefail` for strict error handling
- Failed operations are logged with timestamps

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository.

## License

[Add appropriate license information here]

## Contact

[Add contact information here]
