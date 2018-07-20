from mitmproxy import http
import json
import os
import time

old_time = int(time.time())
data_list = []


def response(flow: http.HTTPFlow) -> None:
    global old_time
    global data_list

    cur_url = flow.request.pretty_url
    if cur_url.find("/ddarticle/v1/article/get") > 0:
        # text = flow.request.text
        # d = json.loads(text)
        # course_id = d.get("course_id")

        content = flow.response.content
        data = content.decode("UTF8")
        data_list.append(data)

    now_time = int(time.time())
    if (now_time - old_time > 120) and (len(data_list) > 0):
        file_name = "/root/course/course_content_{}.json".format(now_time)
        with open(file_name, "wb") as f:
            for line in data_list:
                line += "\r\n"
                f.write(line.encode("UTF8"))

        old_time = now_time
        data_list = []
        print("#" * 20, "start", "#" * 20)
        print(file_name)
        print("#" * 20, "end", "#" * 20)
