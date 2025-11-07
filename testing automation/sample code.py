from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start the web driver (example for Chrome)
driver = webdriver.Chrome(executable_path=r"C:\Users\todupva\Documents\TestingAutomation\chromedriver-129\chromedriver-win64\chromedriver.exe")

# Navigate to the page
driver.get("https://www.verizon.com/home/internet")

try:
    # Wait for the network call to complete
    # (adjust the selector and expected condition as needed)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "some-element"))
    )

    # Get the network logs
    logs = driver.get_log("performance")

    # Find the specific network request
    for log in logs:
        if (
            log["method"] == "Network.responseReceived"
            and "sanalytics" in log["params"]["response"]["url"]
        ):
            # Get the request payload
            request_payload = driver.execute_cdp_cmd(
                "Network.getRequestPostData", {"requestId": log["params"]["requestId"]}
            )

            # Get the response payload
            response_payload = driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": log["params"]["requestId"]}
            )

            # Print or process the payloads
            print("Request Payload:", request_payload)
            print("Response Payload:", response_payload)

            break

except Exception as e:
    print("Error:", e)

finally:
    # Close the browser
    driver.quit()
