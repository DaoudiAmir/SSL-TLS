# SSL/TLS Certificate Analysis Project

A comprehensive system for analyzing SSL/TLS certificates, focusing on RSA key security analysis. This project can efficiently process millions of certificates from Certificate Transparency logs and other sources.

## Authors
- Daoudi Amir Salah Eddine
- Heloui Youssef
- Baye Diop Cheikh

## Overview

This project implements advanced cryptographic analysis tools to identify potential vulnerabilities in SSL/TLS certificates, with a particular focus on RSA key analysis. It can process certificates from various sources including Certificate Transparency logs and Let's Encrypt.

## Key Features

### Certificate Acquisition
- Efficient asynchronous downloading from Certificate Transparency logs
- Advanced proxy rotation system to avoid rate limiting
- Automated proxy testing and validation
- Support for bulk certificate processing

### Certificate Analysis
- Intelligent sorting by key size and type
- Duplicate key detection across large datasets
- Advanced cryptographic analysis using Batch GCD
- Comprehensive CSV conversion for detailed analysis
- Non-RSA certificate filtering

## Project Structure

```
.
├── CertificateAcquisition/
│   ├── AsyncDownload.py      # High-performance certificate downloader
│   ├── NewProxyList.py       # Dynamic proxy management system
│   ├── TestAllProxyList.py   # Automated proxy validation
│   ├── getNewProxyList.py    # Proxy list updater
│   └── Requirements.txt      # Acquisition module dependencies
│
├── CertificateAnalysis/
│   ├── CERT by Size/         # Organized certificate storage
│   ├── DUPES/               # Duplicate certificates storage
│   ├── GCD/                 # GCD analysis results
│   ├── CSV/                 # Certificate data in CSV format
│   ├── RemoveNotRSA.py       # Certificate type filter
│   ├── Sort.py              # Multi-threaded certificate sorter
│   ├── certtocsv.py         # Data conversion utility
│   ├── findDupes.py         # Duplicate detection system
│   ├── findGCD.py           # Cryptographic analysis tool
│   ├── run_analysis_only.sh # Standalone analysis script
│   └── Requirements.txt     # Analysis module dependencies
│
└── projectGUI.sh            # Interactive control interface
```

## System Requirements

- Python 3.x (Tested on Python 3.10.2)
- Linux/Unix-based system or Windows with WSL
- Minimum 8GB RAM (16GB recommended for large datasets)
- Sufficient storage space for certificate processing

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Choose your execution method:

   ### Option 1: GUI Interface (Recommended)
   ```bash
   chmod +x projectGUI.sh
   ./projectGUI.sh
   ```
   The GUI will automatically:
   - Install required system packages
   - Configure Python virtual environments
   - Install Python dependencies
   - Set up certificate storage

   ### Option 2: Manual Installation
   ```bash
   # Set up Certificate Acquisition environment
   cd CertificateAcquisition
   python -m venv .
   source bin/activate  # or 'activate' on Windows
   pip install -r Requirements.txt
   deactivate

   # Set up Certificate Analysis environment
   cd ../CertificateAnalysis
   python -m venv .
   source bin/activate  # or 'activate' on Windows
   pip install -r Requirements.txt
   deactivate
   ```

## Usage Guide

### 1. Interactive GUI Mode (Recommended)
Run `./projectGUI.sh` and follow the menu-driven interface to:
1. Initialize the environment
2. Update and validate proxy lists
3. Download certificates in bulk
4. Process and analyze certificates
5. Generate analysis reports

### 2. Analysis-Only Mode
For pre-downloaded certificates (already present in the folder, or unzipped from the cert by size zip file that we will provide, it contains the certificates downloaded during our project execution process):
```bash
cd CertificateAnalysis
chmod +x run_analysis_only.sh
./run_analysis_only.sh
```

### 3. Advanced Usage (Component-wise)
Execute individual components directly:
```bash
# Certificate Acquisition
cd CertificateAcquisition
source bin/activate
python AsyncDownload.py
deactivate

# Certificate Analysis
cd ../CertificateAnalysis
source bin/activate
python Sort.py
python RemoveNotRSA.py
python certtocsv.py
python findDupes.py
python findGCD.py
deactivate
```

## Implementation Details

### Certificate Acquisition
- Implements asynchronous downloading using Python's `asyncio`
- Utilizes intelligent proxy rotation to avoid rate limiting
- Includes automatic retry mechanisms with exponential backoff
- Supports resumable downloads and checkpoint saving

### Certificate Analysis
- Employs efficient batch processing for large certificate sets
- Implements optimized GCD algorithms for key analysis
- Uses multi-threading for improved performance
- Provides detailed progress tracking and logging

### Data Management
- Organized directory structure for processed certificates
- Automatic backup of critical analysis results
- CSV export functionality for external analysis
- Efficient storage management for large datasets

## Output Structure

Analysis results are organized in the following directories:
- `CertificateAnalysis/CERT by Size/`: Sorted certificates by key size
- `CertificateAnalysis/DUPES/`: Identified duplicate certificates
- `CertificateAnalysis/GCD/`: GCD analysis results
- `CertificateAnalysis/CSV/`: Generated CSV files for further analysis


## License

This project is private, contact adaoudi@et.esiea.fr

