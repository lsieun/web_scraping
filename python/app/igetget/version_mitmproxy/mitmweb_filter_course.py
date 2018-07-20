from mitmproxy import http
import json
import os


def response(flow: http.HTTPFlow) -> None:
    cur_url = flow.request.pretty_url
    if cur_url.find("/course/v2/course/detail") > 0:
        text = flow.request.text
        d = json.loads(text)
        course_id = d.get("course_id")

        content = flow.response.content
        line = content.decode("UTF8")

        file_name = "/root/course/{}.json".format(course_id)
        dir_path = os.path.abspath(os.path.join(file_name, os.pardir))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_name, "wb") as f:
                f.write(line.encode("UTF8"))
