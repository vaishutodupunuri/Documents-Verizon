from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import json
from chromedriver_py import binary_path
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("–disable-search-engine-choice-screen")

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

#svc = webdriver.ChromeService(executable_path=r"C:\Users\todupva\Documents\TestingAutomation\chromedriver-win64\chromedriver-win64\chromedriver.exe")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=capabilities)
driver = webdriver.Chrome(executable_path=r"C:\Users\todupva\Documents\TestingAutomation\chromedriver-win64\chromedriver-win64\chromedriver.exe")
#driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=r'C:\Users\todupva\Documents\TestingAutomation\chromedriver-win64\chromedriver-win64\chromedriver.exe'), options=options)
# Navigate to a website
driver.get("https://www.verizon.com/home/internet/5g/")

# Get the network logs
logs = driver.get_log("performance")

# Iterate over the logs and extract the request payloads for GET requests
for entry in logs:
    log_message = json.loads(entry["message"])
    if log_message["message"]["method"] == "Network.requestWillBeSent":
        request = log_message["message"]["params"]["request"]
        if request["method"] == "GET":
            url = request["url"]
            payload = request.get("postData", None)  # Payload will be None for GET requests
            print(f"GET request to URL: {url}")
            if payload:
                print(f"Request payload: {payload}")
            else:
                print("No request payload for GET request.")
