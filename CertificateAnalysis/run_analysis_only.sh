#!/bin/bash

# SSL/TLS Certificate Analysis Script
# Authors: 
# - Daoudi Amir
# - Heloui Youssef
# - Baye Diop Cheikh
#
# This script performs analysis on pre-downloaded certificates.
# It assumes certificates are already present in the CERT directory.
# The script will:
# 1. Sort certificates by key size
# 2. Remove non-RSA certificates
# 3. Convert certificates to CSV format
# 4. Find duplicate certificates
# 5. Perform GCD analysis

echo "Starting certificate analysis..."

# Create necessary directories if they don't exist
mkdir -p "CERT by Size"
mkdir -p "DUPES"
mkdir -p "GCD"
mkdir -p "CSV"

# Activate Python virtual environment if it exists
if [ -f "bin/activate" ]; then
    source bin/activate
fi

# Step 1: Sort certificates by key size
echo "Sorting certificates by key size..."
python Sort.py 1

# Step 2: Remove non-RSA certificates
echo "Removing non-RSA certificates..."
python RemoveNotRSA.py

# Step 3: Convert certificates to CSV format
echo "Converting certificates to CSV format..."
python certtocsv.py

# Step 4: Find duplicate certificates
echo "Finding duplicate certificates..."
python findDupes.py

# Step 5: Perform GCD analysis
echo "Performing GCD analysis..."
python findGCD.py

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi

echo "Analysis completed!"
echo "Results can be found in:"
echo "- 'CERT by Size' directory: Sorted certificates"
echo "- 'DUPES' directory: Duplicate certificates"
echo "- 'GCD' directory: GCD analysis results"
echo "- 'CSV' directory: Certificate data in CSV format"
