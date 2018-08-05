from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import glob
import shutil
from os.path import expanduser
import time
from selenium_utils import send_user_input
from selenium_utils import click_xpath
from selenium_utils import click_all_xpaths

driver = webdriver.Chrome()
driver.get("https://myaccount.google.com/signin?continue=https://takeout.google.com/settings/takeout/light")

assert "Sign in" in driver.title

elem = driver.find_element_by_name("identifier")
send_user_input(element=elem, prompt="Username: ")
elem.send_keys(Keys.RETURN)

while True:
    if len(driver.find_elements_by_name("password")) > 0:
        break
    time.sleep(1)

elem = driver.find_element_by_name("password")
send_user_input(element=elem, prompt="Password: ")
elem.send_keys(Keys.RETURN)

while True:
    print("Waiting for login success...")
    if "Data tools" in driver.title:
        break
    time.sleep(1)

# uncheck all boxes
click_all_xpaths(driver, "//input[@name='serviceList']")

# check 'plus_photos' box
click_xpath(driver, "//contains(@value, 'plus_photos')]")

click_xpath(driver, "//input[contains(@value, 'Create archive')]")

while True:
    print("Waiting for archive(s) to be prepared...")
    if "An archive of your Google Photos data is currently being prepared" not in driver.page_source:
        break
    driver.get("https://takeout.google.com/settings/takeout/light")
    time.sleep(10)

print("Downloading archive(s)...")

download_links = driver.find_elements(By.XPATH, "//a[contains(., 'Download')]")
for link in download_links:
    driver.execute_script(
        'window.open("{0}", "_blank");'.format(link.get_attribute("href")))

# if 'Sign in' in driver.title:
#     print('Re-entering your password...')
#     elem = driver.find_element_by_name("Passwd")
#     send_user_input(element=elem, prompt='Password: ')
#     elem.send_keys(Keys.RETURN)

#     print('Downloading file...')
#     driver.get('https://takeout.google.com/settings/takeout/light')
#     click_xpath(driver, "//a[contains(., 'Download')]")

# print('Waiting 5s for download to finish...')
# time.sleep(5)


# #%% MOVE DOWNLOADED FILE TO ~/backup/fit/.

# home = expanduser("~")
# source_dir = home + '/Downloads/'
# dest_dir = home + "/backup/takeout/raw"

# for file in glob.glob(r''+ source_dir +'takeout-*.zip'):
#     print('Moving takeout file '+ file +' to backup folder: '+ dest_dir)
#     shutil.move(file, dest_dir)


# #%% LOGOUT AND CLOSE DRIVER

# print('Done. Logging out.')
# click_xpath(driver, '//span[@class="gb_9a gbii"]')
# click_xpath(driver, '//a[@id="gb_71"]')
# driver.close()
