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

# if headless is not working try using pyvirtualdisplay
# remember to comment out options.add_argument("--headless")

"""
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))
display.start
"""

options = webdriver.FirefoxOptions()
options.set_preference("dom.push.enabled", False)
options.set_preference("dom.webnotifications.enabled", False)
options.add_argument("--start-maximized")
# options.headless = True
options.add_argument("window-size=1920,1080")
options.add_argument("--log-level=3")
options.set_capability("excludeSwitches", ["enable-automation"])
options.set_capability("useAutomationExtension", False)
driver = webdriver.Firefox(options=options)

dotenvVal = dotenv_values(".env")
username = dotenvVal["username"]
password = dotenvVal["password"]
randTime = random.randint(11, 19)

# Initialises wait before reporting error.
wait = WebDriverWait(driver, 30)


def signIn():
    driver.get(config.schedule)
    time.sleep(randTime)
    ignoreCookies()
    time.sleep(randTime)
    wait.until(
        ec.element_to_be_clickable((By.CLASS_NAME, "_2I66LI-wCuX47s2um7O7kh"))
    ).click()
    print("Going to the sign in page.")
    ignoreCookies()
    time.sleep(randTime)
    wait.until(ec.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(username)
    time.sleep(randTime)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(randTime)
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "mobile-button"))).click()
    time.sleep(randTime)
    wait.until(ec.url_to_be(config.schedule))
    if ec.presence_of_element_located((By.CLASS_NAME, "_16YqTG4Iq4iNJMhvvUCe3k")):
        print("Signed in.")
    else:
        print("Failed to sign in.")
        driver.quit()
        raise ValueError("Failed to sign in.")


def openStream(url):
    driver.execute_script(f'window.open("{url}","_blank");')


def ignoreCookies():
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "osano-cm-save"))).click()
    wait.until(
        ec.invisibility_of_element_located((By.CLASS_NAME, "osano-cm-dialog__close"))
    )


def main(signedIn):
    if signedIn == False:
        signIn()
    try:
        streams = set()
        driver.switch_to.window(driver.window_handles[0])

        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "events")))

        # Getting live games
        games = driver.find_elements(By.CLASS_NAME, "EventMatch")
        for game in games:
            if game.find_elements(By.XPATH, "//a[starts-with(@href, '/live/')]"):
                link = game.find_element(
                    By.XPATH, "//a[starts-with(@href, '/live/')]"
                ).get_attribute("href")
                if link not in streams:
                    streams.add(link)
        if len(streams) == 0:
            print("No streams found.")
        else:
            for stream in streams:
                time.sleep(randTime)
                openStream(stream)
                print("Opened stream " + link)
            print("Opened all streams. Resting...")
    except Exception as e:
        print(e)


def takeScreenshots():
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        driver.save_screenshot(
            f'Screenshots/{datetime.now().strftime("%d:%m-%H:%M:%S")}.png'
        )


def closeTabs():
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])


def run():
    takeScreenshots()
    closeTabs()
    main(True)


main(False)
takeScreenshots()

schedule.every(30).minutes.do(run)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
