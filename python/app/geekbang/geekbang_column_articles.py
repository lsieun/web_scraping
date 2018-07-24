import geekbang_config
import geekbang_util
import json
import request_util
import time


def parse_article_list(resp_text: str) -> tuple:
    d = json.loads(resp_text)
    data = d.get("data")
    lst = data.get("list")
    page = data.get("page")
    is_more = page.get("more")
    score = lst[len(lst)-1].get("score")
    return is_more, score


def get_articles(column_id: int) -> None:
    url = "https://time.geekbang.org/serv/v1/column/articles"
    prev = 0

    line_list = list()
    while True:
        payload = {
            "cid": column_id,
            "order": "newest",
            "prev": prev,
            "size": 20
        }

        resp_text = request_util.post_json(url, payload)
        line_list.append(resp_text)
        is_more, prev = parse_article_list(resp_text)
        if is_more == False: 
            break
        time.sleep(3)
    
    template = geekbang_config.COLUMN_ARTICLE_LIST_JSON_PATH
    file_path = template.format(column_id)
    geekbang_util.write(line_list, file_path)


def process(column_id: int) -> None:
    get_articles(column_id)


if __name__ == '__main__':
    get_articles(62)
