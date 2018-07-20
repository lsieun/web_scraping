import json
import time
from urllib.parse import urlencode
import request_util
import igetget_config
import lsieun_util


def save_course_detail(course_id: int) -> None:
    url = "https://entree.igetget.com/course/v2/course/detail"
    headers = request_util.get_raw_headers()
    u = headers.get("X-UID")

    post_data = {
        "course_id": course_id,
        "user_id": u
    }

    response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_JSON)
    template = igetget_config.IGETGET_COURSES_DETAIL_PATH
    file_path = template.format(course_id)
    lsieun_util.write(response_text, file_path)


def get_alias_id_list(course_id: int) -> list:
    template = igetget_config.IGETGET_COURSES_DETAIL_PATH
    file_path = template.format(course_id)

    line = lsieun_util.read_line_list(file_path)[0]

    d = json.loads(line)
    c = d.get("c")
    lessons = c.get("lessons")

    alias_id_list = []
    for lsn in lessons:
        audio = lsn.get("audio")
        alias_id = audio.get("alias_id")
        alias_id_list.append(alias_id)

    return alias_id_list


def get_audio_content(alias_id: str) -> str:
    url = "https://entree.igetget.com/acropolis/v1/audio/content"
    post_data = {
        "alias_id" : alias_id,
        "dv" : "1"
    }
    response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_FORM)
    d = json.loads(response_text)
    c = d.get("c")
    content = c.get("content")
    dd_article_token = content.get("dd_article_token")
    return dd_article_token


def get_article(token: str) -> str:
    url_template = "https://entree.igetget.com/ddarticle/v1/article/get?{}"
    sign = request_util.get_sign(token)
    query_dict = {
        "appid": 1632426125495894021,
        "sign": sign,
        "token": token
    }
    query_string = urlencode(query_dict)
    url = url_template.format(query_string)
    response_text = request_util.get(url)
    return response_text


def save_articles(course_id: int, alias_id_list: list) -> None:
    article_list = []

    for alias_id in alias_id_list:

        token = get_audio_content(alias_id)
        response_text = get_article(token)
        time.sleep(3)  # 休息一会儿
        article_list.append(response_text)

    template = igetget_config.IGETGET_COURSES_LESSON_JSON_PATH
    file_path = template.format(course_id)
    lsieun_util.write(article_list, file_path)


def format_html(title: str, content: list) -> list:
    lsieun_util.view(content)
    line_list = list()
    line_list.append('<html>')
    line_list.append('<head>')
    line_list.append('<meta http-equiv="content-type" content="text/html;charset=utf-8">')
    line_list.append('<title>{}</title>'.format(title))
    line_list.append('</head>')
    line_list.append('<body>')
    for c in content:
        t = c.get("type")
        if t == "text":
            value = c.get("value")
            line_list.append(value)
        elif t == "image":
            src = c.get("src")
            img_template = '<img src="{}"/>'
            img = img_template.format(src)
            line_list.append(img)
        elif t == "title" or t == "titleCenter":
            h_value = c.get("value")
            h_template = "<h2>{}</h2>"
            h = h_template.format(h_value)
            line_list.append(h)
        elif t == "":
            value = c.get("value")
            quote_tempalte = "<blockquote>{}</blockquote>"
            quote = quote_tempalte.format(value)
            line_list.append(quote)
        else:
            value = c.get("value")
            line_list.append(value)

    line_list.append('</body>')
    line_list.append('</html>')
    return line_list


def generate_html(course_id: int) -> None:
    template = igetget_config.IGETGET_COURSES_LESSON_JSON_PATH
    file_path = template.format(course_id)
    line_list = lsieun_util.read_line_list(file_path)
    for line in line_list:
        d = json.loads(line)
        data = d.get("data")
        if not data: continue
        content = data.get("content")
        if not content: continue
        lesson = json.loads(content)
        title = lesson.get("title")
        lsn_content = lesson.get("content")
        html_str_list = format_html(title, lsn_content)

        out_template = igetget_config.IGETGET_COURSES_LESSON_CONTENT_HTML_PATH
        out_file = out_template.format(course_id, title)
        lsieun_util.write(html_str_list, out_file)


def process(course_id: int) -> None:
    save_course_detail(course_id)
    alias_id_list = get_alias_id_list(course_id)
    save_articles(course_id, alias_id_list)
    generate_html(course_id)


if __name__ == '__main__':
    process(60)







