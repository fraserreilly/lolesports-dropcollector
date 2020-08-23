"""
LoL Esports Drop Collector
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options
import time
import os

HOMEPAGE_URL = "https://lolesports.com/"
LIVE_URL1 = "https://lolesports.com/live/lec/lec"
LIVE_URL2 = "https://lolesports.com/live/lcs/lcs"
local_username = os.environ.get("LOLESPORTS_USERNAME")
local_password = os.environ.get("LOLESPORTS_PASSWORD")

# adds firefox options to allow us to run headless
options = Options()
options.headless = True

# Open a Firefox browser window
driver = webdriver.Firefox(options=options)

# driver wait
wait = WebDriverWait(driver, 86400)

# Visit the login page
driver.get(HOMEPAGE_URL)
driver.find_element_by_xpath("//*[@data-riotbar-link-id='login']").click()
wait.until(ec.title_is("Sign In"))
print("Going to the sign in page.")

# Gets username and password from local machine and inserts them
driver.find_element_by_name("username").send_keys(local_username)
driver.find_element_by_name("password").send_keys(local_password)
driver.find_element_by_xpath('//*[@title="Sign In"]').click()
print("Logged into riot account.")

# Wait until page is loaded before visiting the the LEC as they are first
wait.until(ec.visibility_of_element_located((By.ID, "riotbar-account")))
driver.get(LIVE_URL1)
print("Watching LEC until it's finished.")
wait.until(ec.url_changes("https://lolesports.com/live/lec/lec"))

# Once LEC is done LCS will be the next stream so we load that stream
driver.get(LIVE_URL2)
print("Changed to LCS as LEC is over.")
wait.until(ec.url_changes("https://lolesports.com/live/lcs/lcs"))

# Once LCS and LEC are both done we quit the driver and tell the user that all games are over.
driver.quit()
print("There are no live games with drops enabled.")
