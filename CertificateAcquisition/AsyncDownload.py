"""
Certificate Downloader Module

Authors: 
- Daoudi Amir
- Heloui Youssef
- Diop Cheikh


This module implements asynchronous certificate downloading from crt.sh.
It uses a proxy rotation system to avoid rate limiting and downloads
certificates in parallel for better performance.

Key Features:
- Asynchronous downloading using asyncio
- Proxy rotation for avoiding rate limits
- Random certificate ID selection within a range
- Automatic retry on failure
"""

import time
import requests
import os
import random
import threading
import asyncio
import sys
from NewProxyList import proxyIPs


url = "https://crt.sh/?d="

async def dlFile(minRange, maxRange,proxy=None):
	try:
		cert = random.randint(minRange, maxRange - 1)
		cert = abs(cert)

		r = requests.get(url + str(cert), timeout=4, proxies=proxy)
		if(r.status_code == 200):
			open("../Cert_Parsing/CERT/" + str(cert) +'.crt', 'wb').write(r.content)
			print("Sucess to download id = " + str(cert) + "\n\n")

			await dlFile(minRange,maxRange,proxy)
		else :
			raise Exception("Certificate not found" + str(cert))

	except Exception as e:
		#print(e)
		#print("Failed to download id = " + str(cert))

		pass


def DownloadCert(minRange, maxRange, thid):
	print("Starting thread :  " + str(thid))
	for i in range(minRange,maxRange):
		try:
			proxy = random.randint(0, len(proxyIPs) - 1)

			proxies = {
				"http": proxyIPs[proxy], "https": proxyIPs[proxy]
			}

			asyncio.run(dlFile(minRange,maxRange,proxies))

		except Exception as e:
			#print(e)
			#print("Failed to download id = " + str(cert))
			pass



if __name__ == "__main__":
	try:

		if len(sys.argv) < 2  or not(sys.argv[1].isnumeric()):
			raise Exception("Usage : AsyncDownload.py [Number of Thread]")
		thNB = int(sys.argv[1])

		maxRange = 1000000000


		part = int(maxRange/thNB)
		thList = []

		for x in range(thNB):
			thList.append( threading.Thread(target=DownloadCert, args=(part * (x-1), part * x - 1, x )) )  

		for x in thList:
			x.start()


		for x in thList:
			x.join()

	except Exception as e:
		print(e)
