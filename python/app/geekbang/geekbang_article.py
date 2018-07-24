import geekbang_config
import geekbang_util
import json
import request_util
import time


def get_article(article_id: int) -> str:
    url = "https://time.geekbang.org/serv/v1/article"
    payload = {"id": article_id}
    resp_text = request_util.post_json(url, payload)
    return resp_text


def get_article_list(column_id: int) -> list:
    template = geekbang_config.COLUMN_ARTICLE_LIST_JSON_PATH
    src_file = template.format(column_id)
    line_list = geekbang_util.read_line_list(src_file)
    
    article_list = list()
    for line in line_list:
        d = json.loads(line)
        data = d.get("data")
        lst = data.get("list")
        article_list += lst

    return article_list


def save_articles(column_id: int) -> None:
    line_list = list()

    article_list = get_article_list(column_id)
    for article in article_list:
        article_id = article.get("id")
        resp_text = get_article(article_id)
        line_list.append(resp_text)
        time.sleep(3)

    template = geekbang_config.COLUMN_ARTICLE_JSON_PATH
    file_path  = template.format(column_id)
    geekbang_util.write(line_list, file_path)


def format_html(resp_text: str) -> tuple:
    d = json.loads(resp_text)
    data = d.get("data")
    article_title = data.get("article_title")
    article_content = data.get("article_content")
    line_list = list()
    line_list.append('<html>')
    line_list.append('<head>')
    line_list.append('<meta http-equiv="content-type" content="text/html;charset=utf-8">')
    line_list.append('<title>{}</title>'.format(article_title))
    line_list.append('</head>')
    line_list.append('<body>')
    line_list.append(article_content)
    line_list.append('</body>')
    line_list.append('</html>')
    return article_title, line_list


def write_html(column_id: int) -> None:
    template = geekbang_config.COLUMN_ARTICLE_JSON_PATH
    src_file  = template.format(column_id)
    line_list = geekbang_util.read_line_list(src_file)
    for line in line_list:
        title, html_str_list = format_html(line)
        out_template = geekbang_config.COLUMN_ARTICLE_HTML_PATH
        out_file = out_template.format(column_id, title)
        geekbang_util.write(html_str_list, out_file)


def process(column_id: int) -> None:
    save_articles(column_id)
    write_html(column_id)
    

if __name__ == '__main__':
    #get_article(3646)
    #get_article_list(62)
    #save_articles(62)
    write_html(62)
