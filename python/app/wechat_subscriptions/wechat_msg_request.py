import json
import time

import requests

import wechat_msg_util as wechat_util
from wechat_subscriptions.webchat_any_proxy import WeChatAnyProxy


class WeChatMsgRequest(object):
    def __init__(self, host="localhost", port=8002, max_request_num=0):
        # （1）請求前：提供anyproxy的host/port和工具
        self.host = host
        self.port = port
        self.proxy = WeChatAnyProxy(host, port)

        # （2）請求中：url和headers
        self.url = ""
        self.headers = {}

        # （3）請求後：response（是否要進行下一次請求的參數信息）
        self.can_msg_continue = 0
        self.next_offset = 0

        # （4）迭代次數控制：當前請求次數、最大限制請求次數
        self.request_num = 0
        self.max_request_num = max_request_num

        # （5）數據容器：保存所有Response結果
        self.response_text_list = []

    def start(self):
        # （1）使用anyproxy工具獲取url和headers
        req = self.proxy.get_latest_request()
        self.url = req.get("url")
        self.headers = req.get("reqHeader")

        # （2）初始化參數值
        self.can_msg_continue = 1
        self.next_offset = 0

    def iterate_request(self, print_detail=True):
        while True:
            # （1）是否要退出while循環的判斷
            if not self.can_msg_continue:
                break
            if self.max_request_num > 0 and self.request_num >= self.max_request_num:
                break
            self.request_num = self.request_num + 1

            # （2）構造新的url
            # https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzU2NTAyNzMxNA==&f=json&offset=46&count=10&is_ok=1&scene=126&uin=777&key=777&pass_ticket=IuwPs5%2FHv%2BsCfDH2y8RfEGKgNbey19uOO4dE9txaeOWjiv9AaeY%2FrnlvZSjwmBo0&wxtoken=&appmsg_token=963_dtAEmQHmjMHR%252Fp3Pw33O6Sy1skV1OMCVU2Ocdg~~&x5=0&f=json
            old_offset = wechat_util.parse_qs(self.url, "offset")
            new_offset = self.next_offset

            old_str = "offset={}".format(old_offset)
            new_str = "offset={}".format(new_offset)

            old_url = self.url
            self.url = self.url.replace(old_str, new_str)
            new_url= self.url

            # （3）發送請求
            r = requests.get(url=self.url, headers=self.headers)
            response_text = r.text
            self.process_response_text(response_text)

            if print_detail:
                print("Request Num: %s" % self.request_num)
                print("old offset = %s, new offset = %s" % (old_offset, new_offset))
                print("OLD URL: %s" % old_url)
                print("NEW URL: %s" % new_url)
                # print("RESPONSE TEXT = %s" % response_text)
                print("")

            # （4）休息一會兒
            time.sleep(5)

    def process_response_text(self, response_text):
        # （1）將“返回的數據”存到“數據容器”中
        self.response_text_list.append(response_text)

        # （2）將“返回的數據”解析出其中兩個參數
        response = json.loads(response_text)
        self.can_msg_continue = response.get("can_msg_continue")
        self.next_offset = response.get("next_offset")

    def write_file(self, file_path):
        with open(file_path, "wb") as f:
            for line in self.response_text_list:
                str = line + "\r\n"
                f.write(str.encode("UTF8"))


if __name__ == '__main__':
    wechat_request = WeChatMsgRequest(host="192.168.0.105", port=8002, max_request_num=3)
    wechat_request.start()
    wechat_request.iterate_request()
    wechat_request.write_file("history.txt")