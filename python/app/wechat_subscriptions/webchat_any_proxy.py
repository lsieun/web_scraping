import requests
import json
import wechat_msg_util as wechat_util


class WeChatAnyProxy(object):
    def __init__(self, host="localhost", port=8002):
        self.host = host
        self.port = port

    def get_log_url(self):
        """
        獲取（由AnyProxy記錄的）Request列表

        :return: 示例，http://192.168.0.105:8002/latestLog?__t=1530615389190
        """
        milliseconds = wechat_util.current_milliseconds()
        url = "http://{}:{}/latestLog?__t={}".format(self.host, self.port, milliseconds)
        return url

    def get_body_url(self, id):
        """
        獲取指定request id的Response

        :param id: request id
        :return: 示例，http://192.168.0.105:8002/fetchBody?id=12&__t=1530628961287
        """
        milliseconds = wechat_util.current_milliseconds()
        url = "http://{}:{}/fetchBody?id={}&__t={}".format(self.host, self.port, id, milliseconds)
        return url

    def get_latest_request(self, print_detail=True):
        # （1）發送請求log_url， 得到結果json_str，再轉換成item_list
        log_url = self.get_log_url()
        r = requests.get(log_url)
        json_str = r.text

        item_list = json.loads(json_str)

        # （2）將item_list逆序放到req_list中
        req_list = []
        for item in item_list:
            req_list.insert(0, item)

        # （3）將最想要的那個請求放到target_req變量中，最後返回
        target_req = None
        for req in req_list:
            id = req.get("id")
            method = req.get("method")
            host = req.get("host")
            url = req.get("url")

            if method == "CONNECT":
                continue
            if host != "mp.weixin.qq.com":
                continue
            if url.find("profile_ext") < 0:
                continue

            action = wechat_util.parse_qs(url, "action")
            if action == "getmsg":
                if print_detail:
                    print("id = %s, url = %s" % (id, url))
                target_req = req
                break

        return target_req

    def get_response_text_by_id(self, id):
        url = self.get_body_url(id)
        r = requests.get(url)
        json_str = r.text

        response_dict = json.loads(json_str)
        res_body = response_dict.get("resBody")
        return res_body

    def get_response_by_id(self, id):
        url = self.get_body_url(id)
        r = requests.get(url)
        json_str = r.text

        return json_str


if __name__ == '__main__':
    server_ip = "192.168.0.105"
    port = 8002

    # （1）獲得最新Request
    proxy = WeChatAnyProxy(host=server_ip, port=port)
    req = proxy.get_latest_request()
    if req is None:
        print("There is No Request.")
        import sys
        sys.exit(0)
    print("\r\n\r\n")

    # （1-1）打印最新Request的字段
    print("（1-1）Latest Request:")
    for item in sorted(req.items()):
        print("\t%s = %s" % item)
    print("\r\n\r\n")

    # （1-2）打印最新Request的Headers
    reqHeader = req.get("reqHeader")
    print("（1-2）Latest Request Headers: type(reqHeader) = %s" % type(reqHeader))
    for key, value in sorted(reqHeader.items()):
        print("\t%s = %s" % (key, value))
    print("\r\n\r\n")
    print("="*120)
    print("\r\n\r\n")

    # （1-3）打印最新Request的Headers
    id = req.get("id")

    # （2）獲得最新Request對應的Response
    response_text = proxy.get_response_by_id(id)
    response = json.loads(response_text)

    # （2-1）打印Response的字段
    print("（2-1）Response Fields:")
    for item in sorted(response.items()):
        print("\t%s = %s" % item)
    print("\r\n\r\n")

    # （2-2）打印Response的resBody
    resBody_str = response.get("resBody")
    # print(resBody_str)
    resBody = json.loads(resBody_str)
    print("（2-2）Response resBody:")
    for key, value in sorted(resBody.items()):
        print("\t%s = %s" % (key, value))
    print("\r\n\r\n")

    # （2-3）打印msg的list
    msg_list_str = resBody.get("general_msg_list")
    msg_list = json.loads(msg_list_str).get("list")
    print("（2-3）Response MSG List:")
    for msg in msg_list:
        print("\t%s" % msg)
    print("\r\n\r\n")

    print("="*60, "GAME OVER", "="*60)