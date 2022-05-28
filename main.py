from dotenv import dotenv_values
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
#uncomment line below if looking for headless linux
#from pyvirtualdisplay import Display
import time

dotenvVal = dotenv_values(".env")
username = dotenvVal["username"]
password = dotenvVal["password"]

#Can't get headless to work atm due to errors (possible blocking on riots end), virtual displays on linux should work though, but haven't been tested
#display = Display(visible=0, size=(800, 600))
#display.start()

# Opens Firefox browser window
driver = webdriver.Firefox()

# Initialises wait before reporting error.
wait = WebDriverWait(driver, 86400)

# Visit the login page

# Time delays added because of possible blocking on riots end, will possibly change in the future
driver.get(config.home)
time.sleep(5)
wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "osano-cm-dialog__close"))).click()
time.sleep(2)
wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "_2I66LI-wCuX47s2um7O7kh"))).click()
print("Going to the sign in page.")

# Gets username and password from .env
wait.until(ec.presence_of_element_located((By.NAME, "username")))
time.sleep(5)
driver.find_element(By.NAME, "username").send_keys(username)
time.sleep(5)
driver.find_element(By.NAME, "password").send_keys(password)
time.sleep(5)
wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "osano-cm-dialog__close"))).click()
wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "osano-cm-dialog__close")))
time.sleep(5)
wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "mobile-button"))).click()
print("Logged into riot account.")
time.sleep(5)

#goes through daily schedule of currently available drop enabled streams
driver.get(config.lck)
print("Watching LCK until it's finished.")
wait.until(ec.url_changes(config.lck))

driver.get(config.lec)
print("Watching LEC until it's finished.")
wait.until(ec.url_changes(config.lec))

driver.get(config.lcs)
print("Watching LCS until it's finished.")
wait.until(ec.url_changes(config.lcs))

driver.get(config.msi)
print("Watching MSI until it's finished.")
wait.until(ec.url_changes(config.msi))

driver.get(config.worlds)
print("Watching MSI until it's finished.")
wait.until(ec.url_changes(config.worlds))

# Once LCK, LEC, LCS, MSI and worlds are done we quit the driver and tell the user that all games are over (works on daily streams, in order of who should be live first.)
driver.quit()
print("All streams have finished for today.")



