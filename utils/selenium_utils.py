from retrying import retry
import json
import random
import requests
import sys, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/config/config.json', 'r') as f:
    config = json.load(f)

CHROME_DRIVER_URL = config['CHROME_DRIVER_URL']

class SeleniumUtils:
    #PC agent 생성
    f = open(os.path.dirname( os.path.abspath( __file__ )) + '/pc_agent_v5.txt', 'r')
    pc_agents = f.read().splitlines()
    f.close()
    driver = None

    def init_driver(self):
        # webdriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("lang=ko_KR")
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("disable-gpu")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        chrome_options.add_argument("user-agent=" + user_agent)
        
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_URL, chrome_options=chrome_options)
        self.driver.implicitly_wait(3)
    
    def close_driver(self):
        self.driver.close()

    
            
