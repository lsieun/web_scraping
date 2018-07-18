import json
import os
import time
import lsieun_util
import request_util
import igetget_config


def simplify(article_dict: dict) -> tuple:
    audio_detail = article_dict.get("audio_detail")
    publish_time = article_dict.get("publish_time")

    article_id = article_dict.get("article_id")
    title = audio_detail.get("title")
    mp3_play_url = audio_detail.get("mp3_play_url")
    publish_time = publish_time.split("T")[0]

    return article_id, title, mp3_play_url, publish_time


def get_article_list(response_text: str) -> list:
    resp_dict = json.loads(response_text)
    content_dict = resp_dict.get("c")
    lst = content_dict.get("list")

    article_list = []
    for item in lst:
        article = simplify(item)
        article_list.append(article)

    return article_list


def get_article_list_by_file(file_path: str) -> list:
    resp_list = lsieun_util.read_line_list(file_path)

    article_list = []
    for line in resp_list:
        lst = get_article_list(line)
        for article in lst:
            article_list.append(article)

    return article_list


def format_html(doc_list: list) -> list:
    line_list = list()
    line_list.append('<html>')
    line_list.append('<head>')
    line_list.append('<meta http-equiv="content-type" content="text/html;charset=utf-8">')
    line_list.append('<title>索引頁</title>')
    line_list.append('</head>')
    line_list.append('<body>')
    line_list.append('<center>')
    line_list.append('<table border="1">')
    line_list.append('<tr><th>ID</th><th>標題</th><th>MP3</th><th>日期</th></tr>')
    for doc in doc_list:
        article_id, title, mp3_play_url, publish_time = doc
        index = mp3_play_url.rfind("/")
        start = index + 1
        local_file_path = mp3_play_url[start:]
        local_file_path = local_file_path.split("_")[1]
        local_file_path = "audio/{}".format(local_file_path)
        template = \
            '<tr><td>&nbsp;&nbsp;{article_id}&nbsp;&nbsp;</td> \
                <td>&nbsp;&nbsp;{title}&nbsp;&nbsp;<a href="html/{article_id}.html">查看</a></td> \
                <td>&nbsp;&nbsp;<a href="{mp3_play_url}">Web鏈接</a>&nbsp;&nbsp;<!--<a href="{local_file_path}">本地鏈接</a>-->&nbsp;&nbsp;</td> \
                <td>{publish_time}</td> \
            </tr>'
        cur_line = template.format(
                article_id=article_id,
                title=title,
                mp3_play_url=mp3_play_url,
                local_file_path=local_file_path,
                publish_time=publish_time)
        line_list.append(cur_line)
    line_list.append('</table>')
    line_list.append('</center>')
    line_list.append('</body>')
    line_list.append('</html>')
    return line_list


def format_txt(doc_list: list) -> list:
    line_list = []

    for doc in doc_list:
        article_id, title, mp3_play_url, publish_time = doc
        line_list.append('{}@#@{}@#@{}@#@{}'.format(article_id, title, mp3_play_url, publish_time))

    return line_list


def create_column_index(column_id: int) -> None:
    src_template = igetget_config.IGETGET_COLUMNS_PATH
    out_html_template = igetget_config.IGETGET_COLUMNS_ARTICLE_HTML_PATH
    out_text_template = igetget_config.IGETGET_COLUMNS_ARTICLE_TEXT_PATH

    src_file = src_template.format(column_id)
    out_html_file = out_html_template.format(column_id)
    out_txt_file = out_text_template.format(column_id)

    article_list = get_article_list_by_file(src_file)

    html_line_list = format_html(article_list)
    lsieun_util.write(html_line_list, out_html_file)

    txt_line_list = format_txt(article_list)
    lsieun_util.write(txt_line_list, out_txt_file)


def get_post_data(article_id: int) -> dict:
    data = {
        "article_id": article_id
    }
    return data


def get_article_id_list(file_path: str) -> list:
    id_list = []
    with open(file_path, "rb") as f:
        for line in f.readlines():
            line = line.decode("UTF8")
            id = line.split("@#@")[0]
            id_list.append(id)
    return id_list


def get_article_content(article_id: int) -> str:
    url = "https://entree.igetget.com/parthenon/v1/articlecontent/getcontent"
    post_data = get_post_data(article_id)
    response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_FORM)
    return response_text


def get_article_content_list(id_list: list, sleep_seconds=3) -> list:
    content_list = []
    index = 0
    print("total: {}".format(len(id_list)))

    for article_id in id_list:
        response_text = get_article_content(article_id)
        content_list.append(response_text)
        index += 1
        print("index = {}".format(index))
        time.sleep(sleep_seconds)
    return content_list


def save_article_content(column_id: int) -> int:
    src_template = igetget_config.IGETGET_COLUMNS_ARTICLE_TEXT_PATH
    out_template = igetget_config.IGETGET_COLUMNS_ARTICLE_JSON_PATH
    src_file = src_template.format(column_id)
    out_file = out_template.format(column_id)

    article_id_list = get_article_id_list(src_file)
    article_content_list = get_article_content_list(article_id_list)
    lsieun_util.write(article_content_list, out_file)


def write_single_html(column_id):
    src_template = igetget_config.IGETGET_COLUMNS_ARTICLE_JSON_PATH
    src_file = src_template.format(column_id)
    line_list = lsieun_util.read_line_list(src_file)

    for line in line_list:
        resp_dict = json.loads(line)
        c = resp_dict.get("c")
        article_content = c.get("article_content")
        # column_detail = c.get("column_detail")

        article_id = article_content.get("article_id")
        html_str = article_content.get("html")

        out_template = igetget_config.IGETGET_COLUMNS_ARTICLE_CONTENT_HTML_PATH
        out_file = out_template.format(column_id, article_id)
        lsieun_util.write(html_str, out_file)


if __name__ == '__main__':
    # create_column_index(46)
    # save_article_content(46)
    write_single_html(46)


