from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}

# Create the webdriver object and pass the arguments
options = webdriver.ChromeOptions()

# Chrome will start in Headless mode
# options.add_argument('headless')

# Ignores any certificate errors if there is any
options.add_argument("--ignore-certificate-errors")

options.add_argument('--disable-blink-features=AutomationControlled')

#driver=webdriver.Chrome(options=options, executable_path=(r'C:\Users\todupva\Documents\TestingAutomation\chromedriver-129\chromedriver-win64\chromedriver.exe'))
driver=webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get("https://www.verizon.com")
time.sleep(10)

result=driver.execute_script("return vzdl;")

print(result)

driver.quit()

filtered_data={k: v for k,v in result.items() if 'page' in k}

df_data=[]

for main_key,nested_dict in filtered_data.items():
    if isinstance(nested_dict,dict):
        for sub_key,value in nested_dict.items():
            df_data.append((main_key,sub_key,value))

df=pd.DataFrame(df_data,columns=['Main_key','Sub_key','Value'])