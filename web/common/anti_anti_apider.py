import requests
import random
import re
import logging

# 反反爬虫
class Anti_Anti_Spider:
    def __init__(self,ip_number,headers1,headers2):
        self.ip_number = ip_number
        self.headers1 = headers1
        self.headers2 = headers2

        # 代理池
        self.available_iplist = []

        self.proxy = {
            'http': '',
            'https': ''
        }

    # 反爬蟲(移除不能用的ip)
    def remove_error_ip(self):
        error_url = self.proxy.get('http')
        error_ip = error_url.split("//")[1]
        new_ip_list = []
        for item in self.available_iplist:
            if item['ip'] != error_ip:
                new_ip_list.append(item)
        self.available_iplist = new_ip_list

    # 反爬蟲(切換不同ip)
    def set_random_proxy(self):
        if self.available_iplist:
            random_ip = random.choice(self.available_iplist)
            self.proxy['http'] = 'http://' + random_ip['ip']
            self.proxy['https'] = 'http://' + random_ip['ip']
            print('Random proxy set:', self.proxy)
        else:
            print('No available IP addresses in the list.')

    # 反爬蟲(移除並切換ip)
    def remove_random_ip(self):
        self.remove_error_ip()
        self.set_random_proxy()

    # 反爬蟲(使用代理驗證可用ip)
    def get_iplist(self):
        res = requests.get('https://free-proxy-list.net/')
        iplist = re.findall('\d+\.\d+\.\d+\.\d+:\d+', res.text)
        for ip in iplist:
            try:
                res = requests.get('https://api.ipify.org?format=json', proxies={'http': ip, 'https': ip}, timeout=5)
                if len(self.available_iplist) < self.ip_number:
                    self.available_iplist.append({'ip': ip})
                    print(ip)
                else:
                    break
            except:
                print('FAIL', ip)
                logging.info(ip)

    # 反爬蟲(切換headers假裝不同瀏覽器)
    def random_headers(self):
        headers = random.choice([self.headers1, self.headers2])
        return headers
