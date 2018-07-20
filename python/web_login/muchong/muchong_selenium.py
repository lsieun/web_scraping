from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from lxml import etree
from config_file import *

driver = webdriver.Chrome()


def parse_question(html_text):
    html = etree.HTML(html_text)
    form_tag = html.xpath('//form[contains(@action, "logging.php?action=login")]')[0]
    div_tag = form_tag.xpath('div[contains(text(), "问题")]')[0]
    question_text = div_tag.text
    print(question_text)

    regexp = r'.*?(\d+)(.*?)(\d+).*'
    re_question = re.compile(regexp)

    m = re_question.match(question_text)
    if m is not None:
        first_num = int(m.group(1))
        oper_str = m.group(2)
        sedonc_num = int(m.group(3))
    else:
        print("m is None")
    return first_num, sedonc_num, oper_str


def get_answer(first_num, second_num, oper_str):
    if oper_str == "加":
        return first_num + second_num
    elif oper_str == "减":
        return first_num - second_num
    elif oper_str == "乘以":
        return int(first_num * second_num)
    else:
        return int(first_num // second_num)


def login():
    login_url = "http://muchong.com/bbs/logging.php?action=login"
    driver.get(url=login_url)

    username = driver.find_element_by_xpath('//input[@name="username"]')
    username.send_keys(MUCHONG_USERNAME)
    password = driver.find_element_by_xpath('//input[@name="password"]')
    password.send_keys(MUCHONG_PASSWORD)
    login_submit = driver.find_element_by_xpath('//input[@name="loginsubmit"]')
    login_submit.click()
    time.sleep(5)


def login_second():
    html_text = driver.page_source
    num1, num2, oper_value = parse_question(html_text)
    answer = get_answer(num1, num2, oper_value)
    print(answer)

    post_sec_code = driver.find_element_by_xpath('//input[@name="post_sec_code"]')
    post_sec_code.send_keys(str(answer))

    login_submit = driver.find_element_by_xpath('//input[@name="loginsubmit"]')
    login_submit.click()
    time.sleep(5)


def get_everyday_gold():
    credit_url = "http://muchong.com/bbs/memcp.php?action=getcredit"
    driver.get(url=credit_url)
    credit_submit = driver.find_element_by_xpath('//input[@name="creditsubmit"]')
    credit_submit.click()
    time.sleep(3)


def get_read_gold():
    index_url = "http://muchong.com/bbs/index.php"
    driver.get(url=index_url)

    p_ok = driver.find_element_by_xpath('//p[contains(@onclick,"view_ok")]')
    p_ok.click()


def quit_driver():
    driver.close()
    driver.quit()


if __name__ == '__main__':
    login()
    login_second()
    get_everyday_gold()
    get_read_gold()