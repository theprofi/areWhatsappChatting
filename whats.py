'''
 it's only the POC
Maybe later I'll make the code cleaner

 Requirements:
 * Download chromewebdriver for selenium and update the path of the downloaded executable in executable_path=
 * Install the required libraries
'''

import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime

# User defined vars
TARGET1 = ""
TARGET2 = ""
SLEEP_TIME = 5
ITERATIONS = 25


chrome_options = Options()
chrome_options.add_argument("user-data-dir=/home/me/chromewebdriver")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/me/onlineChecker/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
nameSearchBoxLoc = '//*[@id="side"]/div[2]/div/label/input'


for i in range(ITERATIONS):
	try:
		print "start iteration %s" % str(i)
		nameSearchBox = wait.until(EC.presence_of_element_located((By.XPATH, nameSearchBoxLoc)))
		TARGET1Online = False
		TARGET2Online = False
		nameSearchBox.send_keys(TARGET1 + Keys.ENTER)
		if '<span title="online"' in driver.page_source:
			TARGET1Online = True
		nameSearchBox.send_keys(TARGET2 + Keys.ENTER)
		if '<span title="online"' in driver.page_source:
			TARGET2Online = True	
		if TARGET1Online == True and TARGET2Online == True:
			with open("output.txt", "a") as output:
				output.write("Both online at: %s \n" % str(datetime.datetime.now()))
				print "Both online at: %s " % str(datetime.datetime.now())
	except:
		try:
			if 'Use Here</button>' in driver.page_source and 'Log out</button>' in driver.page_source:
				driver.refresh()
				print "Refreshed and continuing"
			else:
				print "@@@@@@ UNHANDLED ERROR @@@@@@"
				break
		except:
			print "@@@@@@ UNHANDLED ERROR @@@@@@"
	time.sleep(SLEEP_TIME)
