"""
GCD Analysis Module
Authors: Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

This module performs GCD (Greatest Common Divisor) analysis on certificate
public key moduli to identify potential security vulnerabilities. It processes
certificates that have been previously sorted by key size and identifies any
common factors between different certificates.

Key Features:
- GCD computation between key moduli
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
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def findGCD(size):
    print("Finding GCD in size :" + size)
    csv = open("./CERT by Size/"+size+"/"+size+".csv", "r")

    colnames=['id', 'modulus',  'exponent'] 
    df = pd.read_csv(csv, names=colnames, header=None)

    for i in range(len(df)):
        for j in range(i+1, len(df)):
            try:
                n1 = int(df.iloc[i]['modulus'])
                n2 = int(df.iloc[j]['modulus'])
                gcd_result = gcd(n1, n2)
                if gcd_result != 1:
                    print(f"Found GCD between {df.iloc[i]['id']} and {df.iloc[j]['id']}: {gcd_result}")
                    with open("./GCD/"+size+".txt", "a") as f:
                        f.write(f"{df.iloc[i]['id']},{df.iloc[j]['id']},{gcd_result}\n")
            except Exception as e:
                print(f"Error processing certificates {df.iloc[i]['id']} and {df.iloc[j]['id']}: {e}")

if __name__ == "__main__":
    try:
        certList = os.listdir("./CERT by Size/")
        print(certList)

        for dir in certList:
            size = str(dir)
            crtlistbysize = os.listdir("./CERT by Size/" + dir)
            maxRange = len(crtlistbysize)
            findGCD(size)

    except Exception as e:
        print(e)
