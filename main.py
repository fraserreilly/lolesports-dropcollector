from dotenv import dotenv_values
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec 
from selenium import webdriver
import time
from datetime import datetime
import schedule
import random

#if headless is not working try using pyvirtualdisplay
#remember to comment out options.add_argument("--headless")

"""
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))
display.start
"""

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument("window-size=1920,1080")
options.add_argument('--log-level=3')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)

dotenvVal = dotenv_values(".env")
username = dotenvVal["username"]
password = dotenvVal["password"]
randTime = random.randint(11, 19)

# Initialises wait before reporting error.
wait = WebDriverWait(driver, 30)

def openStream(url):
    driver.execute_script(f'window.open("{url}","_blank");')

def ignoreCookies():
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "osano-cm-save"))).click()
    wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "osano-cm-dialog__close")))
    time.sleep(randTime)

def main(signedIn=False):
    if signedIn == False:
        driver.get(config.schedule)
        ignoreCookies()
        wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "_2I66LI-wCuX47s2um7O7kh"))).click()
        print("Going to the sign in page.")
        ignoreCookies()
        wait.until(ec.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(randTime)
        wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "mobile-button"))).click()
        time.sleep(10)
        if ec.presence_of_element_located((By.CLASS_NAME, "_16YqTG4Iq4iNJMhvvUCe3k")):
            signedIn = True
            print("Signed in.")
        else: 
            print("Failed to sign in.")
            driver.quit()

    try:
        streams = 0
        driver.get(config.schedule)

        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "events")))

        #Getting live games   
        games = driver.find_elements_by_class_name("EventMatch")
        for game in games:
            if game.find_elements_by_xpath("//a[starts-with(@href, '/live/')]"):
                link = game.find_element_by_xpath("//a[starts-with(@href, '/live/')]").get_attribute("href")
                streams += 1
                print("Opened stream " + link)
                openStream(link)
                time.sleep(randTime)

        if streams == 0:
            print("No streams found.")
    except Exception as e:
        print(e)
        
def takeScreenshots():
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        time.sleep(3)
        driver.save_screenshot(f'Screenshots/{datetime.now().strftime("%d:%m-%H:%M:%S")}.png')
    
def closeTabs():
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()

def run():
    takeScreenshots()
    closeTabs()
    main()

main()
takeScreenshots()

schedule.every(30).minutes.do(run)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)