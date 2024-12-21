"""
Certificate Sorting Module
Authors: Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

This module sorts certificates by their key size and organizes them
into appropriate directories. It processes each certificate file,
extracts the key size information, and moves the file to its
corresponding size directory.

Key Features:
- Certificate key size extraction
- Automatic directory organization
- Multi-threaded processing
- Progress tracking
"""

import os
import sys 
import threading
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import shutil

def process_cert_file(cert_path):
    try:
        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
            if not isinstance(cert.public_key(), rsa.RSAPublicKey):
                os.remove(cert_path)
                raise Exception(f"Not RSA: {cert_path}")
            return cert.public_key().key_size
    except Exception as e:
        print(f"Error processing {cert_path}: {e}")
        return None

def sortCertificate(start, end, thid):
    print("Starting thread: " + str(thid))
    for size_dir in os.listdir("./CERT")[start:end]:
        size_path = os.path.join("./CERT", size_dir)
        if not os.path.isdir(size_path):
            continue
            
        for cert_file in os.listdir(size_path):
            if not cert_file.endswith('.crt'):
                continue
                
            cert_path = os.path.join(size_path, cert_file)
            key_size = process_cert_file(cert_path)
            
            if key_size is None:
                continue
                
            target_dir = os.path.join("./CERT by Size", str(key_size))
            os.makedirs(target_dir, exist_ok=True)
            
            target_path = os.path.join(target_dir, cert_file)
            shutil.copy2(cert_path, target_path)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2 or not sys.argv[1].isnumeric():
            raise Exception("Usage: Sort.py [Number of Thread]")
        
        thNB = int(sys.argv[1])
        os.makedirs("./CERT by Size", exist_ok=True)
        
        cert_dirs = os.listdir("./CERT")
        maxRange = len(cert_dirs)
        part = max(1, int(maxRange/thNB))
        
        thList = []
        for x in range(thNB):
            start = x * part
            end = min((x + 1) * part, maxRange)
            thList.append(threading.Thread(target=sortCertificate, args=(start, end, x)))
            
        for x in thList:
            x.start()
            
        for x in thList:
            x.join()
            
    except Exception as e:
        print(e)
