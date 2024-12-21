"""
Certificate Duplicate Finder Module
Authors: Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

This module identifies duplicate certificates by comparing their
public key moduli. It processes certificates that have been previously
sorted by key size and identifies any duplicates within each size group.

Key Features:
- Duplicate key detection
- Size-based processing
- CSV output format
- Multi-threaded processing
"""

import os
import sys 
import pandas as pd
import threading
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import shutil

def findDupes(size):
    print("Finding Dupes in size :" + size)
    csv = open("./CERT by Size/"+size+"/"+size+".csv", "r")

    colnames=['id', 'modulus',  'exponent'] 

    df = pd.read_csv(csv, names=colnames, header=None)

    duplicateRows = df[df.duplicated(['modulus'], keep=False)]
    duplicateRows = duplicateRows.sort_values(by=["modulus"])
    pd.set_option('display.max_rows', duplicateRows.shape[0]+1)

    duplicateRows.to_csv("./DUPES/"+size+".csv", index=False)

if __name__ == "__main__":
    try:
        certList = os.listdir("./CERT by Size/")
        
        print(certList)

        for dir in certList:
            size = str(dir)

            crtlistbysize = os.listdir("./CERT by Size/" + dir)
            maxRange = len(crtlistbysize)

            findDupes(size)

    except Exception as e:
        print(e)
