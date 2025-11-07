'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

s = Service(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

driver = webdriver.Chrome(service=s)
url = 'https://www.verizon.com/home/internet/5g/'
driver.get(r"https://www.verizon.com/home/internet/5g/")

'''
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = 'https://www.verizon.com/home/internet/5g/'

"""# Enable Performance Logging of Chrome.
caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}


# Ignores any certificate errors if there is any
options.add_argument("--ignore-certificate-errors")
options.add_argument('--disable-blink-features=AutomationControlled')"""

options = webdriver.ChromeOptions()

options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
# s = Service(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

# driver = webdriver.Chrome(service=s)
driver.get("https://www.verizon.com/home/internet/5g/")
get_url = driver.current_url
# Sleeps for 10 seconds
time.sleep(10)

print("The current url is:"+str(get_url))


# Find the Shop button and click on it
# btn = driver.find_element(By.ID, value="gnav20-Shop-L3-20")
# btn.click()
'''
# Gets all the logs from performance in Chrome
logs = driver.get_log("performance")
print(logs)

'''
'''
for request in driver.requests:
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers['Content-Type']
        )
'''

driver.quit()
