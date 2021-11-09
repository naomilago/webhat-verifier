###################################################
##                                               ##
##              WEBCHAT VERIFIER                 ##
##            Created by Naomi Lago              ##
##                                               ##
###################################################

from os import stat
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from datetime import datetime
from requests import get
import urllib.request as url
import pandas as pd
import platform
import socket
import time
import os

webchats = {
    'ameplan': 'https://whatsapp.voxline.com.br/ameplan/index.html',
    'cliqx': 'https://facilitabots.com.br:6136/index.html',
    'loga': 'https://facilitabots.com.br:6004/index.html',
    'minfra': 'https://minfrawebchat.chatbsservices.com.br/index.html',
    'unimed_cuiaba': 'https://webchat-cuiaba.facilitabots.com.br/index.html'
}

file_name = datetime.now().strftime('%Y%m%d')
file_path = "C:\logs\webchats\\{}.log".format(file_name)

start_string = '''-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Version 1.0.12.85
# Now: {}
# Description: Webchat Verifier
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

if not os.path.isfile(file_path):
    output = open(r'{}'.format(file_path), "a")
    output.write(start_string)
else:
    output = open(r'{}'.format(file_path), "a")

home_ip = get('https://api.ipify.org').content.decode('utf8')
api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=5fbc86f404664e95bb2a53fb0b333b04&ip_address={}'

for webchat in webchats:
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        first_xpath = '//*[@id="btnAvatar"]'
        second_xpath = '//*[@id="contentBody"]/div[1]/p'

        if webchat == 'loga':
            webchats[webchat] = 'https://facilitabots.com.br:6004'
            driver.get('{}'.format(webchats[webchat]))
            time.sleep(5)
            first_reply = driver.find_element(
                By.XPATH, '//*[@id="chatMain"]/li[2]/div/div/p[2]')
        elif webchat != 'loga':
            driver.get('{}'.format(webchats[webchat]))
            time.sleep(5)
            open_webchat = driver.find_element(By.XPATH, first_xpath)
            open_webchat.click()
            time.sleep(10)

        #! Getting Public ip_addr:
        # * Local -> home_ip = get('https://api.ipify.org').content.decode('utf8')
        # * Webserver -> from='{socket.gethostbyname(urlparse(webchats[webchat]).hostname)}'

        webchat_ip = socket.gethostbyname(urlparse(webchats[webchat]).hostname)

        api_webchat_dataset = pd.read_json(api_url.format(webchat_ip))
        time.sleep(10)
        api_home_dataset = pd.read_json(api_url.format(home_ip))

        results_start = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [DEBUG]  :.initialized: timezone='{api_home_dataset.timezone.values[1]}' isp='{api_home_dataset.connection.values[15]}' sys='{platform.platform()}' arch='{platform.architecture()}' machine='{platform.machine()}'\n"

        results_middle = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [INFO]  :.{webchat}: timezone='{api_webchat_dataset.timezone.values[1]}' isp='{api_webchat_dataset.connection.values[15]}' status='working' http_code='{url.urlopen('{}'.format(webchats[webchat])).getcode()}'\n"

        results_finish = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [DEBUG]  :.disengaged: timezone='{api_home_dataset.timezone.values[1]}' isp='{api_home_dataset.connection.values[15]}' sys='{platform.platform()}' arch='{platform.architecture()}' machine='{platform.machine()}'\n"

        if (list(webchats)[0] == webchat):
            output.write(results_start)
            output.write(results_middle)
        elif (list(webchats)[-1] == webchat):
            output.write(results_middle)
            output.write(results_finish)
        else:
            output.write(results_middle)

    except NoSuchElementException:
        webchat_ip = socket.gethostbyname(urlparse(webchats[webchat]).hostname)

        api_webchat_dataset = pd.read_json(api_url.format(webchat_ip))
        time.sleep(10)
        api_home_dataset = pd.read_json(api_url.format(home_ip))

        results_start = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [DEBUG]  :.initialized: timezone='{api_home_dataset.timezone.values[1]}' isp='{api_home_dataset.connection.values[15]}' sys='{platform.platform()}' arch='{platform.architecture()}' machine='{platform.machine()}'\n"

        results_middle = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [ERROR]  :.{webchat}: timezone='{api_webchat_dataset.timezone.values[1]}' isp='{api_webchat_dataset.connection.values[15]}' status='not_working' http_code='{url.urlopen('{}'.format(webchats[webchat])).getcode()}'\n"

        results_finish = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [DEBUG]  :.disengaged: timezone='{api_home_dataset.timezone.values[1]}' isp='{api_home_dataset.connection.values[15]}' sys='{platform.platform()}' arch='{platform.architecture()}' machine='{platform.machine()}'\n"

        if (list(webchats)[0] == webchat):
            output.write(results_start)
            output.write(results_middle)
        elif (list(webchats)[-1] == webchat):
            output.write(results_middle)
            output.write(results_finish)
        else:
            output.write(results_middle)

output.close()
driver.quit()
