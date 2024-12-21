"""
RSA Certificate Filter Module
Authors: Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

This module filters out non-RSA certificates from the downloaded certificate set.
It processes each certificate file, verifies if it uses RSA encryption,
and removes those that don't.

Key Features:
- RSA certificate validation
- Batch processing of certificate files
- Automatic removal of non-RSA certificates
"""

import os
import sys 
import threading
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import shutil

def removeECC(start, end, thid, size, crtlistbysize):
    print("Starting thread :  " + str(thid))
    for i in range(start, end):
        try:
            f = open("./CERT by Size/"+ size + "/" + crtlistbysize[i], "rb")
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
            if not isinstance(cert.public_key(), rsa.RSAPublicKey):
                print(type(cert.public_key()))
                f.close()
                os.remove(f.name)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    try:
        thNB = 1

        certList = os.listdir("./CERT by Size/")

        for dir in certList:
            size = str(dir)
            crtlistbysize = os.listdir("./CERT by Size/" + dir)
            maxRange = len(crtlistbysize)

            part = int(maxRange/thNB)
            thList = []

            for x in range(thNB):
                thList.append(threading.Thread(target=removeECC, args=(part * (x-1), part * x - 1, x, size, crtlistbysize)))  

            for x in thList:
                x.start()

            for x in thList:
                x.join()
        
    except Exception as e:
        print(e)
