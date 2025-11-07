# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from browsermobproxy import Server
import chromedriver_py
import time
import json
import pandas as pd

urls = {
    "https://www.verizon.com/",
    "https://www.verizon.com/home/internet/5g/"
}
keywords = {
    "askverizon",
    "ispot",
    "1697027605114",
    "invoca",
    "msclkid"
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

    # s = Service(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    for i in range(0, 1):
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

        # Send a request to the website and let it load

        for url in urls:
            driver.get(url)
            get_url = driver.current_url
            # Sleeps for 10 seconds
            time.sleep(10)
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

            # Iterate the logs
            for log in logs:

                # Except block will be accessed if any of the
                # following keys are missing.
                try:
                    # URL is present inside the following keys
                    response_url = log["params"]["response"]["url"]
                    for key in keywords:
                        if key in response_url:
                            print(response_url, log["params"]["response"]["status"], end='\n\n')
                            df = pd.DataFrame(
                                {"3PT URL": [response_url], "Status": [log["params"]["response"]["status"]]})
                            print(df)
                            # create a excel writer object
                            writer = pd.ExcelWriter("testLogs.xlsx")
                            # use to_excel function and specify the sheet_name and index
                            # to store the dataframe in specified sheet
                            if title not in writer.sheetnames:
                                writer.create_sheet(title)
                            df.to_excel('3PT Logs.xlsx', sheet_name=title, index=False)

                except Exception as e:
                    pass

        print("Quitting Selenium WebDriver")
        driver.quit()
        print(i)
        i = i + 1
