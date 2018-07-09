import requests
import time
from lxml import etree
import sys

muchong_everyday_gold_url = "https://mapi.xmcimg.com/bbs/memcp.php?action=getcredit "

def get_cookie_str():
    timestamp = int(time.time())
    cookie_str = "_emuchos=4d65f2cf63178dae|ios|2.0.5|WiFi|0|2|36351ce0455a033fc0b31baaee17e020693a9b76|; "
    cookie_str += "Hm_lpvt_2207ecfb7b2633a3bc5c4968feb58569={}; ".format(timestamp)
    cookie_str += "Hm_lvt_2207ecfb7b2633a3bc5c4968feb58569={}; ".format(timestamp)
    cookie_str += "_discuz_mobile=1; "
    cookie_str += "_discuz_pw=de4f8ab34911f164; "
    cookie_str += "_discuz_uid=657188"
    return cookie_str

def write_file(html_text):
    time.sleep(1)
    timestamp = int(time.time())
    file_name = "{}.html".format(timestamp)
    print("FILE NAME: %s" % file_name)
    with open(file_name, "wb") as f:
        f.write(html_text.encode("GBK"))

cookie = get_cookie_str()
print("Cookie:", cookie)
headers = {
    "Host": "mapi.xmcimg.com",
    "Content-Type" : "application/x-www-form-urlencoded",
    "Origin" : "https://mapi.xmcimg.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79",
    "Referer" : "https://mapi.xmcimg.com/bbs/memcp.php?action=getcredit&_tpl=app&target=1",
    "Accept-Language": "en-us",
    "Accept-Encoding": "br, gzip, deflate",
    "Connection": "keep-alive"
}

r = requests.post(url=muchong_everyday_gold_url, headers=headers)
print("Status Code:", r.status_code)
print("Encoding:", r.encoding)
print("HEADERS:", r.headers)
html_str = r.text
write_file(html_str)

html = etree.HTML(html_str)
form_list = html.xpath('//form[@id="app_credit_form"]')
if len(form_list) < 1:
    print("There is no form element.!!!")
    sys.exit(0)
form = form_list[0]
formhash = form.xpath('./input[@name="formhash"]')[0].get("value")
getmode = form.xpath('./input[@name="getmode"]')[0].get("value")
creditsubmit = form.xpath('./input[@name="creditsubmit"]')[0].get("value")

print("formhash = %s" % formhash)
print("getmode = %s" % getmode)
print("creditsubmit = %s" % creditsubmit)

post_data = {
    "formhash" : formhash,
    "getmode" : getmode,
    "creditsubmit" : creditsubmit
}

r = requests.post(url=muchong_everyday_gold_url, data=post_data, headers=headers)
print("Status Code:", r.status_code)
print("Encoding:", r.encoding)
print("HEADERS:", r.headers)
html_str = r.text
write_file(html_str)

# 2018-07-06 Cookie
# _emuchos=4d65f2cf63178dae|ios|2.0.5|WiFi|0|2|36351ce0455a033fc0b31baaee17e020693a9b76|;
# Hm_lpvt_2207ecfb7b2633a3bc5c4968feb58569=1530858779;
# Hm_lvt_2207ecfb7b2633a3bc5c4968feb58569=1530858779;
# _discuz_mobile=1;
# _discuz_pw=de4f8ab34911f164;
# _discuz_uid=657188

# 2018-07-07 Cookie
# _emuchos=4d65f2cf63178dae|ios|2.0.5|WiFi|0|2|36351ce0455a033fc0b31baaee17e020693a9b76|;
# _ga=GA1.2.1328553009.1530867652;
# Hm_lpvt_2207ecfb7b2633a3bc5c4968feb58569=1530943767;
# Hm_lvt_2207ecfb7b2633a3bc5c4968feb58569=1530943767;
# _discuz_cc=49351254904216309;
# _discuz_mobile=1;
# _discuz_pw=de4f8ab34911f164;
# _discuz_uid=657188;
# _ga=GA1.2.1328553009.1530867652;
# _gat=1;
# _last_fid=312;
# discuz_tpl=qing;
# last_ip=114.244.80.66_657188;
# view_tid=12455744;



