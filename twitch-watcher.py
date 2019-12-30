import sys # used to access command line arguments
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import timeunit
import random
import time

def login():
    input_user = sys.argv[1]
    input_pass = sys.argv[2]

    assert len(sys.argv) == 3 # ensure that the number of passed arguments is 3

    chrome_options = Options()
    #chrome_options.add_argument("--headless")                       # if commented, browser visible.
    #chrome_options.add_argument("--window-size=%s" % "1920,1080")   #
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")


    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.set_page_load_timeout(180)
    driver.get("https://www.twitch.tv/login")

    userbox = driver.find_element_by_xpath('//*[@id="login-username"]')
    passbox = driver.find_element_by_xpath('//*[@id="password-input"]')
    userbox.send_keys(input_user)
    passbox.send_keys(input_pass + Keys.RETURN)

    login_button = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button')
    login_button.click()
    time.sleep(20)

    return driver

def checkMaturity(driver, randomStreamer):
    try:
        button = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div/div/div[9]/div/div[3]/button')  # "start watching" for mature audiences button
        button.click()
    except selenium.common.exceptions.NoSuchElementException:
        print(randomStreamer + " is not marked as 'for mature audiences'.")

def checkOfflineOrHostingOrNotPlaying(raw_html, streamer):
    if raw_html.count("OFFLINE") != 0:
        print("OFFLINE FOUND!")
        findStreamer(driver)
    elif raw_html.upper().count("NOW HOSTING") > 0:
        print("HOST FOUND!")
        findStreamer(driver)
    elif raw_html.upper().count("ESCAPE FROM TARKOV") == 0:
        print("NOT PLAYING TARKOV!")
        findStreamer(driver)
    elif raw_html.upper().count("FOLLOW AND GET NOTIFIED WHEN") > 0:
        print ("OFFLINE FOUND VIA ROUTE 2!")
        findStreamer(driver)
    else:
        print(streamer + " has not went offline, started hosting, or stopped playing Tarkov.")

def refresh(driver, streamer):
    try:
        driver.get('https://www.twitch.tv/' + streamer)
    except selenium.common.exceptions.TimeoutException:
        print("Timeout exception!")
        findStreamer(driver)
        return


def findStreamer(driver):
    list_of_streamers = ['kotton', 'smoke', 'hc_diZee', 'jennajulien', 'klean', 'fortyone', 'pestily', 'sacriel', 'partiallyroyal', 'sacriel', 'quattroace', 'slushpuppy',
                         'anthony_kongphan', 'anton', 'insize', 'drlupo', 'whiteydude', 'stereonline', 'ellohime', 'honeymad', 'thomaspaste', 'alanzoka', 'gius', 'break',
                         'chappie', 'peebro', 'shuretv', 'chickenprism', 'bakeezy', 'danexert', 'baddie', 'kiings', 'shina4', 'mrxavito'] # list of drop-enabled streamers

    randomStreamer = random.choice(list_of_streamers)
    print("Chosen streamer: " + randomStreamer)
    try:
        driver.get('https://www.twitch.tv/' + randomStreamer)
    except selenium.common.exceptions.TimeoutException:
        print("Timeout exception!")
        findStreamer(driver)
        return

    time.sleep(30)

    checkMaturity(driver, randomStreamer)

    raw_html = driver.page_source

    checkOfflineOrHostingOrNotPlaying(raw_html, randomStreamer)

    while 1:
        time.sleep(300)
        refresh(driver, randomStreamer)
        raw_html = driver.page_source
        checkOfflineOrHostingOrNotPlaying(raw_html, randomStreamer)





driver = login()
findStreamer(driver)
