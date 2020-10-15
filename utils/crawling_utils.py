import os
import random
import requests
import re

from retrying import retry

class CrawlingUtils:
    """
    pip install requests
    pip install retrying
    """

    #PC agent 생성
    f = open(os.path.dirname( os.path.abspath( __file__ )) + '/pc_agent_v5.txt', 'r')
    pc_agents = f.read().splitlines()
    f.close()

    def get_random_headers(self):
        headers = {
            'User-Agent': random.choice(self.pc_agents), 
            'Content-Type' : 'application/json'
        }
        return headers 

    @retry(stop_max_attempt_number=7, wait_fixed=3000)
    def get_html(self, url):
        _html = ''
        try:
            resp = requests.get(url, headers=self.get_random_headers())
            if resp.status_code == 200:
                _html = resp.text
            return _html
        except Exception as e:
            print('raise Exception : ' + str(e))
            print('RETRING!!! URL : ' + url)
            raise Exception(str(e))

    def remove_tag(self, content):
        cleanr1 = re.compile('(?!<br>)(<.*?>|[\t\r\n\v\f])|<!--?([^\"\']+)-->?')
        cleanr2 = re.compile(' +')
        cleantext = re.sub(cleanr1, '', content)
        cleantext = re.sub(cleanr2, ' ', cleantext)
        return cleantext