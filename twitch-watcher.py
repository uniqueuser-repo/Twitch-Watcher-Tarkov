import sys # used to access command line arguments
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def connect():
    input_user = sys.argv[1]
    input_pass = sys.argv[2]

    print("First argument being taken as username, second as password.")

    assert len(sys.argv) == 3 # ensure that the number of passed arguments is 3

    chrome_options = Options()
    #chrome_options.add_argument("--headless")                       # if commented, browser visible.
    #chrome_options.add_argument("--window-size=%s" % "1920,1080")   #
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")


    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get("https://www.twitch.tv/login")

    userbox = driver.find_element_by_xpath('//*[@id="login-username"]')
    passbox = driver.find_element_by_xpath('//*[@id="password-input"]')
    userbox.send_keys(input_user)
    passbox.send_keys(input_pass + Keys.RETURN)

    time.sleep(100)

    button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div/div/div[9]/div/div[3]/button') # "start watching" for mature audiences button


    if (button):
        button.click()

    time.sleep(5)

connect()
