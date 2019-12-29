# import modules
import requests
import json
from bs4 import BeautifulSoup
import re
from threading import Thread

global good_list
good_list = []

def get_links(proxy_type=None):
    if proxy_type == "http":
         data = open("site urls.txt").readlines()[0]
    elif proxy_type == "https":
         data = open("site urls.txt").readlines()[1]
    elif proxy_type == "socks4":
         data = open("site urls.txt").readlines()[2]
    elif proxy_type == "socks5":
         data = open("site urls.txt").readlines()[3]
    else:
         data = ""
    return [i.strip() for i in data.split(",") if len(i) > 10]

def parse_proxies_from_html_response(response_data):
    data = re.findall(r'[\w\.-]+:[\w\.-]+', response_data, re.MULTILINE)
    proxies = []
    for i in data:
        if "." in i:
            if i.split(":")[1].isdigit():
                proxies.append(i+"\n") # add \n to make new line for saving in text file
    return proxies

def scrap_proxies(proxy_type=None):
    requests_links = get_links(proxy_type)
    print("Scraping proxies....")
    response_data = """
"""
    for i in requests_links:
        try:
            res = requests.get(i,timeout=10).text
        except:
            res = ""
        response_data += res
    proxy_list = parse_proxies_from_html_response(response_data)
    
    with open(proxy_type.upper()+"-proxies.txt","w+") as file:
        file.writelines(proxy_list)
    print("Saved Successfully!")


def check_proxy_by_url(proxy,url,timeout):
    p = dict(http=proxy, https=proxy)
    try:
        r = requests.get(url, proxies=p, timeout=timeout)
        return True
    except Exception as e:
        return False

def scan_proxies(proxy_type,proxy_list):
    global good_list
    working_list=[]
    proxy_list2 = [proxy_type.lower()+"://"+i.strip() for i in proxy_list]
    for i in proxy_list2:
        #google_check = check_proxy_by_url(i,"http://google.com",10)
        ipinfo_check = check_proxy_by_url(i,"http://ipinfo.io/json",10)
        if ipinfo_check:
            print(i,"Working.")
            working_list.append(i+"\n")# add \n to make new line for saving in text file
                
    good_list += working_list


def main(proxy_type,proxy_list):
    thread_list = []
    lists = proxy_list
    count = 0
    for l in lists:
        thread_list.append(Thread(target=scan_proxies, args=(proxy_type,[l])))
        thread_list[len(thread_list)-1].start()
        count += 1

    for x in thread_list:
        x.join()
    global good_list
    print('Proxies Scanned .')
    with open(proxy_type.upper()+"-working-proxies.txt","w+") as file:
        file.writelines(good_list)
        
def ask_proxy_type():
    proxy_type = input("Which type of proxy you want to Scrape/Scan?\n1.HTTP\n2.HTTPS\n3.SOCKS4\n4.SOCKS5\n5.Back\n==>")
    if str(proxy_type) == "1":
        return "http"
    elif str(proxy_type) == "2":
        return "https"
    elif str(proxy_type) == "3":
        return "socks4"
    elif str(proxy_type) == "4":
        return "socks5"
    elif str(proxy_type) == "5":
        ask_input()
    else:
        print("Wrong input try again!")
        ask_proxy_type()
 
def ask_input():
    user_input = input("What you want to do? (Enter 1 or 2)\n1.Scrape Proxies.\n2.Scan Proxies (Unoptimized)\n==>")
    if str(user_input) == "1":
        proxy_type = ask_proxy_type()
        scrap_proxies(proxy_type)
    elif str(user_input) == "2":
        proxy_type = ask_proxy_type()
        file = input("File Name: ")
        main(proxy_type,open(file).readlines())
    else:
        print("Wrong input try again!")
        ask_input()

if __name__ == "__main__":
    print("Welcome in Proxy Scrapper + Scanner.")
    ask_input()
