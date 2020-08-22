"""
LoL Esports Drop Collector
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os

HOMEPAGE_URL = "https://lolesports.com/"
LIVE_URL = "https://lolesports.com/live"
local_username = os.environ.get("LOLESPORTS_USERNAME")
local_password = os.environ.get("LOLESPORTS_PASSWORD")

# Open a Firefox browser window
driver = webdriver.Firefox()

# driver wait
wait = WebDriverWait(driver, 10)

# Visit the login page
driver.get(HOMEPAGE_URL)
driver.find_element_by_xpath("//*[@data-riotbar-link-id='login']").click()
time.sleep(5)

# Gets username and password from local machine and inserts them
driver.find_element_by_name("username").send_keys(local_username)
driver.find_element_by_name("password").send_keys(local_password)
driver.find_element_by_xpath('//*[@title="Sign In"]').click()

# Wait until page is loaded before visiting the the live url
wait.until(ec.visibility_of_element_located((By.ID, "riotbar-account")))
driver.get(LIVE_URL)
time.sleep(30)

wait.until(ec.url_changes("https://lolesports.com/live/lec/lec" or "https://lolesports.com/live/lcs/lcs"))
driver.quit()
print("There are no live games with drops enabled.")