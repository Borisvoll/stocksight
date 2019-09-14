#  implement random proxy

#https://github.com/hellysmile/fake-useragent    implement random user-agent

from fake_useragent import UserAgent
import requests
from random import randint

from StockSight.Initializer.Redis import rds

class RequestRandomizer:

    @staticmethod
    def get_a_proxy():
        ip_list = RequestRandomizer.get_raw_ip_list()

        ip_list_length = len(ip_list)
        if ip_list_length is 0:
            raise ProxyIpNotFound

        current_location = randint(0, ip_list_length-2);
        selected_ip_origin = ip_list[current_location]
        selected_ip = selected_ip_origin.strip()

        return {'https': selected_ip, 'http': selected_ip}

    @classmethod
    def get_raw_ip_list(cls):
        proxies_list = rds.get('proxy_list')
        if proxies_list is None:
            proxies_list_response = requests.get('https://www.proxy-list.download/api/v1/get?type=https&anon=elite&country=US')
            proxies_list = proxies_list_response.text

            ip_list = proxies_list.split("\r\n")

            rds.set('proxy_list', proxies_list, 86400)
        else:
            ip_list = proxies_list.decode().split("\r\n")

        return ip_list


    @staticmethod
    def get_a_user_agent():
        ua = UserAgent()
        return ua.firefox


class ProxyIpNotFound(Exception):
   """Raised when the PROXY IP are not functional"""
   pass