import time
import requests
import threading
import os


url = "https://crt.sh/?d="
success = []


def testProxies(rangeMin, rangeMax, proxyIPs, proto):

    for i in range(rangeMin, rangeMax):
        try:
            proxy = proxyIPs[i]
            proxy = proxy.replace("\n","")

            #print(proxy)
            if "//" not in proxy:
                proxies = {
                    "http": proto + proxy, "https": proto + proxy
                }
            else :
                proxies = {
                    "http": proxy, "https": proxy
                }

            r = requests.get(url + str(1), timeout=10, proxies=proxies)
            if(r.status_code == 200):
                if "//" not in proxy:
                    success.append(proto + proxy)
                else:
                    success.append(proxy)
                # print("Downloading certificate : " + str(1) )
                open("./TEST proxy/"+str(1)+'.crt', 'wb').write(r.content)
                print(str(proxy))
            else :
                raise Exception("Certificate not found")
            #time.sleep(0)

        except Exception as e:
            #print(e)
            #print("Failed to download id = " + str(1))
            pass


#CHATGPT START
def extract_ips_from_file(file_path):
    ips = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                ips.append(line)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return ips

def extract_ips_from_directory(directory_path):
    ips_list = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            ips = extract_ips_from_file(file_path)
            ips_list.extend(ips)
    return ips_list


def get_all_directories(directory_path):
    directories = []
    if os.path.exists(directory_path):
        # Get a list of all files and directories within the specified directory
        contents = os.listdir(directory_path)
        
        # Filter out only the directories
        for item in contents:
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                directories.append(item_path)
    else:
        print("Directory not found.")
    
    return directories

#CHAT GPT END


if __name__ == "__main__":

    dirs = get_all_directories("./ProxyLIST")
    proxyList = []
    proto = ""
    for d in dirs:
        if "HTTPS" in d:
            proto = "http://"
        elif "HTTP" in d :
            proto = "http://"
        elif "SOCKS4" in d :
            proto = "socks4://"
        elif "SOCKS5" in d:
            proto = "socks5://"

        proxyList.append([extract_ips_from_directory(d), proto])
    
    thNB = 1000
    for proxyIPs in proxyList:
        maxRange = len(proxyIPs[0])
        part = int(maxRange/thNB)
        thList = []

        for x in range(thNB):
            thList.append( threading.Thread(target=testProxies, args=(part * (x-1), part * x - 1 , proxyIPs[0], proxyIPs[1])) )  


        for x in thList:
            x.start()

        print(proxyIPs[1])


        for x in thList:
            x.join()

    print(success)
    
    with open("./NewProxyList.py", 'w') as output_file:
        output_file.write("proxyIPs = [\n")
        for pair in success:
            output_file.write(f"    \"{pair}\",")
        output_file.write("]\n")

