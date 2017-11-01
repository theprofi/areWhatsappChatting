"""
Intro:
This is my little script to 'spy' on two people through Whatsapp.
It constantly check whether the two people that you chose in the target variables
are online at the same time.
If they are it will output the exact time it happened.

Be noted that the script saves localy the whole browsing session meaning you will need to log in for the script
only once and from then on, every time the script runs whatsapp web will be logged in.

Requirements:
1. Provide a path to the Chrome Selenium web driver file.
2. Provide a path to the output file.
3. Provide the names of the targets as they are shown in your Whatsapp.
4. Provide a path to the directory where the script will save the session (read the intro above).

Tested on Windows 10 and Fedora 26.
"""

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import time
import datetime


# User defined vars
TARGET1 = ""  # Teseted with English letters
TARGET2 = ""  # Teseted with English letters
SLEEP_TIME = 5  # Sleep X seconds after each iteration of the status check
ITERATIONS = 10000
OUTPUT_PATH = "output.txt"
SESSION_DIR = "session"

# Constants
NAME_SEARCH_XPATH = '//*[@id="side"]/div[2]/div/label/input'
WHATSAPPWEB_URL = "https://web.whatsapp.com/"
CHROME_SELENIUM_DRIVER_PATH = "chromedriver_win32/chromedriver.exe"
ONLINESTATUS_KEYWORD = '<span title="online"'
USEHERE_BTN_KEYWORD = 'Use Here</button>'
LOGOUT_BTN_KEYWORD = 'Log out</button>'


def set_browser():
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=" + SESSION_DIR)
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROME_SELENIUM_DRIVER_PATH)
    browser.get(WHATSAPPWEB_URL)
    return browser


def are_both_online(name_input_box, browser):
    is_target1_online = False
    # Firstly check if target 1 is online
    name_input_box.send_keys(TARGET1 + Keys.ENTER)
    if ONLINESTATUS_KEYWORD in browser.page_source:
        is_target1_online = True
    name_input_box.send_keys(TARGET2 + Keys.ENTER)
    if ONLINESTATUS_KEYWORD in browser.page_source and is_target1_online is True:
        return True
    return False


def main():
    browser = set_browser()
    wait = WebDriverWait(browser, 20)
    name_input_box = wait.until(EC.presence_of_element_located((By.XPATH, NAME_SEARCH_XPATH)))
    for i in range(ITERATIONS):
        try:
            print "start iteration %s" % str(i)
            # Check if they are both online right now
            if are_both_online(name_input_box, browser):
                with open(OUTPUT_PATH, "a") as output:
                    output.write("Both online at: %s \n" % str(datetime.datetime.now()))
                    print "Both online at: %s " % str(datetime.datetime.now())
        except StaleElementReferenceException:
            browser.refresh()
            # Wait after the refesh for the web app to load and update the element
            # to avoid StaleElementReferenceException again
            name_input_box = wait.until(EC.presence_of_element_located((By.XPATH, NAME_SEARCH_XPATH)))
            print "Refreshed and continuing"
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    # execute only if run as a script
    main()
