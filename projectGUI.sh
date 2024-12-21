#!/bin/bash

# SSL/TLS Certificate Analysis Project
# Authors: 
# - Daoudi Amir
# - Heloui Youssef
# - Baye Diop Cheikh
#
# This script provides a GUI interface for our certificate analysis toolset.
# It handles the installation of required packages, certificate downloading,
# and running various analysis tools on the certificates.
#
# Main features:
# 1. Automated setup of all required dependencies
# 2. Proxy list management for certificate downloading
# 3. Certificate downloading from crt.sh
# 4. Certificate analysis (sorting, duplicate detection, GCD analysis)

echo "Installing the dialog packages for the menu to appear"

if ! command -v dialog &> /dev/null; then
    echo "dialog is not installed. We will install it ..."
    read -p "(Press Enter to Continue)" userInput
    sudo apt update
    sudo apt install -y dialog
    echo "dialog has been installed."
fi

# Function: perform_setup
# Purpose: Installs all required packages and sets up Python environments
# - Installs system packages (unzip, dialog, git, python3, etc.)
# - Sets up Python virtual environments
# - Installs Python dependencies
# - Downloads and extracts certificate archives
perform_setup() {
    dialog --clear
    echo "Performing setup..."

    # Check if all required packages are installed
    required_packages=("unzip" "dialog" "git" "python3" "python3-pip" "curl")
    missing_packages=()

    for package in "${required_packages[@]}"; do
        if ! dpkg -l | grep -q "ii  $package "; then
            missing_packages+=("$package")
        fi
    done

    # Install missing packages
    if [ ${#missing_packages[@]} -eq 0 ]; then
        echo "All required packages are already installed."
    else
        echo "Installing missing packages: ${missing_packages[*]}"
        sudo apt update
        sudo apt install "${missing_packages[@]}"
    fi
    
    # Install git-lfs for handling large files
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    sudo apt-get install git-lfs

    # Create necessary directories
    mkdir -p "CertificateAnalysis/CERT by Size"
    mkdir -p "CertificateAnalysis/DUPES"
    mkdir -p "CertificateAnalysis/GCD"
    mkdir -p "CertificateAnalysis/CSV"

    # Set up Certificate Download environment
    cd CertificateAcquisition
    python3 -m venv .
    source bin/activate
    pip install -r Requirements.txt
    cd ..
    deactivate

    # Set up Certificate Parsing environment
    cd CertificateAnalysis
    python3 -m venv .
    source bin/activate
    pip install -r Requirements.txt
    deactivate

    read -p "We will now Download the certificates archive, this may take a while. (Press Enter to Continue)" userInput
    git lfs pull

    read -p "We will now unzip the certificates, this may take a while. (Press Enter to Continue)" userInput
    unzip "CERT by Size.zip" 
    cd ..

    echo "Setup completed."
    read -p "(Press Enter to Continue)" userInput
}

# Function: proxies_update
# Purpose: Updates and tests proxy list for certificate downloading
# - Downloads latest proxy lists from various sources
# - Tests proxies to find working ones
proxies_update() {
    dialog --clear
    echo "Performing proxy list update..."

    cd CertificateAcquisition
    source bin/activate

    echo "Getting Latest proxy lists"
    python3 getNewProxyList.py

    echo "Testing all proxies to get the working ones"
    python3 TestAllProxyList.py

    cd ..
    deactivate

    echo "Proxies update completed."
    read -p "(Press Enter to Continue)" userInput
}

# Function: download_certs
# Purpose: Downloads certificates from crt.sh using proxy rotation
# - Uses AsyncDownload.py for parallel downloading
# - Implements rate limiting avoidance
download_certs() {
    dialog --clear
    echo "Downloading certificates from crt.sh..."

    cd CertificateAcquisition
    source bin/activate
    
    echo "Starting certificate download..."
    python3 AsyncDownload.py
    
    cd ..
    deactivate

    echo "Certificate download completed."
    read -p "(Press Enter to Continue)" userInput
}

# Function: sort_and_remove
# Purpose: Sorts certificates by key size and removes non-RSA certificates
# - Organizes certificates into directories by key size
# - Filters out non-RSA certificates
sort_and_remove() {
    dialog --clear
    echo "Sorting certificates and removing non-RSA ones..."

    cd CertificateAnalysis
    source bin/activate
    
    echo "Sorting certificates by key size..."
    python3 Sort.py 1
    
    echo "Removing non-RSA certificates..."
    python3 RemoveNotRSA.py
    
    cd ..
    deactivate

    echo "Sorting and filtering completed."
    read -p "(Press Enter to Continue)" userInput
}

# Function: find_Dupes
# Purpose: Identifies duplicate certificates
# - Converts certificates to CSV format
# - Compares moduli to find duplicates
find_Dupes() {
    dialog --clear
    echo "Finding duplicate certificates..."

    cd CertificateAnalysis
    source bin/activate
    
    echo "Converting certificates to CSV..."
    python3 certtocsv.py
    
    echo "Finding duplicates..."
    python3 findDupes.py
    
    cd ..
    deactivate

    echo "Duplicate analysis completed."
    read -p "(Press Enter to Continue)" userInput
}

# Function: find_GCD
# Purpose: Performs GCD analysis on certificate moduli
# - Identifies certificates sharing common factors
# - Helps detect potentially compromised keys
find_GCD() {
    dialog --clear
    echo "Performing GCD analysis..."

    cd CertificateAnalysis
    source bin/activate
    
    echo "Running GCD analysis..."
    python3 findGCD.py
    
    cd ..
    deactivate

    echo "GCD analysis completed."
    read -p "(Press Enter to Continue)" userInput
}

# Function: show_menu
# Purpose: Displays the main menu interface
# - Provides options for all major operations
# - Handles user input and navigation
show_menu() {
    dialog --clear --backtitle "Certificate Analysis Project" \
    --title "[ M A I N - M E N U ]" \
    --menu "You can use the UP/DOWN arrow keys, the first \
    letter of the choice as a hot key, or the \
    number keys 1-9 to choose an option.\
    Choose the TASK" 15 50 4 \
    1 "Perform Setup" \
    2 "Update proxy list" \
    3 "Download certificates" \
    4 "Sort and remove non RSA" \
    5 "Find duplicates" \
    6 "Find GCD" \
    7 "Exit" 2>"${INPUT}"
}

# Main menu loop
INPUT=/tmp/menu.sh.$$
trap "rm -f $INPUT" EXIT

while true; do
    show_menu
    menuitem=$(<"${INPUT}")
    case $menuitem in
        1) perform_setup;;
        2) proxies_update;;
        3) download_certs;;
        4) sort_and_remove;;
        5) find_Dupes;;
        6) find_GCD;;
        7) echo "Bye"; break;;
    esac
done