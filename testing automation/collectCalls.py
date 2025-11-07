# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from browsermobproxy import Server
import chromedriver_py
from selenium.webdriver.common.by import By

from urllib.parse import urlparse, parse_qs
import time
import json
import pandas as pd

urls = {
    "https://www.verizon.com/home/internet"
}
keywords = {
    "collect?configId=60e576ec-f42a-48ad-9fe5-0b9a866a6413"
}
# Main Function
if __name__ == "__main__":

    # Enable Performance Logging of Chrome.
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    # Create the webdriver object and pass the arguments
    options = webdriver.ChromeOptions()

    # Chrome will start in Headless mode
    # options.add_argument('headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("–disable-search-engine-choice-screen")
    # s = Service(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    try:
        for i in range(0, 1):
            driver: WebDriver = webdriver.Chrome(executable_path=r"C:\Users\todupva\Documents\TestingAutomation\chromedriver-win64\chromedriver-win64\chromedriver.exe", options=options)
            # driver = webdriver.Chrome(options=options)
            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            # Send a request to the website and let it load

            for url in urls:
                driver.get(url)
                get_url = driver.current_url
                # Sleeps for 10 seconds
                # time.sleep(10)
                title = driver.title

                # Gets all the logs from performance in Chrome
                logs = driver.get_log("performance")
               
                # Opens a writable JSON file and writes the logs in it
                with open("network_log.json", "w", encoding="utf-8") as f:
                    f.write("[")

                    # Iterates every logs and parses it using JSON
                    for log in logs:
                        network_log = json.loads(log["message"])["message"]

                        # Checks if the current 'method' key has any
                        # Network related value.
                        if "Network.response" in network_log["method"]:
                            # Writes the network log to a JSON file by
                            # converting the dictionary to a JSON string
                            # using json.dumps().

                            f.write(json.dumps(network_log) + ",")
                    f.write("{}]")

                # Read the JSON File and parse it using
                # json.loads() to find the urls containing images.
                json_file_path = "network_log.json"
                with open(json_file_path, "r", encoding="utf-8") as f:
                   logs = json.loads(f.read())

                # Find the specific network request
                for log in logs:
                    # network_log = json.loads(log["message"])["message"]
                    print(log)
                    if log["method"] == "Network.responseReceived":
                        # Get the request payload
                        url = log["params"]["response"]["url"]
                        parsed = urlparse(url)
                        # requestID = parse_qs(parsed.query)['requestId'][0]
                        print(log['params']['response']['headers'])
                        requestID = log['params']['response']['headers']['x-request-id']
                        print("Request ID", requestID)

                        request_payload = (driver.execute_cdp_cmd(
                               "Network.getRequestPostData", {'requestId': requestID}
                      ))

                            # Get the response payload
                        response_payload = driver.execute_cdp_cmd(
                             "Network.getResponseBody", {'requestId': requestID}
                           )

                            # Print or process the payloads
                        print("Request Payload:", request_payload)
                        print("Response Payload:", response_payload)

                        break
    # Close the browser
            driver.quit()

    except Exception as e:
        
        print("Error:", e)


