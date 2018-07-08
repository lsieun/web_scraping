from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from config_file import *


def get_driver(browser="phantomjs"):
    if browser == "firefox":
        driver_instance = webdriver.Firefox()
    elif browser == "chrome":
        driver_instance = webdriver.Chrome()
    elif browser == "headless-chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1902x1080')
        driver_instance = webdriver.Chrome(chrome_options=options)
    elif browser == 'phantomjs':
        driver_instance = webdriver.PhantomJS("/usr/local/phantomjs/bin/phantomjs")
    else:
        driver_instance = webdriver.PhantomJS("/usr/local/phantomjs/bin/phantomjs")
    driver_instance.set_window_size(1902, 1080)
    return driver_instance


# driver = get_driver(browser="phantomjs")
driver = get_driver(browser="headless-chrome")


def login():
    try:
        driver.get(url="http://home.51cto.com/index")
        username = driver.find_element_by_id("loginform-username")
        username.send_keys("your_username")  # 用戶名
        password = driver.find_element_by_id("loginform-password")
        password.send_keys("your_password")  # 密碼
        form = driver.find_element_by_id("login-form")
        form.submit()
        time.sleep(5)
        # wait up to 10 seconds for the elements to become available
        # driver.implicitly_wait(10)
        driver.get_screenshot_as_file('01.login-page.png')
    except Exception as ex:
        print("ERROR: login exception")
        print(ex)
        sys.exit(1)


def home():
    try:
        home_url = "http://home.51cto.com/home"
        driver.get(url=home_url)
        html_text = driver.page_source
        wu_you_bi = driver.find_element_by_id("jsSignGetCredits") # 签到领无忧币
        wu_you_bi.click()
        time.sleep(3)
        driver.get_screenshot_as_file('02.home-page.png')
    except Exception as ex:
        print("ERROR: home exception")
        print(ex)


def down():
    try:
        down_url = "http://down.51cto.com/"
        driver.get(url=down_url)
        xiao_zai_dou = driver.find_element_by_id("jsCreditsSpan") # 领取下载豆
        xiao_zai_dou.click()
        time.sleep(3)
        driver.get_screenshot_as_file('03.down-page.png')
    except Exception as ex:
        print("ERROR: down exception")
        print(ex)


def edu():
    try:
        edu_url = "http://edu.51cto.com/"
        driver.get(url=edu_url)
        qian_dao = driver.find_element_by_id("BannerBtn") # 立即签到
        qian_dao.click()
        time.sleep(3)
        driver.get_screenshot_as_file('04.edu-page.png')
    except Exception as ex:
        print("ERROR: down exception")
        print(ex)


def logout():
    logout_url = "http://home.51cto.com/index/logout"
    driver.get(logout_url)
    driver.get_screenshot_as_file('05.logout-page.png')


def quit_driver():
    driver.close()
    driver.quit()


if __name__ == '__main__':
    login()
    home()
    down()
    edu()
    logout()
    quit_driver()
