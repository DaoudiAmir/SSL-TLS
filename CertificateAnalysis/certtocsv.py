"""
Certificate to CSV Converter Module
Authors: Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

This module converts certificate files into CSV format for easier analysis.
It extracts key information from each certificate including the modulus
and exponent, organizing them by key size.

Key Features:
- Certificate data extraction
- CSV format conversion
- Size-based organization
- Batch processing capability
"""

import os
import sys 
import threading
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import shutil

def certtocsv(start, end, size, crtlistbysize):
    print("Converting cert of size :" + size)

    reset = open("./CERT by Size/"+size+"/"+size+".csv", "w")
    reset.write("\0")

    csv = open("./CERT by Size/"+size+"/"+size+".csv", "a")    
    for i in range(start, end):
        try:
            f = open("./CERT by Size/"+ size + "/" + crtlistbysize[i], "rb")
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())

            csv.write(str(crtlistbysize[i])+","+str(cert.public_key().public_numbers().n) + "," + str(cert.public_key().public_numbers().e) + "\n")

            f.close()

        except Exception as e:
            print(e)
    csv.close()

if __name__ == "__main__":
    try:
        certList = os.listdir("./CERT by Size/")

        print(certList)

        for dir in certList:
            size = str(dir)

            crtlistbysize = os.listdir("./CERT by Size/" + dir)

            maxRange = len(crtlistbysize)

            certtocsv(0, maxRange, size, crtlistbysize)

    except Exception as e:
        print(e)
