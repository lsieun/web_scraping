import geekbang_config
import geekbang_util
import json
import request_util


def get_my_columns() -> None:
    url = "https://time.geekbang.org/serv/v1/my/columns"
    
    resp_text = request_util.post_json(url)
    return resp_text


if __name__ == '__main__':
    response_text = get_my_columns()
    file_path = geekbang_config.MY_COLUMNS_JSON_PATH
    geekbang_util.write(response_text, file_path)
#    d = json.loads(response_text)
#    data = d.get("data")
#    lst = data.get("list")
#    page = data.get("page")
#    geekbang_util.view(page)
    
