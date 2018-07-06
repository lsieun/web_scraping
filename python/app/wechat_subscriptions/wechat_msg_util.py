import time
from urllib import parse


def current_milliseconds():
    timestamp = time.time()
    milliseconds = int(round(timestamp * 1000))
    return milliseconds


def parse_querystring_dict(url):
    parsed_url = parse.urlparse(url)
    qs_dict = parse.parse_qs(parsed_url.query)
    return qs_dict


def parse_qs(url, key, default=None):
    qs_dict = parse_querystring_dict(url)
    if qs_dict is None:
        return default
    value = qs_dict.get(key, default)[0]
    return value


def replace(target_str):
    replace_list = ["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"]

    index = 0
    while index < len(replace_list):
        old_str = replace_list[index]
        new_str = replace_list[index + 1]
        target_str = target_str.replace(old_str, new_str)
        index += 2
    return target_str;


def get_simple_msg(raw_msg):
    title = raw_msg.get("title")
    title = replace(title)

    content_url = raw_msg.get("content_url")
    content_url = replace(content_url)

    mid = parse_qs(content_url, "mid", "#")
    idx = parse_qs(content_url, "idx", "*")
    mid_idx = "{}_{}".format(mid, idx)

    return mid_idx, title, content_url
