import json
import wechat_msg_util as wechat_util


class WeChatMsgParser(object):
    def __init__(self):
        self.line_list = []
        self.simple_msg_list = []

    def read_file(self, target_file):
        self.line_list.clear()
        self.simple_msg_list.clear()

        with open(target_file, "rb") as f:
            for line in f.readlines():
                self.line_list.append(line.decode("UTF8"))

    def extract_line(self, line):
        response = json.loads(line)
        general_msg_list = response.get("general_msg_list")
        msg_list_dict = json.loads(general_msg_list)
        msg_list = msg_list_dict.get("list")

        for raw_msg in msg_list:
            if not raw_msg:
                print("process_response ==> msg = ", raw_msg)
                continue

            comm_msg_info = raw_msg.get("comm_msg_info", None)
            app_msg_ext_info = raw_msg.get("app_msg_ext_info", None)

            if not app_msg_ext_info:
                print("process_response ==> app_msg_ext_info = ", app_msg_ext_info)
                print("process_response ==> comm_msg_info = ", comm_msg_info)
                continue

            # 提取主要文章信息
            simple_msg = wechat_util.get_simple_msg(app_msg_ext_info)
            self.simple_msg_list.append(simple_msg)

            # 提取伴隨文章信息
            is_multi = app_msg_ext_info.get("is_multi")
            if is_multi:
                multi_app_msg_item_list = app_msg_ext_info.get("multi_app_msg_item_list")
                for msg_item in multi_app_msg_item_list:
                    simple_msg_item = wechat_util.get_simple_msg(msg_item)
                    self.simple_msg_list.append(simple_msg_item)

    def extract_msg_list(self):
        for line in self.line_list:
            self.extract_line(line)

    def write_file(self, target_file):
        with open(target_file, "wb") as f:
            for mid_idx, title, content_url in self.simple_msg_list:
                f.write("{}\r\n".format(mid_idx).encode("UTF8"))
                f.write("{}\r\n".format(title).encode("UTF8"))
                f.write("{}\r\n".format(content_url).encode("UTF8"))
                f.write("{}\r\n".format("").encode("UTF8"))
                print(mid_idx, title, content_url)


if __name__ == '__main__':
    file_path = "history.txt"
    wechat_parser = WeChatMsgParser()
    wechat_parser.read_file(file_path)
    wechat_parser.extract_msg_list()
    wechat_parser.write_file("simple_msg.txt")
