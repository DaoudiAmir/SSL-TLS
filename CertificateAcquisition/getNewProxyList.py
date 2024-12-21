import os
import requests

def download_txt_file(url, directory, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(directory, file_name)
            with open(file_path+".txt", 'wb') as file:
                file.write(response.content)
            print(f"File '{file_name}' downloaded successfully to '{directory}'.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define URL arrays for different types of files
    HTTP_urls = [
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
        'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt',
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
        # Add more HTTP file URLs here
    ]

    HTTPS_urls = [
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
        # Add more HTTPS file URLs here
    ]

    SOCKS4_urls = [
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt',
        'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt',
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt',
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
        # Add more SOCKS4 file URLs here
    ]

    SOCKS5_urls = [
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt',
        'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt',
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt',
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
        # Add more SOCKS5 file URLs here
    ]

    # Set the directory where the files will be downloaded

    # Use the arrays to download files with custom directory and filename
    for i, url in enumerate(HTTP_urls):
        download_txt_file(url, "./ProxyLIST/HTTP", str(i))

    for i, url in enumerate(HTTPS_urls):
        download_txt_file(url, "./ProxyLIST/HTTPS", str(i))

    for i, url in enumerate(SOCKS4_urls):
        download_txt_file(url, "./ProxyLIST/SOCKS4", str(i))

    for i, url in enumerate(SOCKS5_urls):
        download_txt_file(url, "./ProxyLIST/SOCKS5", str(i))
