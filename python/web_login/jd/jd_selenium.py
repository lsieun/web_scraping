from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from config_file_jd import *

driver = webdriver.Chrome()

# 打開登錄頁面
jd_login_url = "https://passport.jd.com/new/login.aspx"
driver.get(jd_login_url)
account_login = driver.find_element_by_xpath('//a[text()="账户登录"]')
account_login.click()

# 登錄
loginname = driver.find_element_by_id("loginname")
loginname.send_keys(JD_USERNAME)
nloginpwd = driver.find_element_by_id("nloginpwd")
nloginpwd.send_keys(JD_PASSWORD)
nloginpwd.send_keys(Keys.ENTER)
time.sleep(10)

# 簽到京東豆
sign_url = "https://vip.jd.com/sign/index"
driver.get(sign_url)
time.sleep(3)

driver.close()
driver.quit()
# jd_home_url = "https://www.jd.com/"